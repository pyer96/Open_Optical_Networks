

def ex1():
    listOne = [3, 6, 9, 12, 15, 18, 21]
    listTwo = [4, 8, 12, 16, 20, 24, 28]
    list3 = []
    for i in range(0, max(len(listTwo), len(listOne))):
        if i % 2 != 0:
            list3.append(listOne[i])
        else:
            list3.append(listTwo[i])
    print(list3)

def ex2():
    string = input('enter a list of numbers separated by space: ')
    lst = list(string.split())
    tmp = list[4]
    list1  = lst[:1] + list(lst[4])  + lst[2:] + list(lst[4])
    print(list1)

def ex3():
    sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
    sub1 = sampleList[:int(len(sampleList)/3)]
    sub2 = sampleList[int(len(sampleList)/3):2*int(len(sampleList)/3)]
    sub3 = sampleList[2*int(len(sampleList)/3):]

    print(sub1[::-1])
    print(sub2[::-1])
    print(sub3[::-1])



def ex4():
    sampleList = [11, 45, 8, 11, 23, 45, 23, 45, 89]
    dictionary = dict()
    for el in sampleList:
        dictionary[el] = sampleList.count(el)
    print(dictionary)

def ex5():
    firstList = [2, 3, 4, 5, 6, 7, 8]
    secondList = [4, 9, 16, 25, 36, 49, 64]
    final = set(firstList+secondList)
    print(final)

def ex6():
    firstSet = {23, 42, 65, 57, 78, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}
    intersection = firstSet.intersection(secondSet)
    for i in intersection:
        firstSet.remove(i)
    print(firstSet)

def ex7():
    firstSet = {57, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}
    if firstSet.issubset(secondSet):
        [secondSet.remove(x) for x in firstSet]
    print(secondSet)

def ex8():
    rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
    sampleDict = {'Jhon':47, 'Emma':69, 'Kelly':76, 'Jason':97}
    for el in rollNumber:
        cnt = 0
        for val in sampleDict.values():
            if val == el:
                cnt += 1
        if cnt == 0:
            rollNumber.remove(el)
    print(rollNumber)

def ex9():
    speed = {'Jan':47, 'Feb':52, 'March':47, 'April':44, 'May':52,
    'June':53, 'July':54, 'Aug':44, 'Sept':54}
    l = []
    for val in speed.values():
        if l.count(val)==0:
            l.append(val)
    print(l)

def ex10():
    sampleList = [87, 52, 44, 53, 54, 87, 52, 53]
    sampleList = list(dict.fromkeys(sampleList))
    print(sampleList)



def main():
     ex10()



if __name__ == '__main__':
    main()
