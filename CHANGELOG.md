# Changelog

All notable changes to Universal Database Importer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [1.0.0] - 2024-01-01

### Added
- Initial release of Universal Database Importer
- Multi-database support (MySQL, PostgreSQL, SQLite, SQL Server)
- CSV file import with column selection
- Shapefile import with geometry support
- SQL query interface with results viewer
- Spatial data visualization for geometry columns
- PostGIS integration for PostgreSQL
- Progress tracking during import operations
- Threading support to prevent UI freezing
- Auto-port detection based on database type
- Visual connection status indicators
- Resizable query editor and results panels
- WKT to geometry conversion tools
- Spatial index creation
- Batch import processing (1000 rows per chunk)
- Error handling and fallback mechanisms
- Cross-platform support (Windows, macOS, Linux)

### Features
- **Database Connection Tab**
  - Test connection before connecting
  - Visual feedback with icons
  - Auto-fill default ports
  - Support for all major databases

- **Import Tab**
  - File browser for CSV and Shapefiles
  - Data preview with column headers
  - Select/deselect all columns
  - Table name auto-generation
  - Progress bar with status updates

- **Query Tab**
  - SQL syntax highlighting (basic)
  - Resizable editor and results
  - Horizontal scrolling for wide results
  - Right-click context menu for geometry

- **Spatial Tools Tab** (PostgreSQL only)
  - PostGIS status checking
  - Extension enablement
  - WKT to geometry conversion
  - Spatial table management

### Technical Details
- Built with Python 3.7+ and Tkinter
- Uses SQLAlchemy for database abstraction
- GeoPandas for spatial data handling
- Matplotlib for geometry visualization
- Threading for non-blocking operations

### Known Issues
- PostGIS requires superuser privileges to enable
- Some GDAL installations may require manual setup
- Large shapefiles (>1GB) may require increased memory

---

## Version History

- **1.0.0** - Initial public release (2024-01-01)