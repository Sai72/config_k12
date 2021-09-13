# config_k12
1. "pip install -r requirements.txt"

# Task
1)API:LOGIN
 API Desc:  1. If user tries to login before start time will allow the user and store day details and user details
        in dailyActivity table and based on the dailyActivity table will update the login time in dayActivity table.
        2. If User tries to login the first attempt after start time will not allow
        3. If user tries to login second or more attempts after start will allow
  API Method:POST
  API URI: http://127.0.0.1:8000/k12/authenticate/login/
  API Headers: json
  API Request payload: {"username": "username", "password": "password"}
  API Request Response: Successfully Login 
  

2)API:LOGOUT
  Desc:This api will logout the user and calculates the duration of last login and current logout time.
        If duration hours greatest to 9 hours, Will update the user day status and duration on DailyActivity table.
        Removes the Token once the logout is success.
  API Method:GET
  API URI:http://127.0.0.1:8000/k12/authenticate/logout/
  API Headers: Authorization Token <token>
  API Request Response:Successfully logout
  

3)API:REGISTER USER
  API Desc: This api will do register the user(staff) on User table, id user is already exist it wll send proper response
  API Method: POST
  API URI:  http://127.0.0.1:8000/k12/authenticate/register_user/
  API Headers: json
  API Request Payload:{"username": "username", "password": "password", "email":"emailid"}
  API Request Response: Registered successfully
  

4)API:List OUT All Users
   API Desc:  This api will list out the all users daily attendances and this api will work for day activity
         of particular user
    API Method: GET
    API URI: http://127.0.0.1:8000/k12/authenticate/user_attendance/--> list out all users
    API Response: Json
  
5)API:list out particular user day activity
    API Desc:  This api will list out the all users daily attendances and this api will work for day activity
         of particular user
    API Method: GET
    API URI: http://127.0.0.1:8000/k12/authenticate/user_attendance/?id=2--> list out particular user day activity
    API Response: Json