import pandas as pd
from app.recommender.data_fetcher import DataFetcher  # Adjust the import based on your project structure

def merge_interaction_data(user_id):
    try:
        # Create an instance of the DataFetcher class
        data_fetcher = DataFetcher()

        # Fetch interaction data directly within the function
        user_views_interaction = data_fetcher.get_views_interaction_data(user_id)
        user_bookmark_interaction = data_fetcher.get_bookmark_interaction_data(user_id)
        user_attendance_data = data_fetcher.get_user_attendance_data(user_id)
        user_ratings_data = data_fetcher.get_ratings_data(user_id)
        # Add interaction_type and interaction_strength columns to each dataframe
        all_interactions_data = pd.DataFrame()
        if not isinstance(user_views_interaction, tuple):
            user_views_interaction['interaction_type'] = 'VIEW'
            user_views_interaction['importance'] = 1.0
            all_interactions_data = pd.concat([all_interactions_data, user_views_interaction], ignore_index=True)
            print(user_views_interaction)


        if not isinstance(user_bookmark_interaction, tuple):
            user_bookmark_interaction['interaction_type'] = 'BOOKMARK'
            user_bookmark_interaction['importance'] = 2.0
            all_interactions_data = pd.concat([all_interactions_data, user_bookmark_interaction], ignore_index=True)

        if not isinstance(user_attendance_data, tuple):
            user_attendance_data['interaction_type'] = 'ATTEND'
            user_attendance_data['importance'] = 3.0
            all_interactions_data = pd.concat([all_interactions_data, user_attendance_data], ignore_index=True)
        
        print(type(user_ratings_data))
        if not isinstance(user_ratings_data, tuple):
            user_ratings_data['interaction_type'] = 'RATING'
            user_ratings_data['importance'] = 4.0
            all_interactions_data = pd.concat([all_interactions_data, user_ratings_data], ignore_index=True)

        # Select only the relevant columns
        all_interactions_data = all_interactions_data[['user_id', 'event_id', 'interaction_type', 'importance']]

        # Print the concatenated dataframe
        print(all_interactions_data)
        all_interactions_data = all_interactions_data.sort_values(by=['user_id', 'event_id']).reset_index(drop=True)
        all_interactions_data = all_interactions_data.loc[all_interactions_data.groupby(['user_id', 'event_id']).importance.idxmax()]

        return all_interactions_data

    except Exception as e:
        import traceback
        print(f"Error in merge_interaction_data: {str(e)}")
        traceback.print_exc()
        return None