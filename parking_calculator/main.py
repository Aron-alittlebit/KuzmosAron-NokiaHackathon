from pathlib import Path
from datetime import datetime
import math

def parsing(arrival, departure):
    format_string = "%Y-%m-%d %H:%M:%S"
    d1 = datetime.strptime(arrival, format_string)
    d2 = datetime.strptime(departure, format_string)
    if d1 > d2:
        return
    diff = d2 - d1
    return diff.total_seconds() / 60

def FeeCalculation(period):
    if period <= 30:
        return 0

    days = period // 1440
    restMinutes = period % 1440
    fee = days * 10000

    if restMinutes <= 30:
        return int(fee)

    restMinutes -= 30

    if restMinutes > 180:
        restMinutes -= 180
        rest_fee = 900 + math.ceil(restMinutes / 60) * 500
    else:
        rest_fee = math.ceil(restMinutes / 60) * 300

    fee += min(rest_fee, 10000)

    return int(fee)

def main():
    file_path = Path("input.txt")

    if not file_path.exists():
        print("Hiba: Az input.txt fájl nem található!")
        return

    print(f"Rendszam \t DIJ")

    with file_path.open(encoding="utf-8") as f, Path("parking_results.txt").open("w", encoding="utf-8") as out:
        next(f)
        next(f)
        for line in f:
            if not line.strip():
                continue
            parts = line.split("\t\t")
            if len(parts) != 3:
                print(f"invalid data: {line}")
                continue
            license_plate = parts[0].strip()
            arrival = parts[1].strip()
            departure = parts[2].strip()
            minutes = parsing(arrival, departure)
            if minutes is not None:
                fee = FeeCalculation(minutes)
                out.write(f"{license_plate}: {fee} Ft\n")
                print(f"{license_plate} \t {fee}")
                
            else:
                out.write(f"{license_plate}: HIBA (Időrend)\n")

if __name__ == "__main__":
    main()