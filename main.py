import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('id_ID')  # Indonesian locale

def generate_random_date(start_date, end_date):
    """Generate random date between start_date and end_date"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def generate_insert_statements(num_records=100):
    """Generate SQL INSERT statements for t_listing_document table"""
    
    company_codes = [1111, 1112]
    doc_statuses = ['NOT READY', 'READY', 'COMPLETE']
    sap_doc_types = ['DR', 'DZ', 'RV', 'DG', 'AB']
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    sql_statements = []
    sql_statements.append("-- Generated INSERT statements for t_listing_document")
    sql_statements.append("-- Total records: {}".format(num_records))
    sql_statements.append("")
    
    for i in range(1, num_records + 1):
        posting_date = generate_random_date(start_date, end_date)
        assignment_date = posting_date + timedelta(days=random.randint(1, 30))
        
        company_code = random.choice(company_codes)
        fiscal_year = posting_date.year
        
        # Generate data
        no_kwitansi_dn = f"DN{random.randint(100000, 999999)}"
        customer_payer_id = f"CUST{random.randint(1000, 9999)}"
        customer_payer = fake.company()
        sap_document_type = random.choice(sap_doc_types)
        sap_doc_number = f"{random.randint(1000000000, 9999999999)}"
        no_kwitansi_customer = f"KW{random.randint(100000, 999999)}"
        faktur_pajak = f"FP{random.randint(100000000, 999999999)}"
        amount = random.randint(1000000, 100000000)
        doc_status = random.choice(doc_statuses)
        total_amount = amount + random.randint(0, 5000000)
        collector_name = fake.name()
        collector_email = fake.email()
        created_by = fake.user_name()
        updated_by = created_by
        sales_organization_id = f"SO{random.randint(1000, 9999)}"
        no_bukti_potong = f"BP{random.randint(100000, 999999)}" if random.choice([True, False]) else None
        
        # Build INSERT statement
        insert_sql = f"""INSERT INTO t_listing_document 
(posting_date, no_kwitansi_dn, customer_payer_id, customer_payer, sap_document_type, 
company_code, fiscal_year, sap_doc_number, no_kwitansi_customer, faktur_pajak, 
amount, doc_status, total_amount, collector_name, collector_email, assignment_date, 
created_by, updated_by, sales_organization_id, no_bukti_potong)
VALUES 
('{posting_date.strftime('%Y-%m-%d')}', '{no_kwitansi_dn}', '{customer_payer_id}', '{customer_payer.replace("'", "''")}', 
'{sap_document_type}', {company_code}, {fiscal_year}, '{sap_doc_number}', '{no_kwitansi_customer}', 
'{faktur_pajak}', {amount}, '{doc_status}', {total_amount}, '{collector_name.replace("'", "''")}', 
'{collector_email}', '{assignment_date.strftime('%Y-%m-%d')}', '{created_by}', '{updated_by}', 
'{sales_organization_id}', {'NULL' if no_bukti_potong is None else f"'{no_bukti_potong}'"});"""
        
        sql_statements.append(insert_sql)
    
    return '\n'.join(sql_statements)

def save_to_file(sql_content, filename='insert_listing_document.sql'):
    """Save SQL statements to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    print(f"SQL file generated successfully: {filename}")

if __name__ == "__main__":
    # Set jumlah record yang ingin di-generate
    num_records = int(input("Masukkan jumlah data yang ingin di-generate: "))
    
    print(f"Generating {num_records} records...")
    sql_content = generate_insert_statements(num_records)
    
    # Save to file
    save_to_file(sql_content)
    
    print(f"Total {num_records} INSERT statements generated!")