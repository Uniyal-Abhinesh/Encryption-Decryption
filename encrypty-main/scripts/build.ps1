# PowerShell build script for Windows
# This script replicates the functionality of the Makefile
# Run from project root - it will change to backend/cpp directory

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$CppDir = Join-Path $ProjectRoot "backend" "cpp"

# Change to C++ directory
Set-Location $CppDir

$CXX = "g++"
$CXXFLAGS = "-std=c++17 -g -Wall -I. -Isrc/app/encryptDecrypt -Isrc/app/fileHandling -Isrc/app/processes"

$MAIN_TARGET = "encrypt_decrypt.exe"
$CRYPTION_TARGET = "cryption.exe"

$MAIN_SRC = @(
    "main.cpp",
    "src/app/processes/ProcessManagement.cpp",
    "src/app/fileHandling/IO.cpp",
    "src/app/fileHandling/ReadEnv.cpp",
    "src/app/encryptDecrypt/Cryption.cpp"
)

$CRYPTION_SRC = @(
    "src/app/encryptDecrypt/CryptionMain.cpp",
    "src/app/encryptDecrypt/Cryption.cpp",
    "src/app/fileHandling/IO.cpp",
    "src/app/fileHandling/ReadEnv.cpp"
)

# Function to check if g++ is available
function Test-GPlusPlus {
    try {
        $null = & g++ --version 2>&1
        return $true
    } catch {
        return $false
    }
}

# Check if g++ is installed
if (-not (Test-GPlusPlus)) {
    Write-Host "Error: g++ compiler not found!" -ForegroundColor Red
    Write-Host "Please install MinGW-w64 or use Visual Studio with C++ support." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Install MinGW-w64 from https://www.mingw-w64.org/" -ForegroundColor Cyan
    Write-Host "Option 2: Install MSYS2 from https://www.msys2.org/ (includes MinGW-w64)" -ForegroundColor Cyan
    Write-Host "Option 3: Use Visual Studio Build Tools" -ForegroundColor Cyan
    exit 1
}

Write-Host "Building encryption/decryption project..." -ForegroundColor Green
Write-Host ""

# Clean previous builds if requested
if ($args -contains "clean") {
    Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
    Remove-Item -Path "*.o", "*.exe", "src\app\**\*.o" -ErrorAction SilentlyContinue -Recurse
    Write-Host "Clean complete." -ForegroundColor Green
    Write-Host ""
}

# Build object files for main target
Write-Host "Compiling main target..." -ForegroundColor Cyan
$MAIN_OBJ = @()
foreach ($src in $MAIN_SRC) {
    $obj = $src -replace "\.cpp$", ".o"
    $MAIN_OBJ += $obj
    
    if (-not (Test-Path $obj) -or (Get-Item $src).LastWriteTime -gt (Get-Item $obj).LastWriteTime) {
        Write-Host "  Compiling $src..." -ForegroundColor Gray
        $cmd = "$CXX $CXXFLAGS -c $src -o $obj"
        Invoke-Expression $cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error compiling $src" -ForegroundColor Red
            exit 1
        }
    }
}

# Link main target
Write-Host "  Linking $MAIN_TARGET..." -ForegroundColor Gray
$objList = $MAIN_OBJ -join " "
$cmd = "$CXX $CXXFLAGS $objList -o $MAIN_TARGET"
Invoke-Expression $cmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error linking $MAIN_TARGET" -ForegroundColor Red
    exit 1
}

# Build object files for cryption target
Write-Host "Compiling cryption target..." -ForegroundColor Cyan
$CRYPTION_OBJ = @()
foreach ($src in $CRYPTION_SRC) {
    $obj = $src -replace "\.cpp$", ".o"
    $CRYPTION_OBJ += $obj
    
    if (-not (Test-Path $obj) -or (Get-Item $src).LastWriteTime -gt (Get-Item $obj).LastWriteTime) {
        Write-Host "  Compiling $src..." -ForegroundColor Gray
        $cmd = "$CXX $CXXFLAGS -c $src -o $obj"
        Invoke-Expression $cmd
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error compiling $src" -ForegroundColor Red
            exit 1
        }
    }
}

# Link cryption target
Write-Host "  Linking $CRYPTION_TARGET..." -ForegroundColor Gray
$objList = $CRYPTION_OBJ -join " "
$cmd = "$CXX $CXXFLAGS $objList -o $CRYPTION_TARGET"
Invoke-Expression $cmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error linking $CRYPTION_TARGET" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Build successful!" -ForegroundColor Green
Write-Host "  Created: $MAIN_TARGET" -ForegroundColor Cyan
Write-Host "  Created: $CRYPTION_TARGET" -ForegroundColor Cyan

