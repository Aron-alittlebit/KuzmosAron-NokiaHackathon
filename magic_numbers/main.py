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
    
    result_val = modifyString(numberLength, digits)
    
    if result_val <= number:
        left_part = "".join(digits[:middle])
        new_left = str(int(left_part) + 1)
        
        if numberLength % 2 == 0:
            new_magic = new_left + new_left[::-1]
        else:
            new_magic = new_left + new_left[:-1][::-1]
        return int(new_magic)
    
    return result_val

def modifyString(numberLength, digits_list) -> int:
    
    temp_digits = list(digits_list)
    right_idx = (numberLength + 1) // 2
    
    for i in range(right_idx, numberLength):
        temp_digits[i] = temp_digits[numberLength - 1 - i]
    
    return int("".join(temp_digits))

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
    time_sum = 0
    for _ in range(2500):
        t0 = time.perf_counter_ns()
        main()
        t1 = time.perf_counter_ns()
        time_sum += t1 - t0
    
    time_avg = time_sum / 2500
    
    print(f"ran in {time_avg:.10f} ns")

