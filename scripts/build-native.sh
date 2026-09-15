#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
set -euo pipefail

# Builds ARM32 mpv only; never builds an APK or runs playback/tests.
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
ndk_dir="${1:?Usage: build-native.sh /absolute/path/to/android-ndk-r29}"
[[ "$ndk_dir" = /* ]] || { echo 'NDK path must be absolute' >&2; exit 1; }
[[ -x "$ndk_dir/toolchains/llvm/prebuilt/linux-x86_64/bin/armv7a-linux-androideabi26-clang" ]] || {
    echo 'Requires Linux x86_64 Android NDK r29' >&2; exit 1;
}
grep -Eq 'Pkg.Revision *= *29\.0\.14206865' "$ndk_dir/source.properties"
[[ "$(meson --version)" == '1.6.1' ]] || { echo 'Requires Meson 1.6.1' >&2; exit 1; }
work="$root/.local/build"
[[ ! -e "$work" ]] || { echo 'Build directory exists; retain or move it before a fresh build' >&2; exit 1; }
mkdir -p "$work/provider"
cp -R "$root/vendor/provider/buildscripts" "$work/provider/buildscripts"
cd "$work/provider/buildscripts"
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
while read -r patch_name; do
    [[ -n "$patch_name" ]] || continue
    git -C deps/mpv apply --check "$root/patches/$patch_name"
    git -C deps/mpv apply "$root/patches/$patch_name"
done < "$root/patches/series"
cores="${MPV_BUILD_JOBS:-6}" ./build.sh --arch armv7l mpv
mkdir -p "$root/.local/native"
cp deps/mpv/_build/libmpv.so "$root/.local/native/libmpv.so"
cp deps/mpv/_build/meson-info/intro-buildoptions.json "$root/.local/native/meson-build-options.json"
cp prefix/armeabi-v7a/crossfile.txt "$root/.local/native/crossfile.txt"
tar --exclude=.git --exclude=_build -czf "$root/.local/native/mpv-modified-source.tar.gz" -C deps mpv
printf '%s\n' 'Native output retained under .local/native; package only libmpv.so over the pinned provider AAR.'
