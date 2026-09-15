# JellyScope mpv Android patches

The native patch set used by JellyScope's manually validated Fire TV Cube build.
This repository maintains a patched native **build-input AAR** based on
`dev.jdtech.mpv:libmpv:1.0.0` and mpv 0.41.0. JellyScope continues to compile its
own JNI bridge; this is not a replacement for the application's player module.

The current bundle replaces **only `jni/armeabi-v7a/libmpv.so`**. All other native
libraries and ABIs remain from the provider AAR. A two-image limit is not applied
to ARM64 or x86_64 by this bundle. API 26 and NDK 29.0.14206865 remain unchanged.

## What's here

- `patches/series`: the active three-patch order.
- `vendor/provider/buildscripts/`: unmodified provider build scripts at commit
  `fcf6745703dc1265bca88f12fee8fc355ddf251e`, with the provider's MIT notice.
- `records/`: component revisions, bundle scope, retained Meson options and cross file.
- `scripts/build-native.sh`: consolidated Linux ARM32 build entry point.
- `scripts/package-aar.py`: replace the ARM32 mpv library in a supplied provider AAR
  and include patch/source/license records under `META-INF/jellyscope-mpv/`.
- `experiments/vp9-adaptive-max/`: an unsuccessful FFmpeg experiment, excluded from
  the active patch series and packaging.
- `licenses/`, `LICENSE`, `THIRD_PARTY.md`: component and file license records.
- `docs/BUILD.md`, `docs/DISTRIBUTION.md`, `docs/VALIDATION.md`: build, consumption,
  publication and observed device scope.

The local handoff additionally retains the tested AAR, ARM32 library, original
provider AAR and modified mpv source archive in **ignored `.local/reference/`**.
These files are not committed when this folder is pushed. Logs, app APKs, device
addresses, playback links and media/account information are intentionally absent
from the publishable tree.

## Active patches

1. Upstream ImageReader capacity reduction, 5 to 3, backported from
   `c8d3f6884dd4c4725bae18f72dcf48163b512ea8`.
2. Further reduction from 3 to 2 for the tested Cube's buffer constraints.
3. Optional, bounded numeric image/crop/mapper diagnostics. This adds observations;
   it does not change crop/render calculations or fix the 1080p presentation issue.

See [build instructions](docs/BUILD.md) to reconstruct the native output and
package an AAR. The extracted build route needs a clean native rebuild before
being declared independently reproducible; this handoff verified the patch
chain and packaging against retained artifacts, not a new native compile.

## Consuming the build

Recommended first distribution: **versioned GitHub Release assets**, with a pinned
Gradle artifact-only Ivy repository. No Maven publication is necessary for the
first JellyScope consumer. See [distribution](docs/DISTRIBUTION.md) for the exact
Gradle pattern and migration boundaries. `VERSION` is a proposed first bundle
version, not an already published tag or release.

The app's production dependency remains the provider coordinate until its native
manifest, notices and dependency are deliberately updated together. The local
experimental AAR override can continue to use the retained bundle during that
transition.

See [RELEASE.md](RELEASE.md) for the prepared upload assets and manual GitHub
release steps. Binary/source release assets remain ignored under `dist/`.
