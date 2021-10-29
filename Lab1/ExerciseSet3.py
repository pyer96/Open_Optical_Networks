import numpy as np

def ex1():
    arr  = np.array(([1,2], [3,4], [5,6], [7,8]))
    print(arr)
    print('array shape: ', arr.shape)
    print('array dtype: ', arr.dtype)
    print('array size: ', arr.size)
    print('array base: ', arr.base)

def ex2():
    arr = np.array([[10, 120, 130, 140, 150], [160 , 170 , 180, 190, 200]])
    print(arr)

def ex3():
    arr = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
    print(arr[:,2])

def ex4():
    arr = np.array([[3, 6, 9, 12], [15, 18, 21, 24], [27, 30, 33, 36], [39, 42, 45, 48], [51, 54, 57, 60]])
    arr2 = np.zeros([int(arr.shape[0]/2) , int(arr.shape[1]/2)], int)
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if i % 2 != 0 & j % 2 != 0:
                arr2[i][j] = arr[i][j]

    print(arr2)






def main():
    ex4()


if __name__ == '__main__':
    main()
