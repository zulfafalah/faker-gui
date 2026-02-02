-- Example DDL for testing the Faker GUI application
-- This is the t_listing_document table from the user's example

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
