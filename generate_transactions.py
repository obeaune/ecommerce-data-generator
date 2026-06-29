import random
import string
from datetime import datetime, timedelta

# --- Configuration ---
NUM_TRANSACTIONS = 1000
PAYMENT_TYPES = ["01", "02", "03"]  # 01=debit, 02=credit, 03=pix
STATUSES = ["00", "01", "02"]       # 00=approved, 01=denied, 02=cancelled
CHARGEBACK_REASONS = ["01", "02", "03", "04"]  # 01=fraud, 02=not_recognized, 03=duplicate, 04=defective_product

# --- Helpers ---
def random_digits(n):
    return ''.join(random.choices(string.digits, k=n))

def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

def format_value(value):
    return str(int(value * 100)).zfill(12)

def generate_output_filename(file_type):
    date_str = datetime.now().strftime('%Y%m%d')
    return f"{file_type}_{date_str}.txt"

# --- Transactions file ---
def build_transaction_header(date):
    record_type = "00"
    file_id = random_digits(8)
    date_str = date.strftime("%Y%m%d")
    return f"{record_type}{file_id}{date_str}{'':60}\n"

def build_transaction_detail(date):
    record_type = "01"
    transaction_id = random_digits(16)
    merchant_id = random_digits(10)
    value = round(random.uniform(5.0, 5000.0), 2)
    datetime_str = date.strftime("%Y%m%d%H%M%S")
    payment_type = random.choice(PAYMENT_TYPES)
    installments = str(random.randint(1, 12)).zfill(2)
    status = random.choice(STATUSES)
    return f"{record_type}{transaction_id}{merchant_id}{format_value(value)}{datetime_str}{payment_type}{installments}{status}{'':15}\n"

def build_transaction_trailer(total_records, total_value):
    record_type = "99"
    return f"{record_type}{str(total_records).zfill(8)}{format_value(total_value)}{'':70}\n"

def generate_transactions():
    output_file = generate_output_filename("transactions")
    date = random_date()
    details = []
    total_value = 0.0

    for _ in range(NUM_TRANSACTIONS):
        record_date = random_date()
        detail = build_transaction_detail(record_date)
        details.append(detail)
        value = int(detail[27:39]) / 100
        total_value += value

    with open(output_file, "w") as f:
        f.write(build_transaction_header(date))
        for detail in details:
            f.write(detail)
        f.write(build_transaction_trailer(NUM_TRANSACTIONS, total_value))

    print(f"Transactions file generated: {output_file}")
    print(f"Total transactions: {NUM_TRANSACTIONS}")
    print(f"Total value: R$ {total_value:,.2f}")
    return details

# --- Settlement file ---
def build_settlement_header(date):
    record_type = "00"
    file_id = random_digits(8)
    date_str = date.strftime("%Y%m%d")
    return f"{record_type}{file_id}{date_str}SETTLEMENT{'':50}\n"

def build_settlement_detail(transaction_detail):
    record_type = "02"
    transaction_id = transaction_detail[2:18]
    merchant_id = transaction_detail[18:28]
    gross_value = int(transaction_detail[28:40])
    fee_rate = random.uniform(0.01, 0.05)
    fee = int(gross_value * fee_rate)
    net_value = gross_value - fee
    settlement_date = random_date()
    date_str = settlement_date.strftime("%Y%m%d")
    return f"{record_type}{transaction_id}{merchant_id}{str(gross_value).zfill(12)}{str(fee).zfill(10)}{str(net_value).zfill(12)}{date_str}{'':10}\n"

def build_settlement_trailer(total_records, total_net):
    record_type = "99"
    return f"{record_type}{str(total_records).zfill(8)}{str(int(total_net)).zfill(12)}{'':60}\n"

def generate_settlement(transaction_details):
    output_file = generate_output_filename("settlement")
    approved = [d for d in transaction_details if d[58:60] == "00"]
    total_net = 0

    with open(output_file, "w") as f:
        f.write(build_settlement_header(random_date()))
        for detail in approved:
            record = build_settlement_detail(detail)
            f.write(record)
            total_net += int(record[40:52])
        f.write(build_settlement_trailer(len(approved), total_net))

    print(f"Settlement file generated: {output_file}")
    print(f"Settled transactions: {len(approved)}")
    print(f"Total net value: R$ {total_net/100:,.2f}")

# --- Chargeback file ---
def build_chargeback_header(date):
    record_type = "00"
    file_id = random_digits(8)
    date_str = date.strftime("%Y%m%d")
    return f"{record_type}{file_id}{date_str}CHARGEBACK{'':50}\n"

def build_chargeback_detail(transaction_detail):
    record_type = "03"
    transaction_id = transaction_detail[2:18]
    merchant_id = transaction_detail[18:28]
    value = transaction_detail[28:40]
    reason = random.choice(CHARGEBACK_REASONS)
    chargeback_date = random_date()
    date_str = chargeback_date.strftime("%Y%m%d")
    protocol = random_digits(12)
    return f"{record_type}{transaction_id}{merchant_id}{value}{reason}{date_str}{protocol}{'':10}\n"

def build_chargeback_trailer(total_records, total_value):
    record_type = "99"
    return f"{record_type}{str(total_records).zfill(8)}{str(int(total_value)).zfill(12)}{'':60}\n"

def generate_chargebacks(transaction_details):
    output_file = generate_output_filename("chargeback")
    num_chargebacks = int(NUM_TRANSACTIONS * 0.02)
    chargeback_transactions = random.sample(transaction_details, num_chargebacks)
    total_value = 0

    with open(output_file, "w") as f:
        f.write(build_chargeback_header(random_date()))
        for detail in chargeback_transactions:
            record = build_chargeback_detail(detail)
            f.write(record)
            total_value += int(detail[28:40])
        f.write(build_chargeback_trailer(num_chargebacks, total_value))

    print(f"Chargeback file generated: {output_file}")
    print(f"Total chargebacks: {num_chargebacks} (2% of transactions)")
    print(f"Total chargeback value: R$ {total_value/100:,.2f}")

# --- Main ---
if __name__ == "__main__":
    print("=== Ecommerce Data Generator ===\n")
    transaction_details = generate_transactions()
    print()
    generate_settlement(transaction_details)
    print()
    generate_chargebacks(transaction_details)
    print("\n=== All files generated successfully! ===")