# Validation scope

## Retained manual device evidence

Fire TV Cube AFTR/raven, ARM32 native path, directly connected to a 1080p TV.
The two-image adjustment allowed hardware VP9 decoding where three images still
failed vendor buffer negotiation. Owner-reported smooth playback was obtained for
two 4K-class 60 fps VP9 assets and a 1080p60 H.264 asset. Crop diagnostics were
subsequently manually checked; they report image/crop/mapper values without
changing rendering calculations. No zero-drop or all-device claim is made.

The GPU path still produced 1080p active images for the investigated 4K source on
this display. The archived VP9 maximum-size experiment did not fix that. A direct
MediaCodec surface experiment is not part of this repository's active patch set.
8K AV1 can fall back to software and be unusably slow; these patches do not add
8K hardware support. JellyScope's recovery dialog is an app-side feature and is
not in the native AAR. Minor resume drops were deferred by the owner.

Only the ARM32 libmpv is patched. ARM64/x86_64 payloads are unchanged provider
binaries. Generalizing the two-image adjustment or claiming another platform
validated needs a separate native build and owner-controlled playback checks.

## Repository extraction verification

See records/HANDOFF.md for the completed checks and limitations. The new Linux
build entry point was consolidated from retained successful commands, but a
clean full native rebuild has not been run in this extracted repository.
Patch/source consistency, shell/Python syntax and AAR repackaging do not prove
native reproducibility or new device compatibility. No playback harness or new
automated tests are included.
