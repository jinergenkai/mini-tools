#Requires -Version 5.1
<#
.SYNOPSIS
    Clean safe caches and temp files on C: drive.
.DESCRIPTION
    Only cleans developer caches and temp files that are safe to delete.
    Does NOT uninstall programs or delete user files.
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File clean.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File clean.ps1 -WhatIf
    powershell -NoProfile -ExecutionPolicy Bypass -File clean.ps1 -All
#>

param(
    [switch]$WhatIf,     # Preview only, don't delete
    [switch]$All,        # Clean everything without prompting
    [switch]$SkipNpm,
    [switch]$SkipYarn,
    [switch]$SkipGo,
    [switch]$SkipGradle,
    [switch]$SkipNuGet,
    [switch]$SkipDart,
    [switch]$SkipTemp
)

$ErrorActionPreference = 'SilentlyContinue'
$userProfile = $env:USERPROFILE

function Format-Size($bytes) {
    if ($null -eq $bytes -or $bytes -eq 0) { return "0 MB" }
    if ($bytes -ge 1GB) { return "$([math]::Round($bytes/1GB, 2)) GB" }
    if ($bytes -ge 1MB) { return "$([math]::Round($bytes/1MB, 0)) MB" }
    return "$([math]::Round($bytes/1KB, 0)) KB"
}

function Get-FolderSize($path) {
    if (-not (Test-Path $path)) { return 0 }
    return (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
}

function Remove-FolderContents($path, $label) {
    if (-not (Test-Path $path)) {
        Write-Host "  SKIP $label (not found)" -ForegroundColor Gray
        return 0
    }
    $size = Get-FolderSize $path
    if ($size -lt 1MB) {
        Write-Host "  SKIP $label (< 1 MB)" -ForegroundColor Gray
        return 0
    }
    if ($WhatIf) {
        Write-Host "  WOULD DELETE $label : $(Format-Size $size)" -ForegroundColor Yellow
        return $size
    }
    Write-Host "  CLEANING $label : $(Format-Size $size) ... " -NoNewline -ForegroundColor White
    Remove-Item "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "DONE" -ForegroundColor Green
    return $size
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DISK CLEANER" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "  ** DRY RUN - no files will be deleted **" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan

# Get free space before
$diskBefore = (Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace

$totalCleaned = 0

# --- Temp files ---
if (-not $SkipTemp) {
    Write-Host ""
    Write-Host "[TEMP FILES]" -ForegroundColor Yellow
    $totalCleaned += Remove-FolderContents "$userProfile\AppData\Local\Temp" "User Temp"
    $totalCleaned += Remove-FolderContents "C:\Windows\Temp" "Windows Temp"
    $totalCleaned += Remove-FolderContents "$userProfile\AppData\Local\CrashDumps" "Crash Dumps"
    $totalCleaned += Remove-FolderContents "$userProfile\AppData\Local\D3DSCache" "D3D Shader Cache"
}

# --- npm ---
if (-not $SkipNpm) {
    $npmCache = "$userProfile\AppData\Local\npm-cache"
    if (Test-Path $npmCache) {
        $size = Get-FolderSize $npmCache
        if ($size -gt 1MB) {
            Write-Host ""
            Write-Host "[NPM CACHE]" -ForegroundColor Yellow
            if ($WhatIf) {
                Write-Host "  WOULD CLEAN npm cache: $(Format-Size $size)" -ForegroundColor Yellow
            } else {
                Write-Host "  CLEANING npm cache: $(Format-Size $size) ... " -NoNewline
                & npm cache clean --force 2>$null
                Write-Host "DONE" -ForegroundColor Green
            }
            $totalCleaned += $size
        }
    }
}

# --- Yarn ---
if (-not $SkipYarn) {
    $yarnCache = "$userProfile\AppData\Local\Yarn"
    if (Test-Path $yarnCache) {
        $size = Get-FolderSize $yarnCache
        if ($size -gt 1MB) {
            Write-Host ""
            Write-Host "[YARN CACHE]" -ForegroundColor Yellow
            if ($WhatIf) {
                Write-Host "  WOULD CLEAN Yarn cache: $(Format-Size $size)" -ForegroundColor Yellow
            } else {
                Write-Host "  CLEANING Yarn cache: $(Format-Size $size) ... " -NoNewline
                & yarn cache clean 2>$null
                Write-Host "DONE" -ForegroundColor Green
            }
            $totalCleaned += $size
        }
    }
}

# --- Go ---
if (-not $SkipGo) {
    $goCache = "$userProfile\AppData\Local\go-build"
    if (Test-Path $goCache) {
        $size = Get-FolderSize $goCache
        if ($size -gt 1MB) {
            Write-Host ""
            Write-Host "[GO BUILD CACHE]" -ForegroundColor Yellow
            if ($WhatIf) {
                Write-Host "  WOULD CLEAN Go cache: $(Format-Size $size)" -ForegroundColor Yellow
            } else {
                Write-Host "  CLEANING Go build cache: $(Format-Size $size) ... " -NoNewline
                & go clean -cache 2>$null
                Write-Host "DONE" -ForegroundColor Green
            }
            $totalCleaned += $size
        }
    }
}

# --- Gradle ---
if (-not $SkipGradle) {
    Write-Host ""
    Write-Host "[GRADLE CACHE]" -ForegroundColor Yellow
    $totalCleaned += Remove-FolderContents "$userProfile\.gradle\caches" "Gradle caches"
}

# --- NuGet ---
if (-not $SkipNuGet) {
    $nugetCache = "$userProfile\AppData\Local\NuGet"
    if (Test-Path $nugetCache) {
        $size = Get-FolderSize $nugetCache
        if ($size -gt 1MB) {
            Write-Host ""
            Write-Host "[NUGET CACHE]" -ForegroundColor Yellow
            if ($WhatIf) {
                Write-Host "  WOULD CLEAN NuGet cache: $(Format-Size $size)" -ForegroundColor Yellow
            } else {
                Write-Host "  CLEANING NuGet cache: $(Format-Size $size) ... " -NoNewline
                & dotnet nuget locals all --clear 2>$null
                Write-Host "DONE" -ForegroundColor Green
            }
            $totalCleaned += $size
        }
    }
}

# --- Dart/Pub ---
if (-not $SkipDart) {
    Write-Host ""
    Write-Host "[DART/PUB CACHE]" -ForegroundColor Yellow
    $totalCleaned += Remove-FolderContents "$userProfile\AppData\Local\Pub" "Pub cache"
    $totalCleaned += Remove-FolderContents "$userProfile\AppData\Local\.dartServer" "Dart server"
}

# --- pip ---
$pipCache = "$userProfile\AppData\Local\pip"
if (Test-Path $pipCache) {
    $size = Get-FolderSize $pipCache
    if ($size -gt 1MB) {
        Write-Host ""
        Write-Host "[PIP CACHE]" -ForegroundColor Yellow
        $totalCleaned += Remove-FolderContents $pipCache "pip cache"
    }
}

# --- uv ---
$uvCache = "$userProfile\AppData\Local\uv"
if (Test-Path $uvCache) {
    $size = Get-FolderSize $uvCache
    if ($size -gt 1MB) {
        Write-Host ""
        Write-Host "[UV CACHE]" -ForegroundColor Yellow
        $totalCleaned += Remove-FolderContents $uvCache "uv cache"
    }
}

# --- NVIDIA installer cache ---
$nvCache = "$userProfile\AppData\Local\NVIDIA"
if (Test-Path $nvCache) {
    $size = Get-FolderSize $nvCache
    if ($size -gt 50MB) {
        Write-Host ""
        Write-Host "[NVIDIA CACHE]" -ForegroundColor Yellow
        $totalCleaned += Remove-FolderContents $nvCache "NVIDIA installer cache"
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($WhatIf) {
    Write-Host "  Would free: ~$(Format-Size $totalCleaned)" -ForegroundColor Yellow
} else {
    $diskAfter = (Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace
    $actualFreed = $diskAfter - $diskBefore
    Write-Host "  Space freed: $(Format-Size $actualFreed)" -ForegroundColor Green
    Write-Host "  Free now: $([math]::Round($diskAfter/1GB, 2)) GB" -ForegroundColor Green
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
