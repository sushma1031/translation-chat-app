from models.User import users
from flask import jsonify

def fetch_user_details(user):
  try:
    details = fetch_user_by_email(user["email"])

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
  
def fetch_user_by_email(email):
  details = users.find_one({"email": email}, {"password": 0})
  details["_id"] = str(details["_id"])
  return details