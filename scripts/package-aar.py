#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Replace only ARM32 libmpv in an explicitly supplied provider 1.0.0 AAR."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-aar', type=Path, required=True)
parser.add_argument('--armv7-lib', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
if args.output.exists():
    parser.error('Output already exists; use a new path to preserve the existing artifact')
library = args.armv7_lib.read_bytes()
if library[:5] != b'\x7fELF\x01' or library[5] != 1 or int.from_bytes(library[18:20], 'little') != 40:
    parser.error('Expected a little-endian ARM32 ELF library')
entry = 'jni/armeabi-v7a/libmpv.so'
metadata_prefix = 'META-INF/jellyscope-mpv/'
with ZipFile(args.base_aar) as source:
    names = source.namelist()
    if len(set(names)) != len(names) or names.count(entry) != 1:
        parser.error('Provider input must have unique entries and one ARM32 libmpv.so')
    if any(name.startswith(metadata_prefix) for name in names):
        parser.error('Input is already a JellyScope bundle; supply the original provider AAR')
    metadata = json.loads((root / 'records/bundle.json').read_text())
    metadata['bundle_version'] = (root / 'VERSION').read_text().strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, 'x') as output:
        for member in source.infolist():
            output.writestr(member, library if member.filename == entry else source.read(member))
        output.writestr(metadata_prefix + 'bundle.json', json.dumps(metadata, indent=2) + '\n')
        for relative in ['LICENSE', 'THIRD_PARTY.md', 'records/source-revisions.txt', 'patches/series']:
            output.write(root / relative, metadata_prefix + relative)
        for directory in ['patches', 'licenses']:
            for path in sorted((root / directory).iterdir()):
                if path.is_file() and path.name != 'series':
                    output.write(path, metadata_prefix + str(path.relative_to(root)))
print(f'Packaged {args.output.name}; only {entry} replaced, source/license records added')
