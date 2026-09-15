# Archived VP9 adaptive maximum experiment

Not in patches/series and never applied by scripts/build-native.sh.

Against FFmpeg 8.1 commit 9047fa1b084f76b1b4d065af2d743df1b40dfb56,
0004 sets MediaCodec max-width/max-height to the positive source dimensions for
VP9 only. A manually exercised Cube build delivered the keys to the decoder but
still reported a 1920x1080 image/output. It did not solve the investigated
consumer-dependent output dimensions. The validated bundle therefore retains
provider FFmpeg unchanged. The duplicate draft patch was not imported.

The affected source file is LGPL-2.1-or-later; see THIRD_PARTY.md. No experimental
codec binary or private playback logs are included in this source tree.
