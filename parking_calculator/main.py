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
        return fee
    
    if restMinutes > 180:
        restMinutes -= 180
        fee += 180 * 5
        fee += math.ceil(restMinutes/60) * 500
    else:
        fee += restMinutes * 5   
        
    return int(round(fee))

def main():
    file_path = Path("input.txt")
    
    if not file_path.exists():
        print("Hiba: Az input.txt fájl nem található!")
        return

    
    content = file_path.read_text(encoding="utf-8").splitlines()
    data_lines = content[2:]

    results = []

    for line in data_lines:
        if not line.strip():
            continue
            
        
        parts = line.split()
        
        if len(parts) == 5:
            licencePlate = parts[0]
            arrival = f"{parts[1]} {parts[2]}"
            departure = f"{parts[3]} {parts[4]}"
            
            
            minutes = parsing(arrival, departure)
            
            if minutes is not None:
                
                fee = FeeCalculation(minutes)
                results.append(f"{licencePlate}: {fee} Ft")
                print(f"{licencePlate} -> {minutes:.1f} perc -> {fee} Ft")
            else:
                results.append(f"{licencePlate}: HIBA (Időrend)")

    
    Path("parking_results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nAz eredmények elmentve a parking_results.txt fájlba.")

if __name__ == "__main__":
    main()