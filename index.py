#---------------- Bibliotecas-------------------
import requests
import json
import datetime

#---------------- Variáveis -------------------
token = ''
timer = True
minute = 0
status = False
params={}
user_data = {
    "user_name": "ramon.duarte.rdgs@gmail.com",
    "password": "Dt130100"
  }

#node_id = 3hz9vsqog8Fi88LNvGhMke

#---------------- Funções -------------------
def get_token(user):

  r1 = requests.post('https://api.rainmaker.espressif.com/v1/login',json=user )

  response = r1.text

  response_json = json.loads(response)

  status_login = r1.status_code

  token = response_json['accesstoken']
  
  return token,status_login

def get_node_params(token):
  body = {
    "Authorization": token ,
    "accept": "application/json"
  }

  r2 = requests.get('https://api.rainmaker.espressif.com/v1/user/nodes/params?node_id=3hz9vsqog8Fi88LNvGhMke',headers=body)

  response2 = r2.text

  response2_json = json.loads(response2)
  
  status_node_params = r2.status_code
  
  return response2_json,status_node_params

def verify_time(time_data):
  time_now = datetime.datetime.now()
  time_delta = time_now - time_data
  minute_delta = (time_delta.total_seconds()) / 60
  #print(f'minute_delta é de {minute_delta}')
  return minute_delta


#---------------- LOGIN SERVER USER (POST) -----------------------
if not status:
  token,status_login = get_token(user_data)
  
  if (status_login==200):
    status=True
    
  print('get token')
else:
  print('ERROR TO GET TOKEN')
  
time = datetime.datetime.now()
counter = 0
 
while status:

  timer = verify_time(time)
  
  
  #---------------- NODE PARAMS (GET) ------------------------
  if(int(timer)==5):
    params,status_node_params = get_node_params(token) 
    
    print(params)
    print('get params')
    
    time = datetime.datetime.now()
    counter = counter + 1
    print(f'contador = {counter} às {time}')
    
    if (status_node_params != 200):
      status=False
      print("STATUS NODE PARAMS ERROR")

print('ERROR TO GET NODE PARAMS')


