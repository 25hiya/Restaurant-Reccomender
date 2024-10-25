"""Computing the distance and getting the user answers on their prefrences"""
import math
from typing import Any, TextIO
import csv
from math import acos, sin, cos, radians
from recommender_data import Restaurant, WeightedGraph, User


def load_review_graph(rating_file: TextIO, user_data: TextIO, restaurant_data: TextIO, restaurant_cuisine: TextIO) -> (
        list)[Any]:
    """Return a graph of users' restaurants reviews"""

    review_graph = WeightedGraph()
    all_cuisines = add_cuisine(restaurant_cuisine)
    user_dictionary = {}
    reader1 = csv.reader(user_data)
    for row1 in reader1:
        user_dictionary[row1[0]] = User(row1[0], row1[1], row1[2], row1[3], row1[4], row1[5])

    restaurant_dictionary = {}
    reader2 = csv.reader(restaurant_data)
    for row2 in reader2:
        restaurant = Restaurant(row2[0], row2[1], row2[2])
        restaurant_dictionary[row2[0]] = restaurant
        if row2[0] in all_cuisines:
            restaurant.cuisine = all_cuisines[restaurant.restaurant_id]

    reader = csv.reader(rating_file)
    for row in reader:
        if row[0] not in review_graph.get_all_vertices('user'):
            review_graph.add_vertex(user_dictionary[row[0]], 'user')

        if row[1] not in review_graph.get_all_vertices('restaurant'):
            review_graph.add_vertex(restaurant_dictionary[row[1]], 'restaurant')

        review_graph.add_edge(user_dictionary[row[0]], restaurant_dictionary[row[1]], int(row[2]))

    return [review_graph, user_dictionary, restaurant_dictionary]


def get_distance(user_postal_code: str, geospatial_coordinates: TextIO, restaurants: dict) -> dict[str, str]:
    """Return the distance (in kilometeres) between the user and the restaurant.

    Preconditions:
    - user_postal_code in geospatial_coordinates
    - restaurants != {}
    """

    val = {}
    dict_geospatial = {}
    reader = csv.reader(geospatial_coordinates)
    for row in reader:
        dict_geospatial[row[0]] = (float(row[1]), float(row[2]))

    user_latitude, user_longitude = dict_geospatial[user_postal_code[:3]]
    for restaurant in restaurants:
        restaurant_latitude, restaurant_longitude = dict_geospatial[restaurants[restaurant].postal_code]
        distance = acos(
            (sin(radians(user_latitude)) * sin(radians(restaurant_latitude))
             + (cos(radians(user_latitude)) * cos(radians(restaurant_latitude))
                * cos(radians(restaurant_longitude - user_longitude))))) * 6371
        val[restaurants[restaurant].name] = f'{round(distance, 2)} km'

    return val


def add_cuisine(restaurant_cuisine: TextIO) -> dict[str, list[str]]:
    """Returns a dictionary with a list of cuisines for each restaurant."""

    cuisines = {}
    reader = csv.reader(restaurant_cuisine)
    for row in reader:
        if row[0] not in cuisines:
            cuisines[row[0]] = [row[1]]
        else:
            cuisines[row[0]].append(row[1])

    return cuisines


def get_user_answer(questions: list[str]) -> User:
    """Return a user instance based on the user's answers to the given questions.

    Preconditions:
    - questions == [
            "Are you a Smoker or Non-smoker?",
            "What is your drinking level? Choose from: non-drinker, casual drinker, heavy drinker",
            "What is your dress preference? Choose from: informal, smart-casual, formal",
            "What kind of ambience do you prefer? Choose from: solitary, friends, family",
            "What is your budget? Choose from: low, medium, high"
        ]
    """
    answers_so_far = []
    for question in questions:
        answer = input(question)
        answers_so_far.append(answer.lower())

    user = User("U2000", answers_so_far[0], answers_so_far[1], answers_so_far[2], answers_so_far[3], answers_so_far[4])

    return user


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['TextIO', 'csv', 'math', 'recommender_data'],  # the names (strs) of imported modules
        'allowed-io': ["get_user_answer"],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'disable': ['E1136', 'W0221']})
