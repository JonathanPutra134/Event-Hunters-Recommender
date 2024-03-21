import pandas as pd
from flask import jsonify
from app.models import *
from sqlalchemy import func

class DataFetcher:
    def get_events(self):
        try:
            # Perform a query to select all rows from the 'events' table
            events = Events.query.order_by(Events.id).all()
            # Convert the result to a Pandas DataFrame
            events_df = pd.DataFrame([
                {
                    'id': event.id,
                    'eventcreator_id': event.eventcreator_id,
                    'category': event.category,
                    'preregister_date': event.preregister_date,
                    'endregister_date': event.endregister_date,
                    'startevent_date': event.startevent_date,
                    'endevent_date': event.endevent_date,
                    'created_at': event.created_at,
                    'updated_at': event.updated_at,
                    'latitude': event.latitude,
                    'longitude': event.longitude,
                    'title': event.title,
                    'description': event.description,
                    'is_online': event.is_online,
                    'tags': event.tags,
                    'featured_images': event.featured_images,
                    'guest_star': event.guest_star,
                    'location': event.location
                }
                for event in events
            ])
            return events_df
        
        except Exception as e:
            import traceback
            print(f"Error in get_events: {str(e)}")
            traceback.print_exc()
            return jsonify({'error in get_events': str(e)}), 500  # HTTP 500 for internal server error

    def get_views_interaction_data(self, user_id):
        try:
            # Perform a query to select all rows from the 'events_views' table for a specific user
            user_views_interaction = EventsViews.query.filter_by(user_id=user_id).all()
            user_views_df = pd.DataFrame([
                {
                    'id': interaction.id,
                    'user_id': interaction.user_id,
                    'event_id': interaction.event_id,
                    'view_date': interaction.view_date,
                }
                for interaction in user_views_interaction
            ])
            return user_views_df
        except Exception as e:
            import traceback
            print(f"Error in get_views_interaction_data: {str(e)}")
            traceback.print_exc()
            return jsonify({'error in get_views_interaction_data': str(e)}), 500  # HTTP 500 for internal server error

    def get_bookmark_interaction_data(self, user_id):
        try:
            # Perform a query to select all rows from the 'events_bookmark' table for a specific user
            user_bookmark_interaction = EventsBookmarks.query.filter_by(user_id=user_id).all()
            user_bookmark_df = pd.DataFrame([
                {
                    'id': interaction.id,
                    'user_id': interaction.user_id,
                    'event_id': interaction.event_id,
                    'bookmark_date': interaction.bookmark_date,
                }
                for interaction in user_bookmark_interaction
            ])
            return user_bookmark_df
        except Exception as e:
            import traceback
            print(f"Error in get_bookmark_interaction_data: {str(e)}")
            traceback.print_exc()
            return jsonify({'error in get_bookmark_interaction_data': str(e)}), 500  # HTTP 500 for internal server error

    def get_user_attendance_data(self, user_id):
        try:
            # Perform a query to select all rows from the 'tickets' table for a specific user
            user_attendance_data = Tickets.query.filter_by(user_id=user_id).all()
            user_attendance_df = pd.DataFrame([
                {
                    'id': attendance.id,
                    'user_id': attendance.user_id,
                    'event_id': attendance.event_id,
                    'attendance_date': attendance.registered_date,
                }
                for attendance in user_attendance_data
            ])
            return user_attendance_df
        except Exception as e:
            import traceback
            print(f"Error in get_user_attendance_data: {str(e)}")
            traceback.print_exc()
            return jsonify({'error in get_user_attendance_data': str(e)}), 500  # HTTP 500 for internal server error

    def get_ratings_data(self, user_id):
        try:
            # Perform a query to select all rows from the 'ratings' table for a specific user
            user_ratings_data = Ratings.query.filter_by(user_id=user_id).all()
            user_ratings_df = pd.DataFrame([
                {
                    'id': rating.id,
                    'user_id': rating.user_id,
                    'event_id': rating.event_id,
                    'rating': rating.rating,
                    'rating_date': rating.rating_date,
                }
                for rating in user_ratings_data
            ])
            user_ratings_df = user_ratings_df.sort_values(by='event_id')
            return user_ratings_df
        except Exception as e:
            import traceback
            print(f"Error in get_ratings_data: {str(e)}")
            traceback.print_exc()
            return jsonify({'error in get_ratings_data': str(e)}), 500  # HTTP 500 for internal server error

    def get_user(self, user_id):
        try:
            # Use SQLAlchemy query
            user = Users.query.filter_by(id=user_id).first()

            # Check if the user is not None before returning
            if user:
                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'longitude': user.longitude,
                    'latitude': user.latitude,
                    # Add other fields as needed
                }
                return pd.DataFrame([user_data])

            return pd.DataFrame()  # Return an empty DataFrame if the user is not found

        except Exception as e:
            import traceback
            print(f"Error in get_user: {str(e)}")
            traceback.print_exc()
            return jsonify({'Error in get_user': str(e)}), 500

    def get_user_interactions_count(self, user_views_interaction, user_bookmark_interaction, user_attendance_data, user_ratings_data):
        try:
            total_interaction_count = 0
            if not isinstance(user_views_interaction, tuple):
                total_interaction_count += user_views_interaction.shape[0]


            if not isinstance(user_bookmark_interaction, tuple):
                total_interaction_count += user_bookmark_interaction.shape[0]

            if not isinstance(user_attendance_data, tuple):
                total_interaction_count += user_attendance_data.shape[0]
        
            if not isinstance(user_ratings_data, tuple):
                total_interaction_count += user_ratings_data.shape[0]
        
            return total_interaction_count

        except Exception as e:
            import traceback
            print(f"Error in get_user_interactions_count: {str(e)}")
            traceback.print_exc()
            return jsonify({'Error in get_user_interactions_count': str(e)}), 500