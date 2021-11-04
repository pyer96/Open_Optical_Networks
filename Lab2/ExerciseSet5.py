import json

import pandas as pd
import matplotlib.pyplot as plt
import json as jsn


def ex1():
    #write a python program to convert JSON data to Python objects
    json_obj = '{"Name": "David", "Class": "I", "Age": 6}'
    data = jsn.loads(json_obj)
    print('\nJSON data:')
    print(data)
    print('\nName: ', data['Name'])
    print('Class ', data['Class'])
    print('Age ', data['Age'])

def ex2():
    # Write a Python program to convert Python objects to JSON data
    python_obj = {
    'name': 'David',
    'class': 'I',
    'age': 6
    }
    print(type(python_obj))
    json = jsn.dumps(python_obj)
    print('\nJSON string: ',json)


def ex3():
    # write a python program to convert python objects into JSON strings
    python_dict = {
        'name': 'David',
        'class': 'I',
        'age': 6
    }
    python_list = ['Red', 'Green', 'Black']
    python_string = 'Python Json'
    python_int = 1234
    python_float = 21.34
    python_t = True
    python_f = False
    python_n = None
    json_dict = json.dumps(python_dict)
    json_list = json.dumps(python_list)
    json_str = json.dumps(python_string)
    json_num1 = json.dumps(python_int)
    json_num2 = json.dumps(python_float)
    json_t = json.dumps(python_t)
    json_f = json.dumps(python_f)
    json_n = json.dumps(python_n)
    print('json dict:', json_dict)
    print('json list:', json_list)
    print('json string:', json_str)
    print('json number1:', json_num1)
    print('json number2:', json_num2)
    print('json true:', json_t)
    print('json false:', json_f)
    print('json null:', json_n)


def ex4():
    # write a python program to convert python dictionary objects  (sort by key) to json data.
    # print the objects members with indent level 4
    j_string = { '4': 5, '6':7, '1':3, '2':4}
    print('Original String: ', j_string)
    print('\nJson data: ')
    print(json.dumps(j_string, sort_keys=True, indent=4))

def ex5():
    # write a python program to create a new JSON file from an existing JSON file and also remove a key from each element
    with open('/home/pier/Open_Optical_Networks/Lab2/states.json') as f:
        state_data = json.load(f)
        print('Original JSON keys: ',
              [state.keys()  for state in state_data['states']][0])
        for state in state_data['states']:
            del state['area_codes']
        print('\nModified JSON keys: ', [state.keys() for state in state_data['states']][0])

    with open('/home/pier/Open_Optical_Networks/Lab2/new_states.json', 'w') as f:
        json.dump(state_data, f , indent=2)

    with open('/home/pier/Open_Optical_Networks/Lab2/new_states.json') as f:
        state_data = json.load(f)
    print('\nReloaded JSON keys: ', [state.keys() for state in state_data['states']][0])

def main():
    ex5()


if __name__ == '__main__':
    main()