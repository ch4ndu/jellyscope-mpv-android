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
The provider enables GPL/version-3 FFmpeg code. Shared dependencies are rebuilt
for linking, but their outputs are **not substituted into the packaged AAR**.
The original provider FFmpeg and other native shared libraries stay in the AAR.
Retained `records/meson-build-options.json` and `armv7-crossfile.txt` describe the
validated build; their `/work/...` paths are historical container paths.

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
It creates a fresh `.local/build/`, downloads provider dependencies, checks out
recorded commits, applies the three mpv patches, and builds ARM32 mpv with the
provider options. Outputs and modified mpv source go under `.local/native/`.
It refuses an existing build directory instead of deleting previous source or
outputs. Retain or move that directory before another fresh build. It builds no
APK and launches no tests or playback.

This entry point consolidates the original successful commands, including the
Meson version and explicit shared-library build. It has received shell syntax
and source/patch verification but **has not completed a fresh native build in
this extracted repository**. Do not claim byte-reproducible output: system build
tool packages are not frozen, and native runtime acceptance still belongs to the
resulting artifact/device pair.

## Package the AAR

Supply the original `dev.jdtech.mpv:libmpv:1.0.0` AAR, resolved from the declared
provider dependency, and the rebuilt ARM32 library:

```bash
python3 scripts/package-aar.py \
  --base-aar /absolute/path/to/provider-libmpv-1.0.0.aar \
  --armv7-lib .local/native/libmpv.so \
  --output dist/libmpv-native-0.41.0-jellyscope.1.aar
```

For the local handoff only, the same command can use
`.local/reference/provider-libmpv-1.0.0.aar` and `.local/reference/libmpv.so`.
That repackages the already tested binary; it is not a native rebuild.
The output path must be new. The packager checks unique ZIP entries and ARM32
ELF identity; input provenance is the caller's responsibility, recorded by the
pinned provider coordinate. It never substitutes another ABI or FFmpeg library.

The release record also needs the modified mpv source archive, the source/build
records for the rest of the distributed native graph, patch series and notices.
The automatic repository source ZIP alone omits ignored native/dependency
sources. See [distribution](DISTRIBUTION.md).
