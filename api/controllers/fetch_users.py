from models.User import users

def fetch():
  arr = users.find({}, {"created_at": 0, "email": 0, "password": 0})
  arr = list(arr)
  for u in arr:
    u["_id"] = str(u["_id"])
  return arr