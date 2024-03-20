from app.recommender.data_fetcher import DataFetcher  # Adjust the case based on the actual filename
from app.recommender.first_layer_preprocessing import *
from app.recommender.second_layer_preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
class Recommender:
    def __init__(self):
        self.data_fetcher = DataFetcher()

    def get_user_recommendations(self, user_id):
        data_fetcher = DataFetcher()
    
        user_views_interaction = data_fetcher.get_views_interaction_data(user_id)
        user_bookmark_interaction = data_fetcher.get_bookmark_interaction_data(user_id)
        user_attendance_data = data_fetcher.get_user_attendance_data(user_id)
        user_ratings_data = data_fetcher.get_ratings_data(user_id)
        user_interactions_count = data_fetcher.get_user_interactions_count(user_views_interaction, user_bookmark_interaction, user_attendance_data, user_ratings_data)

        if user_interactions_count < 5:
            error_message = {
            "message": f"User has only {user_interactions_count} interactions, which is not enough for recommendations to work. Please try interacting (bookmark, views, register, rating) with some events."
            }
            return error_message, False
        
        first_layer_results = self.first_layer_recommendations(user_id)
      
        second_layer_results = self.second_layer_recommendations(first_layer_results, user_id)
        return second_layer_results, True

    def first_layer_recommendations(self, user_id):
        data_fetcher = DataFetcher()
        events = data_fetcher.get_events()
       
        user_views_interaction = data_fetcher.get_views_interaction_data(user_id)
        user_bookmark_interaction = data_fetcher.get_bookmark_interaction_data(user_id)
        user_attendance_data = data_fetcher.get_user_attendance_data(user_id)
        user_ratings_data = data_fetcher.get_ratings_data(user_id)
      
        user_interaction = merge_interaction_data(user_id, user_views_interaction, user_bookmark_interaction, user_attendance_data, user_ratings_data)
        viewed_events_id, viewed_events_indices = get_viewed_event_indices(user_interaction)
        bookmarked_events_id, bookmarked_events_indices = get_bookmarked_event_indices(user_interaction)
        attended_events_id, attended_events_indices = get_attended_event_indices(user_interaction)
        rated_events_id, rated_events_indices = get_rated_event_indices(user_interaction)
      
        events_content_based_df = get_events_for_content_based(events)
        stopword_list = get_indonesia_stopwords()
        
        events_textdata = get_all_events_textdata(events_content_based_df, events)

        rated_events_weights = get_ratings_weight(user_ratings_data)
        rated_weight_dict = map_rated_events_id_and_weight(rated_events_id, rated_events_weights)
   
        tfidf_vectorizer = TfidfVectorizer(stop_words=stopword_list)
        tfidf_matrix_events = get_item_profile(tfidf_vectorizer, events_textdata)
        viewed_events_tfidf = get_weighted_tfidf(tfidf_matrix_events, viewed_events_indices, 1)
        bookmarked_events_tfidf = get_weighted_tfidf(tfidf_matrix_events, bookmarked_events_indices, 2)
        attended_events_tfidf = get_weighted_tfidf(tfidf_matrix_events, attended_events_indices, 3)
        rated_events_tfidf = get_rated_events_tfidf(rated_weight_dict, rated_events_indices, tfidf_matrix_events)
        user_profile = get_user_profile(viewed_events_tfidf, bookmarked_events_tfidf, attended_events_tfidf, rated_events_tfidf)

        cosine_similarity_matrix = cosine_similarity(user_profile, tfidf_matrix_events)
        candidate_events = get_candidate_events(events_content_based_df, cosine_similarity_matrix, viewed_events_id, bookmarked_events_id, attended_events_id, rated_events_id)

        
        return candidate_events

    def second_layer_recommendations(self, candidate_events, user_id):
        data_fetcher = DataFetcher()
        user = data_fetcher.get_user(user_id)
        latuser = float(user["latitude"].iloc[0])
        lonuser = float(user["longitude"].iloc[0])
        top_events = get_events_score(latuser, lonuser, candidate_events)
        top_events = top_events.nlargest(20, 'final_score')[['event_id', 'final_score', 'distance(km)', 'days_before_registration', 'interaction_score', 'similarity_score']]
        top_events['distance(km)'] = top_events['distance(km)'].round(2)
        top_events['final_score'] = top_events['final_score'].round(2)
        top_events['similarity_score'] = top_events['similarity_score'].round(2)
        return top_events