#!/bin/bash
# Force Render to use our build.sh
echo "Executing custom build script..."

# Ensure we're in the right directory
cd /opt/render/project/src || exit 1

# Run the actual build
exec ./build.sh
