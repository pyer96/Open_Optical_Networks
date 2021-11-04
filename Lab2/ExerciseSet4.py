import pandas as pd
import matplotlib.pyplot as plt

def ex1():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    print(df)
    print(df['total_profit'])
    plt.plot(df['total_profit'])
    plt.ylabel('montly profit')
    plt.xlabel('months')
    plt.show()

def ex2():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    plt.plot(df['total_profit'], label = 'Profit data of last year', color = 'r', marker = 'o', markerfacecolor = 'k', linestyle = '-', linewidth = 3)
    plt.legend()
    plt.show()


def ex3():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    months = df['month_number'].values
    face_cream_sales_data = df['facecream'].values
    face_wash_sales_data = df['facewash'].values
    tooth_paste_sales_data = df['toothpaste'].values
    bathing_soap_sales_data = df['bathingsoap'].values
    shampoo_sales_data = df['shampoo'].values
    moisturizer_sales_data = df['moisturizer'].values
    plt.figure()
    plt.plot(months, face_cream_sales_data,
             label= 'Face cream Sales Data', marker ='o', linewidth = 3)
    plt.plot(months, face_wash_sales_data, label='Face wash Sales Data', marker ='o', linewidth = 3)
    plt.plot(months, tooth_paste_sales_data, label='ToothPaste Sales Data', marker ='o', linewidth = 3)
    plt.plot(months, bathing_soap_sales_data, label='Bathing Soap Sales Data', marker ='o', linewidth = 3)
    plt.plot(months, shampoo_sales_data, label='Shampoo Sales Data', marker ='o', linewidth = 3)
    plt.plot(months, moisturizer_sales_data, label='Moisturizer Sales Data', marker ='o', linewidth = 3)
    plt.xlabel('Month Number ')
    plt.ylabel('Sales units in number')
    plt.legend(loc='upper left')
    plt.xticks(months)
    plt.yticks([1e3, 2e3, 4e3, 6e3, 8e3, 10e3, 12e3, 15e3, 18e3])
    plt.title('Sales data')
    plt.show()


def ex4():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    col = df['toothpaste']
    plt.scatter(range(len(col)), col )
    plt.show()

def ex5():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    bathing_soap_sales = df['bathingsoap']
    plt.bar(bathing_soap_sales.index, bathing_soap_sales)
    plt.xlabel('months')
    plt.ylabel('bathingsoap sales')
    plt.savefig('bathingsoap_sales')
    plt.show()

def ex6():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    tot_profit = df['total_profit']
    plt.hist(tot_profit)
    plt.show()


def ex7():
    df = pd.read_csv('/home/pier/Open_Optical_Networks/Lab2/sales_data.csv')
    facewash = df['facewash']
    bath = df['bathingsoap']
    fig, axs = plt.subplots(2)
    axs[0].plot(facewash)
    axs[1].plot(bath)
    plt.show()

def main():
    ex3()


if __name__ == '__main__':
    main()