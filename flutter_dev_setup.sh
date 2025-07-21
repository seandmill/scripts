#!/bin/bash

# Flutter Development Setup Script
# This script improves the dev environment for memory usage
# As always, make executable by running: chmod +x flutter_dev_setup.sh

echo "Starting dev setup..."

# Stop any existing Gradle daemons
echo "Stopping Gradle daemons..."
cd android && ./gradlew --stop 2>/dev/null || true
gradle --stop 2>/dev/null || true
cd ..

# Clean Flutter project
echo "Cleaning Flutter project..."
flutter clean

# Clear Gradle cache if it's too large (>500MB)
GRADLE_CACHE_SIZE=$(du -sm ~/.gradle 2>/dev/null | cut -f1 || echo "0")
if [ "$GRADLE_CACHE_SIZE" -gt 500 ]; then
    echo "Large Gradle cache detected (${GRADLE_CACHE_SIZE}MB), cleaning..."
    rm -rf ~/.gradle/caches/
    echo "Gradle cache cleaned"
fi

# Get dependencies
echo "Getting Flutter dependencies..."
flutter pub get

# Pre-warm Gradle
echo "Pre-warming Gradle (this could take a while)..."
cd android
./gradlew tasks --quiet > /dev/null 2>&1
cd ..

echo "Dev environment ready."
echo
echo "Memory optimization tips:"
echo " 1. Gradle heap limited to 2GB (was 8GB)"
echo " 2. Avoid multiple IDE instances"
echo " 3. Check 'ps aux | grep java' if memory issues persist"
echo
echo "Start development with: flutter run"