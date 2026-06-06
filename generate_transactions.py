import random
import string
from datetime import datetime, timedelta

# --- Configuration ---
OUTPUT_FILE = f"transactions_{datetime.now().strftime('%Y%m%d')}.txt"
NUM_TRANSACTIONS = 1000

PAYMENT_TYPES = ["01", "02", "03"]  # 01=debit, 02=credit, 03=pix
STATUSES = ["00", "01", "02"]       # 00=approved, 01=denied, 02=cancelled

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

# --- Record builders ---
def build_header(date):
    record_type = "00"
    file_id = random_digits(8)
    date_str = date.strftime("%Y%m%d")
    return f"{record_type}{file_id}{date_str}{'':60}\n"

def build_detail(date):
    record_type = "01"
    transaction_id = random_digits(16)
    merchant_id = random_digits(10)
    value = round(random.uniform(5.0, 5000.0), 2)
    datetime_str = date.strftime("%Y%m%d%H%M%S")
    payment_type = random.choice(PAYMENT_TYPES)
    installments = str(random.randint(1, 12)).zfill(2)
    status = random.choice(STATUSES)
    return f"{record_type}{transaction_id}{merchant_id}{format_value(value)}{datetime_str}{payment_type}{installments}{status}{'':15}\n"

def build_trailer(total_records, total_value):
    record_type = "99"
    return f"{record_type}{str(total_records).zfill(8)}{format_value(total_value)}{'':70}\n"

# --- Main ---
def generate():
    date = random_date()
    details = []
    total_value = 0.0

    for _ in range(NUM_TRANSACTIONS):
        record_date = random_date()
        detail = build_detail(record_date)
        details.append(detail)
        value = int(detail[27:39]) / 100
        total_value += value

    with open(OUTPUT_FILE, "w") as f:
        f.write(build_header(date))
        for detail in details:
            f.write(detail)
        f.write(build_trailer(NUM_TRANSACTIONS, total_value))

    print(f"File generated: {OUTPUT_FILE}")
    print(f"Total transactions: {NUM_TRANSACTIONS}")
    print(f"Total value: R$ {total_value:,.2f}")

if __name__ == "__main__":
    generate()