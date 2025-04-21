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


def extract_information(property_string: str) -> dict:
    # Read the property string and create a dictionary of property's information
    delimeter = ','
    string_list = property_string.split(delimeter)
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
    property_dict['prop_type'] = prop_type(property_dict)
    property_dict['suburb'] = suburb(property_dict)
    property_dict['property_features'] = string_list[property_dict_definition['property_features'][0]].split(';')
    if property_dict['prop_type'] == 'apartment':
        property_dict['floor_number'] = property_dict_definition['floor_number'][1](string_list[property_dict_definition['floor_number'][0]])
    else:
        property_dict['land_area'] = property_dict_definition['land_area'][1](string_list[property_dict_definition['land_area'][0]])
    return property_dict

def prop_type(property_dict: dict) -> str:
    if '/' in property_dict.get('full_address'):
        prop_type = property_dict_definition['prop_type']('apartment')
    else:
        prop_type = property_dict_definition['prop_type']('house')
    return prop_type

def suburb(property_dict: dict) -> str:
    property_dict['suburb'] = property_dict.get("full_address").split()[-3]

def add_feature(property_dict: dict, feature: str) -> None:
    list_of_feature = property_dict.get('property_features')
    if feature not in list_of_feature:
        list_of_feature.append(feature)
    else:
        print("The feature is already in the list.")

def remove_feature(property_dict: dict, feature: str) -> None:
    list_of_feature = property_dict.get('property_features')
    if feature in list_of_feature:
        list_of_feature.remove(feature)
    else:
        print("The feature is not available to remove.")



def main():
    sample_string = "P10001,3 Antrim Place Langwarrin VIC 3910,4,2,2,-38.16655678,145.1838435,,608,257,870000,dishwasher;central heating"
    property_dict = extract_information(sample_string)
    print(f"The first property is at {property_dict['full_address']} and is valued at ${property_dict['price']}")

    sample_string_2 = "P10002,G01/7 Rugby Road Hughesdale VIC 3166,2,1,1,-37.89342337,145.0862616,1,,125,645000,dishwasher;air conditioning;balcony"
    property_dict_2 = extract_information(sample_string_2)
    
    print(f"The second property is in {property_dict_2['suburb']} and is located on floor {property_dict_2['floor_number']}")

    add_feature(property_dict, 'electric hot water')
    print(f"Property {property_dict['prop_id']} has the following features: {property_dict['property_features']}")

if __name__ == '__main__':
    main()