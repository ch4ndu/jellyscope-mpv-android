# JellyScope mpv Android patches

This repository maintains a native build-input AAR based on
`dev.jdtech.mpv:libmpv:1.0.0` and mpv 0.41.0. JellyScope compiles its own JNI
bridge. The published `0.41.0-jellyscope.1` remains immutable; `VERSION` prepares
`0.41.0-jellyscope.2`, whose fresh build and static/package checks have passed; source/publication
and device qualification remain pending.

The prepared bundle replaces `libmpv.so` and `libavformat.so` for armeabi-v7a,
arm64-v8a and x86_64: six provider entries. The other 44 provider ZIP entries
remain unchanged, including provider x86 that JellyScope excludes. API 26,
NDK 29.0.14206865, and the pinned component revisions remain unchanged.

## Active changes

- `patches/series`: ARM32 ImageReader capacity backport (5 to 3), further
  reduction to 2, numeric crop diagnostics, then the common audio patch.
- `patches/series-common`: AudioTrack preserves the encoded IEC61937 carrier
  rate, including E-AC-3's 192 kHz carrier. PCM still follows its native rate cap.
- `vendor/provider/buildscripts/scripts/ffmpeg.sh`: enables only the SPDIF muxer
  after the provider's disabled-muxer option. Other vendored scripts retain the
  provider configuration and MIT notices.

The ImageReader/crop patches remain ARM32-only; diagnostics do not change crop
calculations. `experiments/vp9-adaptive-max/` remains outside the active build.
The other newly compiled FFmpeg/dependency libraries are link inputs and are
not substituted into the AAR's retained provider graph.

## Build, consume and validate

[BUILD.md](docs/BUILD.md) documents the fresh three-ABI build and release-mode
packager. [DISTRIBUTION.md](docs/DISTRIBUTION.md) describes immutable public
GitHub Release assets and the artifact-only Ivy consumer. [RELEASE.md](RELEASE.md)
owns the source/notice assembly and publication checkpoints.

`records/meson-build-options.json` and `records/armv7-crossfile.txt` retain
historical `.1` ARM32 verification evidence. Fresh per-ABI records belong in the
new source asset. [VALIDATION.md](docs/VALIDATION.md) separates historical Cube
acceptance, build checks, and pending qualification of new bytes; no general
surround or all-device claim follows from compilation.

`dist/` and `.local/` contain ignored build/source/notice assets and evidence.
They are absent from the committed tree and automatic GitHub source archives.
Release source assets must carry the complete corresponding component/submodule
sources and build materials. Keep logs, APKs, credentials and device/media
identity out of publication. Component terms and notice obligations live in
[THIRD_PARTY.md](THIRD_PARTY.md); the native graph includes GPL-enabled FFmpeg.
