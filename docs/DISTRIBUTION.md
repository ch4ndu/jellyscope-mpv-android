# Distribution and JellyScope consumption

## Immutable public assets

The public `jellyscope-mpv-android` repository distributes pinned AAR, complete
source and notice assets through versioned GitHub Releases. Published `.1`
remains immutable. `VERSION` prepares `.2`; fresh build, asset binding and
physical qualification must finish before the separately authorized publication.
[RELEASE.md](../RELEASE.md) owns those checkpoints and assembly commands.
Never resolve `latest`, a branch name or mutable native bytes.

The versioned assets are:

- `libmpv-native-0.41.0-jellyscope.2.aar`
- `libmpv-native-0.41.0-jellyscope.2-sources.tar.gz`
- `libmpv-native-0.41.0-jellyscope.2-notices.zip`

The prepared AAR replaces libmpv/libavformat on three ABIs, with ARM32-only
ImageReader/crop changes. Keep this scope and physical limits in release notes.
Never publish under the upstream provider's coordinate or overwrite old assets.

## Artifact-only Gradle wiring

JellyScope uses an exclusive artifact-only Ivy repository, with the public
repository owner in `OWNER` below. Pin a version that has actually been
published; a prepublication local override does not prove public resolution.

```kotlin
ivy {
    name = "JellyScopeMpvReleases"
    url = uri("https://github.com/OWNER/jellyscope-mpv-android/releases/download")
    patternLayout {
        artifact("v[revision]/[artifact]-[revision].[ext]")
    }
    metadataSources { artifact() }
    content { includeModule("io.github.OWNER", "libmpv-native") }
}
```

The native build-input configuration stays nontransitive:

```kotlin
add(pinnedMpvAar.name, "io.github.OWNER:libmpv-native:0.41.0-jellyscope.2@aar")
```

Keep native extraction, x86 exclusion and upstream `libplayer.so` exclusion.
The app builds its own JNI bridge; do not add a parallel runtime dependency.
API25 apps/API26 mpv, three shipped ABIs and existing codec/passthrough policy
remain consumer-owned. Preserve ordinary AGP stripping when qualifying APKs.

Only `jni/**` is extracted; AAR `META-INF/jellyscope-mpv/` records are not
packaged automatically. Adoption updates app native manifests, attribution,
source tag/real commit/routes, component inventory and generated notice assets
together. Run the existing wrapper/native guards and ordinary final verification
using public resolution after publication. Unexplained stripped-native identity
mismatches block acceptance.

## Corresponding source and notices

Modified mpv files have their own LGPL-2.1-or-later terms, but the native graph
includes GPL-enabled FFmpeg and other components. The provider's MIT wrapper and
this repository's tooling license do not replace component obligations; do not
label the graph LGPL-only. [THIRD_PARTY.md](../THIRD_PARTY.md) owns the inventory.

The complete source asset carries all inherited component/submodule/provider
inputs, exact per-ABI modified mpv archives, pinned unmodified FFmpeg source,
controlling recipe/configuration, toolchain instructions, build records and
component notices. Per-ABI archives match the newly packaged AAR's recorded
source hashes unchanged. A modified-mpv delta alone and automatic GitHub source
archives are insufficient. Validate fresh build/source delivery before treating
new bytes as externally distributable; record checks are engineering evidence.

Public Release assets avoid GitHub Packages authentication for clone builds.
A Maven registry migration is outside this native adoption scope.
