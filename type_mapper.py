"""
Type mapper module for mapping SQL types to Faker generators.
"""

import re
from typing import Any, Optional
from faker import Faker


class TypeMapper:
    """Maps SQL column types to appropriate Faker methods."""
    
    def __init__(self):
        self.faker = Faker('id_ID')  # Use Indonesian locale
    
    def get_faker_value(self, column_name: str, column_type: str, 
                       enum_values: Optional[list] = None,
                       config_value: Any = None) -> Any:
        """
        Generate a fake value based on column name and type.
        
        Args:
            column_name: Name of the column
            column_type: SQL type of the column
            enum_values: List of enum values if column is ENUM type
            config_value: Override value from JSON config
            
        Returns:
            Generated fake value
        """
        # If config value is provided, use it
        if config_value is not None:
            if isinstance(config_value, list):
                return self.faker.random_element(config_value)
            return config_value
        
        # Handle ENUM types
        if enum_values:
            return self.faker.random_element(enum_values)
        
        # Context-aware generation based on column name
        column_name_lower = column_name.lower()
        
        # Business-specific patterns
        
        # Kwitansi/Receipt numbers (DN prefix)
        if 'kwitansi_dn' in column_name_lower or 'no_kwitansi_dn' in column_name_lower:
            return f"DN{self.faker.random_int(min=100000, max=999999)}"
        
        # Customer Kwitansi (KW prefix)
        if 'kwitansi_customer' in column_name_lower or 'no_kwitansi_customer' in column_name_lower:
            return f"KW{self.faker.random_int(min=100000, max=999999)}"
        
        # Faktur Pajak (FP prefix)
        if 'faktur' in column_name_lower or 'faktur_pajak' in column_name_lower:
            return f"FP{self.faker.random_int(min=100000000, max=999999999)}"
        
        # Bukti Potong (BP prefix)
        if 'bukti_potong' in column_name_lower or 'no_bukti_potong' in column_name_lower:
            # Sometimes null
            if self.faker.boolean(chance_of_getting_true=70):
                return f"BP{self.faker.random_int(min=100000, max=999999)}"
            return None
        
        # Customer ID/Payer ID
        if 'customer_payer_id' in column_name_lower or 'payer_id' in column_name_lower:
            return f"CUST{self.faker.random_int(min=1000, max=9999)}"
        
        # Customer/Payer name (company name)
        if 'customer_payer' in column_name_lower or 'payer' in column_name_lower:
            return self.faker.company()
        
        # SAP Document Type
        if 'sap_document_type' in column_name_lower or 'document_type' in column_name_lower:
            sap_types = ['DR', 'DZ', 'RV', 'DG', 'AB', 'DA', 'SA']
            return self.faker.random_element(sap_types)
        
        # SAP Document Number
        if 'sap_doc' in column_name_lower and 'number' in column_name_lower:
            return f"{self.faker.random_int(min=1000000000, max=9999999999)}"
        
        # Sales Organization ID
        if 'sales_org' in column_name_lower or 'organization_id' in column_name_lower:
            return f"SO{self.faker.random_int(min=1000, max=9999)}"
        
        # User fields (created_by, updated_by, etc)
        if any(x in column_name_lower for x in ['created_by', 'updated_by', 'user', 'username']):
            if 'email' not in column_name_lower:
                return self.faker.user_name()
        
        # Email fields
        if 'email' in column_name_lower:
            return self.faker.email()
        
        # Name fields (person names)
        if 'name' in column_name_lower and 'file' not in column_name_lower and 'company' not in column_name_lower:
            if 'first' in column_name_lower:
                return self.faker.first_name()
            elif 'last' in column_name_lower:
                return self.faker.last_name()
            else:
                return self.faker.name()
        
        # Phone fields
        if 'phone' in column_name_lower or 'telepon' in column_name_lower:
            return self.faker.phone_number()
        
        # Address fields
        if 'address' in column_name_lower or 'alamat' in column_name_lower:
            return self.faker.address()
        
        # City fields
        if 'city' in column_name_lower or 'kota' in column_name_lower:
            return self.faker.city()
        
        # Country fields
        if 'country' in column_name_lower or 'negara' in column_name_lower:
            return self.faker.country()
        
        # URL fields
        if 'url' in column_name_lower or 'website' in column_name_lower:
            return self.faker.url()
        
        # Description/text fields
        if 'description' in column_name_lower or 'desc' in column_name_lower or 'note' in column_name_lower:
            return self.faker.sentence(nb_words=6)
        
        # Company fields
        if 'company' in column_name_lower or 'perusahaan' in column_name_lower:
            return self.faker.company()
        
        # Type-based generation
        column_type_lower = column_type.lower()
        
        # String types
        if any(t in column_type_lower for t in ['varchar', 'char', 'text']):
            # Extract max length if specified
            match = re.search(r'\((\d+)\)', column_type)
            max_length = int(match.group(1)) if match else 100
            
            # Generate appropriate length text
            if max_length <= 10:
                # Short codes/IDs
                return self.faker.bothify(text='??####')[:max_length]
            elif max_length <= 20:
                # Short identifiers or codes
                return f"{self.faker.word()}{self.faker.random_int(min=100, max=999)}"[:max_length]
            elif max_length <= 50:
                # Single word or short phrase
                return self.faker.word()[:max_length]
            elif max_length <= 100:
                # Short sentence
                return self.faker.sentence(nb_words=3)[:max_length]
            else:
                # Longer text
                return self.faker.sentence(nb_words=8)[:max_length]
        
        # Integer types
        if any(t in column_type_lower for t in ['int', 'integer', 'bigint', 'smallint', 'tinyint']):
            if 'bigint' in column_type_lower:
                return self.faker.random_int(min=1, max=999999999)
            return self.faker.random_int(min=1, max=99999)
        
        # Decimal/Float types
        if any(t in column_type_lower for t in ['decimal', 'numeric', 'float', 'double']):
            # Extract precision and scale if specified
            match = re.search(r'\((\d+),(\d+)\)', column_type)
            if match:
                precision = int(match.group(1))
                scale = int(match.group(2))
                max_value = 10 ** (precision - scale) - 1
                return round(self.faker.random.uniform(0, max_value), scale)
            
            match = re.search(r'\((\d+)\)', column_type)
            if match:
                precision = int(match.group(1))
                max_value = 10 ** precision - 1
                return self.faker.random_int(min=0, max=max_value)
            
            return round(self.faker.random.uniform(0, 999999), 2)
        
        # Date type
        if 'date' == column_type_lower:
            return self.faker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
        
        # Datetime/Timestamp types
        if any(t in column_type_lower for t in ['datetime', 'timestamp']):
            return self.faker.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        
        # Time type
        if 'time' in column_type_lower:
            return self.faker.time()
        
        # Year type
        if 'year' in column_type_lower:
            return self.faker.random_int(min=2020, max=2026)
        
        # Boolean type
        if any(t in column_type_lower for t in ['bool', 'boolean']):
            return self.faker.random_int(min=0, max=1)
        
        # Default: return a word
        return self.faker.word()
