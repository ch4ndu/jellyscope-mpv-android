# Third-party source and notices

The table is the mpv/provider portion of JellyScope's retained native inventory.
It describes components; the exact Git pins are in records/source-revisions.txt
and the provider's dependency version/download files. Generic license texts are
retained under licenses/. Component-specific copyright and notice files remain
part of their corresponding source and must accompany release source delivery.
This inventory is not a claim that the complete graph is permissively licensed.

| Component | Version | License | Corresponding source |
| --- | --- | --- | --- |
| mpv | 0.41.0 | GPL-2.0-or-later | https://github.com/mpv-player/mpv/tree/v0.41.0 |
| FFmpeg | 8.1 | LGPL-2.1-or-later; GPL-3.0-or-later code enabled | https://github.com/FFmpeg/FFmpeg/tree/n8.1 |
| dav1d | 1.5.3 | BSD-2-Clause | https://code.videolan.org/videolan/dav1d/-/tree/1.5.3 |
| libplacebo | 7.360.1 | LGPL-2.1-or-later | https://github.com/haasn/libplacebo/tree/v7.360.1 |
| libass | 0.17.4 | ISC | https://github.com/libass/libass/tree/0.17.4 |
| fontconfig | 2.17.1 | MIT | https://gitlab.freedesktop.org/fontconfig/fontconfig/-/tree/2.17.1 |
| freetype | 2-14-3 | FreeType License; GPL-2.0-or-later option | https://github.com/freetype/freetype/tree/VER-2-14-3 |
| harfbuzz | 14.1.0 | MIT | https://github.com/harfbuzz/harfbuzz/tree/14.1.0 |
| fribidi | 1.0.16 | LGPL-2.1-or-later | https://github.com/fribidi/fribidi/tree/v1.0.16 |
| libunibreak | 6_1 | zlib | https://github.com/adah1972/libunibreak/tree/libunibreak_6_1 |
| libxml2 | 2.15.2 | MIT | https://github.com/GNOME/libxml2/tree/v2.15.2 |
| mbedTLS | 3.6.6 | Apache-2.0 | https://github.com/Mbed-TLS/mbedtls/tree/v3.6.6 |
| Lua | 5.2.4 | MIT | https://www.lua.org/versions.html#5.2 |
| libmpv-android wrapper base | 1.0.0 | MIT | https://github.com/jarnedemeulemeester/libmpv-android/tree/v1.0.0 |

## Patch ownership

Patches 0001-0003 modify mpv `video/out/hwdec/hwdec_aimagereader.c`, whose header
credits Copyright (c) 2021 sfan5 and licenses that file LGPL-2.1-or-later.
Patch 0001 backports upstream commit c8d3f6884dd4c4725bae18f72dcf48163b512ea8.
Patch 0002 lowers the image limit further; patch 0003 adds bounded observations.
Keep the original file header when applying or distributing these modifications.

The archived FFmpeg patch modifies `libavcodec/mediacodecdec.c`, whose header
credits Copyright (c) 2015-2016 Matthieu Bouron and licenses that file
LGPL-2.1-or-later. It is not part of the active native output.

The provider's vendored build scripts retain their original MIT license in
vendor/provider/LICENSE, including the Ilya Zhuravlev and sfan5 notices.
The provider AAR's original wrapper is not the JNI bridge shipped by JellyScope:
the consuming application retains ownership of its separately built bridge and
its corresponding source. App-side Media3 FFmpeg and LibVLC dependencies are
outside this native patch repository and stay in the app's own inventory.
