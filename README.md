# Ecommerce Data Generator

Python script that generates synthetic positional flat files simulating financial transactions from a payment acquirer.

## About

The generated file follows a fixed-width positional format, commonly used in financial systems and payment acquirers. Each record type has a fixed structure:

| Record Type | Code | Description |
|-------------|------|-------------|
| Header      | 00   | File identification and date |
| Detail      | 01   | Transaction data |
| Trailer     | 99   | Totals and record count |

## Detail Record Layout

| Field          | Positions | Length | Description |
|----------------|-----------|--------|-------------|
| Record type    | 0-1       | 2      | Always "01" |
| Transaction ID | 2-17      | 16     | Unique transaction identifier |
| Merchant ID    | 18-27     | 10     | Merchant identifier |
| Value          | 28-39     | 12     | Amount in cents (e.g., 004990 = R$ 49,90) |
| DateTime       | 40-53     | 14     | Format: YYYYMMDDHHmmss |
| Payment type   | 54-55     | 2      | 01=debit, 02=credit, 03=pix |
| Installments   | 56-57     | 2      | Number of installments |
| Status         | 58-59     | 2      | 00=approved, 01=denied, 02=cancelled |

## Usage

```bash
python generate_transactions.py
```

## Output

Generates a file named `transactions_YYYYMMDD.txt` in the project root.

## Requirements

- Python 3.13+