import time
from pathlib import Path

def next_magic_num(number):
    strNumber = str(number)
    numberLength = len(strNumber)

    if strNumber == '9' * numberLength:
        return number + 2
    
    if numberLength % 2 == 0:
        middle = numberLength // 2
    else:
        middle = (numberLength // 2) + 1
    
    digits = list(strNumber)

    for i in range(middle):
        digits[numberLength-1-i] = digits[i]
    
    mirrored = "".join(digits)
    
    if mirrored <= strNumber:
        left = str(int(strNumber[:middle])+1)
        if numberLength % 2 == 0:
            return int(left + left[::-1])
        else:
            return int(left + left[:-1][::-1])
    
    return int(mirrored)



def main():
    data = (Path(__file__).parent / "input.txt").read_text(encoding="utf-8")
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        if '^' in line:
            left_part, right_part = line.split('^')
            number = pow(int(left_part), int(right_part))
        else:
            number = int(line)       
        print(next_magic_num(number))   



if __name__ == "__main__":
    main()

