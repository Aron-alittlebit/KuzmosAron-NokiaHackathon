from datetime import datetime

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
        fee += restMinutes * 500/60
    else:
        fee += restMinutes * 5   
        
    print(fee)

FeeCalculation(1800)
FeeCalculation(85.35)


