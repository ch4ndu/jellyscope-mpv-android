# Prepare and publish the native bundle

Prepared version: `0.41.0-jellyscope.2`
Proposed tag: `v0.41.0-jellyscope.2`
Proposed title: `mpv 0.41.0 - JellyScope native bundle 2`

The `.1` release stays immutable. The `.2` fresh build and static/package
checks have passed. Complete source binding, remaining physical qualification
and publication are pending; these instructions do not establish release
readiness or authorize Git/publication actions.

## Assets and source binding

Prepare new ignored paths; never overwrite an existing asset:

```text
dist/releases/v0.41.0-jellyscope.2/
  libmpv-native-0.41.0-jellyscope.2.aar
  libmpv-native-0.41.0-jellyscope.2-sources.tar.gz
  libmpv-native-0.41.0-jellyscope.2-notices.zip
  RELEASE-NOTES.md
```

Build and package using [BUILD.md](docs/BUILD.md). The AAR replaces six entries;
verify the 44 retained provider entries and imports against that retained graph.
Describe common AudioTrack/SPDIF changes and ARM32-only ImageReader/crop patches
in release notes, with actual build/device evidence and remaining limits.

Inspect the `.1` complete source asset's member paths and links before extracting
into fresh staging with `tar -xzf <.1-sources.tar.gz> -C <fresh-staging>`. Rename
the root to `libmpv-native-0.41.0-jellyscope.2-sources`. Preserve the complete
`upstream/` component/submodule/provider source archive set, including pinned
FFmpeg and upstream mpv; verify the component inventory and revisions rather
than assuming historical counts. Keep toolchain source/instructions and notices.
Move obsolete ARM32-only modified-source/config records under `historical-v1/`
or remove them from current-build scope.

After an explicitly authorized native source commit, replace staged `repository/`
with that exact committed tree:

```bash
mkdir <empty-repository-dir>
git archive <actual-commit> | tar -x -C <empty-repository-dir>
```

For each ABI, copy the same fresh build's `mpv-modified-source.tar.gz` unchanged
into `builds/<abi>/`, together with crossfile, Meson options, applied series,
FFmpeg config/components/muxer-list and source-revision records. Compare every
hash recorded in the AAR's per-ABI `bundle.json` to those source-offer files.
Do not recreate the per-ABI mpv archives or use historical candidate outputs.
The committed repository supplies the exact modified FFmpeg recipe and pins.

Check staged inventory, paths/links, notices, privacy, source coverage and
repository/tree identity before sealing. Only the outer archive is manually
created:

```bash
tar -czf <new-.2-sources.tar.gz> -C <staging-parent> <.2-source-root>
tar -tzf <new-.2-sources.tar.gz>
```

Assemble a fresh notice root from license texts and complete original
component/provider notices, updating `.2` scope. From its parent:

```bash
zip -r <absolute-new-.2-notices.zip> <notice-root>
unzip -Z1 <absolute-new-.2-notices.zip>
```

Compare inventories to the component/source record. Missing source, unsafe
members, mismatched hashes or incomplete notices block the asset gate.
Automatic GitHub repository archives omit ignored source materials and do not
replace the attached source offer. Keep outer asset hashes in ignored evidence,
not tracked records. Exclude logs, APKs, credentials, private paths, caches and
generated binaries from source/notice delivery.

## Action checkpoints

1. Finish fresh native/static/package checks, integrated review and Shield/TiVo
   qualification before publication. A local AAR override is qualification
   evidence only; normal public resolution is a later gate.
2. Present the exact reviewed diff/tree and proposed commit/tag for explicit
   local Git authorization. Commit source, refresh source/AAR/notice assets and
   app metadata against the real commit, then verify bindings. Create the tag
   last. Any tracked native edit after committing requires a new commit and
   refreshed repository snapshot/assets before tagging. Never put a commit's
   own hash into that commit's tracked records.
3. Present the actual commit/tag, three complete asset inventories, release
   notes and qualification for separate push/publication authorization. Push
   that commit/tag and create its immutable pre-release only when authorized.
   Leave the stable/latest designation off; never replace `.1` assets or tag.
4. Confirm anonymous AAR/source/notice access and ordinary app resolution of
   `.2` without local init overrides. Verify ordinary stripped APK/native
   identity, the final app matrix, and bounded original-asset device smoke.
   Publication alone does not prove ordinary clone/release behavior.

The app adoption updates native pin/source/notice metadata together, preserving
its JNI bridge and ABI/API policy. [DISTRIBUTION.md](docs/DISTRIBUTION.md) owns
consumer wiring. No app version bump, release or Git action follows from native
preparation. Reconcile partial/ambiguous remote actions before retrying.
