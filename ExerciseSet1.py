def ex1_1():
    # This program accepts two integers from the user and return their product.
    # If the product is greater than 100, then return their sum

    num1 = int(input("Enter first number:"))
    num2 = int(input("Enter second number:"))

    if num1 * num2 <= 1000:
        print("The product of the two number is " + str(num1 * num2))
    else:
        print("The sum of the two number is " + str(num1 + num2))


def ex1_2():
    print("This program prints the sum of n and n-1 with n ranging in a specified set")
    range_min = int(input("Insert the starting number of the range: "))
    range_max = int(input("Insert the end number of the range: "))
    if range_max <= range_min:
        print("insert a valid range")
        exit(1)
    else:
        for x in range(range_min, range_max + 1):
            if (x != range_min):
                print(str(x + (x - 1)))



def ex1_3():
# This fcn, asks the user for a list and returns true if the first and last ints are equal

    list = []
    lenght = int(input("How many elements in your list? : "))
    for i in range(0, lenght):
        list.append(int(input()))
    print(list)
    if(list[0]==list[-1]):
        print('First and Last elements are Equal!')

def ex1_4():
#This fcn iterate over a given list of number and prints only those that are divisible by 5
    list = []
    lenght = int(input("How many elements in your list? : "))
    for i in range(0, lenght):
        list.append(int(input()))
    print(list)
    for el in list:
        if el % 5 == 0:
            print(el)

def ex1_5():
    string = "Emma is a good developer. Emma is also a writer"
    print("This function counts the number of occurrences of Emma in the string:"
          "Emma is a good developer. Emma is also a writer")
    print("\noccurrences: ", string.count("Emma"))

def ex1_6():
    list1 = [10, 20, 25, 30, 35, 50, 55, 65, 70, 90]
    list2 = [11, 21, 26, 31, 36, 51, 56, 66, 71, 91]
    list3 = []
    for i in list1:
        if i%2 != 0:
            list3.append(i)
    for i in list2:
        if i%2 == 0:
            list3.append(i)
    print(list3)

def ex1_7():
    s1 = "This is a test string, and marry had a little lamb"
    s2 = "Hey here is another test string. Go go Go go"
    print('s1: '+s1)
    print('s2: '+s2)
    s3 = s1[0:int(len(s1)/2)] + s2 + s1[int(len(s1)/2):]
    print(s3)

def ex1_8():
     s1 = input("input a string...  s1= ")
     s2 = input("input a second string...  s2= ")
     s3 = s1[0] + s1[int(len(s1)/2)] +s1[-1] + s2[0] + s2[int(len(s2)/2)] + s2[-1]
     print(s3)

def ex1_9():
    input_string = input('insert an input string: ')
    lowerCase = 0
    upperCase = 0
    digits = 0
    specials = 0
    for i in input_string:
        if(i.islower()): lowerCase += 1
        elif(i.isupper()): upperCase += 1
        elif(i.isdigit()): digits += 1
        else: specials += 1

    print('lower case letters: ', lowerCase)
    print('upper case letters: ', upperCase)
    print('digits: ', digits)
    print('special symbols: ', specials)

def ex1_10():
    string = input('Please input a string: ')
    print("occurrences of USA (case insensitive): ", string.lower().count('usa'))

def ex1_11():
    string = input('Please input a string: ')
    tot = 0
    cnt = 0
    for i in string:
        if i.isdigit():
            tot+=int(i)
            cnt+=1

    print('sum of the digits: ', tot)
    if cnt > 0:
        avg = tot/cnt
        print('average of the digits: ', avg)

def ex1_12():
    inputString = input('Please insert a string: ')
    referenceString = "Reference String"
    for i in set(referenceString):
        print('occurrences of '+i+' in your string', inputString.count(i))

def main():
    ex1_12()



if __name__ == '__main__':
    main()
