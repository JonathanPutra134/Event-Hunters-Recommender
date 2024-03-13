from flask import jsonify
from app import app
from app.models import *
from app.recommender.recommend import Recommender
from flask import jsonify


@app.route('/recommend/<int:user_id>')
def index(user_id):
    try:
        session_exists = Sessions.query.filter_by(user_id=user_id).first() is not None
        if session_exists:
            # Create an instance of the Recommender class
            recommender = Recommender()
            
            # Call the get_user_recommendations method
            result, success = recommender.get_user_recommendations(user_id)

            if not success:
                # Return the error message
                return jsonify(result), 400

            # Convert the result to a JSON response using jsonify
            result_json = jsonify(result.to_dict(orient='records'))

            # Return the JSON response
            return result_json
        
        return jsonify({'error': 'unauthorized'}), 401  # HTTP 401 for unauthorized
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'})