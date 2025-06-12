# Setup Guide for Universal Database Importer

This guide provides detailed setup instructions for different operating systems and databases.

## Table of Contents

- [System Requirements](#system-requirements)
- [Python Installation](#python-installation)
- [Project Setup](#project-setup)
- [Database-Specific Setup](#database-specific-setup)
- [Troubleshooting Setup Issues](#troubleshooting-setup-issues)

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 500MB for application + space for data
- **Display**: 1024x768 resolution

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: SSD with 10GB+ free space
- **Display**: 1920x1080 or higher

### Operating System Requirements
- **Windows**: Windows 10 or later (64-bit)
- **macOS**: macOS 10.14 (Mojave) or later
- **Linux**: Ubuntu 18.04+, Debian 10+, Fedora 30+, or equivalent

## Python Installation

### Windows

1. **Download Python**
   - Visit [python.org](https://python.org/downloads/)
   - Download Python 3.7 or later (64-bit)

2. **Install Python**
   - Run the installer
   - ✅ Check "Add Python to PATH"
   - Click "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

### macOS

1. **Using Homebrew** (recommended)
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.9
   ```

2. **Using Official Installer**
   - Download from [python.org](https://python.org/downloads/)
   - Run the .pkg installer

3. **Verify Installation**
   ```bash
   python3 --version
   pip3 --version
   ```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
```

#### Fedora
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

#### Arch Linux
```bash
sudo pacman -S python python-pip tk
```

## Project Setup

### 1. Clone or Download the Repository

#### Using Git
```bash
git clone https://github.com/yourusername/universal-database-importer.git
cd universal-database-importer
```

#### Using Download
1. Download ZIP from GitHub
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

### 2. Create Virtual Environment

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter errors, try installing packages individually:

```bash
pip install pandas==1.3.0
pip install pymysql==1.0.2
pip install psycopg2-binary==2.9.0
pip install pyodbc==4.0.32
pip install sqlalchemy==1.4.0
pip install geopandas==0.12.0
pip install shapely==2.0.0
pip install fiona==1.9.0
pip install pyproj==3.4.0
pip install geoalchemy2==0.12.0
pip install matplotlib==3.4.0
pip install pillow==8.0.0
```

### 4. Platform-Specific Dependencies

#### macOS - Additional Setup
```bash
# Install GDAL (required for spatial data)
brew install gdal

# Install PostgreSQL client (for psycopg2)
brew install postgresql
```

#### Linux - Additional Setup
```bash
# Ubuntu/Debian
sudo apt install gdal-bin libgdal-dev
sudo apt install postgresql-client

# Fedora
sudo dnf install gdal gdal-devel
sudo dnf install postgresql
```

#### Windows - Additional Setup
- GDAL installation can be complex on Windows
- Consider using pre-compiled wheels:
  ```cmd
  pip install GDAL‑3.4.3‑cp39‑cp39‑win_amd64.whl
  ```
- Download wheels from: https://www.lfd.uci.edu/~gohlke/pythonlibs/

## Database-Specific Setup

### MySQL Setup

1. **Install MySQL Server**
   - Download from [mysql.com](https://dev.mysql.com/downloads/)
   - Follow installation wizard
   - Note root password

2. **Create Database and User**
   ```sql
   CREATE DATABASE your_database;
   CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON your_database.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### PostgreSQL Setup

1. **Install PostgreSQL**
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Follow installation wizard

2. **Create Database and User**
   ```sql
   CREATE DATABASE your_database;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;
   ```

3. **Enable PostGIS** (for spatial data)
   ```sql
   -- Connect to your database
   \c your_database
   
   -- Enable PostGIS
   CREATE EXTENSION postgis;
   ```

### SQL Server Setup

1. **Install SQL Server**
   - Download SQL Server Express from Microsoft
   - Install SQL Server Management Studio (SSMS)

2. **Install ODBC Driver 17**
   
   **Windows:**
   - Download from [Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   
   **macOS:**
   ```bash
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   brew update
   brew install msodbcsql17
   ```
   
   **Linux (Ubuntu):**
   ```bash
   curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
   curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
   apt-get update
   ACCEPT_EULA=Y apt-get install -y msodbcsql17
   ```

3. **Enable TCP/IP**
   - Open SQL Server Configuration Manager
   - Enable TCP/IP protocol
   - Restart SQL Server service

### SQLite Setup

No installation required! SQLite comes with Python.

To use:
1. Choose SQLite as database type
2. Enter the full path to your database file
3. Leave other fields empty

## Troubleshooting Setup Issues

### Common Installation Issues

#### 1. pip: command not found
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

#### 2. psycopg2 Installation Fails

**macOS:**
```bash
brew install postgresql
pip install psycopg2-binary
```

**Linux:**
```bash
sudo apt install libpq-dev  # Ubuntu/Debian
sudo dnf install postgresql-devel  # Fedora
```

#### 3. GDAL/Fiona Installation Issues

**Windows:**
- Use OSGeo4W installer
- Or use conda: `conda install -c conda-forge gdal fiona`

**macOS:**
```bash
brew install gdal
pip install --no-binary fiona fiona
```

**Linux:**
```bash
sudo apt install gdal-bin python3-gdal  # Ubuntu
pip install fiona --no-binary fiona
```

#### 4. Tkinter Not Found

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Verification Script

Create a file `test_setup.py`:

```python
#!/usr/bin/env python3
"""Test if all dependencies are correctly installed."""

import sys

def test_imports():
    """Test all required imports."""
    modules = [
        ('pandas', 'Data manipulation'),
        ('tkinter', 'GUI framework'),
        ('pymysql', 'MySQL support'),
        ('psycopg2', 'PostgreSQL support'),
        ('pyodbc', 'SQL Server support'),
        ('sqlalchemy', 'Database abstraction'),
        ('geopandas', 'Spatial data support'),
        ('shapely', 'Geometric operations'),
        ('matplotlib', 'Data visualization'),
        ('PIL', 'Image processing')
    ]
    
    failed = []
    
    for module, description in modules:
        try:
            __import__(module)
            print(f"✓ {module:<15} - {description}")
        except ImportError as e:
            print(f"✗ {module:<15} - {description}")
            failed.append((module, str(e)))
    
    if failed:
        print("\n❌ Some modules failed to import:")
        for module, error in failed:
            print(f"  - {module}: {error}")
        sys.exit(1)
    else:
        print("\n✅ All modules imported successfully!")

if __name__ == "__main__":
    test_imports()
```

Run the test:
```bash
python test_setup.py
```

## Running the Application

Once setup is complete:

### Windows
```cmd
run.bat
```

### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

### Direct Python
```bash
python main.py  # Windows
python3 main.py  # macOS/Linux
```

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting-setup-issues) section
2. Search existing [GitHub Issues](https://github.com/yourusername/universal-database-importer/issues)
3. Create a new issue with:
   - Your operating system and version
   - Python version (`python --version`)
   - Error messages (full traceback)
   - Steps to reproduce the issue

---

Happy importing! 🚀