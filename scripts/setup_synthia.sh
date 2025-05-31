#!/bin/bash
# setup_synthia.sh - This script installs and runs Synthea to generate synthetic health records
# Copyright (C) 2025 J. Keith Lawson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

set -e

# Set output directory
OUTPUT_DIR="output"
mkdir -p $OUTPUT_DIR

# Clone Synthea if it doesn't exist
if [ ! -d "synthea" ]; then
  git clone https://github.com/synthetichealth/synthea.git
  cd synthea
else
  cd synthea
  git pull
fi

# Run Synthea with default settings for Massachusetts
./gradlew build
./run_synthea -p 100 -cs 0 -o $OUTPUT_DIR Massachusetts

cd ..
echo "✅ Synthea data generated in $OUTPUT_DIR"