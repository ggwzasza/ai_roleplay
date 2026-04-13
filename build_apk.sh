#!/bin/bash
set -e

echo "========================================"
echo "  AI Roleplay - Android APK Build"
echo "========================================"

if ! command -v buildozer &> /dev/null; then
    echo "[ERROR] buildozer not found. Install it first:"
    echo "  pip install buildozer cython"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/3] Cleaning previous build..."
buildozer android clean 2>/dev/null || true

echo "[2/3] Building debug APK..."
buildozer -v android debug

echo "[3/3] APK location:"
ls -la bin/*.apk 2>/dev/null || echo "  Check bin/ directory for the APK file"

echo ""
echo "========================================"
echo "  Build complete!"
echo "  To deploy to device: buildozer android deploy run"
echo "========================================"
