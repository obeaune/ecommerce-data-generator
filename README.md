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

## Output

Generates three positional flat files in the project root:

| File | Description |
|------|-------------|
| `transactions_YYYYMMDD.txt` | Raw payment transactions |
| `settlement_YYYYMMDD.txt` | Settlement records for approved transactions, including fees and net values |
| `chargeback_YYYYMMDD.txt` | Chargeback records (2% of transactions) with reason codes |

## Record Layout

### Transactions (record type 01)

| Field          | Positions | Length | Description |
|----------------|-----------|--------|--------------|
| Record type    | 0-1       | 2      | Always "01" |
| Transaction ID | 2-17      | 16     | Unique transaction identifier |
| Merchant ID    | 18-27     | 10     | Merchant identifier |
| Value          | 28-39     | 12     | Amount in cents |
| DateTime       | 40-53     | 14     | Format: YYYYMMDDHHmmss |
| Payment type   | 54-55     | 2      | 01=debit, 02=credit, 03=pix |
| Installments   | 56-57     | 2      | Number of installments |
| Status         | 58-59     | 2      | 00=approved, 01=denied, 02=cancelled |

### Settlement (record type 02)

| Field          | Positions | Length | Description |
|----------------|-----------|--------|--------------|
| Record type    | 0-1       | 2      | Always "02" |
| Transaction ID | 2-17      | 16     | References original transaction |
| Merchant ID    | 18-27     | 10     | Merchant identifier |
| Gross value    | 28-39     | 12     | Original transaction value in cents |
| Fee            | 40-49     | 10     | Acquirer fee in cents |
| Net value      | 50-61     | 12     | Settled amount in cents |
| Settlement date| 62-69     | 8      | Format: YYYYMMDD |

### Chargeback (record type 03)

| Field          | Positions | Length | Description |
|----------------|-----------|--------|--------------|
| Record type    | 0-1       | 2      | Always "03" |
| Transaction ID | 2-17      | 16     | References original transaction |
| Merchant ID    | 18-27     | 10     | Merchant identifier |
| Value          | 28-39     | 12     | Disputed amount in cents |
| Reason code    | 40-41     | 2      | 01=fraud, 02=not_recognized, 03=duplicate, 04=defective_product |
| Chargeback date| 42-49     | 8      | Format: YYYYMMDD |
| Protocol       | 50-61     | 12     | Dispute protocol number |

## Usage

```bash
python generate_transactions.py
```

## Output

Generates a file named `transactions_YYYYMMDD.txt` in the project root.

## Requirements

- Python 3.13+