from pathlib import Path

def min_num_of_drops(n, k):
    if n == 1: return k
    
    levels = [0] * (n + 1)
    cnt = 0
    
    while levels[n] < k:
        cnt += 1
    
        for i in range(n, 0, -1):
            levels[i] = levels[i] + levels[i-1] + 1
            
    return cnt


def main():
    data = (Path(__file__).parent / "input.txt").read_text(encoding="utf-8")
    
    for line in data.splitlines():
        line = line.strip()
        
        if not line:
            continue

        parts = line.split(',')
        
        if len(parts) == 2:
            n = int(parts[0].strip())
            h = int(parts[1].strip())
            result = min_num_of_drops(n, h)
            print(result)
            
            


if __name__ == "__main__":
    main()
   

