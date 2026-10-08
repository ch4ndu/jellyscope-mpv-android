#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Replace libmpv and libavformat for every shipped ABI in an explicitly supplied provider 1.0.0 AAR."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

# Shipped ABI -> (ELF class, e_machine). Every other provider entry is copied unchanged.
ELF_IDENTITY = {
    'armeabi-v7a': (1, 40),
    'arm64-v8a': (2, 183),
    'x86_64': (2, 62),
}
LIBRARIES = ['libmpv.so', 'libavformat.so']
# Build output -> per-ABI bundle.json hash key.
HASHED_OUTPUTS = {
    'libmpv.so': 'libmpv_sha256',
    'libavformat.so': 'libavformat_sha256',
    'mpv-modified-source.tar.gz': 'modified_source_sha256',
    'ffmpeg-config.h': 'ffmpeg_config_sha256',
    'ffmpeg-config_components.h': 'ffmpeg_config_components_sha256',
    'ffmpeg-muxer_list.c': 'ffmpeg_muxer_list_sha256',
}
BUILD_OUTPUTS = list(HASHED_OUTPUTS) + ['applied-patch-series', 'meson-build-options.json', 'crossfile.txt', 'ffmpeg-source-revision']
# Scripts controlling FFmpeg compilation; ffmpeg.sh differs from the provider commit.
FFMPEG_BUILD_SCRIPTS = [
    'vendor/provider/LICENSE',
    'vendor/provider/buildscripts/build.sh',
    'vendor/provider/buildscripts/include/depinfo.sh',
    'vendor/provider/buildscripts/include/path.sh',
    'vendor/provider/buildscripts/scripts/ffmpeg.sh',
]
METADATA_PREFIX = 'META-INF/jellyscope-mpv/'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-aar', type=Path, required=True)
parser.add_argument('--native-dir', type=Path, required=True, help='build-native.sh output with one directory per shipped ABI')
parser.add_argument('--output', type=Path, required=True)
parser.add_argument(
    '--bundle-version',
    required=True,
    help='release being prepared; must equal VERSION and must not be listed in records/bundle.json published_versions',
)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
if args.output.exists():
    parser.error('Output already exists; use a new path to preserve the existing artifact')
prepared_version = (root / 'VERSION').read_text().strip()
if not prepared_version or args.bundle_version != prepared_version:
    parser.error(f'--bundle-version must equal the prepared VERSION {prepared_version}')

metadata = json.loads((root / 'records/bundle.json').read_text())
published_versions = metadata.get('published_versions')
if not isinstance(published_versions, list) or not published_versions:
    parser.error('records/bundle.json must list published_versions')
# Published bytes are immutable; a new release advances VERSION first.
if args.bundle_version in published_versions:
    parser.error(f'{args.bundle_version} is already published; advance VERSION before packaging')
metadata['bundle_version'] = args.bundle_version
if set(metadata['abis']) != set(ELF_IDENTITY):
    parser.error('records/bundle.json must describe exactly the shipped ABIs')
if sorted(metadata['modified_entries']) != sorted(f'jni/{abi}/{name}' for abi in ELF_IDENTITY for name in LIBRARIES):
    parser.error('records/bundle.json modified_entries must list exactly libmpv.so and libavformat.so per shipped ABI')
revisions = dict(line.split() for line in (root / 'records/source-revisions.txt').read_text().splitlines() if line.strip())

# Validate every ABI result before reading the base or creating output.
libraries = {}
for abi, (elf_class, machine) in ELF_IDENTITY.items():
    abi_dir = args.native_dir / abi
    missing = [name for name in BUILD_OUTPUTS if not (abi_dir / name).is_file()]
    if missing:
        parser.error(f'{abi} build output is incomplete: {", ".join(missing)}')
    for name in LIBRARIES:
        library = (abi_dir / name).read_bytes()
        if (
            len(library) < 20
            or library[:4] != b'\x7fELF'
            or library[4] != elf_class
            or library[5] != 1
            or int.from_bytes(library[16:18], 'little') != 3
            or int.from_bytes(library[18:20], 'little') != machine
        ):
            parser.error(f'{abi} {name} is not a little-endian shared ELF for that ABI')
        libraries[f'jni/{abi}/{name}'] = library
    abi_record = metadata['abis'][abi]
    if (abi_dir / 'applied-patch-series').read_bytes() != (root / abi_record['applied_patch_series']).read_bytes():
        parser.error(f'{abi} was not built with {abi_record["applied_patch_series"]}')
    # mpv's spdif filter needs the muxer; demuxer registration or strings are not evidence.
    configuration = next(
        (line for line in (abi_dir / 'ffmpeg-config.h').read_text().splitlines() if line.startswith('#define FFMPEG_CONFIGURATION ')),
        '',
    )
    muxers_disabled = configuration.find('--disable-muxers')
    libavformat = libraries[f'jni/{abi}/libavformat.so']
    if (
        (abi_dir / 'ffmpeg-source-revision').read_text().strip() != revisions['ffmpeg']
        or muxers_disabled < 0
        or configuration.find('--enable-muxer=spdif', muxers_disabled) < 0
        or '#define CONFIG_SPDIF_MUXER 1\n' not in (abi_dir / 'ffmpeg-config_components.h').read_text()
        or '&ff_spdif_muxer,' not in (abi_dir / 'ffmpeg-muxer_list.c').read_text()
        or b'ff_spdif_muxer\0' not in libavformat
        or b'IEC 61937 (used on S/PDIF - IEC958)\0' not in libavformat
    ):
        parser.error(f'{abi} libavformat.so lacks pinned-source, configure, registration or unstripped spdif muxer evidence')
    for name, key in HASHED_OUTPUTS.items():
        abi_record[key] = hashlib.sha256((abi_dir / name).read_bytes()).hexdigest()

records = ['LICENSE', 'THIRD_PARTY.md', 'records/source-revisions.txt'] + FFMPEG_BUILD_SCRIPTS + [
    str(path.relative_to(root))
    for directory in ['patches', 'licenses']
    for path in sorted((root / directory).iterdir())
    if path.is_file()
]
added = [METADATA_PREFIX + 'bundle.json'] + [METADATA_PREFIX + record for record in records]
with ZipFile(args.base_aar) as source:
    names = source.namelist()
    if len(set(names)) != len(names):
        parser.error('Provider input must have unique entries')
    if any(names.count(entry) != 1 for entry in libraries):
        parser.error('Provider input must contain one libmpv.so and one libavformat.so per shipped ABI')
    if any(name.startswith(METADATA_PREFIX) for name in names):
        parser.error('Input is already a JellyScope bundle; supply the original provider AAR')
    if len(set(added)) != len(added) or set(added) & set(names):
        parser.error('Bundle records would duplicate an output entry')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, 'x') as output:
        for member in source.infolist():
            replacement = libraries.get(member.filename)
            output.writestr(member, replacement if replacement is not None else source.read(member))
        output.writestr(METADATA_PREFIX + 'bundle.json', json.dumps(metadata, indent=2) + '\n')
        for record in records:
            output.write(root / record, METADATA_PREFIX + record)
print(
    f'Packaged {args.output.name}; replaced {len(libraries)} entries ({", ".join(sorted(libraries))}), '
    f'preserved {len(names) - len(libraries)} provider entries, source/license records added'
)
