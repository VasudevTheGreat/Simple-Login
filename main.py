import os
import hashlib
import base64
from firebase import firebase
status = True

firebase = firebase.FirebaseApplication('https://vasudev-db.firebaseio.com/', None)

while status:
  users = firebase.get('/users', None)
  answer = input("login or register")


  if (answer == "login"):
    
    username = input("username:")
    password = input("password:").encode()
    
    for k,v in users.items():
      if username == v['username']:
        m = hashlib.md5()
        salt = base64.b64decode(v['salt'].encode())
        m.update(salt + password)
        hash = m.hexdigest()
        if hash == v['password']:
          print("access granted")
          choice = input("Upload or Download")
          if (choice == "upload"):
            f = open("file.txt", "rb")
            v['file'] = f.read().decode('UTF-8')

            result = firebase.patch('/users/',data=users, params={'print': 'pretty'})
            f.close()
          elif (choice == "download"):
            f = open("file.txt", "w+")
            users = firebase.get('/users', None)
            f.write(users[k]['file'])
            f.close()
                   


  if (answer == "register"):

    username = input("username:")
    found = False
    key = None
    if not  users is None:
      for k,v in users.items():
        if username == v['username']:
          found = True
    if found:
      print("This username is already taken")
    else:
      password = input("password:").encode()
      salt = os.urandom(16)
      m = hashlib.md5()
      m.update(salt + password)
      hash = m.hexdigest()
      salt  = base64.b64encode(salt).decode("utf-8")
      new_user = {'username': username,'password': hash, 'salt': salt}
      result = firebase.post('/users', data=new_user, params={'print': 'pretty'})
      status = True

