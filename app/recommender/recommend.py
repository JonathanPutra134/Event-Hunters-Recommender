from app.recommender.data_fetcher import DataFetcher  # Adjust the case based on the actual filename
from app.recommender.preprocessing import *
class Recommender:
    def __init__(self):
        self.data_fetcher = DataFetcher()

    def get_user_recommendations(self, user_id):

        # Call the merge_interaction_data function
        recommendations = merge_interaction_data(user_id)

        return recommendations