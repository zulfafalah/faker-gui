"""
Faker GUI - A cross-platform application for generating fake SQL data.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
from data_generator import DataGenerator
from query_builder import QueryBuilder


class FakerGUI:
    """Main GUI application for generating fake SQL data."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Faker GUI - SQL Data Generator")
        self.root.geometry("1200x800")
        
        # Set minimum window size
        self.root.minsize(900, 600)
        
        # File tracking
        self.current_file = None
        self.is_modified = False
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.grid_rowconfigure(3, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_container, text="SQL Faker Data Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Create input section
        self._create_input_section(main_container)
        
        # Create controls section
        self._create_controls_section(main_container)
        
        # Create output section
        self._create_output_section(main_container)
    
    def _create_menu_bar(self):
        """Create the menu bar with File menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.load_configuration, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_configuration, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_configuration_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Ctrl+Q")
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.load_configuration())
        self.root.bind('<Control-s>', lambda e: self.save_configuration())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_configuration_as())
        self.root.bind('<Control-q>', lambda e: self.exit_application())
    
    def _create_input_section(self, parent):
        """Create the input section with DDL and JSON config."""
        input_frame = ttk.LabelFrame(parent, text="Input", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.grid_rowconfigure(1, weight=1)
        input_frame.grid_columnconfigure(0, weight=3)
        input_frame.grid_columnconfigure(1, weight=1)
        
        # DDL Input
        ddl_label = ttk.Label(input_frame, text="DDL Statement (CREATE TABLE):", 
                             font=('Arial', 10, 'bold'))
        ddl_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.ddl_text = scrolledtext.ScrolledText(input_frame, height=15, width=70, 
                                                  font=('Courier', 10), wrap=tk.WORD)
        self.ddl_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          padx=(0, 10))
        
        # Add placeholder text
        placeholder_ddl = """-- Paste your CREATE TABLE statement here
-- Example:
CREATE TABLE `t_listing_document` (
  `listing_document_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `posting_date` date DEFAULT NULL,
  `customer_payer` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`listing_document_id`)
);"""
        self.ddl_text.insert('1.0', placeholder_ddl)
        self.ddl_text.bind('<FocusIn>', self._on_ddl_focus_in)
        self.ddl_text.bind('<KeyRelease>', self._on_text_modified)
        
        # JSON Config Input
        json_label = ttk.Label(input_frame, text="JSON Config (Optional):", 
                              font=('Arial', 10, 'bold'))
        json_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.json_text = scrolledtext.ScrolledText(input_frame, height=15, width=30,
                                                   font=('Courier', 10), wrap=tk.WORD)
        self.json_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add placeholder JSON
        placeholder_json = """{
  "company_code": ["1111", "1112"],
  "fiscal_year": [2024, 2025, 2026]
}"""
        self.json_text.insert('1.0', placeholder_json)
        self.json_text.bind('<FocusIn>', self._on_json_focus_in)
        self.json_text.bind('<KeyRelease>', self._on_text_modified)
    
    def _create_controls_section(self, parent):
        """Create the controls section with record count and generate button."""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Record count
        count_label = ttk.Label(controls_frame, text="Number of Records:", 
                               font=('Arial', 10, 'bold'))
        count_label.grid(row=0, column=0, padx=(0, 10))
        
        self.count_var = tk.StringVar(value="10")
        count_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10000, 
                                   textvariable=self.count_var, width=10)
        count_spinbox.grid(row=0, column=1, padx=(0, 20))
        
        # Generate button
        generate_btn = ttk.Button(controls_frame, text="Generate SQL", 
                                 command=self.generate_sql, style='Accent.TButton')
        generate_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(controls_frame, text="Clear All", 
                              command=self.clear_all)
        clear_btn.grid(row=0, column=3, padx=(0, 10))
    
    def _create_output_section(self, parent):
        """Create the output section for displaying generated SQL."""
        output_frame = ttk.LabelFrame(parent, text="Generated SQL", padding="10")
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, 
                                                     font=('Courier', 10), wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons frame
        btn_frame = ttk.Frame(output_frame)
        btn_frame.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Copy button
        copy_btn = ttk.Button(btn_frame, text="Copy to Clipboard", 
                             command=self.copy_to_clipboard)
        copy_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear output button
        clear_output_btn = ttk.Button(btn_frame, text="Clear Output", 
                                     command=self.clear_output)
        clear_output_btn.grid(row=0, column=1)
    
    def _on_ddl_focus_in(self, event):
        """Clear placeholder text when DDL field is focused."""
        if self.ddl_text.get('1.0', 'end-1c').startswith('-- Paste your CREATE TABLE'):
            self.ddl_text.delete('1.0', tk.END)
    
    def _on_json_focus_in(self, event):
        """Clear placeholder text when JSON field is focused."""
        current_text = self.json_text.get('1.0', 'end-1c').strip()
        if current_text.startswith('{') and '"company_code"' in current_text:
            self.json_text.delete('1.0', tk.END)
    
    def _on_text_modified(self, event):
        """Mark configuration as modified when text changes."""
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
    
    def generate_sql(self):
        """Generate SQL INSERT statements based on inputs."""
        try:
            # Get inputs
            ddl = self.ddl_text.get('1.0', 'end-1c').strip()
            json_config = self.json_text.get('1.0', 'end-1c').strip()
            
            # Validate DDL
            if not ddl or ddl.startswith('-- Paste your CREATE TABLE'):
                messagebox.showerror("Error", "Please enter a valid DDL statement")
                return
            
            # Validate record count
            try:
                count = int(self.count_var.get())
                if count < 1:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of records (minimum 1)")
                return
            
            # Generate data
            generator = DataGenerator(ddl, json_config)
            records = generator.generate_records(count)
            
            # Build SQL query
            table_name = generator.get_table_name()
            sql = QueryBuilder.build_insert_query(table_name, records, batch_size=100)
            
            # Display output
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert('1.0', sql)
            
            # Show success message
            messagebox.showinfo("Success", 
                              f"Generated {count} records for table '{table_name}'")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy generated SQL to clipboard."""
        sql = self.output_text.get('1.0', 'end-1c').strip()
        if sql:
            self.root.clipboard_clear()
            self.root.clipboard_append(sql)
            messagebox.showinfo("Success", "SQL copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No SQL to copy. Generate SQL first.")
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete('1.0', tk.END)
    
    def clear_all(self):
        """Clear all input and output fields."""
        self.ddl_text.delete('1.0', tk.END)
        self.json_text.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
        self.count_var.set("10")
        self.is_modified = False
        self.update_title()
    
    def new_file(self):
        """Create a new configuration (reset all fields)."""
        if self.is_modified:
            response = messagebox.askyesnocancel("Save Changes?", 
                                                 "Do you want to save changes to the current configuration?")
            if response is True:  # Yes, save
                self.save_configuration()
            elif response is None:  # Cancel
                return
        
        self.clear_all()
        self.current_file = None
        self.is_modified = False
        self.update_title()
    
    def save_configuration(self):
        """Save current configuration to file."""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_configuration_as()
    
    def save_configuration_as(self):
        """Save current configuration to a new file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".faker",
            filetypes=[("Faker Configuration", "*.faker"), ("All Files", "*.*")],
            title="Save Configuration As"
        )
        
        if filepath:
            self._save_to_file(filepath)
    
    def _save_to_file(self, filepath):
        """Internal method to save configuration to specified file."""
        try:
            # Get current DDL and JSON config
            ddl = self.ddl_text.get('1.0', 'end-1c').strip()
            json_config = self.json_text.get('1.0', 'end-1c').strip()
            count = self.count_var.get()
            
            # Create configuration dictionary
            config = {
                "ddl_statement": ddl,
                "json_config": json_config,
                "record_count": count
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.current_file = filepath
            self.is_modified = False
            self.update_title()
            messagebox.showinfo("Success", f"Configuration saved to:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
    
    def load_configuration(self):
        """Load configuration from file."""
        if self.is_modified:
            response = messagebox.askyesnocancel("Save Changes?", 
                                                 "Do you want to save changes to the current configuration?")
            if response is True:  # Yes, save
                self.save_configuration()
            elif response is None:  # Cancel
                return
        
        filepath = filedialog.askopenfilename(
            defaultextension=".faker",
            filetypes=[("Faker Configuration", "*.faker"), ("All Files", "*.*")],
            title="Open Configuration"
        )
        
        if filepath:
            self._load_from_file(filepath)
    
    def _load_from_file(self, filepath):
        """Internal method to load configuration from specified file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Clear existing content
            self.ddl_text.delete('1.0', tk.END)
            self.json_text.delete('1.0', tk.END)
            self.output_text.delete('1.0', tk.END)
            
            # Load DDL statement
            if 'ddl_statement' in config:
                self.ddl_text.insert('1.0', config['ddl_statement'])
            
            # Load JSON config
            if 'json_config' in config:
                self.json_text.insert('1.0', config['json_config'])
            
            # Load record count
            if 'record_count' in config:
                self.count_var.set(config['record_count'])
            
            self.current_file = filepath
            self.is_modified = False
            self.update_title()
            messagebox.showinfo("Success", f"Configuration loaded from:\n{filepath}")
            
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid configuration file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
    
    def update_title(self):
        """Update window title with current file name."""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            modified_flag = "*" if self.is_modified else ""
            self.root.title(f"Faker GUI - {filename}{modified_flag}")
        else:
            modified_flag = "*" if self.is_modified else ""
            self.root.title(f"Faker GUI - SQL Data Generator{modified_flag}")
    
    def exit_application(self):
        """Exit the application with save prompt if needed."""
        if self.is_modified:
            response = messagebox.askyesnocancel("Save Changes?", 
                                                 "Do you want to save changes before exiting?")
            if response is True:  # Yes, save
                self.save_configuration()
                self.root.destroy()
            elif response is False:  # No, don't save
                self.root.destroy()
            # Cancel: do nothing
        else:
            self.root.destroy()


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = FakerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
