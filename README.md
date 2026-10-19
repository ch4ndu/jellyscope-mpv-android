# JellyScope mpv Android patches

This repository maintains a native build-input AAR based on
`dev.jdtech.mpv:libmpv:1.0.0` and mpv 0.41.0. JellyScope compiles its own JNI
bridge. Published `.1` and `.2` assets remain immutable. `VERSION` prepares
`0.41.0-jellyscope.3` with FFmpeg 8.1.3; the fresh native build and ELF/package checks pass. The isolated app candidate also passes its full host/release-package gate.
Final source commit binding, physical qualification and publication remain separate gates.

The candidate replaces libmpv and all seven FFmpeg shared libraries for
armeabi-v7a, arm64-v8a and x86_64: 24 provider entries. The other 26 provider
ZIP entries remain unchanged, including x86 that JellyScope excludes. API 26,
NDK 29.0.14206865, mpv 0.41.0 and the other dependency pins stay unchanged.

## Active changes

- `patches/series`: ARM32 ImageReader capacity backport (5 to 3), further
  reduction to 2, numeric crop diagnostics, then the common audio patch.
- `patches/series-common`: AudioTrack preserves the encoded IEC61937 carrier
  rate, including E-AC-3's 192 kHz carrier. PCM still follows its native rate cap.
- `vendor/provider/buildscripts/scripts/ffmpeg.sh`: enables only the SPDIF muxer
  after the provider's disabled-muxer option. `include/depinfo.sh` selects
  FFmpeg 8.1.3; the exact commit is in `records/source-revisions.txt`. Original
  provider MIT notices remain intact.

The ImageReader/crop patches remain ARM32-only; diagnostics do not change crop
calculations. `experiments/vp9-adaptive-max/` remains outside the active build.
All FFmpeg libraries are packaged from the same fresh per-ABI build. Other
dependencies are rebuilt for linking and retain the provider bytes in the AAR.

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
