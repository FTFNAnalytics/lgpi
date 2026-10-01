#!/usr/bin/env python3
"""Inspect Ontario's official 2023 FIR by-schedule ZIP files."""

from __future__ import annotations

import csv
import io
import re
import urllib.request
import zipfile

from openpyxl import load_workbook

BASE = "https://efis.fma.csc.gov.on.ca/fir/wp-content/uploads/fir-files/open-data/by-schedule-and-year/2019-on"
SCHEDULES = ["02","10","12","26","40","42","51","70","74","80"]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent":"LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()


def decode(data: bytes) -> str:
    for encoding in ("utf-8-sig","cp1252","latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="replace")


def main() -> None:
    for schedule in SCHEDULES:
        url=f"{BASE}/VIEWFIR2023-{schedule}.zip"
        payload=fetch(url)
        print(f"\n=== SCHEDULE {schedule} bytes={len(payload)} url={url} ===")
        with zipfile.ZipFile(io.BytesIO(payload)) as zf:
            print("members=", zf.namelist())
            for name in zf.namelist():
                if name.endswith("/"):
                    continue
                data=zf.read(name)
                print(f"-- MEMBER {name} bytes={len(data)}")
                low=name.lower()
                if low.endswith((".csv",".txt",".dat")):
                    text=decode(data)
                    lines=text.splitlines()
                    for i,line in enumerate(lines[:12],start=1):
                        print(f"LINE {i}: {line[:1200]}")
                elif low.endswith(".xlsx"):
                    workbook=load_workbook(io.BytesIO(data), read_only=True, data_only=True)
                    print(f"xlsx_sheets={workbook.sheetnames}")
                    for sheet_name in workbook.sheetnames[:3]:
                        ws=workbook[sheet_name]
                        print(f"XLSX SHEET {sheet_name!r} rows={ws.max_row} cols={ws.max_column}")
                        for row_number,row in enumerate(ws.iter_rows(values_only=True),start=1):
                            values=[str(value)[:220] if value is not None else None for value in row[:24]]
                            if any(value not in (None,"") for value in values):
                                print(f"XROW {row_number}: {values}")
                            if row_number >= 12:
                                break
                else:
                    print(f"binary_prefix={data[:40]!r}")


if __name__=="__main__":
    main()
