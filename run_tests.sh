#!/usr/bin/env bash
# Run all unit tests for Codey/Cody

set -e

echo "========================================"
echo "  Codey/Cody Unit Tests"
echo "========================================"
echo ""

# Set PYTHONPATH
export PYTHONPATH=/mnt/c/Users/ortlu/Codey/Codey-repo/Codey/src

# Run tests
python3 -m unittest discover -s /mnt/c/Users/ortlu/Codey/Codey-repo/Codey/tests -v

echo ""
echo "========================================"
echo "  All tests completed!"
echo "========================================"
