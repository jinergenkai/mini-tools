#Requires -Version 5.1
<#
.SYNOPSIS
    Compact Docker Desktop VHDX to reclaim unused disk space.
.DESCRIPTION
    Stops Docker, shuts down WSL, compacts the virtual disk, then optionally restarts Docker.
    Must be run as Administrator.
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\project\py-ws\clean-wins\compact-docker.ps1
#>

$ErrorActionPreference = 'Stop'

# Check admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host ""
    Write-Host "  Not running as Admin. Relaunching elevated..." -ForegroundColor Yellow
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

$vhdxPath = "$env:USERPROFILE\AppData\Local\Docker\wsl\disk\docker_data.vhdx"

if (-not (Test-Path $vhdxPath)) {
    Write-Host "  Docker VHDX not found at: $vhdxPath" -ForegroundColor Red
    Write-Host "  Is Docker Desktop installed?" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DOCKER VHDX COMPACTOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Show before size
$sizeBefore = (Get-Item $vhdxPath).Length
$sizeBeforeGB = [math]::Round($sizeBefore / 1GB, 2)
Write-Host ""
Write-Host "  VHDX path: $vhdxPath" -ForegroundColor Gray
Write-Host "  Size BEFORE: $sizeBeforeGB GB" -ForegroundColor Yellow

# Stop Docker Desktop
Write-Host ""
Write-Host "  [1/4] Stopping Docker Desktop..." -ForegroundColor White
$dockerProc = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if ($dockerProc) {
    Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
    # Also stop backend processes
    Stop-Process -Name "com.docker.backend" -Force -ErrorAction SilentlyContinue
    Stop-Process -Name "com.docker.proxy" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "  Docker Desktop stopped." -ForegroundColor Green
} else {
    Write-Host "  Docker Desktop not running." -ForegroundColor Gray
}

# Shutdown WSL
Write-Host "  [2/4] Shutting down WSL..." -ForegroundColor White
wsl --shutdown 2>$null
Start-Sleep -Seconds 5
Write-Host "  WSL stopped." -ForegroundColor Green

# Create diskpart script
Write-Host "  [3/4] Compacting VHDX (this may take a few minutes)..." -ForegroundColor White
$diskpartScript = "$env:TEMP\compact_docker.txt"
@"
select vdisk file="$vhdxPath"
compact vdisk
exit
"@ | Set-Content $diskpartScript -Encoding ASCII

diskpart /s $diskpartScript

Remove-Item $diskpartScript -Force -ErrorAction SilentlyContinue

# Show after size
$sizeAfter = (Get-Item $vhdxPath).Length
$sizeAfterGB = [math]::Round($sizeAfter / 1GB, 2)
$freedGB = [math]::Round(($sizeBefore - $sizeAfter) / 1GB, 2)

Write-Host ""
Write-Host "  [4/4] Done!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Size BEFORE: $sizeBeforeGB GB" -ForegroundColor Yellow
Write-Host "  Size AFTER:  $sizeAfterGB GB" -ForegroundColor Green
Write-Host "  FREED:       $freedGB GB" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Docker Desktop is stopped. Start it manually when you need it." -ForegroundColor Gray
Write-Host ""
pause
