#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import geopandas as gpd
from database_manager import DatabaseManager
import os
import threading
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class DatabaseImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Database Importer")
        self.root.geometry("1000x800")
        
        # Set application icon
        self.set_app_icon()
        
        self.db_manager = DatabaseManager()
        self.csv_data = None
        self.shapefile_data = None
        self.selected_columns = []
        self.file_type = None
        
        # Database default ports
        self.default_ports = {
            'MySQL': '3306',
            'PostgreSQL': '5432',
            'SQLite': '',
            'SQL Server': '1433'
        }
        
        self.setup_ui()
        
    def set_app_icon(self):
        """Set application icon"""
        try:
            # First try to create/load actual icon file
            import os
            icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.png')
            
            if not os.path.exists(icon_path):
                # Create icon if it doesn't exist
                from icon import create_app_icon
                create_app_icon()
            
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
            else:
                # Fallback to embedded icon data
                icon_data = '''
                R0lGODlhEAAQAPeAAP///8PDw7Ozs6Ojo5SUlISEhHR0dGRkZFRUVERERDQ0NCQkJBQUFAQEBP//
                /wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                AAAAAAAAAAAAACH5BAAAAAAALAAAAAAQABAAAAiAAAEIFBigYMGBCA0KTMiwIUKBDQUuFBihokWK
                Ey9qzMiRY0ePIEOKHEmSZMmTKFOiVLmSZcuXMGPKnEmzZs2bOHPizLmTZ8+fQIMKHUq0aNGjSJMi
                VbqUadOnUKNKnUq1KlWCBwEAOw==
                '''
                self.root.iconphoto(True, tk.PhotoImage(data=icon_data))
        except Exception as e:
            print(f"Could not set icon: {e}")
            pass
        
    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.connection_tab = ttk.Frame(notebook)
        self.import_tab = ttk.Frame(notebook)
        self.query_tab = ttk.Frame(notebook)
        
        notebook.add(self.connection_tab, text="Database Connection")
        notebook.add(self.import_tab, text="Import Data")
        notebook.add(self.query_tab, text="SQL Query")
        
        # Add spatial tools tab if PostgreSQL
        self.spatial_tab = ttk.Frame(notebook)
        notebook.add(self.spatial_tab, text="Spatial Tools")
        
        self.setup_connection_tab()
        self.setup_import_tab()
        self.setup_query_tab()
        self.setup_spatial_tab()
        
    def setup_connection_tab(self):
        frame = ttk.LabelFrame(self.connection_tab, text="Database Configuration", padding=20)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Database Type with port auto-fill
        ttk.Label(frame, text="Database Type:").grid(row=0, column=0, sticky='w', pady=5)
        self.db_type = ttk.Combobox(frame, values=['MySQL', 'PostgreSQL', 'SQLite', 'SQL Server'], width=30)
        self.db_type.set('MySQL')
        self.db_type.grid(row=0, column=1, pady=5)
        self.db_type.bind('<<ComboboxSelected>>', self.on_db_type_changed)
        
        ttk.Label(frame, text="Host/URL:").grid(row=1, column=0, sticky='w', pady=5)
        self.host_entry = ttk.Entry(frame, width=32)
        self.host_entry.insert(0, 'localhost')
        self.host_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Port:").grid(row=2, column=0, sticky='w', pady=5)
        self.port_entry = ttk.Entry(frame, width=32)
        self.port_entry.insert(0, '3306')
        self.port_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Username:").grid(row=3, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(frame, width=32)
        self.username_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=4, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=32)
        self.password_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Database:").grid(row=5, column=0, sticky='w', pady=5)
        self.database_entry = ttk.Entry(frame, width=32)
        self.database_entry.grid(row=5, column=1, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        self.test_btn = ttk.Button(button_frame, text="Test Connection", command=self.test_connection)
        self.test_btn.pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Connect", command=self.connect_database).pack(side='left', padx=5)
        
        # Status frame with icon
        status_frame = ttk.Frame(frame)
        status_frame.grid(row=7, column=0, columnspan=2)
        
        self.status_icon_label = ttk.Label(status_frame, text="")
        self.status_icon_label.pack(side='left', padx=5)
        
        self.connection_status = ttk.Label(status_frame, text="Not connected", foreground="red")
        self.connection_status.pack(side='left')
        
    def on_db_type_changed(self, event):
        """Auto-fill port when database type changes"""
        db_type = self.db_type.get()
        if db_type in self.default_ports:
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, self.default_ports[db_type])
            
    def setup_import_tab(self):
        main_frame = ttk.Frame(self.import_tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=10)
        file_frame.pack(fill='x', pady=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side='left', padx=10)
        
        ttk.Button(file_frame, text="Browse CSV", command=self.browse_csv).pack(side='right', padx=10)
        ttk.Button(file_frame, text="Browse Shapefile", command=self.browse_shapefile).pack(side='right', padx=10)
        
        preview_frame = ttk.LabelFrame(main_frame, text="Data Preview & Column Selection", padding=10)
        preview_frame.pack(fill='both', expand=True)
        
        columns_frame = ttk.Frame(preview_frame)
        columns_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(columns_frame, text="Select All", command=self.select_all_columns).pack(side='left', padx=5)
        ttk.Button(columns_frame, text="Deselect All", command=self.deselect_all_columns).pack(side='left', padx=5)
        
        self.columns_listbox = tk.Listbox(preview_frame, selectmode='multiple', height=6)
        self.columns_listbox.pack(fill='x', pady=(0, 10))
        
        ttk.Label(preview_frame, text="Data Preview:").pack(anchor='w')
        
        self.preview_tree = ttk.Treeview(preview_frame, height=10)
        self.preview_tree.pack(fill='both', expand=True)
        
        preview_scroll = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_tree.yview)
        preview_scroll.pack(side='right', fill='y')
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)
        
        import_frame = ttk.Frame(main_frame)
        import_frame.pack(fill='x', pady=10)
        
        ttk.Label(import_frame, text="Table Name:").pack(side='left', padx=5)
        self.table_name_entry = ttk.Entry(import_frame, width=30)
        self.table_name_entry.pack(side='left', padx=5)
        
        self.import_btn = ttk.Button(import_frame, text="Import to Database", command=self.import_to_database)
        self.import_btn.pack(side='right', padx=10)
        
    def setup_query_tab(self):
        # Main paned window for resizable sections
        paned = ttk.PanedWindow(self.query_tab, orient='vertical')
        paned.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top frame for query
        query_frame = ttk.Frame(paned)
        paned.add(query_frame, weight=1)
        
        ttk.Label(query_frame, text="SQL Query:").pack(anchor='w')
        
        self.query_text = scrolledtext.ScrolledText(query_frame, height=8, width=80)
        self.query_text.pack(fill='both', expand=True, pady=(5, 10))
        
        self.execute_btn = ttk.Button(query_frame, text="Execute Query", command=self.execute_query)
        self.execute_btn.pack()
        
        # Bottom frame for results
        results_frame = ttk.Frame(paned)
        paned.add(results_frame, weight=2)
        
        ttk.Label(results_frame, text="Results:").pack(anchor='w', pady=(10, 5))
        
        # Results tree with horizontal scrollbar
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill='both', expand=True)
        
        self.results_tree = ttk.Treeview(tree_frame)
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.results_tree.yview)
        v_scroll.grid(row=0, column=1, sticky='ns')
        
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.results_tree.xview)
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        self.results_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add context menu for spatial data visualization
        self.results_tree.bind("<Button-3>", self.on_right_click)
        
    def setup_spatial_tab(self):
        """Setup spatial tools tab for managing PostGIS and spatial data"""
        main_frame = ttk.Frame(self.spatial_tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # PostGIS Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="PostGIS Status", padding=10)
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.postgis_status_label = ttk.Label(status_frame, text="Not connected to database")
        self.postgis_status_label.pack(anchor='w', pady=5)
        
        button_frame = ttk.Frame(status_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Check PostGIS Status", 
                  command=self.check_postgis_status).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Enable PostGIS", 
                  command=self.enable_postgis).pack(side='left', padx=5)
        
        # Spatial Tables Frame
        tables_frame = ttk.LabelFrame(main_frame, text="Spatial Tables", padding=10)
        tables_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Button(tables_frame, text="Refresh Tables", 
                  command=self.refresh_spatial_tables).pack(anchor='w', pady=5)
        
        # Create treeview for spatial tables
        columns = ('Table', 'Column', 'Type', 'Action')
        self.spatial_tree = ttk.Treeview(tables_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.spatial_tree.heading(col, text=col)
            self.spatial_tree.column(col, width=150)
        
        self.spatial_tree.pack(fill='both', expand=True, pady=5)
        
        # Add scrollbar
        scroll = ttk.Scrollbar(tables_frame, orient='vertical', command=self.spatial_tree.yview)
        scroll.pack(side='right', fill='y')
        self.spatial_tree.configure(yscrollcommand=scroll.set)
        
        # Conversion Frame
        convert_frame = ttk.LabelFrame(main_frame, text="Convert WKT to Geometry", padding=10)
        convert_frame.pack(fill='x')
        
        ttk.Label(convert_frame, text="Select a table with WKT data above and click:").pack(anchor='w', pady=5)
        ttk.Button(convert_frame, text="Convert Selected Table", 
                  command=self.convert_selected_table).pack(anchor='w', pady=5)
        
        self.conversion_status = ttk.Label(convert_frame, text="", foreground="blue")
        self.conversion_status.pack(anchor='w', pady=5)
        
    def on_right_click(self, event):
        """Handle right-click on results tree"""
        item = self.results_tree.identify('item', event.x, event.y)
        if item:
            column = self.results_tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            
            if col_index >= 0 and col_index < len(self.results_tree['columns']):
                col_name = self.results_tree['columns'][col_index]
                value = self.results_tree.item(item)['values'][col_index]
                
                # Check if it's a geometry column (including geometry_wkt columns)
                if isinstance(value, str) and (value.startswith('POINT') or value.startswith('LINESTRING') or 
                                             value.startswith('POLYGON') or value.startswith('MULTIPOINT') or
                                             value.startswith('MULTILINESTRING') or value.startswith('MULTIPOLYGON') or
                                             value.startswith('GEOMETRYCOLLECTION')):
                    menu = tk.Menu(self.root, tearoff=0)
                    menu.add_command(label="Visualize Geometry", 
                                   command=lambda: self.visualize_geometry(value))
                    menu.post(event.x_root, event.y_root)
                elif col_name.lower() in ['geometry', 'geom', 'geometry_wkt', 'geom_wkt', 'wkt']:
                    # Also check column name for geometry columns
                    menu = tk.Menu(self.root, tearoff=0)
                    menu.add_command(label="Visualize Geometry", 
                                   command=lambda: self.visualize_geometry(value))
                    menu.post(event.x_root, event.y_root)
                    
    def visualize_geometry(self, wkt_string):
        """Visualize spatial geometry data"""
        try:
            from shapely import wkt
            geom = wkt.loads(wkt_string)
            
            # Create a new window for visualization
            viz_window = tk.Toplevel(self.root)
            viz_window.title("Geometry Visualization")
            viz_window.geometry("600x600")
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(8, 8))
            
            # Plot the geometry
            if geom.geom_type == 'Point':
                ax.scatter(geom.x, geom.y, s=100, c='red', marker='o')
            elif geom.geom_type in ['LineString', 'MultiLineString']:
                x, y = geom.xy if hasattr(geom, 'xy') else ([], [])
                ax.plot(x, y, 'b-', linewidth=2)
            elif geom.geom_type in ['Polygon', 'MultiPolygon']:
                from matplotlib.patches import Polygon as MplPolygon
                if geom.geom_type == 'Polygon':
                    patch = MplPolygon(list(geom.exterior.coords), alpha=0.5, fc='blue', ec='black')
                    ax.add_patch(patch)
                else:
                    for poly in geom.geoms:
                        patch = MplPolygon(list(poly.exterior.coords), alpha=0.5, fc='blue', ec='black')
                        ax.add_patch(patch)
            
            ax.set_aspect('equal')
            ax.autoscale_view()
            ax.grid(True)
            ax.set_title(f"{geom.geom_type} Visualization")
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=viz_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Failed to visualize geometry: {str(e)}")
            
    def test_connection(self):
        """Test database connection with threading to prevent freezing"""
        self.test_btn.config(state='disabled', text="Testing...")
        self.connection_status.config(text="Testing connection...", foreground="orange")
        
        def test_thread():
            try:
                config = {
                    'db_type': self.db_type.get(),
                    'host': self.host_entry.get(),
                    'port': self.port_entry.get(),
                    'username': self.username_entry.get(),
                    'password': self.password_entry.get(),
                    'database': self.database_entry.get()
                }
                
                success = self.db_manager.test_connection(config)
                
                # Update UI in main thread
                self.root.after(0, self.update_test_result, success)
                
            except Exception as e:
                self.root.after(0, self.update_test_result, False, str(e))
                
        thread = threading.Thread(target=test_thread, daemon=True)
        thread.start()
        
    def update_test_result(self, success, error_msg=None):
        """Update UI after connection test"""
        self.test_btn.config(state='normal', text="Test Connection")
        
        if success:
            self.connection_status.config(text="Test successful!", foreground="green")
            self.status_icon_label.config(text="✓", foreground="green")
            messagebox.showinfo("Success", "Connection test successful!")
        else:
            self.connection_status.config(text="Test failed", foreground="red")
            self.status_icon_label.config(text="✗", foreground="red")
            error_text = error_msg if error_msg else "Connection test failed!"
            messagebox.showerror("Error", error_text)
            
    def connect_database(self):
        """Connect to database with threading"""
        def connect_thread():
            try:
                config = {
                    'db_type': self.db_type.get(),
                    'host': self.host_entry.get(),
                    'port': self.port_entry.get(),
                    'username': self.username_entry.get(),
                    'password': self.password_entry.get(),
                    'database': self.database_entry.get()
                }
                
                success = self.db_manager.connect(config)
                self.root.after(0, self.update_connection_status, success)
                
            except Exception as e:
                self.root.after(0, self.update_connection_status, False, str(e))
                
        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()
        
    def update_connection_status(self, success, error_msg=None):
        """Update UI after connection attempt"""
        if success:
            self.connection_status.config(text="Connected", foreground="green")
            self.status_icon_label.config(text="●", foreground="green")
            messagebox.showinfo("Success", "Connected to database!")
            # Update spatial tools if PostgreSQL
            if self.db_manager.db_type == 'PostgreSQL':
                self.check_postgis_status()
                self.refresh_spatial_tables()
        else:
            self.connection_status.config(text="Not connected", foreground="red")
            self.status_icon_label.config(text="○", foreground="red")
            error_text = error_msg if error_msg else "Failed to connect to database!"
            messagebox.showerror("Error", error_text)
            
    def browse_csv(self):
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            # Load file in thread for better performance
            self.file_label.config(text="Loading...")
            
            def load_thread():
                try:
                    data = pd.read_csv(filename)
                    self.root.after(0, self.update_csv_data, data, filename)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to read CSV: {str(e)}"))
                    
            thread = threading.Thread(target=load_thread, daemon=True)
            thread.start()
            
    def update_csv_data(self, data, filename):
        """Update UI with loaded CSV data"""
        self.csv_data = data
        self.shapefile_data = None
        self.file_type = 'csv'
        self.file_label.config(text=os.path.basename(filename))
        
        self.columns_listbox.delete(0, tk.END)
        for col in self.csv_data.columns:
            self.columns_listbox.insert(tk.END, col)
        
        self.update_preview()
        
        base_name = os.path.splitext(os.path.basename(filename))[0]
        self.table_name_entry.delete(0, tk.END)
        self.table_name_entry.insert(0, base_name.replace(' ', '_').replace('-', '_'))
    
    def browse_shapefile(self):
        filename = filedialog.askopenfilename(
            title="Select Shapefile",
            filetypes=[("Shapefiles", "*.shp"), ("All files", "*.*")]
        )
        
        if filename:
            self.file_label.config(text="Loading...")
            
            def load_thread():
                try:
                    data = gpd.read_file(filename)
                    self.root.after(0, self.update_shapefile_data, data, filename)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to read Shapefile: {str(e)}"))
                    
            thread = threading.Thread(target=load_thread, daemon=True)
            thread.start()
            
    def update_shapefile_data(self, data, filename):
        """Update UI with loaded shapefile data"""
        self.shapefile_data = data
        self.csv_data = None
        self.file_type = 'shapefile'
        self.file_label.config(text=os.path.basename(filename))
        
        self.columns_listbox.delete(0, tk.END)
        for col in self.shapefile_data.columns:
            self.columns_listbox.insert(tk.END, col)
        
        self.update_preview()
        
        base_name = os.path.splitext(os.path.basename(filename))[0]
        self.table_name_entry.delete(0, tk.END)
        self.table_name_entry.insert(0, base_name.replace(' ', '_').replace('-', '_'))
                
    def update_preview(self):
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
            
        data = self.csv_data if self.file_type == 'csv' else self.shapefile_data
        
        if data is not None:
            columns = list(data.columns)
            if self.file_type == 'shapefile' and 'geometry' in columns:
                columns = [col for col in columns if col != 'geometry']
            
            self.preview_tree['columns'] = columns
            self.preview_tree['show'] = 'headings'
            
            for col in columns:
                self.preview_tree.heading(col, text=col)
                self.preview_tree.column(col, width=100)
                
            for idx, row in data.head(20).iterrows():
                row_values = []
                for col in columns:
                    val = row[col]
                    if hasattr(val, 'wkt'):
                        val = val.wkt[:50] + '...' if len(val.wkt) > 50 else val.wkt
                    row_values.append(val)
                self.preview_tree.insert('', 'end', values=row_values)
                
    def select_all_columns(self):
        self.columns_listbox.selection_set(0, tk.END)
        
    def deselect_all_columns(self):
        self.columns_listbox.selection_clear(0, tk.END)
        
    def import_to_database(self):
        """Import data with threading and progress bar"""
        if not self.db_manager.is_connected():
            messagebox.showerror("Error", "Please connect to a database first!")
            return
            
        if self.csv_data is None and self.shapefile_data is None:
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        selected_indices = self.columns_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one column!")
            return
            
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name!")
            return
            
        # Create progress window
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Import Progress")
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Progress widgets
        status_label = ttk.Label(progress_window, text="Preparing import...")
        status_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=350, mode='determinate')
        progress_bar.pack(pady=10)
        
        details_label = ttk.Label(progress_window, text="")
        details_label.pack(pady=5)
        
        cancel_btn = ttk.Button(progress_window, text="Cancel", state='disabled')
        cancel_btn.pack(pady=10)
        
        self.import_btn.config(state='disabled', text="Importing...")
        
        def update_progress(current, total, status):
            """Update progress bar from any thread"""
            def update():
                if total > 0:
                    progress = (current / total) * 100
                    progress_bar['value'] = progress
                status_label.config(text=status)
                details_label.config(text=f"{current:,} / {total:,} rows")
                progress_window.update()
            self.root.after(0, update)
        
        def import_thread():
            try:
                selected_columns = [self.columns_listbox.get(i) for i in selected_indices]
                
                if self.file_type == 'csv':
                    data_to_import = self.csv_data[selected_columns]
                    success = self.db_manager.import_data(data_to_import, table_name, 
                                                         progress_callback=update_progress)
                else:
                    if 'geometry' not in selected_columns and 'geometry' in self.shapefile_data.columns:
                        selected_columns.append('geometry')
                    
                    data_to_import = self.shapefile_data[selected_columns]
                    success = self.db_manager.import_spatial_data(data_to_import, table_name,
                                                                progress_callback=update_progress)
                    
                self.root.after(0, self.close_progress_and_update, progress_window, success, table_name)
                    
            except Exception as e:
                self.root.after(0, self.close_progress_and_update, progress_window, False, None, str(e))
                
        thread = threading.Thread(target=import_thread, daemon=True)
        thread.start()
        
    def close_progress_and_update(self, progress_window, success, table_name, error_msg=None):
        """Close progress window and update import status"""
        progress_window.destroy()
        self.update_import_status(success, table_name, error_msg)
        
    def update_import_status(self, success, table_name, error_msg=None):
        """Update UI after import attempt"""
        self.import_btn.config(state='normal', text="Import to Database")
        
        if success:
            msg = f"Data imported successfully to table '{table_name}'!"
            if self.file_type == 'shapefile':
                msg = f"Spatial data imported successfully to table '{table_name}'!"
                # Check if geometry was imported as WKT
                if self.db_manager.db_type == 'PostgreSQL':
                    try:
                        # Check if table has geometry_wkt column
                        result = self.db_manager.execute_query(
                            f"SELECT column_name FROM information_schema.columns "
                            f"WHERE table_name = '{table_name}' AND column_name = 'geometry_wkt'"
                        )
                        if result:
                            msg += "\n\nNote: Geometry was imported as WKT text because PostGIS is not available."
                            msg += "\nTo enable full spatial support, ask your database administrator to run:"
                            msg += "\nCREATE EXTENSION postgis;"
                    except:
                        pass
            messagebox.showinfo("Success", msg)
        else:
            error_text = error_msg if error_msg else "Failed to import data!"
            messagebox.showerror("Error", error_text)
            
    def execute_query(self):
        """Execute query with threading"""
        if not self.db_manager.is_connected():
            messagebox.showerror("Error", "Please connect to a database first!")
            return
            
        query = self.query_text.get('1.0', tk.END).strip()
        if not query:
            messagebox.showerror("Error", "Please enter a query!")
            return
            
        self.execute_btn.config(state='disabled', text="Executing...")
        
        def query_thread():
            try:
                results = self.db_manager.execute_query(query)
                self.root.after(0, self.update_query_results, results)
            except Exception as e:
                self.root.after(0, self.update_query_results, None, str(e))
                
        thread = threading.Thread(target=query_thread, daemon=True)
        thread.start()
        
    def update_query_results(self, results, error_msg=None):
        """Update UI with query results"""
        self.execute_btn.config(state='normal', text="Execute Query")
        
        if error_msg:
            messagebox.showerror("Error", f"Query error: {error_msg}")
            return
            
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if results:
            columns = list(results[0].keys()) if results else []
            self.results_tree['columns'] = columns
            self.results_tree['show'] = 'headings'
            
            for col in columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, width=100)
                
            for row in results:
                self.results_tree.insert('', 'end', values=list(row.values()))
                
            messagebox.showinfo("Success", f"Query executed successfully! {len(results)} rows returned.")
        else:
            messagebox.showinfo("Success", "Query executed successfully!")
    
    def check_postgis_status(self):
        """Check if PostGIS is enabled"""
        if not self.db_manager.is_connected():
            self.postgis_status_label.config(text="Not connected to database", foreground="red")
            return
            
        if self.db_manager.db_type != 'PostgreSQL':
            self.postgis_status_label.config(text="PostGIS is only available for PostgreSQL", foreground="orange")
            return
            
        try:
            result = self.db_manager.execute_query(
                "SELECT COUNT(*) FROM pg_extension WHERE extname = 'postgis'"
            )
            if result and result[0]['count'] > 0:
                self.postgis_status_label.config(text="PostGIS is enabled ✓", foreground="green")
            else:
                self.postgis_status_label.config(text="PostGIS is not enabled ✗", foreground="red")
        except Exception as e:
            self.postgis_status_label.config(text=f"Error checking PostGIS: {str(e)}", foreground="red")
    
    def enable_postgis(self):
        """Try to enable PostGIS extension"""
        if not self.db_manager.is_connected():
            messagebox.showerror("Error", "Please connect to a database first!")
            return
            
        if self.db_manager.db_type != 'PostgreSQL':
            messagebox.showerror("Error", "PostGIS is only available for PostgreSQL databases!")
            return
            
        success, message = self.db_manager.enable_postgis()
        
        if success:
            messagebox.showinfo("Success", message)
            self.check_postgis_status()
            self.refresh_spatial_tables()
        else:
            messagebox.showerror("Error", message)
    
    def refresh_spatial_tables(self):
        """Refresh the list of spatial tables"""
        if not self.db_manager.is_connected():
            return
            
        # Clear existing items
        for item in self.spatial_tree.get_children():
            self.spatial_tree.delete(item)
            
        # Get spatial tables
        spatial_tables = self.db_manager.get_spatial_tables()
        
        for table_info in spatial_tables:
            action = "Ready" if table_info['type'] == 'geometry' else "Convert to Geometry"
            self.spatial_tree.insert('', 'end', values=(
                table_info['table'],
                table_info['column'],
                table_info['type'].upper(),
                action
            ))
    
    def convert_selected_table(self):
        """Convert WKT to geometry for selected table"""
        selection = self.spatial_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a table to convert")
            return
            
        item = self.spatial_tree.item(selection[0])
        values = item['values']
        
        if values[2] != 'WKT':
            messagebox.showinfo("Info", "This table already has proper geometry column")
            return
            
        table_name = values[0]
        wkt_column = values[1]
        
        # Show progress
        self.conversion_status.config(text="Converting... Please wait.")
        self.spatial_tab.update()
        
        success, message = self.db_manager.convert_wkt_to_geometry(table_name, wkt_column)
        
        if success:
            self.conversion_status.config(text="Conversion successful!", foreground="green")
            messagebox.showinfo("Success", message)
            self.refresh_spatial_tables()
        else:
            self.conversion_status.config(text="Conversion failed", foreground="red")
            messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseImporterApp(root)
    root.mainloop()