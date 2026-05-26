#!/usr/bin/env python3
"""
sheets_read.py — Lee una pestaña de un Google Sheet usando un service account.

Uso:
  python3 sheets_read.py --sheet-id <ID> --tab "<NombreDePestaña>" [--range "A1:Z100"]

Env requerida:
  GOOGLE_SERVICE_ACCOUNT_JSON: JSON completo del service account (string).

Output: CSV en stdout.
"""
import argparse
import csv
import io
import json
import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: faltan dependencias. Instalar con:", file=sys.stderr)
    print("  pip install google-api-python-client google-auth", file=sys.stderr)
    sys.exit(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet-id", required=True)
    parser.add_argument("--tab", required=True)
    parser.add_argument("--range", default=None, help="Ej. A1:Z200 (opcional)")
    args = parser.parse_args()

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON env var no está set", file=sys.stderr)
        sys.exit(1)

    try:
        info = json.loads(sa_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: GOOGLE_SERVICE_ACCOUNT_JSON no es JSON válido: {e}", file=sys.stderr)
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    range_ = f"'{args.tab}'"
    if args.range:
        range_ = f"'{args.tab}'!{args.range}"

    result = service.spreadsheets().values().get(
        spreadsheetId=args.sheet_id, range=range_
    ).execute()
    values = result.get("values", [])

    writer = csv.writer(sys.stdout)
    for row in values:
        writer.writerow(row)


if __name__ == "__main__":
    main()
