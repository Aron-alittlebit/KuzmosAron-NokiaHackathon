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

print(next_magic_num(808))  
print(next_magic_num(2133))  
print(next_magic_num(1000))   
print(next_magic_num(123))   