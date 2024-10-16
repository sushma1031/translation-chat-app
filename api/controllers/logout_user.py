from flask import jsonify, make_response

def logout():
  try:
    response = make_response(jsonify({
          "message": "session end",
          "success": True
      }), 200)
    response.set_cookie(
          'access_token_cookie',
          '',
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