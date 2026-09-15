# Distribution and JellyScope consumption

## Recommendation

Start with a public GitHub repository plus **versioned GitHub Releases**. Publish
an AAR and its source/notice records as release assets. Gradle supports a custom
artifact-only Ivy layout, so this still gives JellyScope a pinned dependency and
normal Gradle caching. Do not resolve `latest`, a branch name or a mutable build.
No remote repository, release or Maven package is configured or published by this
local handoff.

For example, a future release tagged `v0.41.0-jellyscope.1` could contain:

- `libmpv-native-0.41.0-jellyscope.1.aar`
- the matching modified mpv source archive
- the complete corresponding-source/build/notice materials for the distributed graph

Keep experimental ARM32-only scope visible in release notes. Do not publish a
replacement under the upstream provider's coordinate or overwrite old versions.

## Proposed Gradle wiring

Replace `OWNER` and the example group with the eventual public repository owner.
This is an integration example, not an app change already made:

```kotlin
// In the app's dependencyResolutionManagement.repositories block:
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

In `:android-libmpv`, replace the single external input to `pinnedMpvAar` with the
chosen pinned coordinate, for example:

```kotlin
add(pinnedMpvAar.name, "io.github.OWNER:libmpv-native:0.41.0-jellyscope.1@aar")
```

Keep that configuration nontransitive. Keep the app's existing native extraction,
x86 exclusion and provider `libplayer.so` exclusion. The app must continue to
compile its own JNI bridge with the typed logging/idempotent teardown changes.
Do not add this AAR as a parallel runtime `implementation` dependency.

The app currently extracts only `jni/**`; the AAR's `META-INF/jellyscope-mpv/`
records are not automatically packaged into the APK. During adoption, update the
app's native manifest, attribution, corresponding-source routes and generated
license assets together, then run its existing wrapper/native package guards.
Retain current Android ABI/API and codec capability policy. This handoff changes
none of those production declarations.

## Maven options

GitHub Packages' Maven registry requires authentication even for public packages.
That adds token setup to local and external builds, so it is not the recommended
public download route here. GitHub Actions has its own supported token route.

Maven Central is a reasonable later destination if this becomes a general-purpose
library for multiple consumers. It needs namespace setup, signing and required
publication metadata. That work is independent of the native patch itself and
is unnecessary for a first consumer using a versioned release artifact.

Sources checked for this recommendation:

- [GitHub Maven authentication](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-apache-maven-registry)
- [GitHub release asset URLs](https://docs.github.com/en/rest/releases/assets)
- [Gradle custom repository layouts](https://docs.gradle.org/current/userguide/supported_repository_types.html)
- [Maven Central publication requirements](https://central.sonatype.org/publish/requirements/)

## Source and license delivery

The active patches modify an LGPL-2.1-or-later mpv source file, but the retained
native dependency graph includes GPL-enabled FFmpeg and other components. Neither
the provider's MIT wrapper license nor this repository's tooling license replaces
those obligations. Retain component notices and exact corresponding-source/build
materials with the binary release. Do not label the graph LGPL-only.

The ignored retained mpv archive contains the exact modified mpv source for the
validated binary; it is not by itself the corresponding source for every native
library in the AAR. Preserve the pinned provider sources, each dependency and its
submodules or versioned source archives, build scripts/configuration and notices.
Complete that release source delivery and verify the fresh build before treating
a new binary as ready for external distribution.
