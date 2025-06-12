# Universal Database Importer

A powerful cross-platform GUI application for importing CSV files and Shapefiles into various database systems with advanced spatial data support and visualization capabilities.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Overview

Universal Database Importer is a comprehensive solution for data engineers, GIS professionals, and developers who need to efficiently import structured and spatial data into multiple database systems. With its intuitive GUI and robust feature set, it simplifies the process of data migration and spatial data management.

## Key Features

### 🗄️ Multi-Database Support
- **MySQL** (default port: 3306)
- **PostgreSQL** with PostGIS (default port: 5432)
- **SQLite** (file-based)
- **SQL Server** (default port: 1433)

### 📊 Data Import Capabilities
- **CSV Import**: Browse, preview, and selectively import CSV data
- **Shapefile Import**: Full support for geographic data with automatic geometry handling
- **Column Selection**: Choose specific columns to import
- **Batch Processing**: Efficient chunk-based import for large datasets
- **Progress Tracking**: Real-time progress bars with row counts

### 🌍 Spatial Data Features
- **PostGIS Integration**: Automatic detection and enablement
- **Geometry Visualization**: Right-click to visualize spatial data
- **WKT Support**: Fallback to Well-Known Text when PostGIS unavailable
- **Spatial Index Creation**: Automatic indexing for better performance
- **Multiple Geometry Types**: POINT, LINESTRING, POLYGON, and MULTI* variants

### 💻 User Experience
- **Tabbed Interface**: Organized workflow with Connection, Import, Query, and Spatial Tools tabs
- **Visual Status Indicators**: Connection status with ✓/✗ icons
- **Auto Port Detection**: Automatically fills default ports based on database type
- **Threading Support**: Non-blocking operations prevent UI freezing
- **Resizable Panels**: Adjustable query editor and results view

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended for large datasets)
- **Storage**: Varies based on data size

## Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/universal-database-importer.git
   cd universal-database-importer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Database-Specific Setup

#### PostgreSQL with PostGIS
For full spatial support:
```sql
CREATE EXTENSION postgis;
```
Or use the provided `enable_postgis.sql` script.

#### SQL Server
Install ODBC Driver 17:
- **Windows**: [Download from Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- **macOS**: `brew install msodbcsql17`
- **Linux**: Follow [Microsoft's guide](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)

## Usage Guide

### Starting the Application

#### Windows
```bash
# Using the batch file
run.bat

# Or directly
python main.py
```

#### macOS/Linux
```bash
# Using the shell script
chmod +x run.sh
./run.sh

# Or directly
python3 main.py
```

### Step-by-Step Guide

1. **Database Connection**:
   - Select your database type (auto-fills default port)
   - Enter connection details (host, port, username, password, database)
   - Click "Test Connection" to verify (shows ✓ on success, ✗ on failure)
   - Click "Connect" to establish connection

2. **Import CSV**:
   - Click "Browse CSV" to select your file
   - Preview data and select columns to import
   - Enter table name (auto-filled from filename)
   - Click "Import to Database"

3. **Import Shapefile**:
   - Click "Browse Shapefile" to select your .shp file
   - Preview attributes and select columns to import
   - Geometry column is automatically included for spatial data
   - Enter table name (auto-filled from filename)
   - Click "Import to Database"

4. **SQL Queries**:
   - Type your SQL query in the text area
   - Click "Execute Query"
   - View results in the resizable table below
   - Right-click on geometry values to visualize spatial data

5. **Spatial Tools** (PostgreSQL only):
   - Check PostGIS extension status
   - Enable PostGIS if you have permissions
   - View all tables with spatial data
   - Convert WKT text columns to proper geometry columns
   - Automatic spatial index creation during conversion

### New Features

- **Non-Blocking Operations**: All database operations run in separate threads
- **Resizable Panes**: Drag the divider between query and results sections
- **Geometry Visualization**: View POINT, LINESTRING, POLYGON, and MULTI* geometries
- **Performance Optimization**: Faster file loading and data preview
- **Enhanced Status Feedback**: Visual indicators for connection status
- **Progress Bar**: Real-time progress tracking during import with row counts and status messages
- **Smart PostGIS Handling**: Automatic fallback to WKT format if PostGIS is not available
- **Spatial Tools Tab**: Manage PostGIS extension and convert WKT tables to proper geometry

## Database-Specific Notes

### SQLite
- For SQLite, enter the full path to your database file in the "Database" field
- Leave other fields as default
- Port field is automatically cleared

### SQL Server
- Requires ODBC Driver 17 for SQL Server
- Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Default port: 1433

### PostgreSQL
- Default port: 5432
- PostGIS extension automatically enabled for spatial data

### MySQL
- Default port: 3306
- Spatial data supported with geometry columns

## Spatial Data Support

The application supports importing and visualizing spatial data:

1. **Import**: Shapefiles (.shp) are automatically recognized and imported with geometry
2. **Query**: Use spatial SQL functions in your queries
3. **Visualize**: Right-click on any geometry value in query results to see a visual representation
4. **Progress Tracking**: See detailed progress during spatial data import

Supported geometry types:
- POINT
- LINESTRING
- POLYGON
- MULTIPOINT
- MULTILINESTRING
- MULTIPOLYGON

### PostgreSQL PostGIS Note
If PostGIS extension is not available, the application will automatically fall back to importing geometry as WKT (Well-Known Text) format. 

To enable full spatial support:
1. Use the "Spatial Tools" tab in the application
2. Click "Enable PostGIS" (requires superuser privileges)
3. Or ask your database administrator to run the included `enable_postgis.sql` script

Once PostGIS is enabled, you can:
- Import spatial data directly with proper geometry types
- Convert existing WKT tables to geometry using the Spatial Tools tab
- Use all PostGIS spatial functions in your queries

## Project Structure

```
universal-database-importer/
│
├── main.py                 # Main application entry point
├── database_manager.py     # Database connection and operations handler
├── icon.py                # Application icon generator
├── requirements.txt       # Python dependencies
├── run.bat               # Windows launcher script
├── run.sh                # Unix/Linux launcher script
├── enable_postgis.sql    # PostGIS enablement SQL script
├── README.md             # Documentation (this file)
├── LICENSE               # MIT License
├── .gitignore           # Git ignore rules
├── CONTRIBUTING.md       # Contribution guidelines
│
├── app_icon.png          # Application icon (16x16)
├── app_icon.ico          # Windows icon format
├── app_icon_small.png    # Small icon variant
│
└── venv/                 # Virtual environment (not tracked in git)
```

## Advanced Usage

### Spatial Data Workflow

1. **Import Shapefile**
   - Select .shp file (associated .dbf, .shx files loaded automatically)
   - Preview attribute data
   - Choose columns (geometry included automatically)
   - Import with progress tracking

2. **Enable PostGIS** (PostgreSQL only)
   - Navigate to Spatial Tools tab
   - Click "Check PostGIS Status"
   - If not enabled, click "Enable PostGIS"
   - Requires superuser privileges

3. **Convert WKT to Geometry**
   - View tables with WKT columns
   - Select table to convert
   - Click "Convert Selected Table"
   - Automatic spatial index creation

4. **Visualize Geometry**
   - Execute query returning geometry data
   - Right-click on geometry value
   - Select "Visualize Geometry"
   - View in matplotlib window

### Performance Tips

- **Large Datasets**: Data is imported in 1000-row chunks
- **Indexing**: Create indexes on frequently queried columns
- **Spatial Queries**: Use spatial indexes for better performance
- **Memory**: Close unused connections to free resources

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify database server is running
   - Check firewall allows connections
   - Ensure correct port number
   - Validate username/password

2. **Import Errors**
   - Check column data types compatibility
   - Ensure table name is valid (no spaces)
   - Verify user has CREATE TABLE permission
   - Check disk space availability

3. **PostGIS Issues**
   - Requires PostgreSQL superuser for installation
   - Use `enable_postgis.sql` script if needed
   - Check PostgreSQL version compatibility

4. **Visualization Errors**
   - Ensure matplotlib is installed
   - Check geometry data is valid
   - Verify display backend compatibility

### Error Messages

| Error | Solution |
|-------|----------|
| "PostGIS extension required" | Enable PostGIS or import as WKT |
| "Permission denied" | Check database user privileges |
| "Invalid geometry" | Validate shapefile integrity |
| "Connection timeout" | Check network and firewall settings |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints
- Update documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **GeoPandas** - Spatial data handling
- **SQLAlchemy** - Database abstraction
- **Tkinter** - GUI framework
- **Shapely** - Geometric operations
- **PostGIS** - Spatial database extension

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Multi-database support
- CSV and Shapefile import
- Spatial data visualization
- PostGIS integration
- Progress tracking
- Threading support

---

Made with ❤️ by the Mohammad Afzal Khan