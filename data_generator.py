"""
Data generator module for generating fake data based on column definitions.
"""

import json
from typing import Dict, List, Any
from ddl_parser import Column, DDLParser
from type_mapper import TypeMapper


class DataGenerator:
    """Generates fake data for database tables."""
    
    def __init__(self, ddl: str, json_config: str = "{}"):
        """
        Initialize the data generator.
        
        Args:
            ddl: DDL statement defining the table structure
            json_config: JSON string with configuration overrides
        """
        self.parser = DDLParser(ddl)
        self.table_info = self.parser.parse()
        self.type_mapper = TypeMapper()
        
        # Parse JSON config
        try:
            self.config = json.loads(json_config) if json_config.strip() else {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON config: {e}")
    
    def generate_records(self, count: int) -> List[Dict[str, Any]]:
        """
        Generate specified number of fake records.
        
        Args:
            count: Number of records to generate
            
        Returns:
            List of dictionaries representing records
        """
        records = []
        insertable_columns = self.parser.get_insertable_columns()
        
        for _ in range(count):
            record = {}
            for column in insertable_columns:
                # Get config value for this column if available
                config_value = self.config.get(column.name)
                
                # Generate value
                value = self.type_mapper.get_faker_value(
                    column_name=column.name,
                    column_type=column.data_type,
                    enum_values=column.enum_values if column.enum_values else None,
                    config_value=config_value
                )
                
                record[column.name] = value
            
            records.append(record)
        
        return records
    
    def get_table_name(self) -> str:
        """Get the table name from parsed DDL."""
        return self.table_info['table_name']
    
    def get_columns(self) -> List[Column]:
        """Get list of columns that will be inserted."""
        return self.parser.get_insertable_columns()
