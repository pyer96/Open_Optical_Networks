# This program, given a range of numbers, iterates from the i-th number to the end
# and prints the sum of the current number and the previous number


print("This program prints the sum of n and n-1 with n ranging in a specified set")
range_min = int(input("Insert the starting number of the range: "))
range_max = int(input("Insert the end number of the range: "))
if range_max <= range_min:
    print("insert a valid range")
    exit(1)
else:
    for x in range(range_min, range_max+1):
        if (x != range_min):
            print(str(x+(x-1)))
