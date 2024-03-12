import pandas as pd
from app.recommender.data_fetcher import DataFetcher  # Adjust the import based on your project structure
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def merge_interaction_data(user_id, user_views_interaction, user_bookmark_interaction, user_attendance_data, user_ratings_data):
    try:
        # Add interaction_type and interaction_strength columns to each dataframe
        all_interactions_data = pd.DataFrame()
        if not isinstance(user_views_interaction, tuple):
            user_views_interaction['interaction_type'] = 'VIEW'
            user_views_interaction['importance'] = 1.0
            all_interactions_data = pd.concat([all_interactions_data, user_views_interaction], ignore_index=True)


        if not isinstance(user_bookmark_interaction, tuple):
            user_bookmark_interaction['interaction_type'] = 'BOOKMARK'
            user_bookmark_interaction['importance'] = 2.0
            all_interactions_data = pd.concat([all_interactions_data, user_bookmark_interaction], ignore_index=True)

        if not isinstance(user_attendance_data, tuple):
            user_attendance_data['interaction_type'] = 'ATTEND'
            user_attendance_data['importance'] = 3.0
            all_interactions_data = pd.concat([all_interactions_data, user_attendance_data], ignore_index=True)
        
        if not isinstance(user_ratings_data, tuple):
            user_ratings_data['interaction_type'] = 'RATING'
            user_ratings_data['importance'] = 4.0
            all_interactions_data = pd.concat([all_interactions_data, user_ratings_data], ignore_index=True)

        # Select only the relevant columns
        all_interactions_data = all_interactions_data[['user_id', 'event_id', 'interaction_type', 'importance']]
        all_interactions_data = all_interactions_data.sort_values(by=['user_id', 'event_id']).reset_index(drop=True)
        all_interactions_data = all_interactions_data.loc[all_interactions_data.groupby(['user_id', 'event_id']).importance.idxmax()]

        return all_interactions_data

    except Exception as e:
        import traceback
        print(f"Error in merge_interaction_data: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in merge_interaction_data': str(e)}), 500  # HTTP 500 for internal server error

def get_viewed_event_indices(user_interaction):
    try:
        viewed_events_id = user_interaction[user_interaction["interaction_type"] == "VIEW"]["event_id"].astype(int).tolist()
        viewed_events_indices = [event_id - 1 for event_id in viewed_events_id]
        return viewed_events_id, viewed_events_indices
    except Exception as e:
        import traceback
        print(f"Error in get_viewed_event_indices: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_viewed_event_indices': str(e)}), 500  # HTTP 500 for internal server error

def get_bookmarked_event_indices(user_interaction):
    try:
        bookmarked_events_id = user_interaction[user_interaction["interaction_type"] == "BOOKMARK"]["event_id"].astype(int).tolist()
        bookmarked_events_indices = [event_id - 1 for event_id in bookmarked_events_id]
        return bookmarked_events_id, bookmarked_events_indices
    except Exception as e:
        import traceback
        print(f"Error in get_bookmarked_event_indices: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in et_bookmarked_event_indices': str(e)}), 500  # HTTP 500 for internal server error

def get_attended_event_indices(user_interaction):
    try:
        attended_events_id = user_interaction[user_interaction["interaction_type"] == "ATTEND"]["event_id"].astype(int).tolist()
        attended_events_indices = [event_id - 1 for event_id in attended_events_id]
        return attended_events_id, attended_events_indices
    except Exception as e:
        import traceback
        print(f"Error in get_attended_event_indices: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_attended_event_indices': str(e)}), 500  # HTTP 500 for internal server error

def get_rated_event_indices(user_interaction):
    try:
        rated_events_id = user_interaction[user_interaction["interaction_type"] == "RATING"]["event_id"].astype(int).tolist()
        rated_events_indices = [event_id - 1 for event_id in rated_events_id]
        return rated_events_id, rated_events_indices
    except Exception as e:
        import traceback
        print(f"Error in get_rated_event_indices: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_rated_event_indices': str(e)}), 500  # HTTP 500 for internal server error

def get_events_for_content_based(events):
    try:
        events_content_based_df = events[["id", "category", "title", "description", "tags", "guest_star", "location"]]
        events_content_based_df.loc[:, 'category'] = events_content_based_df['category'].apply(lambda x: ' '.join(x) if x else '')
        events_content_based_df.loc[:, 'tags'] = events_content_based_df['tags'].apply(lambda x: ' '.join(x) if x else '')
        events_content_based_df.loc[:, 'guest_star'] = events_content_based_df['guest_star'].apply(lambda x: ' '.join(x) if x else '')
        events_content_based_df = events_content_based_df.rename(columns={"id": "event_id"})
        return events_content_based_df
    except Exception as e:
        import traceback
        print(f"Error in get_events_for_content_based: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_events_for_content_based': str(e)}), 500  # HTTP 500 for internal server error


def get_indonesia_stopwords():
    stopwords_path = os.path.join(os.path.dirname(__file__), 'tala-stopwords-indonesia.txt')
    
    try:
        with open(stopwords_path, 'r') as f:
            stopword_list = [line.strip() for line in f]
        
        return stopword_list
    except Exception as e:
        import traceback
        print(f"Error in get_indonesia_stopwords: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_indonesia_stopwords': str(e)}), 500  # HTTP 500 for internal server error

def get_all_events_textdata(events_content_based_df, events):
    try:
        text_columns = ['description', 'location', 'title', 'category', 'tags', 'guest_star']
        all_events_text_data = events_content_based_df[text_columns].apply(lambda x: ' '.join(x), axis=1)
        
        eventdf_withtextdata = pd.DataFrame({'event_id': events['id'], 'aggregated_text': all_events_text_data})
        return eventdf_withtextdata
    except Exception as e:
        import traceback
        print(f"Error in get_all_events_textdata: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_all_events_textdata': str(e)}), 500  # HTTP 500 for internal server error

def get_item_profile(tfidf_vectorizer, events_content_based_df):
    try:
        tfidf_matrix_events = tfidf_vectorizer.fit_transform(events_content_based_df['aggregated_text'])
        return tfidf_matrix_events
    except Exception as e:
        import traceback
        print(f"Error in get_item_profile: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_item_profile': str(e)}), 500  # HTTP 500 for internal server error

def get_ratings_weight(user_ratings_data):
    try:
        rated_events_weights = []
        if not isinstance(user_ratings_data, tuple):
            for index, row in user_ratings_data.iterrows():
                rating = row['rating']

                # Assign interaction strength based on the rating
                if rating == 1:
                    rated_events_weights.append(0)
                elif rating == 2:
                    rated_events_weights.append(0)
                elif rating == 3:
                    rated_events_weights.append(1)
                elif rating == 4:
                    rated_events_weights.append(3)
                elif rating == 5:
                    rated_events_weights.append(5)
            return rated_events_weights
    except Exception as e:
        import traceback
        print(f"Error in get_ratings_weight: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_ratings_weight': str(e)}), 500  # HTTP 500 for internal server error
def map_rated_events_id_and_weight(rated_events_id, rated_events_weights):
    try:
        if rated_events_id and rated_events_weights:
            rated_weight_dict = dict(zip(rated_events_id, rated_events_weights))
            return rated_weight_dict
    except Exception as e:
        import traceback
        print(f"Error in map_rated_events_id_and_weight: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in map_rated_events_id_and_weight': str(e)}), 500  # HTTP 500 for internal server error

def get_rated_events_tfidf(rated_weight_dict, rated_events_indices, tfidf_matrix_events):
    try:
        rated_events_tfidf = np.zeros(tfidf_matrix_events.shape[1])
        for index in rated_events_indices:
            weight = rated_weight_dict.get(index + 1, None)
            rated_events_tfidf += weight * tfidf_matrix_events[index]

        return np.asarray(rated_events_tfidf)
    except Exception as e:
        import traceback
        print(f"Error in get_rated_events_tfidf: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_rated_events_tfidf': str(e)}), 500  # HTTP 500 for internal server error

def get_user_profile(viewed_events_tfidf, bookmarked_events_tfidf, attended_events_tfidf, rated_events_tfidf):
    try:
        user_profile = viewed_events_tfidf + bookmarked_events_tfidf + attended_events_tfidf + rated_events_tfidf
        user_profile = user_profile / np.linalg.norm(user_profile)
        return np.asarray(user_profile)
    except Exception as e:
        import traceback
        print(f"Error in get_user_profile: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_user_profile': str(e)}), 500  # HTTP 500 for internal server error

def get_candidate_events(events_content_based_df, cosine_similarity_matrix, viewed_events_id, bookmarked_events_id, attended_events_id, rated_events_id):
    try:
        all_event_ids = events_content_based_df['event_id'].tolist()
        all_event_titles = events_content_based_df['title'].tolist()
        similarity = cosine_similarity_matrix[0].tolist()
        similarity_df = pd.DataFrame({
            'event_id': all_event_ids,  # All event IDs in the original order
            'event_title': all_event_titles,  # All event IDs in the original order
            'cosine_similarity_score': similarity,  # Similarity scores for the user
        })
        candidate_events = similarity_df[~similarity_df['event_id'].isin(viewed_events_id + bookmarked_events_id + attended_events_id + rated_events_id)].sort_values(by='cosine_similarity_score', ascending=False)

        candidate_events = candidate_events.head(20)
        return candidate_events
    except Exception as e:
        import traceback
        print(f"Error in get_candidate_events: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_candidate_events': str(e)}), 500  # HTTP 500 for internal server error

def get_weighted_tfidf(tfidf_matrix, indices, weights):
    try:
        print(indices)
        weighted_tfidf = np.zeros(tfidf_matrix.shape[1])

        for index in indices:
            weighted_tfidf += weights * tfidf_matrix[index]

        return np.asarray(weighted_tfidf)
    except Exception as e:
        import traceback
        print(f"Error in get_weighted_tfidf: {str(e)}")
        traceback.print_exc()
        return jsonify({'error in get_weighted_tfidf': str(e)}), 500  # HTTP 500 for internal server error