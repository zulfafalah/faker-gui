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

## License

MIT License - Feel free to use and modify as needed.
