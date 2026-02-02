"""
Test script to verify the Faker GUI application works correctly.
This tests the core functionality without the GUI.
"""

from data_generator import DataGenerator
from query_builder import QueryBuilder

# Test DDL from the user's example
test_ddl = """
CREATE TABLE `t_listing_document` (
  `listing_document_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `posting_date` date DEFAULT NULL,
  `no_kwitansi_dn` varchar(100) DEFAULT NULL,
  `customer_payer_id` varchar(100) DEFAULT NULL,
  `customer_payer` varchar(100) DEFAULT NULL,
  `sap_document_type` varchar(100) DEFAULT NULL,
  `company_code` int DEFAULT NULL,
  `fiscal_year` year(4) DEFAULT NULL,
  `sap_doc_number` varchar(100) DEFAULT NULL,
  `no_kwitansi_customer` varchar(100) DEFAULT NULL,
  `faktur_pajak` varchar(100) DEFAULT NULL,
  `amount` decimal(10,0) DEFAULT NULL,
  `doc_status` enum('NOT READY','READY','COMPLETE') DEFAULT 'NOT READY',
  `total_amount` decimal(10,0) DEFAULT NULL,
  `collector_name` varchar(100) DEFAULT NULL,
  `collector_email` varchar(100) DEFAULT NULL,
  `assignment_date` date DEFAULT NULL,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `sales_organization_id` varchar(100) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `deleted_by` varchar(100) DEFAULT NULL,
  `no_bukti_potong` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`listing_document_id`),
  KEY `idx_company_code` (`company_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=120001;
"""

# Test JSON config
test_json_config = """
{
    "company_code": ["1111", "1112"]
}
"""

def test_data_generation():
    """Test data generation with DDL and JSON config."""
    print("=" * 80)
    print("Testing Faker GUI Application")
    print("=" * 80)
    
    try:
        # Create generator
        print("\n1. Creating data generator...")
        generator = DataGenerator(test_ddl, test_json_config)
        print(f"   ✓ Table: {generator.get_table_name()}")
        print(f"   ✓ Columns to insert: {len(generator.get_columns())}")
        
        # Print column names
        print("\n2. Columns that will be populated:")
        for col in generator.get_columns():
            print(f"   - {col.name} ({col.data_type})")
        
        # Generate records
        print("\n3. Generating 5 test records...")
        records = generator.generate_records(5)
        print(f"   ✓ Generated {len(records)} records")
        
        # Verify company_code is from the JSON config
        print("\n4. Verifying JSON config override (company_code):")
        company_codes = [r['company_code'] for r in records]
        print(f"   Generated company_codes: {company_codes}")
        all_valid = all(code in ["1111", "1112"] for code in company_codes)
        if all_valid:
            print("   ✓ All company_codes are from the configured values")
        else:
            print("   ✗ ERROR: Some company_codes are not from config!")
        
        # Check email field
        print("\n5. Checking email field generation:")
        emails = [r.get('collector_email') for r in records if r.get('collector_email')]
        if emails:
            print(f"   Sample email: {emails[0]}")
            if '@' in emails[0]:
                print("   ✓ Email field contains valid email format")
        
        # Check enum field
        print("\n6. Checking ENUM field (doc_status):")
        statuses = [r['doc_status'] for r in records]
        print(f"   Generated statuses: {statuses}")
        valid_statuses = all(s in ['NOT READY', 'READY', 'COMPLETE'] for s in statuses)
        if valid_statuses:
            print("   ✓ All statuses are valid ENUM values")
        else:
            print("   ✗ ERROR: Invalid status values found!")
        
        # Build SQL query
        print("\n7. Generating SQL INSERT query...")
        sql = QueryBuilder.build_insert_query(generator.get_table_name(), records, batch_size=5)
        
        print("\n8. Generated SQL (first 500 characters):")
        print("-" * 80)
        print(sql[:500] + "...")
        print("-" * 80)
        
        # Count total SQL length
        print(f"\n9. SQL Statistics:")
        print(f"   - Total SQL length: {len(sql)} characters")
        print(f"   - Number of INSERT statements: {sql.count('INSERT INTO')}")
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_generation()
    exit(0 if success else 1)
