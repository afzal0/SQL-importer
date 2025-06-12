import pandas as pd
import geopandas as gpd
import pymysql
import psycopg2
import sqlite3
import pyodbc
from sqlalchemy import create_engine, inspect, text
from geoalchemy2 import Geometry, WKTElement
import urllib.parse

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.engine = None
        self.db_type = None
        self.config = None
        
    def test_connection(self, config):
        try:
            if config['db_type'] == 'MySQL':
                conn = pymysql.connect(
                    host=config['host'],
                    port=int(config['port']),
                    user=config['username'],
                    password=config['password'],
                    database=config['database']
                )
                conn.close()
                return True
                
            elif config['db_type'] == 'PostgreSQL':
                conn = psycopg2.connect(
                    host=config['host'],
                    port=int(config['port']),
                    user=config['username'],
                    password=config['password'],
                    database=config['database']
                )
                conn.close()
                return True
                
            elif config['db_type'] == 'SQLite':
                conn = sqlite3.connect(config['database'])
                conn.close()
                return True
                
            elif config['db_type'] == 'SQL Server':
                connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config['host']},{config['port']};DATABASE={config['database']};UID={config['username']};PWD={config['password']}"
                conn = pyodbc.connect(connection_string)
                conn.close()
                return True
                
        except Exception as e:
            print(f"Connection test error: {str(e)}")
            return False
            
    def connect(self, config):
        try:
            self.config = config
            self.db_type = config['db_type']
            
            if config['db_type'] == 'MySQL':
                password = urllib.parse.quote_plus(config['password'])
                connection_string = f"mysql+pymysql://{config['username']}:{password}@{config['host']}:{config['port']}/{config['database']}"
                
            elif config['db_type'] == 'PostgreSQL':
                password = urllib.parse.quote_plus(config['password'])
                connection_string = f"postgresql+psycopg2://{config['username']}:{password}@{config['host']}:{config['port']}/{config['database']}"
                
            elif config['db_type'] == 'SQLite':
                connection_string = f"sqlite:///{config['database']}"
                
            elif config['db_type'] == 'SQL Server':
                params = urllib.parse.quote_plus(
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={config['host']},{config['port']};"
                    f"DATABASE={config['database']};"
                    f"UID={config['username']};"
                    f"PWD={config['password']}"
                )
                connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
                
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            return True
            
        except Exception as e:
            print(f"Connection error: {str(e)}")
            self.connection = None
            self.engine = None
            return False
            
    def is_connected(self):
        return self.connection is not None
        
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.engine = None
            
    def import_data(self, dataframe, table_name, progress_callback=None):
        try:
            if not self.is_connected():
                return False
                
            total_rows = len(dataframe)
            
            if progress_callback:
                progress_callback(0, total_rows, "Creating table structure...")
                
            # Import with progress tracking
            chunk_size = 1000
            chunks = [dataframe[i:i + chunk_size] for i in range(0, len(dataframe), chunk_size)]
            
            for i, chunk in enumerate(chunks):
                if progress_callback:
                    rows_processed = min(i * chunk_size, total_rows)
                    progress_callback(rows_processed, total_rows, f"Importing data... {rows_processed}/{total_rows}")
                    
                chunk.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='replace' if i == 0 else 'append',
                    index=False,
                    method='multi'
                )
                
            if progress_callback:
                progress_callback(total_rows, total_rows, "Import completed successfully")
                
            return True
            
        except Exception as e:
            print(f"Import error: {str(e)}")
            if progress_callback:
                progress_callback(0, total_rows, f"Error: {str(e)}")
            return False
            
    def execute_query(self, query):
        try:
            if not self.is_connected():
                return None
                
            if query.strip().upper().startswith('SELECT'):
                result = pd.read_sql_query(query, self.engine)
                return result.to_dict('records')
            else:
                self.connection.execute(query)
                self.connection.commit()
                return []
                
        except Exception as e:
            print(f"Query error: {str(e)}")
            raise e
            
    def get_tables(self):
        try:
            if not self.is_connected():
                return []
                
            inspector = inspect(self.engine)
            return inspector.get_table_names()
            
        except Exception as e:
            print(f"Error getting tables: {str(e)}")
            return []
            
    def get_table_info(self, table_name):
        try:
            if not self.is_connected():
                return []
                
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            return columns
            
        except Exception as e:
            print(f"Error getting table info: {str(e)}")
            return []
    
    def check_postgis_extension(self):
        """Check if PostGIS extension is available for PostgreSQL databases"""
        if self.db_type != 'PostgreSQL':
            return True
            
        try:
            # First check if extension exists
            result = self.connection.execute(text(
                "SELECT COUNT(*) FROM pg_extension WHERE extname = 'postgis'"
            ))
            count = result.fetchone()[0]
            
            if count == 0:
                # Try to create the extension
                try:
                    self.connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
                    self.connection.commit()
                except Exception as create_error:
                    # If creation fails, check if we have superuser privileges
                    try:
                        result = self.connection.execute(text(
                            "SELECT current_user, usesuper FROM pg_user WHERE usename = current_user"
                        ))
                        user_info = result.fetchone()
                        if not user_info[1]:  # Not a superuser
                            print("\n" + "="*60)
                            print("POSTGIS EXTENSION REQUIRED")
                            print("="*60)
                            print(f"\nCannot create PostGIS extension. User '{user_info[0]}' is not a superuser.")
                            print("\nPostGIS is required for importing spatial data (shapefiles, GeoJSON, etc.)")
                            print("\nTo enable PostGIS, please ask your database administrator to run:")
                            print("\n   CREATE EXTENSION postgis;")
                            print("\nAlternatively, connect as a superuser and run the enable_postgis.sql script:")
                            print("   psql -U postgres -d your_database -f enable_postgis.sql")
                            print("\n" + "="*60 + "\n")
                            return False
                    except:
                        pass
                    raise create_error
                
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error checking/creating PostGIS extension: {error_msg}")
            
            if 'permission denied' in error_msg.lower() or 'must be superuser' in error_msg.lower():
                print("\n" + "="*60)
                print("POSTGIS PERMISSION DENIED")
                print("="*60)
                print("\nSuperuser privileges are required to enable PostGIS.")
                print("\nPlease contact your database administrator or run:")
                print("   CREATE EXTENSION postgis;")
                print("\n" + "="*60 + "\n")
            
            return False
    
    def enable_postgis(self):
        """Try to enable PostGIS extension for the current database"""
        if self.db_type != 'PostgreSQL':
            return False, "PostGIS is only available for PostgreSQL databases"
            
        try:
            # Try to create the extension
            self.connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            self.connection.commit()
            return True, "PostGIS extension enabled successfully!"
            
        except Exception as e:
            error_msg = str(e)
            if "permission denied" in error_msg.lower() or "must be superuser" in error_msg.lower():
                return False, "Permission denied. Please ask your database administrator to run:\nCREATE EXTENSION postgis;"
            else:
                return False, f"Failed to enable PostGIS: {error_msg}"
    
    def convert_wkt_to_geometry(self, table_name, wkt_column='geometry_wkt', geom_column='geometry', srid=4326):
        """Convert WKT column to proper geometry column (requires PostGIS)"""
        if self.db_type != 'PostgreSQL':
            return False, "Geometry conversion is only available for PostgreSQL databases"
            
        try:
            # Check if PostGIS is available
            if not self.check_postgis_extension():
                return False, "PostGIS extension is required for geometry conversion"
                
            # Add geometry column if it doesn't exist
            self.connection.execute(text(
                f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {geom_column} geometry(Geometry, {srid})"
            ))
            
            # Update geometry column from WKT
            self.connection.execute(text(
                f"UPDATE {table_name} SET {geom_column} = ST_GeomFromText({wkt_column}, {srid}) WHERE {wkt_column} IS NOT NULL"
            ))
            
            # Create spatial index
            self.connection.execute(text(
                f"CREATE INDEX IF NOT EXISTS {table_name}_{geom_column}_idx ON {table_name} USING GIST ({geom_column})"
            ))
            
            self.connection.commit()
            
            # Optionally drop the WKT column
            # self.connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {wkt_column}"))
            
            return True, f"Successfully converted WKT to geometry column in table '{table_name}'"
            
        except Exception as e:
            return False, f"Failed to convert WKT to geometry: {str(e)}"
    
    def get_spatial_tables(self):
        """Get list of tables with spatial data (either geometry or WKT columns)"""
        try:
            if not self.is_connected():
                return []
                
            tables_with_spatial = []
            
            if self.db_type == 'PostgreSQL':
                # Check for geometry columns
                result = self.connection.execute(text(
                    """
                    SELECT DISTINCT table_name, column_name, 'geometry' as type
                    FROM information_schema.columns 
                    WHERE data_type = 'USER-DEFINED' 
                    AND udt_name = 'geometry'
                    AND table_schema = 'public'
                    
                    UNION
                    
                    SELECT DISTINCT table_name, column_name, 'wkt' as type
                    FROM information_schema.columns 
                    WHERE column_name LIKE '%geometry_wkt%' 
                    OR column_name LIKE '%geom_wkt%'
                    AND table_schema = 'public'
                    ORDER BY table_name
                    """
                ))
                
                for row in result:
                    tables_with_spatial.append({
                        'table': row[0],
                        'column': row[1],
                        'type': row[2]
                    })
                    
            return tables_with_spatial
            
        except Exception as e:
            print(f"Error getting spatial tables: {str(e)}")
            return []
    
    def import_spatial_data(self, geodataframe, table_name, geom_col='geometry', srid=None, progress_callback=None):
        """Import spatial data from a GeoDataFrame to the database"""
        try:
            if not self.is_connected():
                return False
                
            # Detect SRID if not provided
            if srid is None and geodataframe.crs:
                srid = geodataframe.crs.to_epsg() or 4326
            elif srid is None:
                srid = 4326
                
            total_rows = len(geodataframe)
            
            if self.db_type == 'PostgreSQL':
                if progress_callback:
                    progress_callback(0, total_rows, "Checking PostGIS extension...")
                    
                postgis_available = self.check_postgis_extension()
                
                if not postgis_available:
                    # Try alternative import method without PostGIS
                    if progress_callback:
                        progress_callback(0, total_rows, "PostGIS not available, using alternative method...")
                    
                    # Convert geometry to WKT and import as text
                    gdf_copy = geodataframe.copy()
                    
                    # Get the geometry column (might be named 'geometry' or might be the active geometry)
                    geom_col = gdf_copy.geometry.name
                    
                    # Create WKT column from geometry
                    gdf_copy['geometry_wkt'] = gdf_copy[geom_col].apply(
                        lambda geom: geom.wkt if geom else None
                    )
                    
                    # Drop the geometry column
                    gdf_copy = gdf_copy.drop(columns=[geom_col])
                    
                    if progress_callback:
                        progress_callback(0, total_rows, "Creating table...")
                        
                    gdf_copy.to_sql(
                        name=table_name,
                        con=self.engine,
                        if_exists='replace',
                        index=False,
                        method='multi',
                        chunksize=1000
                    )
                    
                    if progress_callback:
                        progress_callback(total_rows, total_rows, "Import completed (geometry as text)")
                    return True
                    
                # Use PostGIS if available - but wrap in try/catch in case it still fails
                try:
                    if progress_callback:
                        progress_callback(0, total_rows, "Creating spatial table...")
                    
                    # Fix the duplicate geometry column issue
                    # Rename the geometry column if it exists to avoid conflicts
                    gdf_for_import = geodataframe.copy()
                    if 'geometry' in gdf_for_import.columns:
                        # Ensure geometry column has a proper name
                        gdf_for_import = gdf_for_import.rename_geometry('geom')
                        
                    gdf_for_import.to_postgis(
                        name=table_name,
                        con=self.engine,
                        if_exists='replace',
                        index=False,
                        chunksize=1000,
                        dtype={'geom': Geometry(srid=srid)}  # Explicitly set geometry type
                    )
                    
                    if progress_callback:
                        progress_callback(total_rows, total_rows, "Spatial import completed")
                        
                except Exception as postgis_error:
                    # Fallback to WKT if PostGIS fails
                    error_msg = str(postgis_error)
                    print(f"PostGIS import failed: {error_msg}")
                    
                    # Check if it's a missing PostGIS extension error
                    if 'type "geometry" does not exist' in error_msg or 'UndefinedObject' in error_msg:
                        print("\n" + "="*60)
                        print("POSTGIS EXTENSION NOT ENABLED")
                        print("="*60)
                        print("\nThe PostGIS extension is required for spatial data import.")
                        print("\nTo fix this issue, you have two options:")
                        print("\n1. Ask your database administrator to run:")
                        print("   CREATE EXTENSION postgis;")
                        print("\n2. Or run the provided SQL script as a superuser:")
                        print("   psql -U postgres -d your_database -f enable_postgis.sql")
                        print("\n" + "="*60 + "\n")
                    
                    print("Falling back to WKT format...")
                    
                    if progress_callback:
                        progress_callback(0, total_rows, "PostGIS failed, using WKT format...")
                    
                    # Convert geometry to WKT and import as text
                    gdf_copy = geodataframe.copy()
                    
                    # Get the geometry column (might be named 'geometry' or might be the active geometry)
                    geom_col = gdf_copy.geometry.name
                    
                    # Create WKT column from geometry
                    gdf_copy['geometry_wkt'] = gdf_copy[geom_col].apply(
                        lambda geom: geom.wkt if geom else None
                    )
                    
                    # Drop the geometry column
                    gdf_copy = gdf_copy.drop(columns=[geom_col])
                    
                    if progress_callback:
                        progress_callback(0, total_rows, "Creating table with WKT...")
                        
                    gdf_copy.to_sql(
                        name=table_name,
                        con=self.engine,
                        if_exists='replace',
                        index=False,
                        method='multi',
                        chunksize=1000
                    )
                    
                    if progress_callback:
                        progress_callback(total_rows, total_rows, "Import completed (geometry as WKT)")
                
            elif self.db_type == 'SQLite':
                if progress_callback:
                    progress_callback(0, total_rows, "Preparing SQLite spatial data...")
                    
                # For SQLite with SpatiaLite
                gdf_copy = geodataframe.copy()
                
                # Get the geometry column
                geom_col = gdf_copy.geometry.name
                
                # Convert geometry to WKT
                gdf_copy[geom_col] = gdf_copy[geom_col].apply(
                    lambda geom: geom.wkt if geom else None
                )
                
                if progress_callback:
                    progress_callback(0, total_rows, "Creating table...")
                    
                gdf_copy.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='replace',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                
                if progress_callback:
                    progress_callback(total_rows, total_rows, "Import completed")
                
            elif self.db_type == 'MySQL':
                if progress_callback:
                    progress_callback(0, total_rows, "Preparing MySQL spatial data...")
                    
                # For MySQL with spatial support
                gdf_copy = geodataframe.copy()
                
                # First create the table without geometry
                non_geom_cols = [col for col in gdf_copy.columns if col != 'geometry']
                
                if progress_callback:
                    progress_callback(0, total_rows, "Creating table structure...")
                    
                gdf_copy[non_geom_cols].to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='replace',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                
                # Add geometry column
                if progress_callback:
                    progress_callback(0, total_rows, "Adding geometry column...")
                    
                self.connection.execute(text(
                    f"ALTER TABLE {table_name} ADD COLUMN geometry GEOMETRY"
                ))
                
                # Insert geometry values in batches
                batch_size = 100
                for i in range(0, total_rows, batch_size):
                    if progress_callback:
                        progress_callback(i, total_rows, f"Inserting geometry data... {i}/{total_rows}")
                        
                    batch = geodataframe.iloc[i:i+batch_size]
                    for idx, row in batch.iterrows():
                        if row['geometry']:
                            self.connection.execute(text(
                                f"UPDATE {table_name} SET geometry = ST_GeomFromText('{row['geometry'].wkt}', {srid}) "
                                f"WHERE {non_geom_cols[0]} = :val"
                            ), {'val': row[non_geom_cols[0]]})
                            
                if progress_callback:
                    progress_callback(total_rows, total_rows, "Spatial import completed")
                        
            elif self.db_type == 'SQL Server':
                if progress_callback:
                    progress_callback(0, total_rows, "Preparing SQL Server spatial data...")
                    
                # For SQL Server with spatial support
                gdf_copy = geodataframe.copy()
                gdf_copy['geometry'] = gdf_copy['geometry'].apply(
                    lambda geom: geom.wkt if geom else None
                )
                
                if progress_callback:
                    progress_callback(0, total_rows, "Creating table...")
                    
                gdf_copy.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='replace',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                
                if progress_callback:
                    progress_callback(total_rows, total_rows, "Import completed")
                
            return True
            
        except Exception as e:
            print(f"Spatial import error: {str(e)}")
            if progress_callback:
                progress_callback(0, total_rows, f"Error: {str(e)}")
            return False