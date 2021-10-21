# This program accepts two integers from the user and return their product.
# If the product is greater than 100, then return their sum

num1 = int(input("Enter first number:"))
num2 = int(input("Enter second number:"))

if num1*num2 <= 1000:
    print("The product of the two number is "+ str(num1*num2))
else:
    print("The sum of the two number is "+ str(num1 + num2))
