# Building and packaging

## Recorded inputs

Provider v1.0.0: `fcf6745703dc1265bca88f12fee8fc355ddf251e`.
mpv v0.41.0: `41f6a645068483470267271e1d09966ca3b9f413`.
The other Git revisions are in `records/source-revisions.txt`. libunibreak 6.1
and Lua 5.2.4 are provider versioned release archives, listed in the vendored
`include/depinfo.sh` and downloaded by `include/download-deps.sh`. Recursive
submodules follow the pinned parent commits' gitlinks. No second dependency
checksum allowlist is maintained here.

Toolchain: Linux x86_64, Android NDK r29 (`29.0.14206865`), API 26, Meson 1.6.1.
The provider enables GPL/version-3 FFmpeg code. The packaged AAR replaces
`libmpv.so` and `libavformat.so` for the three shipped ABIs. Other shared
dependencies are rebuilt for linking, but their outputs are not substituted;
all other provider native entries remain unchanged.
Retained `records/meson-build-options.json` and `armv7-crossfile.txt` describe the historical
`.1` ARM32 verification build; their `/work/...` paths are historical container paths.

## Fresh native build

Obtain the Linux NDK r29 from the Android NDK distribution and extract it outside
this repository. Supply its absolute directory to the script. The included
Dockerfile installs the build tools and Meson 1.6.1. From this repository:

```bash
docker build --platform linux/amd64 -t jellyscope-mpv-native-build .
docker run --rm --platform linux/amd64 \
  --mount type=bind,source="$PWD",target=/bundle \
  --mount type=bind,source=/absolute/path/to/android-ndk-r29,target=/ndk,readonly \
  jellyscope-mpv-native-build bash scripts/build-native.sh /ndk
```

On a Linux x86_64 host with the same tools, invoke the script directly instead.
It creates separate fresh `.local/build/<abi>/` trees for armeabi-v7a,
arm64-v8a and x86_64. Each tree downloads provider dependencies, checks out the
recorded revisions and submodules, applies its patch series, and compiles mpv
and FFmpeg with the provider options plus the SPDIF muxer. ARM32 uses
`patches/series`; ARM64 and x86_64 use `patches/series-common`.

Outputs under `.local/native/<abi>/` include `libmpv.so`, `libavformat.so`,
`mpv-modified-source.tar.gz`, `applied-patch-series`, `meson-build-options.json`,
`crossfile.txt`, `ffmpeg-config.h`, `ffmpeg-config_components.h`,
`ffmpeg-muxer_list.c` and `ffmpeg-source-revision`. Preserve the builder-produced
mpv archive unchanged when assembling corresponding source.

Before any work, the script refuses existing build or output directories for
any shipped ABI. Retain or move previous directories before another fresh run;
do not combine different runs. It builds no APK and launches no playback/tests.
The historical ARM32 build is documented in
[validation](VALIDATION.md#clean-native-build-verification). The prepared `.2`
completed the maintained fresh three-ABI build on 2026-10-08. System tools are not frozen; do not claim
byte-reproducible output or runtime acceptance from compilation.

### macOS Docker storage

Use a Linux Docker volume for the NDK and build workspace. The Linux NDK contains
case-distinct header names that collide on the usual case-insensitive macOS
filesystem. Keep the downloaded ZIP on the host and extract it inside Linux.
The following builds committed source; commit intended source changes first.
Use a new volume/container name for another fresh build, preserving prior outputs.

```bash
mkdir -p .local
git archive --format=tar HEAD --output=.local/native-source.tar
docker volume create jellyscope-mpv-native-work
docker run --name jellyscope-mpv-native-build --platform linux/amd64 \
  --mount type=volume,source=jellyscope-mpv-native-work,target=/work \
  --mount type=bind,source="$PWD/.local/native-source.tar",target=/source.tar,readonly \
  --mount type=bind,source=/absolute/path/to/android-ndk-r29-linux.zip,target=/ndk.zip,readonly \
  jellyscope-mpv-native-build bash -c '
    set -euo pipefail
    mkdir /work/bundle /work/toolchain
    tar -xf /source.tar -C /work/bundle
    unzip -q /ndk.zip -d /work/toolchain
    cd /work/bundle
    bash scripts/build-native.sh /work/toolchain/android-ndk-r29
  '
docker cp jellyscope-mpv-native-build:/work/bundle/.local/native .local/native
```

Use a new local destination for `docker cp` if `.local/native` already exists.
The build container and volume are retained for inspection; removing a container
does not remove its named volume.

## Package the AAR

Supply the original `dev.jdtech.mpv:libmpv:1.0.0` AAR, resolved from the declared
provider dependency, and fresh three-ABI output. With `VERSION` prepared as `.2`:

```bash
python3 scripts/package-aar.py \
  --base-aar /absolute/path/to/provider-libmpv-1.0.0.aar \
  --native-dir .local/native \
  --bundle-version 0.41.0-jellyscope.2 \
  --output dist/releases/v0.41.0-jellyscope.2/libmpv-native-0.41.0-jellyscope.2.aar
```

The requested version must equal `VERSION` and must not appear in
`records/bundle.json`'s `published_versions`. The list retains `.1`; add `.2`
at the next release preparation, not before packaging `.2`. The output path
must be new. Published assets must never be overwritten.

The packager checks all ABI outputs before creating the AAR: ELF identity,
applied patch series, pinned FFmpeg revision, configure order, enabled SPDIF
muxer, registration and unstripped symbol evidence. It records source/config
hashes in `META-INF/jellyscope-mpv/bundle.json`. It replaces exactly the three
`libmpv.so` and three `libavformat.so` entries. Separately confirm the expected
44 retained entries byte-for-byte and validate imports against the retained
provider libraries plus API-26 stubs, rather than newly rebuilt sibling libraries.

The complete source/notice asset gate is in [RELEASE.md](../RELEASE.md).
Automatic GitHub source ZIPs omit ignored component sources and do not replace
that delivery. New native bytes require separate artifact/device acceptance.
