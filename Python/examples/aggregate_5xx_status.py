from pathlib import Path

errors = 0

with Path(__file__).resolve().with_name("app.log").open(encoding="utf-8") as file:
    for line in file:
        parts = line.split('"')
        if len(parts) >= 3:
            response = parts[2].split()
            if 500 <= int(response[0]) <= 599:
                errors += 1

print(errors)
