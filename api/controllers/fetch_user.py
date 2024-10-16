from models.User import users
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def fetch_user_details(user):
  try:
    details = users.find_one({"email": user["email"]}, {"password": 0})
    details["_id"] = str(details["_id"])

    return jsonify({
      "message": "user details",
      "succes": True,
      "data": details
    })
  except Exception as e:
    return jsonify({
      "message": str(e), 
      "error": True
    }), 500