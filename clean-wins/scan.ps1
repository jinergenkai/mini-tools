#Requires -Version 5.1
<#
.SYNOPSIS
    Scan C: drive and report what's using space.
.DESCRIPTION
    Run this first to see what's eating your disk.
    Then run clean.ps1 to clean safe caches.
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File scan.ps1
#>

param(
    [switch]$Detailed
)

$ErrorActionPreference = 'SilentlyContinue'
$userProfile = $env:USERPROFILE

function Format-Size($bytes) {
    if ($bytes -ge 1GB) { return "$([math]::Round($bytes/1GB, 2)) GB" }
    if ($bytes -ge 1MB) { return "$([math]::Round($bytes/1MB, 0)) MB" }
    return "$([math]::Round($bytes/1KB, 0)) KB"
}

function Get-FolderSize($path) {
    if (-not (Test-Path $path)) { return 0 }
    return (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DISK SPACE SCANNER" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan

# Disk overview
Write-Host ""
Write-Host "[DISK OVERVIEW]" -ForegroundColor Yellow
$disk = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'"
$total = [math]::Round($disk.Size / 1GB, 2)
$free = [math]::Round($disk.FreeSpace / 1GB, 2)
$used = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 2)
$pct = [math]::Round(($used / $total) * 100, 1)
$bar = "[" + ("=" * [math]::Floor($pct / 2)) + (" " * (50 - [math]::Floor($pct / 2))) + "]"
Write-Host "  Total: $total GB  |  Used: $used GB ($pct%)  |  Free: $free GB"
Write-Host "  $bar" -ForegroundColor $(if ($pct -gt 90) { 'Red' } elseif ($pct -gt 75) { 'Yellow' } else { 'Green' })

# Cleanable caches
Write-Host ""
Write-Host "[CLEANABLE CACHES]" -ForegroundColor Yellow

$caches = @(
    @{ Name = "Windows Temp";   Path = "C:\Windows\Temp" }
    @{ Name = "User Temp";      Path = "$userProfile\AppData\Local\Temp" }
    @{ Name = "npm cache";      Path = "$userProfile\AppData\Local\npm-cache" }
    @{ Name = "Yarn cache";     Path = "$userProfile\AppData\Local\Yarn" }
    @{ Name = "Go build cache"; Path = "$userProfile\AppData\Local\go-build" }
    @{ Name = "Gradle caches";  Path = "$userProfile\.gradle\caches" }
    @{ Name = "NuGet cache";    Path = "$userProfile\AppData\Local\NuGet" }
    @{ Name = "Pub cache";      Path = "$userProfile\AppData\Local\Pub" }
    @{ Name = "Dart server";    Path = "$userProfile\AppData\Local\.dartServer" }
    @{ Name = "D3DSCache";      Path = "$userProfile\AppData\Local\D3DSCache" }
    @{ Name = "CrashDumps";     Path = "$userProfile\AppData\Local\CrashDumps" }
    @{ Name = "pip cache";      Path = "$userProfile\AppData\Local\pip" }
    @{ Name = "uv cache";       Path = "$userProfile\AppData\Local\uv" }
    @{ Name = "NVIDIA cache";   Path = "$userProfile\AppData\Local\NVIDIA" }
)

$totalCleanable = 0
foreach ($c in $caches) {
    $size = Get-FolderSize $c.Path
    if ($size -gt 10MB) {
        $totalCleanable += $size
        $sizeStr = Format-Size $size
        Write-Host "  $($c.Name.PadRight(20)) $($sizeStr.PadLeft(10))   $($c.Path)" -ForegroundColor White
    }
}
Write-Host ""
Write-Host "  TOTAL CLEANABLE: $(Format-Size $totalCleanable)" -ForegroundColor Green

# Large user folders
Write-Host ""
Write-Host "[USER PROFILE - LARGE FOLDERS]" -ForegroundColor Yellow
Get-ChildItem $userProfile -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = Get-FolderSize $_.FullName
    [PSCustomObject]@{ Name = $_.Name; Size = $size; Path = $_.FullName }
} | Where-Object { $_.Size -gt 200MB } | Sort-Object Size -Descending | ForEach-Object {
    Write-Host "  $($_.Name.PadRight(20)) $($(Format-Size $_.Size).PadLeft(10))   $($_.Path)" -ForegroundColor White
}

# AppData Local large folders
Write-Host ""
Write-Host "[APPDATA LOCAL - LARGE FOLDERS]" -ForegroundColor Yellow
Get-ChildItem "$userProfile\AppData\Local" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = Get-FolderSize $_.FullName
    [PSCustomObject]@{ Name = $_.Name; Size = $size; Path = $_.FullName }
} | Where-Object { $_.Size -gt 200MB } | Sort-Object Size -Descending | ForEach-Object {
    Write-Host "  $($_.Name.PadRight(20)) $($(Format-Size $_.Size).PadLeft(10))   $($_.Path)" -ForegroundColor White
}

# AppData Roaming large folders
Write-Host ""
Write-Host "[APPDATA ROAMING - LARGE FOLDERS]" -ForegroundColor Yellow
Get-ChildItem "$userProfile\AppData\Roaming" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = Get-FolderSize $_.FullName
    [PSCustomObject]@{ Name = $_.Name; Size = $size; Path = $_.FullName }
} | Where-Object { $_.Size -gt 200MB } | Sort-Object Size -Descending | ForEach-Object {
    Write-Host "  $($_.Name.PadRight(20)) $($(Format-Size $_.Size).PadLeft(10))   $($_.Path)" -ForegroundColor White
}

# Installed programs
Write-Host ""
Write-Host "[INSTALLED PROGRAMS - TOP 15 LARGEST]" -ForegroundColor Yellow
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -and $_.EstimatedSize -gt 100000 } |
    Select-Object DisplayName, @{N='SizeMB';E={[math]::Round($_.EstimatedSize/1024,1)}} |
    Sort-Object SizeMB -Descending |
    Select-Object -First 15 |
    ForEach-Object {
        Write-Host "  $($_.DisplayName.PadRight(50).Substring(0,50)) $("$($_.SizeMB) MB".PadLeft(12))" -ForegroundColor White
    }

# Docker check
Write-Host ""
Write-Host "[DOCKER]" -ForegroundColor Yellow
$dockerData = Get-FolderSize "$userProfile\AppData\Local\Docker"
if ($dockerData -gt 1GB) {
    Write-Host "  Docker data: $(Format-Size $dockerData)" -ForegroundColor Red
    Write-Host "  Tip: run 'docker system prune -a' to clean unused images" -ForegroundColor Gray
} else {
    Write-Host "  Docker data: $(Format-Size $dockerData)" -ForegroundColor Green
}

# Recycle Bin
Write-Host ""
Write-Host "[RECYCLE BIN]" -ForegroundColor Yellow
try {
    $shell = New-Object -ComObject Shell.Application
    $rb = $shell.Namespace(0xA)
    $rbSize = ($rb.Items() | Measure-Object -Property Size -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host "  Recycle Bin: $(Format-Size $rbSize)"
} catch {
    Write-Host "  Could not read Recycle Bin size"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Run clean.ps1 to clean safe caches" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
