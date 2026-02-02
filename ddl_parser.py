"""
DDL Parser module for parsing MySQL CREATE TABLE statements.
"""

import re
from typing import Dict, List, Optional


class Column:
    """Represents a table column."""
    
    def __init__(self, name: str, data_type: str, nullable: bool = True,
                 auto_increment: bool = False, default: Optional[str] = None,
                 enum_values: Optional[List[str]] = None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.auto_increment = auto_increment
        self.default = default
        self.enum_values = enum_values or []
    
    def __repr__(self):
        return f"Column(name={self.name}, type={self.data_type}, nullable={self.nullable}, auto_increment={self.auto_increment})"


class DDLParser:
    """Parser for MySQL CREATE TABLE DDL statements."""
    
    def __init__(self, ddl: str):
        self.ddl = ddl
        self.table_name = ""
        self.columns: List[Column] = []
    
    def parse(self) -> Dict:
        """
        Parse the DDL statement and extract table information.
        
        Returns:
            Dictionary containing table name and columns
        """
        # Extract table name
        table_match = re.search(r'CREATE TABLE\s+`?(\w+)`?', self.ddl, re.IGNORECASE)
        if not table_match:
            raise ValueError("Invalid DDL: Could not find CREATE TABLE statement")
        
        self.table_name = table_match.group(1)
        
        # Extract column definitions
        # Match everything between the first ( and last )
        columns_match = re.search(r'CREATE TABLE[^(]+\((.*)\)', self.ddl, re.IGNORECASE | re.DOTALL)
        if not columns_match:
            raise ValueError("Invalid DDL: Could not find column definitions")
        
        columns_section = columns_match.group(1)
        
        # Split by lines and process each column definition
        lines = columns_section.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines, PRIMARY KEY, KEY, and other constraints
            if not line or line.startswith('PRIMARY KEY') or line.startswith('KEY ') or \
               line.startswith('UNIQUE') or line.startswith('FOREIGN') or \
               line.startswith('INDEX') or line.startswith('CONSTRAINT') or \
               line.startswith(')'):
                continue
            
            # Remove trailing comma
            line = line.rstrip(',')
            
            # Parse column definition
            column = self._parse_column_definition(line)
            if column:
                self.columns.append(column)
        
        return {
            'table_name': self.table_name,
            'columns': self.columns
        }
    
    def _parse_column_definition(self, definition: str) -> Optional[Column]:
        """Parse a single column definition line."""
        
        # Extract column name (first quoted or unquoted identifier)
        name_match = re.match(r'`?(\w+)`?\s+(.+)', definition)
        if not name_match:
            return None
        
        column_name = name_match.group(1)
        rest_of_definition = name_match.group(2)
        
        # Extract data type
        # Handle ENUM specially
        if rest_of_definition.upper().startswith('ENUM'):
            enum_match = re.match(r"ENUM\s*\(([^)]+)\)", rest_of_definition, re.IGNORECASE)
            if enum_match:
                enum_values_str = enum_match.group(1)
                # Extract enum values
                enum_values = [v.strip().strip("'\"") for v in enum_values_str.split(',')]
                data_type = 'ENUM'
                rest_of_definition = rest_of_definition[enum_match.end():]
            else:
                data_type = 'ENUM'
                enum_values = []
        else:
            # Extract data type (word possibly followed by parentheses)
            type_match = re.match(r'(\w+(?:\s+unsigned)?(?:\([^)]+\))?)', rest_of_definition, re.IGNORECASE)
            if type_match:
                data_type = type_match.group(1)
                rest_of_definition = rest_of_definition[type_match.end():]
                enum_values = []
            else:
                return None
        
        # Check for constraints
        nullable = 'NOT NULL' not in rest_of_definition.upper()
        auto_increment = 'AUTO_INCREMENT' in rest_of_definition.upper()
        
        # Extract default value
        default = None
        default_match = re.search(r"DEFAULT\s+([^,\s]+(?:\s+ON\s+UPDATE\s+[^,]+)?)", rest_of_definition, re.IGNORECASE)
        if default_match:
            default = default_match.group(1).strip("'\"")
        
        return Column(
            name=column_name,
            data_type=data_type,
            nullable=nullable,
            auto_increment=auto_increment,
            default=default,
            enum_values=enum_values
        )
    
    def get_insertable_columns(self) -> List[Column]:
        """
        Get columns that should be included in INSERT statements.
        Excludes AUTO_INCREMENT columns.
        """
        return [col for col in self.columns if not col.auto_increment]
