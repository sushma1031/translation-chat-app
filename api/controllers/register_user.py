from flask import request, jsonify, make_response
from models.User import User, users

async def register_user(data):
  try:
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    profile_pic = data.get('profile_pic') or ""

    check_email = users.find_one({'email': email})

    if(check_email):
      return jsonify({
                'message': 'User already exists',
                'error': True,
            }), 400
    
    user = User(
            name=name,
            email=email,
            profile_pic=profile_pic,
            password=password
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