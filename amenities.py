from __future__ import annotations
from typing import Tuple, List, Union


class Amenity:
    # class variables
    instances = []

    def __init__(
        self,
        amenity_code: str,
        amenity_name: str,
        amenity_type: str,
        amenity_subtype: str,
        coordinates: Tuple[float, float],
    ):
        self.amenity_code = amenity_code
        self.amenity_name = amenity_name
        self.amenity_type = amenity_type
        self.amenity_subtype = amenity_subtype
        self.coordinates = coordinates

        Amenity.instances.append(self)

    def get_amenity_code(self) -> str:
        return self.amenity_code

    def set_amenity_name(self, amenity_name: str) -> None:
        if type(amenity_name) == str:
            self.amenity_name = amenity_name
        else:
            raise TypeError

    def get_amenity_name(self) -> str:
        return self.amenity_name

    def get_amenity_coords(self) -> Tuple[float, float]:
        return self.coordinates

    def get_amenity_type(self) -> str:
        return self.amenity_type

    def set_amenity_subtype(self, amenity_subtype: Union[str, None]) -> None:
        if type(amenity_subtype) == str:
            self.amenity_subtype = amenity_subtype
        else:
            raise TypeError

    def get_amenity_subtype(self) -> Union[str, None]:
        return self.amenity_subtype

    @classmethod
    def search_by_code(cls, amenity_code: str) -> Union[Amenity, None]:
        """Searches for an Amenity using the amenity_code

        Args:
            amenity_code (str): The code uniquely identifying an amenity

        Returns:
            Union[Amenity, None]: An amenity that has the matched code, if not found returns None
        """
        instance = None
        for instance in Amenity.instances:
            if instance.get_amenity_code() == amenity_code:
                result = instance
        return result


if __name__ == "__main__":
    a = Amenity("1001")
