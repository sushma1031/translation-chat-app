from flask import request, jsonify, make_response
from flask_bcrypt import generate_password_hash
from models.User import User, users
from utils.languages import language_mapping

async def register_user(data):
  try:
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    profile_pic = data.get('profile_pic') or ""
    language = data.get('language') or "en"

    check_email = users.find_one({'email': email})

    if(check_email):
      return jsonify({
                'message': 'User already exists',
                'error': True,
            }), 400
    
    hashed = generate_password_hash(password, 5).decode('utf-8')
    user = User(
            name=name,
            email=email,
            profile_pic=profile_pic,
            password=hashed,
            language=language
        )
    
    result = users.insert_one(user.model_dump())
    saved = users.find_one({'_id': result.inserted_id})
    saved['_id'] = str(saved['_id'])

    return jsonify({
        'message': 'User created successfully',
        'data': saved, 
        'success': True
    }), 201

  except Exception as e:
    return jsonify({
      "message": str(e), 
      "error": True
    }), 500
  
def send_languages():
  return language_mapping