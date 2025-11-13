# Parallel Encryption and Decryption

## Overview

This project demonstrates the implementation of encryption and decryption mechanisms using parallel processing techniques in C++. By leveraging both multiprocessing and multithreading, the project aims to enhance the efficiency and performance of cryptographic operations.

The project includes:
- **C++ Backend**: High-performance parallel encryption/decryption engine
- **Web Frontend**: Modern, user-friendly browser-based interface built with Flask
- **Command-Line Interface**: Direct access to encryption/decryption functionality

### Encryption Algorithm

The project uses a simple but effective encryption algorithm:
- **Encryption**: Each byte is shifted by a key value: `encrypted_byte = (original_byte + key) % 256`
- **Decryption**: Each byte is shifted back: `decrypted_byte = (encrypted_byte - key) % 256`
- **Key**: Stored in environment variable `ENCRYPTION_KEY` (defaults to a preset value if not set)

### Parallel Processing

The system processes multiple files concurrently using:
- **Multiprocessing**: Child processes handle individual files
- **Task Queue**: Efficient task distribution and management
- **Parallel Execution**: Significantly faster than sequential processing

## Branches

The repository contains two primary branches, each focusing on a distinct parallel processing approach:

### 1. `add/childProcessing`

**Description:** This branch showcases the use of parallel multiprocessing by creating child processes to handle encryption and decryption tasks. It utilizes the `fork()` system call to spawn child processes, enabling concurrent execution of tasks.

**Key Features:**

- **Process Management:** Implements process creation and management using `fork()`.
- **Task Queue:** Manages encryption and decryption tasks using a queue structure.
- **Task Execution:** Child processes execute tasks independently, allowing parallel processing.

### 2. `add/multithreading`

**Description:** This branch focuses on multithreading combined with shared memory to perform encryption and decryption. It employs POSIX threads (`pthread`) and utilizes shared memory segments for efficient inter-thread communication.

**Key Features:**

- **Multithreading:** Implements concurrent execution using POSIX threads.
- **Shared Memory:** Utilizes shared memory for communication between threads.
- **Semaphores:** Employs semaphores to manage synchronization and ensure data consistency.

## Prerequisites

### Required Software

- **C++ Compiler:** GCC 7.0+ or Clang with C++17 support
- **Python 3.7+:** Required for the web frontend
- **Make:** For building the C++ project (Linux/Mac/WSL)
- **Flask:** Python web framework (installed via requirements.txt)

### Platform-Specific Requirements

**Linux/WSL:**
```bash
# Install build tools
sudo apt update
sudo apt install build-essential -y
```

**Windows:**
- MinGW-w64, MSYS2, or Visual Studio with C++ support
- PowerShell 5.0+ (for build scripts)

**macOS:**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

## Installation

### Step 1: Clone the Repository

```bash
git clone <repo-url>
cd encrypty-main
```

### Step 2: Build the C++ Project

**On Linux/Mac/WSL (using Make):**

```bash
# Navigate to C++ backend directory
cd backend/cpp

# Build the encryption/decryption executables
make

# If you encounter linker errors with __isoc23_strtol, the Makefile includes
# a compatibility fix (compat.c) that should resolve the issue

# Or build from project root
cd backend/cpp && make
```

**On Windows (using PowerShell):**

```powershell
# Option 1: Use the PowerShell build script (from project root)
.\scripts\build.ps1

# Option 2: Use the batch file wrapper
.\scripts\build.bat

# To clean and rebuild
.\scripts\build.ps1 clean

# Or navigate to C++ directory and use make (if available)
cd backend\cpp
make
```

**Note for Windows users:** You need a C++ compiler installed. Options:
- **MinGW-w64**: Download from https://www.mingw-w64.org/
- **MSYS2**: Download from https://www.msys2.org/ (includes MinGW-w64)
- **Visual Studio**: Install Visual Studio with C++ support

If you have MinGW-w64 installed, make sure `g++` is in your PATH. You can verify by running:
```powershell
g++ --version
```

**Build Output:**
This will create two executables in `backend/cpp/`:
- `encrypt_decrypt` (or `encrypt_decrypt.exe` on Windows): Main program for processing directories
- `cryption` (or `cryption.exe` on Windows): Helper program for individual file operations

### Step 3: Set Up Python Environment (for Web Frontend)

**On Linux/Mac/WSL:**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify you're using the venv's Python/pip
which python  # Should show: .../encrypty-main/venv/bin/python
which pip     # Should show: .../encrypty-main/venv/bin/pip

# Install Python dependencies
pip install -r requirements.txt

# Verify Flask is installed
pip list | grep -i flask
```

**On Windows:**

```powershell
# Create a virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

**Important:** Always activate the virtual environment before running the Flask app. If `which pip` shows `/usr/bin/pip` instead of the venv path, deactivate and reactivate:
```bash
deactivate
source venv/bin/activate  # Linux/Mac/WSL
# or
venv\Scripts\activate     # Windows
```

### Step 4: Set Up Environment Variable (Optional)

The encryption key can be set via environment variable:

```bash
# Linux/Mac/WSL
export ENCRYPTION_KEY=123

# Windows PowerShell
$env:ENCRYPTION_KEY="123"

# Windows CMD
set ENCRYPTION_KEY=123
```

If not set, the system uses a default key.

### Step 5: Create Test Directories (Optional)

```bash
# Create test directory with sample files (in data/test)
python3 backend/python/scripts/makeDirs.py

# Or specify a custom directory name (will be created in data/)
python3 backend/python/scripts/makeDirs.py mytest

# Or create in a custom absolute path
python3 backend/python/scripts/makeDirs.py /path/to/custom/directory
```

## How to Run

This section provides complete step-by-step instructions to get the project running.

### Prerequisites Check

Before running, ensure you have:
1. ✅ Built the C++ project (see [Installation - Step 2](#step-2-build-the-c-project))
2. ✅ Set up Python virtual environment (see [Installation - Step 3](#step-3-set-up-python-environment-for-web-frontend))
3. ✅ Installed Python dependencies

### Quick Run Guide

**For Web Frontend (Recommended):**
```bash
# 1. Navigate to project root
cd encrypty-main

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac/WSL
# or
venv\Scripts\activate     # Windows

# 3. Start the server
python backend/python/app.py

# 4. Open browser to http://localhost:5000
```

**For Command Line:**
```bash
# 1. Navigate to C++ backend
cd encrypty-main/backend/cpp

# 2. Run the executable
./encrypt_decrypt  # Linux/Mac/WSL
# or
.\encrypt_decrypt.exe  # Windows

# 3. Follow prompts to enter directory and action
```

---

## Usage

### Option 1: Web Frontend (Recommended)

The web frontend provides a user-friendly interface for encrypting and decrypting files.

**Complete Step-by-Step Instructions:**

**Step 1: Navigate to Project Directory**
```bash
# WSL/Linux/Mac
cd /path/to/encrypty-main

# Windows PowerShell
cd C:\path\to\encrypty-main
```

**Step 2: Activate Virtual Environment**
```bash
# Linux/Mac/WSL
source venv/bin/activate

# Windows PowerShell
venv\Scripts\activate

# Windows CMD
venv\Scripts\activate.bat
```

**Step 3: Verify Virtual Environment is Active**
```bash
# Check Python path (should show venv path)
which python   # Linux/Mac/WSL
where python   # Windows

# Check pip path (should show venv path)
which pip      # Linux/Mac/WSL
where pip      # Windows

# If paths don't show venv, reactivate:
# Linux/Mac/WSL: deactivate && source venv/bin/activate
# Windows: deactivate && venv\Scripts\activate
```

**Step 4: Start the Flask Server**
```bash
# From project root directory
python backend/python/app.py

# Or using python3
python3 backend/python/app.py

# Alternative: Navigate to backend/python first
cd backend/python
python app.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
Press CTRL+C to quit
```

**Step 5: Access the Web Interface**
- Open your web browser
- Navigate to: `http://localhost:5000`
- The encryption/decryption interface should load

**Step 6: Stop the Server**
- Press `CTRL+C` in the terminal where the server is running

**Using the Interface:**

- **Upload Files Tab:**
  - Click "Select Files" to choose one or more files
  - Select either "Encrypt" or "Decrypt" radio button
  - Click "Process Files"
  - Wait for processing to complete
  - Download processed files from the results section

- **Process Directory Tab:**
  - Enter the full path to a directory containing files
  - Select either "Encrypt" or "Decrypt" radio button
  - Click "Process Directory"
  - All files in the directory (and subdirectories) will be processed
  - Results will show the number of files processed

**Supported File Types:**
- Text files (.txt)
- Documents (.pdf, .doc, .docx)
- Images (.jpg, .jpeg, .png, .gif)
- Archives (.zip)
- Binary files (.bin)

**Note:** The web interface processes files in a temporary directory and copies results to the `processed/` folder for download.

### Option 2: Command Line Interface

For command-line usage without the web interface:

**Complete Step-by-Step Instructions:**

**Step 1: Navigate to C++ Backend Directory**
```bash
# Linux/Mac/WSL
cd encrypty-main/backend/cpp

# Windows
cd encrypty-main\backend\cpp
```

**Step 2: Ensure Executable Exists and Has Permissions**
```bash
# Linux/Mac/WSL - Make executable if needed
chmod +x encrypt_decrypt

# Verify executable exists
ls -la encrypt_decrypt  # Linux/Mac/WSL
dir encrypt_decrypt.exe # Windows
```

**Step 3: Run the Executable**
```bash
# Linux/Mac/WSL
./encrypt_decrypt

# Windows PowerShell
.\encrypt_decrypt.exe

# Windows CMD
encrypt_decrypt.exe
```

**Step 4: Follow the Prompts**

When the program starts, you'll be prompted for:

1. **Directory Path:**
   - Enter the path to the directory containing files to process
   - Can be relative (e.g., `../../data/test`) or absolute (e.g., `/mnt/c/Users/Documents/files`)
   - The program will recursively process all files in the directory

2. **Action:**
   - Enter `encrypt` to encrypt files
   - Enter `decrypt` to decrypt files

**Example Session:**
```bash
$ cd encrypty-main/backend/cpp
$ ./encrypt_decrypt
Enter the directory path: ../../data/test
Enter the action (encrypt/decrypt): encrypt

# Program processes files in parallel
# You'll see output indicating progress
# Files are modified in-place (encrypted)
```

**Example with Absolute Path:**
```bash
$ ./encrypt_decrypt
Enter the directory path: /mnt/c/Users/prema/Documents/myfiles
Enter the action (encrypt/decrypt): decrypt

# All files in myfiles directory (and subdirectories) will be decrypted
```

**Important Notes:**
- Files are modified **in-place** (original files are encrypted/decrypted)
- The program processes files in **parallel** for better performance
- Make sure you have **write permissions** for the directory
- The program will process **all files recursively** in the specified directory

**Processing Directories:**
- The program recursively processes all files in the specified directory
- Files are processed in parallel for better performance
- Original files are modified in-place (encrypted/decrypted)

## Project Structure

```
encrypty-main/
├── README.md              # Project documentation
│
├── backend/               # Backend code
│   ├── cpp/              # C++ backend
│   │   ├── main.cpp      # Main C++ entry point
│   │   ├── compat.c      # Compatibility shim for glibc issues
│   │   ├── Makefile      # Build configuration (Linux/Mac/WSL)
│   │   ├── encrypt_decrypt(.exe)  # Compiled executable (main program)
│   │   ├── cryption(.exe)         # Compiled helper executable
│   │   └── src/
│   │       └── app/
│   │           ├── encryptDecrypt/  # Encryption/decryption logic
│   │           │   ├── Cryption.cpp
│   │           │   ├── Cryption.hpp
│   │           │   └── CryptionMain.cpp
│   │           ├── fileHandling/    # File I/O operations
│   │           │   ├── IO.cpp
│   │           │   ├── IO.hpp
│   │           │   └── ReadEnv.cpp
│   │           └── processes/       # Process management
│   │               ├── ProcessManagement.cpp
│   │               ├── ProcessManagement.hpp
│   │               └── Task.hpp
│   │
│   └── python/           # Python/Flask backend
│       ├── app.py        # Flask web server
│       ├── requirements.txt  # Python dependencies (Flask, flask-cors)
│       └── scripts/
│           └── makeDirs.py  # Test directory creation script
│
├── frontend/              # Frontend code
│   ├── templates/
│   │   └── index.html    # Web frontend HTML
│   └── static/
│       ├── css/
│       │   └── style.css # Frontend styling
│       └── js/
│           └── main.js   # Frontend JavaScript
│
├── scripts/               # Build and utility scripts
│   ├── build.ps1         # PowerShell build script (Windows)
│   └── build.bat          # Batch file wrapper (Windows)
│
├── data/                  # Runtime data directories
│   ├── uploads/          # Temporary upload directory (auto-created)
│   ├── processed/        # Processed files directory (auto-created)
│   └── test/             # Test directory (created by makeDirs.py)
│
└── venv/                  # Python virtual environment (not in git)
```

## API Endpoints

The Flask backend provides the following REST API endpoints:

- **`GET /`** - Serves the web frontend HTML page
- **`POST /api/encrypt`** - Process uploaded files
  - Content-Type: `multipart/form-data`
  - Form fields:
    - `files`: One or more files to process
    - `action`: Either "encrypt" or "decrypt"
  - Returns: JSON with success status, message, and processed file list
- **`POST /api/process-directory`** - Process files in a directory
  - Content-Type: `application/json`
  - JSON body: `{"directory": "path/to/directory", "action": "encrypt|decrypt"}`
  - Returns: JSON with success status, message, and file count
- **`GET /api/download/<filename>`** - Download processed files
  - Returns: File download

## Troubleshooting

### C++ Build Issues

**g++ not found (Linux/WSL):**
```bash
sudo apt update
sudo apt install build-essential -y
g++ --version  # Verify installation
```

**Linker error: `__isoc23_strtol` undefined reference:**
- This is a compatibility issue with newer glibc versions
- The Makefile includes `compat.c` which provides a compatibility shim
- If you still see this error, try:
  ```bash
  make clean
  make
  ```

**Make not found (Windows):**
- Use the provided `build.ps1` or `build.bat` scripts instead
- Or install make via MSYS2 or Chocolatey

**Clean and rebuild:**
- **Linux/Mac/WSL:**
  ```bash
  make clean
  make
  ```
- **Windows:**
  ```powershell
  .\build.ps1 clean
  .\build.ps1
  ```

### Web Frontend Issues

**ModuleNotFoundError: No module named 'flask':**
```bash
# Make sure venv is activated
source venv/bin/activate  # Linux/Mac/WSL
venv\Scripts\activate      # Windows

# Verify you're using venv's pip
which pip  # Should show venv path, not /usr/bin/pip

# If it shows /usr/bin/pip, reactivate:
deactivate
source venv/bin/activate
pip install -r requirements.txt
```

**Port already in use:**
- Change the port in `app.py` (line: `app.run(..., port=5000)`)
- Or stop the process using port 5000:
  ```bash
  # Linux/Mac/WSL
  lsof -ti:5000 | xargs kill -9
  
  # Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

**Executable not found error in web interface:**
- Make sure you've run `make` (or `build.ps1` on Windows) to build the C++ project
- Ensure `encrypt_decrypt` (or `encrypt_decrypt.exe`) exists in `backend/cpp/` directory
- Check that the file has execute permissions:
  ```bash
  chmod +x backend/cpp/encrypt_decrypt
  ```

**Virtual environment not activating properly:**
```bash
# Check if venv exists
ls -la venv/

# If not, recreate it
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Verify activation
which python  # Should show venv path
pip install -r requirements.txt
```

### File Processing Issues

**Directory not found:**
- Use absolute paths for directories
- On Windows/WSL, use forward slashes: `C:/Users/Documents/test`
- Or escaped backslashes: `C:\\Users\\Documents\\test`
- In WSL, Windows paths: `/mnt/c/Users/Documents/test`

**Files not processing:**
- Check file permissions: `ls -la <directory>`
- Ensure files are not locked by other applications
- Verify the directory contains readable files
- Check that the C++ executable has permission to write to the directory

**Permission denied when running executable:**
```bash
chmod +x encrypt_decrypt
chmod +x cryption
```

**Clock skew warning (WSL):**
- This is a harmless warning about time sync between Windows and WSL
- It doesn't affect functionality
- Can be ignored or fixed by syncing WSL time:
  ```bash
  sudo hwclock -s
  ```

## Development

### Building from Source

**Linux/Mac/WSL:**
```bash
# Navigate to C++ backend directory
cd backend/cpp

# Clean previous builds
make clean

# Build all targets
make

# Build specific target
make encrypt_decrypt
make cryption
```

**Windows:**
```powershell
# From project root
.\scripts\build.ps1 clean
.\scripts\build.ps1

# Or use the batch file
.\scripts\build.bat clean
.\scripts\build.bat

# Or navigate to C++ directory
cd backend\cpp
make clean
make
```

### Running Tests

```bash
# Create test directory
python3 backend/python/scripts/makeDirs.py

# Test encryption via command line
cd backend/cpp
./encrypt_decrypt
# Enter: ../../data/test
# Enter: encrypt

# Test decryption
./encrypt_decrypt
# Enter: ../../data/test
# Enter: decrypt

# Test web interface (from project root)
source venv/bin/activate
python backend/python/app.py
# Open http://localhost:5000 in browser
# Upload test files and verify encryption/decryption
```

### Code Structure

- **C++ Backend**: Handles the core encryption/decryption logic with parallel processing
- **Flask Backend**: Provides REST API and serves the web frontend
- **Frontend**: Modern HTML/CSS/JavaScript interface for user interaction

### Adding New Features

1. **C++ Changes**: Modify source files in `src/app/`, then rebuild with `make`
2. **Backend Changes**: Edit `app.py` for API changes
3. **Frontend Changes**: Edit files in `templates/` and `static/`

## Security Notes

- The encryption algorithm is simple and intended for demonstration purposes
- For production use, consider implementing stronger encryption (AES, RSA, etc.)
- Environment variables should be kept secure
- Processed files are temporarily stored; consider adding cleanup mechanisms
- File uploads should be validated and sanitized in production

## Performance

- Parallel processing significantly speeds up batch operations
- Performance scales with the number of CPU cores
- Large files are processed in chunks to manage memory
- Web interface provides real-time feedback on processing status

## Contributing

When contributing to this project:

1. Test your changes with both command-line and web interfaces
2. Ensure C++ code compiles without warnings
3. Follow existing code style and structure
4. Update documentation as needed
5. Test on multiple platforms if possible (Linux, Windows, WSL)

## License

[Add your license information here]

## Support

For issues, questions, or contributions:
- Create an issue on the repository
- Contact the maintainers
- Check the troubleshooting section above

## Quick Start Summary

### First Time Setup (One-Time)

**For WSL/Linux users:**
```bash
# 1. Navigate to project
cd encrypty-main

# 2. Build C++ project
cd backend/cpp && make && cd ../..

# 3. Create Python virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install Python dependencies
pip install -r backend/python/requirements.txt
```

**For Windows users:**
```powershell
# 1. Navigate to project
cd encrypty-main

# 2. Build C++ project
.\scripts\build.ps1

# 3. Create Python virtual environment
python -m venv venv

# 4. Activate virtual environment
venv\Scripts\activate

# 5. Install Python dependencies
pip install -r backend\python\requirements.txt
```

### Running the Project (Every Time)

**Web Frontend:**
```bash
# 1. Navigate to project root
cd encrypty-main

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac/WSL
venv\Scripts\activate      # Windows

# 3. Start server
python backend/python/app.py

# 4. Open http://localhost:5000 in browser
```

**Command Line:**
```bash
# 1. Navigate to C++ backend
cd encrypty-main/backend/cpp

# 2. Run executable
./encrypt_decrypt      # Linux/Mac/WSL
.\encrypt_decrypt.exe  # Windows

# 3. Follow prompts
```

---

**Happy Encrypting! 🔐**
