def min_num_of_drops(n, h):
    dp = [0] * (n + 1)
    m = 0
    while dp[n] < h:
        m += 1
        for i in range(n, 0, -1):
            dp[i] = dp[i] + dp[i-1] + 1
    return m
""""
print(min_num_of_drops(1, 100))
print(min_num_of_drops(2, 100))
print(min_num_of_drops(3, 100))
print(min_num_of_drops(4, 100))
print(min_num_of_drops(1, 1))
print(min_num_of_drops(2, 456))
print(min_num_of_drops(3, 456))

print(min_num_of_drops(2, 789))
print(min_num_of_drops(3, 789))
"""

print(min_num_of_drops(4, 456))
print(min_num_of_drops(4, 789))
