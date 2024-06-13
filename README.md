asgiref==3.8.1
Django==5.0.6
djangorestframework==3.15.1
mysqlclient==2.2.4
sqlparse==0.5.0
# Social_Network

API

SignUp

      curl --location 'http://localhost:8000/user/signup/' \
      --header 'Content-Type: application/json' \
      --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO' \
      --data-raw '{
          "name": "newUser",
          "password": "newUser@123",
          "email": "new@gmail.com"
      }'


Login

    curl --location 'http://localhost:8000/user/login' \
    --header 'Content-Type: application/json' \
    --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO' \
    --data-raw '{
        "name": "newUser1",
        "password": "newUser1@123",
        "email": "new1@gmail.com"
    }'

Get user by email
      
      curl --location 'http://localhost:8000/user/getUserDetails?email=new%40gmail.com' \
    --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO'

get user by name

      curl --location 'http://localhost:8000/user/getUserDetails?name=ne' \
      --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO'

send friend request
      curl --location 'http://127.0.0.1:8000/api/users/friend-request/send/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
        "sender_username":"aman",
        "receiver_email": "new@gmail.com"
        }'

pending friend request

      curl --location --request GET 'http://localhost:8000/api/users/friend-requests/pending/' \
      --header 'Content-Type: application/json' \
      --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO' \
      --data '{
        "username":"newUser"
      }'

Manage friend request

      curl --location 'http://localhost:8000/api/users/friend-request/manage/' \
      --header 'Content-Type: application/json' \
      --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO' \
      --data '{
            "request_id": 10,
            "username":"newUser",
            "action": "accept"
            }'

List friends
      curl --location --request GET 'http://localhost:8000/api/users/friends/' \
      --header 'Content-Type: application/json' \
      --header 'Cookie: csrftoken=pOQCL9FTJrVnoDTXCQ6XjnzmoMol0XYO' \
      --data '{
            "username":"newUser"
      }'


