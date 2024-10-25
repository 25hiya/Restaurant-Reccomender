"""MAIN FILE THAT NEEDS TO BE RUN"""

from computation_compiling import load_review_graph, get_user_answer, get_distance

if __name__ == "__main__":
    with (open("Data Files/userprofile_new.csv") as user_data, open(
            "Data Files/restaurant_cuisine.csv") as restaurant_cuisine, open(
        "Data Files/restaurant_data.csv") as restaurant_data, open(
        "Data Files/rating_final_edited.csv") as rating_file, open("Data Files/Geospatial_Coordinates.csv")
          as geospatial_coordinates):
        data_lst = load_review_graph(rating_file, user_data, restaurant_data, restaurant_cuisine)
        user_questions = [
            "Are you a Smoker or Non-smoker?",
            "What is your drinking level? Choose from: non-drinker, casual drinker, heavy drinker",
            "What is your dress preference? Choose from: informal, smart-casual, formal",
            "What kind of ambience do you prefer? Choose from: solitary, friends, family",
            "What is your budget? Choose from: low, medium, high"
        ]

        # To visualize the graph uncomment the lines below:
        #from visualization import visualize_weighted_graph
        #visualize_weighted_graph(data_lst[0])

        user = get_user_answer(user_questions)
        limit = int(input("How many restaurant recommendations do you want?"))
        user_postal_code = input("What is your postal code(only Toronto)").upper()
        distances = get_distance(user_postal_code, geospatial_coordinates, data_lst[2])
        recommended_restaurants = data_lst[0].recommend_restaurants(user, limit, data_lst[1], distances)

    import plotly.express as px

    the_dict = {'restaurant name': [], 'restaurant rating': [], 'distance from you': [], 'cuisine': []}
    for restaurant in recommended_restaurants:
        the_dict['restaurant name'].append(restaurant)
        the_dict['restaurant rating'].append(recommended_restaurants[restaurant][0])
        the_dict['distance from you'].append(recommended_restaurants[restaurant][1])
        the_dict['cuisine'].append(recommended_restaurants[restaurant][2])

    fig = px.bar(the_dict, x='restaurant name', y='restaurant rating',
                 hover_data=['distance from you', 'cuisine'], color='distance from you',
                 height=400)
    fig.show()
