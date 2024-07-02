import pandas as pd
from collections import Counter

def get_data():
    try:
        # Lectura del Archivo
        data = pd.read_csv('./data/roomies.csv')
        # Extract Parsed Data 
        parsed_data = data.values
        return parsed_data
    except Exception as err:
        print(f"Error reading data: {err}")
        return None
    
    
def get_realtionship(user_id : int, roomies_quant : int):
    
    # print('User_id', user_id, 'Quantity', roomies_quant)
    
    try:
        result = get_data()
        
        #*  Extract useful data
        other_users_data =  []
        
        for row in result:
            if row[0] != user_id:
                other_users_data.append(row)
            else:
                user_data = row
        
        #* Get Tolerance Degree
        tolerance_degrees = {}
        user_data_cycle = user_data[3:]
        
        for other_data in other_users_data: 
            row_data = other_data[3:]
            total = 0.0   
            for i in range(len(row_data)):
                if not isinstance(row_data[i], str):
                    total = total + (user_data_cycle[i] * row_data[i])
                    # print(f'''
                    #     cicle '{i}'
                    #     total '{total}'
                    #     user_data_cycle '{user_data_cycle[i]}'
                    #     row_data '{row_data[i]}'
                    # ''')
                    
            tolerance_degrees[other_data[0]] = total

        #*  Get highest tolerances
        counter = Counter(tolerance_degrees)
        highest_n_values = counter.most_common(roomies_quant) 
        
        highest_values = {}
        for key, value in highest_n_values:
            highest_values[key] = value
        
        return highest_values
    
    except Exception as err:
        return err
    

def format_numpy_data(user_data):
    parsed_data =[]

    for data in user_data:
        parsed_data.append(data)
        
    return parsed_data
    
def format_to_graph(user_id : int, possible_roomies : dict):
    try:
        users_data = []
        result = get_data()
        
        for row in result:
            if row[0] == user_id:
                parsed_data =format_numpy_data(row)
                parsed_data.append("-- User --")
                users_data.append(parsed_data)
        
        for key, value in possible_roomies.items():
            for row in result:
                if key == row[0]:
                    parsed_data =format_numpy_data(row)
                    parsed_data.append(value)
                    users_data.append(parsed_data)
        
        return users_data
    
    except Exception as err:
        return err
    
    
# print(get_realtionship(1, 10))
# data : dict = {1: 633.0, 10: 623.0, 6: 581.5}
# print(format_to_graph(11, data))
# Perfect Match 1210