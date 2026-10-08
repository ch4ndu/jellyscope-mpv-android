# Validation scope

## Retained manual device evidence

Fire TV Cube AFTR/raven, ARM32 native path, directly connected to a 1080p TV.
The two-image adjustment allowed hardware VP9 decoding where three images still
failed vendor buffer negotiation. Owner-reported smooth playback was obtained for
two 4K-class 60 fps VP9 assets and a 1080p60 H.264 asset. Crop diagnostics were
subsequently manually checked; they report image/crop/mapper values without
changing rendering calculations. No zero-drop or all-device claim is made.

The GPU path still produced 1080p active images for the investigated 4K source on
this display. The archived VP9 maximum-size experiment did not fix that. Direct
MediaCodec output selection belongs to the app, not this repository's patch set.
8K AV1 can fall back to software and be unusably slow; these patches do not add
8K hardware support. JellyScope's recovery dialog is an app-side feature and is
not in the native AAR. Minor resume drops were deferred by the owner.

In published `.1`, only ARM32 libmpv is patched. Its ARM64/x86_64 payloads
are unchanged provider binaries. Generalizing the two-image adjustment or claiming another platform
validated needs a separate native build and owner-controlled playback checks.

## Repository extraction verification

See `records/HANDOFF.md` for the original extraction checks. A later clean native
build is recorded below; it does not extend the retained device acceptance.

## Clean native build verification

On 2026-09-15, the tracked source at
`8a2e7e75c53c7fb818d86299d4653cbde650a434` completed a clean ARM32 native build
and AAR packaging. No build-script, Dockerfile, or native-patch changes were needed.

- A fresh source export and empty Linux build workspace were used. Dependencies
  were downloaded and compiled; all eleven recorded Git revisions were confirmed.
  The original Linux NDK r29 ZIP was extracted inside Linux. Meson was 1.6.1.
- The unchanged Dockerfile built successfully on Docker Desktop / Apple Silicon
  using Linux x86_64. A damaged host Docker parent snapshot required an isolated
  builder and export/import of the same builder filesystem as a single layer.
  This was a host workaround, not a native source or tool-option change.
- mpv produced an ARM32 little-endian ELF shared library and modified-source
  archive. Meson option values matched `records/meson-build-options.json` exactly.
  The patched ImageReader file matched the modified source supplied with the
  published release. FFmpeg had no tracked source changes; the Mbed TLS build
  regenerated its test certificate header as logged by its normal build.
- The library retained the tested library's dependency list and all 54 public
  `mpv_` API exports. Static checking found no unresolved strong imports against
  the retained provider native libraries and Android API 26 stub exports. This
  is not an Android loader or playback test.
- `scripts/package-aar.py` packaged the newly compiled library over the original
  provider AAR. Only `jni/armeabi-v7a/libmpv.so` changed; the other 49 provider ZIP
  entries were preserved byte-for-byte, and 20 source/license metadata entries
  were added. The original AAR's 40 native-library entries remained present.

The rebuilt library differs from the previously tested bytes. It remains a local
verification artifact; the published release and app dependency were not replaced.
This establishes that the native build completes from clean source, not byte-for-
byte reproducibility or runtime acceptance of the rebuilt binary. No new tests,
playback harness, APK installation, or device playback were performed.

## Prepared three-ABI audio bundle

`0.41.0-jellyscope.2` prepares the common AudioTrack carrier patch and FFmpeg
SPDIF muxer for three ABIs, preserving ARM32 ImageReader/crop scope. On 2026-10-08, its maintained
fresh three-ABI build completed in about 46 minutes. The Linux build environment
required isolated export/import recovery. GNOME Git returned HTTP 503 for
libxml2; a read-only existing Git cache supplied the exact pinned commit for
fresh checkouts, with no compiled-output reuse or recipe change.

Static checks found no unresolved strong imports against the retained provider
libraries plus API-26 stubs, preserved provider exports and DT_NEEDED, and
verified the enabled/registered SPDIF muxer. Packaging replaced exactly six
entries and preserved the other 44 byte-for-byte. Per-ABI modified-source and
FFmpeg configuration records match the generated AAR hashes unchanged.
Complete committed-source/notice asset binding, publication and Shield/TiVo
qualification remain pending. Earlier Cube acceptance and the
local audio candidate's TiVo results do not qualify these new libraries.

The historical `records/meson-build-options.json` and `armv7-crossfile.txt`
remain `.1` ARM32 evidence. New records accompany each ABI in the `.2` source
asset. Host structure/import checks do not establish Android loader behavior,
receiver format, loudness, surround delivery, or physical Cube/x86 acceptance.
