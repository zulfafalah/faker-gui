"""
SQL Query builder module for constructing INSERT statements.
"""

from typing import List, Dict, Any


class QueryBuilder:
    """Builds SQL INSERT statements from generated data."""
    
    @staticmethod
    def format_value(value: Any) -> str:
        """
        Format a value for SQL insertion.
        
        Args:
            value: The value to format
            
        Returns:
            SQL-formatted string representation of the value
        """
        if value is None:
            return 'NULL'
        
        if isinstance(value, (int, float)):
            return str(value)
        
        if isinstance(value, bool):
            return '1' if value else '0'
        
        # String values - escape single quotes
        value_str = str(value).replace("'", "''").replace("\\", "\\\\")
        return f"'{value_str}'"
    
    @staticmethod
    def build_insert_query(table_name: str, records: List[Dict[str, Any]], 
                          batch_size: int = 10) -> str:
        """
        Build INSERT query from records.
        
        Args:
            table_name: Name of the table
            records: List of record dictionaries
            batch_size: Number of records per INSERT statement
            
        Returns:
            SQL INSERT query string
        """
        if not records:
            return ""
        
        # Get column names from first record
        columns = list(records[0].keys())
        column_list = ', '.join([f'`{col}`' for col in columns])
        
        queries = []
        
        # Process records in batches
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            # Build values list
            values_list = []
            for record in batch:
                values = [QueryBuilder.format_value(record[col]) for col in columns]
                values_str = ', '.join(values)
                values_list.append(f"({values_str})")
            
            # Build INSERT statement
            values_section = ',\n  '.join(values_list)
            query = f"INSERT INTO `{table_name}` ({column_list})\nVALUES\n  {values_section};"
            queries.append(query)
        
        return '\n\n'.join(queries)
    
    @staticmethod
    def build_single_row_inserts(table_name: str, records: List[Dict[str, Any]]) -> str:
        """
        Build individual INSERT statements for each record.
        
        Args:
            table_name: Name of the table
            records: List of record dictionaries
            
        Returns:
            SQL INSERT queries (one per record)
        """
        if not records:
            return ""
        
        # Get column names from first record
        columns = list(records[0].keys())
        column_list = ', '.join([f'`{col}`' for col in columns])
        
        queries = []
        
        for record in records:
            values = [QueryBuilder.format_value(record[col]) for col in columns]
            values_str = ', '.join(values)
            query = f"INSERT INTO `{table_name}` ({column_list}) VALUES ({values_str});"
            queries.append(query)
        
        return '\n'.join(queries)
