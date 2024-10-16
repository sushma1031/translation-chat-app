from models.User import User, users
from flask import jsonify, make_response
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token

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
    access_token = create_access_token(identity={"email": email, "id": str(em["_id"])})
    response = make_response(jsonify({
        "message": "login successful",
        "token": access_token,
        "success": True
    }), 200)
    response.set_cookie(
        'access_token_cookie',
        access_token,
        httponly=True,
        secure=True,
        samesite='None'
    )
    return response
  except Exception as e:
    return jsonify({
      "message": str(e), 
      "error": True
    }), 500