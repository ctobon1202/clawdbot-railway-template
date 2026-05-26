#!/usr/bin/env python3
"""
sheets_write.py — Append una fila a una pestaña de Google Sheets.

Uso:
  python3 sheets_write.py --sheet-id <ID> --tab "<Pestaña>" --row "COL1=val1,COL2=val2,..."

Convierte el string --row en una fila respetando el orden de headers de la pestaña.

Env requerida:
  GOOGLE_SERVICE_ACCOUNT_JSON: JSON completo del service account.
"""
import argparse
import json
import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: faltan dependencias. pip install google-api-python-client google-auth", file=sys.stderr)
    sys.exit(2)


def parse_row(row_str):
    """Parse 'K1=V1,K2=V2' → dict. Soporta comas dentro del valor si están entre comillas."""
    out = {}
    # split simple por comas que NO estén dentro de comillas — enough para v1.
    import re
    parts = re.split(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", row_str)
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet-id", required=True)
    parser.add_argument("--tab", required=True)
    parser.add_argument("--row", required=True, help="K1=V1,K2=V2,...")
    args = parser.parse_args()

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON env var no está set", file=sys.stderr)
        sys.exit(1)

    info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    # 1. Leer primera fila (headers).
    header_range = f"'{args.tab}'!1:1"
    result = service.spreadsheets().values().get(
        spreadsheetId=args.sheet_id, range=header_range
    ).execute()
    headers = result.get("values", [[]])[0]

    # 2. Mapear --row contra headers.
    row_dict = parse_row(args.row)
    new_row = [row_dict.get(h, "") for h in headers]

    # 3. Append.
    append_range = f"'{args.tab}'!A:Z"
    service.spreadsheets().values().append(
        spreadsheetId=args.sheet_id,
        range=append_range,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [new_row]},
    ).execute()

    print(f"OK: appended {len(new_row)} cols to '{args.tab}'")


if __name__ == "__main__":
    main()
