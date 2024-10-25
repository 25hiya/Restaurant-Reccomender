"""User class and loading data"""

from __future__ import annotations
from typing import Any, Union
import networkx as nx


class User:
    """A User who is using or has used the program.

    Instance Attributes:
        - user_id: the unique id associated with the user
        - smoker: whether the user smokes or not
        - drink_level: drinking habit of the user
        - dress_preference: prefered dress attire of the user
        - ambience: the user's preferred company
        - budget: level of budget the user is willing to spend


    Representation Invariants:
        - self.user_id != ''
        - self.smoker in {'Non-smoker', 'Smoker'}
        - self.drink_level in {'non-drinker', 'casual drinker', 'heary drinker'}
        - self.dress_preference in {'formal', 'informal', 'smart casual'}
        - self.ambience in {'family', 'friends', 'solitary'}
        - self.budget in {'low', 'medium', 'high'}
        """
    user_id: str
    smoker: str
    drink_level: str
    dress_preference: str
    ambience: str
    budget: str

    def __init__(self, user_id: str, smoker: str, drink_level: str, dress_preference: str, ambience: str,
                 budget: str) -> None:
        """Initialize a new user.
        """

        self.user_id = user_id
        self.smoker = smoker
        self.drink_level = drink_level
        self.dress_preference = dress_preference
        self.ambience = ambience
        self.budget = budget

    def preference_lst(self) -> list[int]:
        """Return a list of the user's preferences into a list of scores for each preference.

        Preconditions:
        - self.kind == 'user'
        """
        lst = [self.smoker, self.drink_level, self.dress_preference, self.ambience, self.budget]

        if lst[0] == "Smoker":
            lst[0] = 1
        else:
            lst[0] = 0

        lst[1] = self.preference_list_helper()

        if lst[2] == 'informal':
            lst[2] = 0
        elif lst[2] == 'smart-casual':
            lst[2] = 1
        else:
            lst[2] = 2

        if lst[3] == 'solitary':
            lst[3] = 0
        elif lst[3] == 'friends':
            lst[3] = 1
        else:
            lst[3] = 2

        if lst[4] == 'low':
            lst[4] = 0
        elif lst[4] == 'medium':
            lst[4] = 1
        else:
            lst[4] = 2

        return lst

    def preference_list_helper(self) -> int:
        """
        Return the number associated with the drink level choice.
        """

        if self.drink_level == 'non-drinker':
            return 0
        elif self.drink_level == 'casual drinker':
            return 1
        else:
            return 2


class Restaurant:
    """A Restaurant reviewed in the program.

    Instance Attributes:
        - restaurant_id: the unique id associated with the restaurant
        - name: the restaurant's name
        - cuisine: the types of cuisines the restaurant serves
        - postal_code: restaurant's postal code

    Representation Invariants:
        - self.restaurant_id != ''
        - self.name != ''
        - self.cuisine != []
        - all({cuisine in {'Afghan', 'African', 'American', 'Armenian', 'Asian', 'Bagels', 'Bakery', 'Bar',
        'Bar_Pub_Brewery', 'Barbecue', 'Brazilian', 'Breakfast Brunch', 'Burgers', 'Cafe Coffee Shop', 'Cafeteria',
        'California', 'Caribbean', 'Chinese', 'Contemporary', 'Continental-European', 'Deli-Sandwiches',
        'Dessert-Ice Cream', 'Diner', 'Dutch-Belgian', 'Eastern-European', 'Ethiopian', 'Family', 'Fast Food',
        'Fine Dining', 'French' ,'Game' ,'German', 'Greek', 'Hot Dogs', 'International', 'Italian', 'Japanese',
        'Juice', 'Korean', 'Latin_American', 'Mediterranean', 'Mexican', 'Mongolian', 'Organic-Healthy', 'Persian',
        'Pizzeria', 'Polish', 'Regional' ,'Seafood', 'Soup', 'Southern' ,'Southwestern, 'Spanish', 'Steaks', 'Sushi',
        'Thai', 'Turkish', 'Vegetarian', 'Vietnamese'} for cuisine in self.cuisine})
        - len(self.postal_code) == 3
        - self.postal_code != ''
    """

    restaurant_id: str
    name: str
    cuisine: list[str]
    postal_code: str

    def __init__(self, restaurant_id: str, name: str, postal_code: str) -> None:
        """Initialize a new resturant.
        """

        self.restaurant_id = restaurant_id
        self.name = name
        self.cuisine = []
        self.postal_code = postal_code


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: The type of this vertex: 'user' or 'restaurant'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - self.kind != ''
        - self.kind in {'user', 'restaurant'}
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: User | Restaurant
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item, kind, and neighbours."""
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def similarity_list(self, other: User) -> list[int]:
        """Return similarity list between this vertex and other.

        Preconditions:
        - self.kind == 'user'
        """
        curr_user_preference = self.item.preference_lst()
        stored_user_preference = other.preference_lst()

        score = []
        for i in range(0, 5):
            score.append(abs(curr_user_preference[i] - stored_user_preference[i]))

        return score


class _WeightedVertex(_Vertex):
    """A vertex in a weighted user review graph, used to represent a user or restaurant.

    Instance Attributes:
        - item: The data stored in this vertex.
        - kind: The type of this vertex: 'user' or 'restaurant'.
        - neighbours: The vertices that are adjacent to this vertex and their corresponding edge weights

    Representation Invariants:
        - self not in self.neighbours
        - self.kind != ''
        - self.kind in {'user', 'restaurant'}
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: User | Restaurant
    kind: str
    neighbours: dict[_WeightedVertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new weighted vertex with the given item, kind, and neighbours."""
        super().__init__(item, kind)
        self.neighbours = {}


class Graph:
    """A graph used to represent a restaurant review network.

    Instance Attributes:
        - _vertices: A collection of the vertices contained in this graph. Maps item to _Vertex object.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, kind: str, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set[_Vertex]:
        """Return a set of all vertex in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.values())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


class WeightedGraph(Graph):
    """A weighted graph used to represent a book review network that keeps track of review scores.

    Note that this is a subclass of the Graph class from Exercise 3, and so inherits any methods
    from that class that aren't overridden here.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        Graph.__init__(self)

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _WeightedVertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.neighbours.get(v2, 0)

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours.keys():
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item, weight=v.neighbours[u])

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def get_similar_users(self, program_user: User) -> list[str]:
        """Return a list of the similar users that match the program user's preferences.
        """
        vertices_list = sorted(list(self.get_all_vertices('user')), key=lambda x: x.item.user_id)

        subtracted_numbers_dict = {}
        for vertex in vertices_list:
            subtracted_numbers_dict[vertex.item.user_id] = vertex.similarity_list(program_user)

        zeros_dict = {}
        for item in subtracted_numbers_dict:
            num_zeroes = subtracted_numbers_dict[item].count(0)
            sum_of_list = sum(subtracted_numbers_dict[item])
            zeros_dict[item] = (num_zeroes, sum_of_list)

        sorted_subtracted_numbers_dict = dict(sorted(zeros_dict.items(), key=lambda item: (item[1][0], item[1][1]),
                                                     reverse=True))
        return list(sorted_subtracted_numbers_dict.keys())

    def recommend_restaurants(self, program_user: User, limit: int, all_users: dict, distances: dict) -> (
            dict[str, tuple[float, str, list[str]]]):
        """Return a list of recommended restaurants based on user's preferences

        Preconditions:
        - all_users != {} and all({u in self._vertices for u in all_users})
        - distances != {}
        - limit >= 1
        """

        similar_users = self.get_similar_users(program_user)

        dict_so_far = {}
        for u_id in similar_users:
            user = self._vertices[all_users[u_id]]
            restaurants = user.neighbours

            for restaurant in restaurants:
                if self.get_weight(user.item, restaurant.item) >= 4:
                    if restaurant.item.name not in dict_so_far:
                        dict_so_far[restaurant.item.name] = (
                            self.get_average_review(restaurant.item), distances[restaurant.item.name],
                            restaurant.item.cuisine)

        return dict(list(dict_so_far.items())[:limit])

    def get_average_review(self, restaurant: Restaurant) -> float:
        """
        Return the average rating given by users of the restaurant.

        Preconditions:
        - restaurant in self._vertices
        """
        restaurant_vertex = self._vertices[restaurant]
        users = restaurant_vertex.neighbours
        reviews_so_far = 0
        for user in users:
            reviews_so_far += self.get_weight(user.item, restaurant_vertex.item)

        return round(reviews_so_far / len(users), 2)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'disable': ['E1136', 'W0221', 'W0237', 'R0913'],
    })
