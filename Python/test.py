#!/usr/bin/env python3

from pathlib import Path

errors = 0

with (Path(__file__).resolve().parent / "examples" / "app.log").open(
    encoding="utf-8"
) as file:
    for line in file:
        parts = line.split('"')
        response = parts[2].split()
        status = int(response[0])
        if 500 <= status <= 599:
            errors += 1

print(errors)
