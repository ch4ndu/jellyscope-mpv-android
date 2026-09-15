# Extraction verification

- Active three-patch sequence was reversed from and reapplied to the retained modified mpv source; resulting source matched exactly.
- Vendored provider build scripts match the retained pinned provider source.
- Shell syntax and Python AST checks passed.
- Packager executed successfully using retained provider AAR and tested ARM32 libmpv.so. All 50 original AAR entries, including 40 native libraries, match the tested two-crop input. Only META-INF source/license records were added.
- Publishable text was checked for local machine paths, server addresses and common token patterns. No matched private values were included.
- No full native rebuild, Docker build, app build, automated test or device playback was performed for this extraction.
- No Git initialization, staging, commit, remote creation or publishing was performed. VERSION names a proposed first artifact.

These bullets describe the original extraction handoff. Release source/notices,
publication, and JellyScope dependency adoption were subsequently completed.
The consolidated entry point later passed clean ARM32 compilation and AAR
packaging without native-source or build-script changes; see
[the current validation record](../docs/VALIDATION.md#clean-native-build-verification).
Existing Cube acceptance still applies to the retained published bytes, not to
the newly compiled verification artifact.
