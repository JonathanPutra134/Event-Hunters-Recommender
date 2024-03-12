from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from datetime import datetime
from app.models import *
from sqlalchemy import func


def get_events_score(latuser, lonuser, candidate_events):
    try:
        top_20_event_ids = candidate_events['event_id'].head(20)
        # Use raw SQL query
        top_20_event_ids = [int(event_id) for event_id in top_20_event_ids]
        events = db.session.query(
            Events.id.label('event_id'),
            Events.title,
            Events.endregister_date,
            Events.latitude,
            Events.longitude,
            Events.is_online,
            func.coalesce(func.count(EventsViews.user_id.distinct()), 0).label('view_count'),
            func.coalesce(func.count(EventsBookmarks.user_id.distinct()), 0).label('bookmark_count'),
            func.coalesce(func.count(Tickets.user_id.distinct()), 0).label('attendance_count')
        ).outerjoin(EventsViews, Events.id == EventsViews.event_id) \
        .outerjoin(EventsBookmarks, Events.id == EventsBookmarks.event_id) \
        .outerjoin(Tickets, Events.id == Tickets.event_id) \
        .filter(Events.id.in_(top_20_event_ids)) \
        .group_by(Events.id).all()

  # Convert the result to a Pandas DataFrame
        events_df = pd.DataFrame([
            {
                    'event_id': event.event_id,
                    'title': event.title,
                    'endregister_date': event.endregister_date,
                    'latitude': event.latitude,
                    'longitude': event.longitude,
                    'is_online': event.is_online,
                    'view_count': event.view_count,
                    'bookmark_count': event.bookmark_count,
                    'attendance_count': event.attendance_count
            }
                for event in events
            ])
        
        events_df = pd.merge(events_df, candidate_events, on='event_id', how='inner')
        events_df['interaction_score'] = events_df.apply(
            lambda row: get_combined_interaction_score(row['view_count'], row['bookmark_count'], row['attendance_count']), axis=1
        )
        events_df['distance(km)'] = events_df.apply(
            lambda row: 0 if row['is_online'] else haversine_distance(latuser, lonuser, float(row['latitude']), float(row['longitude'])), axis=1
        )
        events_df['days_before_registration'] = events_df.apply(
            lambda row: calculate_days_before_registration(row['endregister_date']), axis=1
        )
        min_distance = events_df['distance(km)'].min()
        max_distance = events_df['distance(km)'].max()

        events_df['distance_score'] = events_df['distance(km)'].apply(
            lambda x: inverse_min_max_scaling(x, min_distance, max_distance)
        )
        
        min_interaction = events_df['interaction_score'].min()
        max_interaction = events_df['interaction_score'].max()
        
        events_df['popularity_score'] = events_df['interaction_score'].apply(
            lambda x: min_max_scaling(x, min_interaction, max_interaction)
        )
        
        min_days = events_df['days_before_registration'].min()
        max_days = events_df['days_before_registration'].max()
        
        events_df['closeness_date_score'] = events_df['days_before_registration'].apply(
            lambda x: inverse_min_max_scaling(x, min_days, max_days)
        )
        min_similarity = events_df['cosine_similarity_score'].min()
        max_similarity = events_df['cosine_similarity_score'].max()
        events_df['similarity_score'] = events_df['cosine_similarity_score'].apply(
            lambda x: min_max_scaling(x, min_similarity, max_similarity)
        )
        events_df['final_score'] = events_df.apply(
        lambda row: calculate_final_score(
            row['distance_score'],
            row['closeness_date_score'],
            row['popularity_score'],
            row['similarity_score'],
        ),
        axis=1
        )
        events_df = events_df.sort_values(by='final_score', ascending=False)
        # Rest of your code...

        return events_df

    except Exception as e:
        import traceback
        print(f"Error in get_events_score: {str(e)}")
        traceback.print_exc()
        return None


#INVERSE MIN MAX SCALING FOR CALCULATE SCORE DISTANCE AND DAYS BEFORE REGISTRATION
# Notes: The closest/smaller the distance, then the score will be higher, as same as days count before registration so we do inverse here
def inverse_min_max_scaling(x, min_val, max_val):
    try:
        if min_val == max_val: 
            return 0
        # Apply min-max scaling
        scaled_value = (x - min_val) / (max_val - min_val)
        
        # Apply inverse relationship
        score = 1 - scaled_value
        
        return score
    except Exception as e:
        import traceback
        print(f"Error in inverse_min_max_scaling: {str(e)}")
        traceback.print_exc()
        return None

def min_max_scaling(x, x_min, x_max):
    if x_min == x_max:
        return 0
    return (x - x_min) / (x_max - x_min)

def get_combined_interaction_score(view_count, bookmark_count, attendance_count):
    try:
        weight_attendance = 3
        weight_bookmark = 2
        weight_view = 1

        # Calculate scores
        view_count = view_count * weight_view
        bookmark_count = bookmark_count * weight_bookmark
        attendance_count = attendance_count * weight_attendance

        # Combine scores with weights
        combined_score = (
            view_count +
            bookmark_count +
            attendance_count
        )
        return combined_score
    except Exception as e:
        import traceback
        print(f"Error in get_combined_interaction_score : {str(e)}")
        traceback.print_exc()
        return None

def haversine_distance(lat1, lon1, lat2, lon2):
    try:
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radius of Earth in kilometers (you might need to adjust this based on your use case)
        radius = 6371.0

        # Calculate the distance
        distance = radius * c

        return distance
    except Exception as e:
        import traceback
        print(f"Error in haversine_distance : {str(e)}")
        traceback.print_exc()
        return None

def calculate_days_before_registration(event_endregister_date):
    try:
        event_endregister_date = pd.to_datetime(event_endregister_date, errors='coerce')
        # Get the current date
        current_date = datetime.now()
        # Calculate the time difference
        days_count = (event_endregister_date - current_date).days
        return days_count
    except Exception as e:
        import traceback
        print(f"Error in calculate_days_before_registration : {str(e)}")
        traceback.print_exc()
        return None

def calculate_final_score(distance_score, closeness_date_score, popularity_score, similarity_score):
    try:
        weight_distance = 0.4
        weight_closeness_date = 0.2
        weight_popularity = 0.1
        weight_similarity = 0.3
        return (weight_distance * distance_score) + (weight_closeness_date * closeness_date_score) + (weight_popularity * popularity_score) + ((weight_similarity * similarity_score))                  
    except Exception as e:
        import traceback
        print(f"Error in calculate_final_score : {str(e)}")
        traceback.print_exc()
        return None