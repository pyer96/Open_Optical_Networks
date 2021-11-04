import pandas as pd
import matplotlib.pyplot as plt
import json as jsn


def ex1():
    json_obj = '{"Name ": " David", "Class ": "I", "Age": 6}'
    data = jsn.loads(json_obj)
    print(data)

def ex2():
    python_obj = {
    'name': 'David',
    'class': 'I',
    'age': 6
    }
    json = jsn.dumps(python_obj)
    print(json)



def main():
    ex2()


if __name__ == '__main__':
    main()