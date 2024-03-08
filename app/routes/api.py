from flask import jsonify
from app import app
from app.models import Events
from app.recommender.recommend import Recommender
from flask import jsonify


@app.route('/recommend/<int:user_id>')
def index(user_id):
    try:
        # Create an instance of the Recommender class
        recommender = Recommender()

        # Call the get_user_recommendations method
        events_df = recommender.get_user_recommendations(user_id)

        return events_df.to_html(index=False)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'})