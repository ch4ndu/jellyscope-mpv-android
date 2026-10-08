#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
set -euo pipefail

# Builds libmpv and libavformat for every shipped ABI; never builds an APK or runs playback/tests.
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
ndk_dir="${1:?Usage: build-native.sh /absolute/path/to/android-ndk-r29}"
[[ "$ndk_dir" = /* ]] || { echo 'NDK path must be absolute' >&2; exit 1; }
grep -Eq 'Pkg.Revision *= *29\.0\.14206865' "$ndk_dir/source.properties"
[[ "$(meson --version)" == '1.6.1' ]] || { echo 'Requires Meson 1.6.1' >&2; exit 1; }

toolchain="$ndk_dir/toolchains/llvm/prebuilt/linux-x86_64/bin"
abis=(armeabi-v7a arm64-v8a x86_64)
declare -A provider_arch=([armeabi-v7a]=armv7l [arm64-v8a]=arm64 [x86_64]=x86_64)
declare -A api26_clang=(
    [armeabi-v7a]=armv7a-linux-androideabi26-clang
    [arm64-v8a]=aarch64-linux-android26-clang
    [x86_64]=x86_64-linux-android26-clang
)
# Provider mpv.sh and ffmpeg.sh build into _build$ndk_suffix inside their checkouts.
declare -A build_suffix=([armeabi-v7a]='' [arm64-v8a]=-arm64 [x86_64]=-x64)
# ImageReader patches stay ARM32-only; every ABI receives the common audio fix.
declare -A patch_series=([armeabi-v7a]=series [arm64-v8a]=series-common [x86_64]=series-common)

# Check every ABI before any work so a partial run never mixes old and new output.
for abi in "${abis[@]}"; do
    [[ -x "$toolchain/${api26_clang[$abi]}" ]] || {
        echo "Requires Linux x86_64 Android NDK r29 with the $abi API-26 toolchain" >&2; exit 1;
    }
    [[ ! -e "$root/.local/build/$abi" ]] || {
        echo "Build directory for $abi exists; retain or move it before a fresh build" >&2; exit 1;
    }
    [[ ! -e "$root/.local/native/$abi" ]] || {
        echo "Native output for $abi exists; retain or move it before a fresh build" >&2; exit 1;
    }
done

for abi in "${abis[@]}"; do
    # Each ABI gets its own provider tree and mpv checkout; a patched tree is never reused.
    work="$root/.local/build/$abi/provider"
    mkdir -p "$work"
    cp -R "$root/vendor/provider/buildscripts" "$work/buildscripts"
    cd "$work/buildscripts"
    mkdir -p sdk/android-sdk-linux/ndk
    ln -s "$ndk_dir" sdk/android-sdk-linux/ndk/29.0.14206865
    ./include/download-deps.sh
    while read -r component revision; do
        [[ -n "$component" ]] || continue
        # Resolve the recorded commit, including its pinned submodule gitlinks.
        git -C "deps/$component" fetch origin "$revision"
        git -C "deps/$component" checkout --detach "$revision"
        git -C "deps/$component" submodule update --init --recursive
        [[ "$(git -C "deps/$component" rev-parse HEAD)" == "$revision" ]]
    done < "$root/records/source-revisions.txt"
    series="$root/patches/${patch_series[$abi]}"
    while read -r patch_name; do
        [[ -n "$patch_name" ]] || continue
        git -C deps/mpv apply --check "$root/patches/$patch_name"
        git -C deps/mpv apply "$root/patches/$patch_name"
    done < "$series"
    cores="${MPV_BUILD_JOBS:-6}" ./build.sh --arch "${provider_arch[$abi]}" mpv
    mpv_build="deps/mpv/_build${build_suffix[$abi]}"
    ffmpeg_build="deps/ffmpeg/_build${build_suffix[$abi]}"
    # FFmpeg source stays the unmodified pinned commit; only ffmpeg.sh options differ from the provider.
    git -C deps/ffmpeg diff --quiet HEAD -- || { echo "FFmpeg source for $abi was modified" >&2; exit 1; }
    out="$root/.local/native/$abi"
    mkdir -p "$out"
    cp "$mpv_build/libmpv.so" "$out/libmpv.so"
    cp "prefix/$abi/lib/libavformat.so" "$out/libavformat.so"
    cp "$mpv_build/meson-info/intro-buildoptions.json" "$out/meson-build-options.json"
    cp "prefix/$abi/crossfile.txt" "$out/crossfile.txt"
    cp "$series" "$out/applied-patch-series"
    tar --exclude=.git --exclude='_build*' -czf "$out/mpv-modified-source.tar.gz" -C deps mpv
    # Generated FFmpeg configuration: configure invocation, component macros and muxer registration.
    cp "$ffmpeg_build/config.h" "$out/ffmpeg-config.h"
    cp "$ffmpeg_build/config_components.h" "$out/ffmpeg-config_components.h"
    cp "$ffmpeg_build/libavformat/muxer_list.c" "$out/ffmpeg-muxer_list.c"
    git -C deps/ffmpeg rev-parse HEAD > "$out/ffmpeg-source-revision"
done
printf '%s\n' 'Native output retained under .local/native/<abi>; package only the three libmpv.so and three libavformat.so files over the pinned provider AAR.'
