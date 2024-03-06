# app/routes/api.py

from flask import jsonify
from app import app
from app.models.recommender import generate_recommendations

@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    recommendations = generate_recommendations(user_id)
    return jsonify({'user_id': user_id, 'recommendations': recommendations})
