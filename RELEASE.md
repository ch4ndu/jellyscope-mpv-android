# Publish the first native bundle

Prepared version: `0.41.0-jellyscope.1`  
Release tag: `v0.41.0-jellyscope.1`  
Release title: `mpv 0.41.0 - JellyScope native bundle 1`

## Local files

The three upload assets and copy-ready `RELEASE-NOTES.md` are in:

```text
dist/releases/v0.41.0-jellyscope.1/
  libmpv-native-0.41.0-jellyscope.1.aar
  libmpv-native-0.41.0-jellyscope.1-sources.tar.gz
  libmpv-native-0.41.0-jellyscope.1-notices.zip
  RELEASE-NOTES.md
```

`dist/` and `.local/` are ignored. Commit the repository's patches, scripts,
records, licenses and documentation; upload the three assets separately.
GitHub's automatically generated repository source archives do not contain
these ignored source materials and do not replace the attached sources asset.

## GitHub steps

1. Commit the prepared repository and push it to your public GitHub repository.
   Keep the published commit consistent with `repository/` inside the sources
   asset. If you change source, patches, scripts or records before release,
   refresh the matching assets first. No local Git commit or tag is fabricated
   in the prepared source snapshot.
2. Open the repository's **Releases** page and select **Draft a new release**.
3. Choose/create tag **v0.41.0-jellyscope.1** and target the commit you just pushed.
4. Enter the title above and paste `dist/releases/v0.41.0-jellyscope.1/RELEASE-NOTES.md`.
5. Attach the three `.aar`, `.tar.gz` and `.zip` files listed above.
6. Select **Set as a pre-release**. Leave the stable/latest designation off.
7. Save a draft. Check the tag target, all three completed uploads, filenames,
   ARM32-only scope and build-validation limitation, then publish when ready.
8. Open the published release while signed out and confirm all three assets
   download. Keep this version immutable; publish changed bytes under a new version.

GitHub's current UI instructions:
[Managing releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## After publication

With `OWNER` replaced by your GitHub owner, the AAR URL will be:

```text
https://github.com/OWNER/jellyscope-mpv-android/releases/download/v0.41.0-jellyscope.1/libmpv-native-0.41.0-jellyscope.1.aar
```

If you choose another repository name, update that segment too. Send the release
URL back for the separate JellyScope adoption change. The proposed Gradle Ivy
configuration is in [DISTRIBUTION.md](docs/DISTRIBUTION.md). Adoption must update
native manifest/source/notice records alongside the dependency, preserving the
app-owned JNI bridge and current ABI/API limits. Public Release assets avoid
GitHub Packages token setup for developers cloning the app.

## Verification boundary

These assets preserve the previously exercised native bytes and include pinned
source and notice materials. Artifact structure, provider-entry preservation and
the active patch chain were checked locally. The standalone native builder still
needs a clean native rebuild before being described as independently reproducible.
No app build, installation or device test is part of this packaging handoff.
