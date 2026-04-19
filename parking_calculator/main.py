from pathlib import Path
from datetime import datetime
import math

def parsing(arrival, departure):
    format_string = "%Y-%m-%d %H:%M:%S"
    d1 = datetime.strptime(arrival, format_string)
    d2 = datetime.strptime(departure, format_string)
    if d1 > d2:
        return
    
    diff = d2-d1
    return diff.total_seconds() / 60

def FeeCalculation(period):
    fee = 0
    if period <= 30:
        return 0
    
    days = period // 1440
    restMinutes = period % 1440
    fee += days * 10000
    if restMinutes >= 30:
        restMinutes -= 30
    else:
        return int(round(fee))
    
    if restMinutes > 180:
        restMinutes -= 180
        fee += math.ceil(180 / 60) * 300 
        fee += math.ceil(restMinutes/60) * 500
    else:
        fee += math.ceil(restMinutes/60) * 300  
        
    return int(round(fee))

def main():
    file_path = Path("input.txt")
    
    if not file_path.exists():
        print("Hiba: Az input.txt fájl nem található!")
        return
    
    content = file_path.read_text(encoding="utf-8").splitlines()
    data_lines = content[2:]
    results = []
    print(f"Rendszam \t DIJ")
    for line in data_lines:
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
            results.append(f"{license_plate}: {fee} Ft")
            print(f"{license_plate} \t {fee}")
        else:
            results.append(f"{license_plate}: HIBA (Időrend)")
    
    Path("parking_results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nAz eredmények elmentve a parking_results.txt fájlba.")

if __name__ == "__main__":
    main()