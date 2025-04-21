import re


class RegexHandler:
    def __init__(self) -> None:
        pass

    def validate_email(self, str2check: str) -> bool:
        """Check of email in correct format"""
        pattern = r"^[a-zA-z.]+[@]{1}[a-z]+[.a-z]+$"
        result = re.findall(pattern, str2check) != list()
        return result

    def validate_phone(self, str2check: str) -> bool:
        """Check if phone in correct format"""
        pattern = r"^(\(61\)|61){1}(0){1}([0-9]){9}$"
        result = re.findall(pattern, str2check) != list()
        return result


def matcher(
    prop_fpath: str, contact_fpath: str, contact_types: list, is_required: bool
) -> str:
    """Generates the CSV-like string of the property details and their email/phone contacts

    Args:
        prop_fpath (str): File path of the properties
        contact_fpath (str): File path of the email/phone contacts
        contact_types (list): List fo contact types to be populated
        is_required (bool): A flag to indicate whether it is required to have at least one valid contact

    Returns:
        str: CSV-like string of the properties and their contact information
    """
    regex_handler = RegexHandler()
    props_infos, prop_headers = csv_to_dict(prop_fpath)
    contact_infos, _ = csv_to_dict(contact_fpath)

    # validate and transform contact info
    validations = []
    for prop in contact_infos:
        # check if the property exists or not
        prop_info_idx = find_by_id(props_infos, prop["prop_id"])
        if prop_info_idx != None:
            # do the validation
            is_valid_contact = False
            for contact_type in contact_types:
                match contact_type:
                    case "email":
                        is_valid_contact = regex_handler.validate_email(prop["email"])
                    case "phone":
                        is_valid_contact = regex_handler.validate_phone(prop["phone"])
                if is_valid_contact:
                    validations.append(
                        {
                            "prop_id": prop["prop_id"],
                            "contact_type": contact_type,
                            "value": prop[contact_type],
                            "is_valid": True,
                        }
                    )
                else:
                    validations.append(
                        {
                            "prop_id": prop["prop_id"],
                            "contact_type": contact_type,
                            "value": None,
                            "is_valid": False,
                        }
                    )

    # merge properties details and their contacts
    result_props = []
    for prop in props_infos:
        populated_prop = None
        atleast_one_valid = False
        # make the match between property details and their contacts
        for contact in validations:
            if prop["prop_id"] == contact["prop_id"]:
                if contact["is_valid"]:
                    atleast_one_valid = True
                # add contact info
                if populated_prop == None: # if one contact has been added
                    populated_prop = {
                        **prop,
                        contact["contact_type"]: contact["value"],
                    }
                else: # no contact has been added
                    populated_prop = {
                        **populated_prop,
                        contact["contact_type"]: contact["value"],
                    }

        # check if contact required
        # add to result output
        if is_required:
            if populated_prop and atleast_one_valid:
                result_props.append(populated_prop)
        elif populated_prop:
            result_props.append(populated_prop)

    result = dict_to_csv(prop_headers + contact_types, result_props)
    return result


def prop_email_matcher(prop_fpath: str, email_fpath: str) -> str:
    """Generates property information with matching email contact

    Args:
        prop_fpath (str): File path of the property information
        email_fpath (str): File path of the email file

    Returns:
        str: property information with email contact in csv format
    """
    return matcher(prop_fpath, email_fpath, ["email"], False)


def prop_phone_matcher(prop_fpath: str, phone_fpath: str) -> str:
    """Generates property information with matching phone contact

    Args:
        prop_fpath (str): File path of the property information
        phone_fpath (str): File path of the phone file

    Returns:
        str: property information with phone contact in csv format
    """
    return matcher(prop_fpath, phone_fpath, ["phone"], False)


def merge_prop_email_phone(prop_fpath: str, email_phone_fpath: str) -> str:
    """Generates property information with matching email/phone contact

    Args:
        prop_fpath (str): File path of the property information
        email_phone_fpath (str): File path of the email/phone file

    Returns:
        str: property information with email/phone contact in csv format
    """
    return matcher(prop_fpath, email_phone_fpath, ["email", "phone"], True)


def find_by_id(props: list, prop_id: str) -> int:
    """Finds and return the property using prop_id

    Args:
        props (list): List of property to be searched
        prop_id (str): prop_id of property being searched

    Returns:
        int: index of the matched property in the given list
    """
    prop_idx = None
    for i in range(len(props)):
        if props[i]["prop_id"] == prop_id:
            prop_idx = i
    return prop_idx


def csv_to_dict(file_name: str) -> tuple:
    """Converts csv file into python dictionary

    Args:
        file_name (str): Name of the csv file

    Returns:
        tuple: Dictionary of parsed csv file, and headers of the file
    """
    result = []

    with open(file_name, "r") as file:
        # read header
        line = file.readline()
        headers = [header.strip() for header in line.split(",")]

        # read body
        line = file.readline()
        while line:
            prop = {}
            values = line.split(",")
            for i in range(len(values)):
                prop[headers[i]] = values[i].strip()
            result.append(prop)

            line = file.readline()

    return result, headers


def dict_to_csv(headers: list, data: list) -> str:
    """Converts python dictionary into csv string format

    Args:
        headers (list): List of headers for the output csv string
        data (list): List of data dictionary to be output

    Returns:
        str: CSV-like string of the headers and data combined
    """
    result = None

    # header part
    header = ",".join(headers)
    if data:
        header += "\n"

    # body part
    body = []
    for i in range(len(data)):
        row = []
        for j in range(len(headers)):
            if data[i][headers[j]]:
                row.append(data[i][headers[j]])
            else:
                row.append("")
        row_str = ",".join(row)
        row_str += "\n"
        body.append(row_str)

    result = header + "".join(body)

    return result


if __name__ == "__main__":
    print("Task 1 results: ")
    print(
        prop_email_matcher("sample_properties.csv", "sample_properties_email_phone.csv")
    )
    print("=" * 50)
    print("Task 2 results: ")
    print(
        prop_phone_matcher("sample_properties.csv", "sample_properties_email_phone.csv")
    )
    print("=" * 50)
    print("Task 3 results: ")
    print(
        merge_prop_email_phone(
            "sample_properties.csv", "sample_properties_email_phone.csv"
        )
    )
