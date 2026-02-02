# Faker GUI - SQL Data Generator

A cross-platform GUI application for generating fake SQL data from DDL statements using the Faker library.

## Features

- 🎯 **DDL Parsing**: Automatically parse MySQL CREATE TABLE statements
- 🎲 **Smart Data Generation**: Context-aware fake data generation using Faker
- ⚙️ **JSON Config**: Override specific columns with fixed or random values from a list
- 📋 **Copy to Clipboard**: Easy copy-paste of generated SQL
- 💻 **Cross-Platform**: Works on Windows and Linux (using tkinter)

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)

### Setup

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python faker_gui.py
```

### How to Use

1. **Enter DDL Statement**: Paste your MySQL CREATE TABLE statement in the DDL input area
2. **Add JSON Config (Optional)**: Specify fixed values for certain columns using JSON format
3. **Set Record Count**: Choose how many records to generate
4. **Click Generate**: Click the "Generate SQL" button
5. **Copy Output**: Use "Copy to Clipboard" to copy the generated INSERT statements

### Example

#### DDL Input:
```sql
CREATE TABLE `t_listing_document` (
  `listing_document_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `posting_date` date DEFAULT NULL,
  `no_kwitansi_dn` varchar(100) DEFAULT NULL,
  `customer_payer_id` varchar(100) DEFAULT NULL,
  `customer_payer` varchar(100) DEFAULT NULL,
  `company_code` int DEFAULT NULL,
  `fiscal_year` year(4) DEFAULT NULL,
  `amount` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`listing_document_id`)
);
```

#### JSON Config:
```json
{
  "company_code": ["1111", "1112"],
  "fiscal_year": [2024, 2025, 2026]
}
```

#### Output:
The application will generate INSERT statements with:
- `company_code` randomly selected from ["1111", "1112"]
- `fiscal_year` randomly selected from [2024, 2025, 2026]
- All other fields filled with appropriate fake data
- `listing_document_id` excluded (AUTO_INCREMENT)

## Supported SQL Types

The application intelligently maps SQL types to appropriate fake data:

| SQL Type | Generated Data |
|----------|---------------|
| VARCHAR, TEXT | Random text/names |
| INT, BIGINT | Random integers |
| DECIMAL, NUMERIC | Random decimal numbers |
| DATE | Random dates |
| DATETIME, TIMESTAMP | Random timestamps |
| YEAR | Random year values |
| ENUM | Random selection from enum values |

### Context-Aware Generation

The generator recognizes column names and generates appropriate data:

- `*email*` → Email addresses
- `*name*` → Person names
- `*phone*`, `*telepon*` → Phone numbers
- `*address*`, `*alamat*` → Addresses
- `*company*` → Company names
- And more...

## JSON Config Format

The JSON config allows you to override specific columns with fixed values or a list of values to randomly choose from:

```json
{
  "column_name": ["value1", "value2", "value3"],
  "another_column": "fixed_value"
}
```

## Platform Compatibility

- ✅ **Windows**: Fully supported
- ✅ **Linux**: Fully supported
- ⚠️ **macOS**: Should work (tkinter is available on macOS)

## Notes

- AUTO_INCREMENT columns are automatically excluded from INSERT statements
- The application uses Indonesian locale for Faker by default (can be changed in `type_mapper.py`)
- Generated values respect column constraints (NOT NULL, data types, etc.)

## Building Windows Executable

You can compile this application into a standalone Windows executable (.exe) that runs without Python installed.

### Prerequisites for Building

- Python 3.11 or higher
- All runtime dependencies (`requirements.txt`)
- Build dependencies (`requirements-build.txt`)

### Build Instructions

#### Option 1: Build on Windows (Recommended)

1. **Install Dependencies:**
   ```cmd
   pip install -r requirements.txt
   pip install -r requirements-build.txt
   ```

2. **Run Build Script:**
   ```cmd
   python build.py
   ```

3. **Find Your Executable:**
   - Location: `dist/FakerGUI.exe`
   - Size: ~15-25 MB (includes Python runtime)
   - Standalone - no Python installation needed to run

#### Option 2: Build Using Spec File

For more control over the build process:

```cmd
pyinstaller faker_gui.spec
```

This uses the spec file which includes example files and custom configuration.

#### Option 3: Cross-compile on Linux (Advanced)

If you're on Linux but need a Windows executable:

1. **Install Wine:**
   ```bash
   sudo apt-get install wine wine64
   ```

2. **Install Windows Python in Wine:**
   ```bash
   wget https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
   wine python-3.11.7-amd64.exe
   ```

3. **Install Dependencies:**
   ```bash
   wine python -m pip install -r requirements.txt
   wine python -m pip install -r requirements-build.txt
   ```

4. **Build:**
   ```bash
   wine python build.py
   ```

**Note:** Cross-compilation is experimental. Native Windows builds are recommended for production.

### Distribution

Once built, `FakerGUI.exe` can be:
- Distributed as a single file
- Run on Windows 10/11 without Python
- Shared via USB, email, or download
- No installation required

### Build Files

- `build.py` - Automated build script
- `faker_gui.spec` - PyInstaller configuration
- `requirements-build.txt` - Build-time dependencies

## License

MIT License - Feel free to use and modify as needed.

