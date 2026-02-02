"""
Quick demo to show the improved contextual output
"""

from data_generator import DataGenerator
from query_builder import QueryBuilder

# Example DDL
ddl = """
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
  PRIMARY KEY (`listing_document_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
"""

json_config = '{"company_code": ["1111", "1112"]}'

# Generate 3 records
generator = DataGenerator(ddl, json_config)
records = generator.generate_records(3)

# Show the generated data
print("=" * 80)
print("IMPROVED CONTEXTUAL OUTPUT")
print("=" * 80)
print()

for i, record in enumerate(records, 1):
    print(f"Record {i}:")
    print(f"  no_kwitansi_dn: {record['no_kwitansi_dn']}")
    print(f"  customer_payer_id: {record['customer_payer_id']}")
    print(f"  customer_payer: {record['customer_payer']}")
    print(f"  sap_document_type: {record['sap_document_type']}")
    print(f"  sap_doc_number: {record['sap_doc_number']}")
    print(f"  no_kwitansi_customer: {record['no_kwitansi_customer']}")
    print(f"  faktur_pajak: {record['faktur_pajak']}")
    print(f"  collector_name: {record['collector_name']}")
    print(f"  collector_email: {record['collector_email']}")
    print()

print("=" * 80)
print("FULL SQL OUTPUT:")
print("=" * 80)
sql = QueryBuilder.build_insert_query(generator.get_table_name(), records, batch_size=3)
print(sql)
