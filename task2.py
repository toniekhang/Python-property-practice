# DO NOT DELETE THIS LINE
import csv
from haversine import haversine_distance

def process_properties(file_name: str) -> dict:
    with open(file_name, "r") as source:
        property_list = source.readlines()
        properties = {}
        for row in range(1,len(property_list)):
            property_string = property_list[row].strip('\n').split(',')
            properties[property_string[0]] = extract_information(property_string)
    return properties 

def extract_information(string_list: list) -> dict:
    '''Read the property string and create a dictionary of property's attributes.'''
    #Define the order of property dictionary and data type of each piece of information:
    property_dict_definition ={
        'prop_id': [0, str],
        'full_address': [1, str],
        'bedrooms': [2, int],
        'bathrooms': [3, int],
        'parking_spaces': [4, int],
        'latitude': [5, float],
        'longitude': [6, float],
        'floor_number': [7, int],
        'land_area': [8, int],
        'floor_area': [9, int],
        'price': [10, int],
        'property_features': [11,list],
        'prop_type': str,
        'suburb': str
}
    # Looping to create the dictionary
    property_dict = {
        'prop_id': 0,
        'full_address': 0,
        'bedrooms': 0,
        'bathrooms': 0,
        'parking_spaces': 0,
        'latitude': 0,
        'longitude': 0,
        'floor_area': 0,
        'price': 0,
    }
    for k in property_dict.keys():
        property_dict[k] = property_dict_definition[k][1](string_list[property_dict_definition[k][0]])
    if '/' in property_dict.get('full_address'):
        property_dict['prop_type'] = property_dict_definition['prop_type']('apartment')
    else:
        property_dict['prop_type'] = property_dict_definition['prop_type']('house')
    property_dict['suburb'] = property_dict.get("full_address").split()[-3]
    property_dict['property_features'] = string_list[property_dict_definition['property_features'][0]].split(';')
    if property_dict['prop_type'] == 'apartment':
        property_dict['floor_number'] = property_dict_definition['floor_number'][1](string_list[property_dict_definition['floor_number'][0]])
    else:
        property_dict['land_area'] = property_dict_definition['land_area'][1](string_list[property_dict_definition['land_area'][0]])
    return property_dict


def process_stations(file_name: str) -> dict:
    '''Read the station information and put into dictionary'''
    stations = {}
    with open('train_stations.csv', 'r') as source:
        station_list = source.readlines()
        for row in range(1,len(station_list)):
            station_string = station_list[row].strip('\n').split(',')
            stations[station_string[0]] = extract_train_info(station_string)
    return stations
            
        
def extract_train_info(station_attribute: list) -> dict:
    '''Read the string of station information and put into dictionary of attributes.'''
    station_attribute_dict = {
        "stop_id": [0,str],
        "stop_name": [1,str],
        "stop_lat": [2, float],
        "stop_long": [3, float]
    }
    stop_dict = {
        "stop_id": 0,
        "stop_name": 0,
        "stop_lat": 0,
        "stop_long": 0
    }
    for k in stop_dict.keys():
        stop_dict[k] = station_attribute_dict[k][1](station_attribute[station_attribute_dict[k][0]])
    return stop_dict
    

def nearest_station(properties: dict, stations: dict, prop_id: str) -> str:
    prop_long = properties[prop_id]["longitude"]
    prop_lat = properties[prop_id]["latitude"]
    distances = {}
    for stop_id in stations.keys():
        stop_long = stations[stop_id]["stop_long"]
        stop_lat = stations[stop_id]["stop_lat"]
        distances[stop_id] = haversine_distance(prop_lat,prop_long,stop_lat,stop_long)
    nearest_distance = None
    nearest_station = None
    for k,v in distances.items(): 
        if nearest_distance == None:
            nearest_distance = v
        elif v <= nearest_distance:
            nearest_distance = v
            nearest_station = stations[k]["stop_name"]
    return nearest_station
        
     
        

def main():
    """
    #You need not touch this function, if your 
    #code is correct, this function will work as intended 
    """
    # Process the properties
    properties_file = 'sample_properties.csv'
    properties = process_properties(properties_file)

    # Process the train stations
    stations_file = 'train_stations.csv'
    stations = process_stations(stations_file)

    # Check the validity of stations
    sample_prop = 'P10001'
    print(f"The nearest station for property {sample_prop} is {nearest_station(properties, stations, sample_prop)}")
    


if __name__ == '__main__':
    main()