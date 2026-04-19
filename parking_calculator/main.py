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
    BASE_DIR = Path(__file__).resolve().parent
    data = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    
    with open(BASE_DIR / "output.txt", "w", encoding="utf-8") as f:
        f.write("License plate\tFee\n")
        print("License plate\tFee")
        
        for line in data.splitlines()[2:]:
            parts = line.split()

            license_plate = parts[0]
            start = parts[1] + " " + parts[2]
            end = parts[3] + " " + parts[4]
            
            fee = FeeCalculation(parsing(start, end))

            result = f"{license_plate}\t\t{fee}"

            print(result)
            f.write(result + "\n")

if __name__ == "__main__":
    main()