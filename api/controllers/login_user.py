from models.User import User, users
from flask import jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

def validate(email, password):
  try:
    em: User = users.find_one({"email": email})
    if not em:
      return jsonify({
        "message": "user does not exist",
        "error": True
      }), 400
    if not check_password_hash(em['password'], password):
      return jsonify({
        "message": "incorrect password",
        "error": True,
      }), 400

    em['_id'] = str(em['_id'])
    return jsonify({
      "message": "user verified",
      "success": True,
      "data": em
    }), 200
  except Exception as e:
    return jsonify({
      "message": str(e), 
      "error": True
    }), 500