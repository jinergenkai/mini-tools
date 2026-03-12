Windows Disk Cleanup Scripts
============================

3 scripts:

1. scan.ps1           - Scan and report what's using space (read-only, safe)
2. clean.ps1          - Clean safe caches and temp files
3. compact-docker.ps1 - Compact Docker VHDX to reclaim unused space

Usage:
------

# Scan disk usage:
powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\scan.ps1

# Preview what would be cleaned (dry run, no delete):
powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\clean.ps1 -WhatIf

# Clean everything:
powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\clean.ps1

# Skip specific caches:
powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\clean.ps1 -SkipNpm -SkipGradle

# Compact Docker VHDX (auto-elevates to Admin):
powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\compact-docker.ps1

What each script does:
----------------------

scan.ps1
  - Shows C: drive usage overview
  - Lists cleanable caches with sizes
  - Shows large folders in user profile, AppData\Local, AppData\Roaming
  - Lists top 15 largest installed programs
  - Checks Docker and Recycle Bin size
  - Read-only, changes nothing

clean.ps1
  - Cleans developer caches and temp files that are safe to delete:
    Temp files, npm, Yarn, Go, Gradle, NuGet, Dart/Pub, pip, uv,
    NVIDIA installer cache, D3D shader cache, crash dumps
  - Does NOT touch: personal files, installed programs, Windows system,
    project source code, browser data, config/settings
  - Use -WhatIf to preview without deleting
  - Available skip flags:
    -SkipNpm -SkipYarn -SkipGo -SkipGradle -SkipNuGet -SkipDart -SkipTemp

compact-docker.ps1
  - Compacts Docker Desktop WSL2 virtual disk (VHDX)
  - The VHDX grows over time but never auto-shrinks after pruning
  - Stops Docker Desktop, shuts down WSL, compacts via diskpart
  - Shows before/after size and space freed
  - Requires Admin (auto-elevates if needed)
  - Docker stays stopped after - start manually when needed
