from __future__ import annotations
import math
from abc import ABC, abstractmethod
from amenity import Amenity
from typing import Tuple, List, Union


class Property(ABC):
    def __init__(
        self,
        prop_id: str,
        bedrooms: int,
        bathrooms: int,
        parking_spaces: int,
        full_address: str,
        floor_area: int,
        price: int,
        property_features: List[str],
        coordinates: Tuple[float, float],
    ):
        self.prop_id = prop_id
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.full_address = full_address
        self.floor_area = floor_area
        self.price = price
        self.property_features = property_features
        self.coordinates = coordinates

    def get_prop_id(self) -> str:
        return self.prop_id

    def get_full_address(self) -> str:
        return self.full_address

    def get_suburb(self) -> str:
        splitted_address = self.get_full_address().split()
        return splitted_address[-3]

    @abstractmethod
    def get_prop_type(self) -> str:
        pass

    def set_bedrooms(self, bedrooms: int) -> None:
        if bedrooms >= 1:
            self.bedrooms = bedrooms
        else:
            raise ValueError

    def get_bedrooms(self) -> int:
        return self.bedrooms

    def set_bathrooms(self, bathrooms: int) -> None:
        if bathrooms >= 1:
            self.bathrooms = bathrooms
        else:
            raise ValueError

    def get_bathrooms(self) -> int:
        return self.bathrooms

    def set_parking_spaces(self, parking_spaces: int) -> None:
        if parking_spaces >= 0:
            self.parking_spaces = parking_spaces
        else:
            raise ValueError

    def get_parking_spaces(self) -> int:
        return self.parking_spaces

    def get_coordinates(self) -> Tuple[float, float]:
        return self.coordinates

    @abstractmethod
    def set_floor_number(self, floor_number: int) -> None:
        pass

    @abstractmethod
    def get_floor_number(self) -> Union[int, None]:
        pass

    @abstractmethod
    def set_land_area(self, land_area: int) -> None:
        pass

    @abstractmethod
    def get_land_area(self) -> Union[int, None]:
        pass

    def set_floor_area(self, floor_area: int) -> None:
        if floor_area >= 0:
            self.floor_area = floor_area
        else:
            raise ValueError

    def get_floor_area(self) -> int:
        return self.floor_area

    def set_price(self, price: int) -> None:
        if price >= 0:
            self.price = price
        else:
            raise ValueError

    def get_price(self) -> int:
        return self.price

    def set_property_features(self, property_features: List[str]) -> None:
        if type(property_features) == list:
            self.property_features = property_features
        else:
            raise TypeError

    def get_property_features(self) -> List[str]:
        return self.property_features

    def add_feature(self, feature: str) -> None:
        curr_prop_features = self.get_property_features()
        if feature not in curr_prop_features:
            curr_prop_features.append(feature)
            self.set_property_features(curr_prop_features)

    def remove_feature(self, feature: str) -> None:
        curr_prop_features = self.get_property_features()
        if curr_prop_features.count(feature):
            curr_prop_features.remove(feature)
            self.set_property_features(curr_prop_features)

    def search_by_id(self, property_id: str) -> Union[Property, None]:
        """Searches for a property using property_id

        Args:
            property_id (str): An id uniquely identifying a property

        Returns:
            Union[Property, None]: A property that has the matched id, if not found returns None
        """
        instance = None
        for instance in Property.instances:
            if instance.get_prop_id() == property_id:
                result = instance
        return result

    def nearest_amenity(
        self, amenities: List[Amenity], amenity_type: str, amenity_subtype: str = None
    ) -> Tuple[Amenity, float]:
        """Finds a closest amenity to the property and the distance to this particular Amenity

        Args:
            amenities (List[Amenity]): List of amenities to be searched
            amenity_type (str): Type of amenity to be searched
            amenity_subtype (str, optional): Subtype of amenity to be searched. Defaults to None.

        Returns:
            Tuple[Amenity, float]: The closest amenity and the distance to this Amenity
        """
        prop_lat, prop_lon = self.get_coordinates()
        distances = {}

        # filter unrelated amenities
        for amenity in amenities:
            if amenity.get_amenity_type() != amenity_type:
                continue
            if amenity_subtype != None:
                if amenity.get_amenity_subtype() != amenity_subtype:
                    if amenity.get_amenity_subtype() != "Pri/Sec":
                        continue

            # find distance
            amen_lat, amen_lon = amenity.get_amenity_coords()
            distance = self.haversine_distance(prop_lat, prop_lon, amen_lat, amen_lon)
            distances[amenity.get_amenity_code()] = distance

        nearest_amen_code = None
        nearest_amen = None
        min_dist = None
        if distances:
            # find the nearest amenity code
            min_dist = min(list(distances.values()))
            for amen_code, distance in distances.items():
                if distance == min_dist:
                    nearest_amen_code = amen_code

            # find the nearest amenity
            nearest_amen = Amenity.search_by_code(nearest_amen_code)

        return nearest_amen, min_dist

    def haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        radius_of_earth = 6371  # Radius of the earth in kilometers.
        distance = radius_of_earth * c

        return distance


if __name__ == "__main__":
    pass
