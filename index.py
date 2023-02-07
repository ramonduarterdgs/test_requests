#---------------- Bibliotecas-------------------
import requests
import json
import datetime

#---------------- Variáveis -------------------
token = ''
timer_verif = 1   # TEMPO PARA REALIZAR A AQUISIÇÃO DE DADOS
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

  request_token = requests.post('https://api.rainmaker.espressif.com/v1/login',json=user )

  response_json = request_token.json()

  status_login = request_token.status_code

  token = response_json['accesstoken']
  
  return token,status_login

def get_node_params(token):
  header = {
    "Authorization": token ,
    "accept": "application/json"
  }

  request_params = requests.get('https://api.rainmaker.espressif.com/v1/user/nodes/params?node_id=3hz9vsqog8Fi88LNvGhMke',headers=header)

  response_json = request_params.json()
  
  status_node_params = request_params.status_code
  
  return response_json,status_node_params

def verify_time(time_data):
  time_now = datetime.datetime.now()
  time_delta = time_now - time_data
  minute_delta = (time_delta.total_seconds()) / 60
  #print(f'minute_delta é de {minute_delta}')
  return minute_delta

def clean_data(params,count):
  agua_bruta = params['IFC050 Água Bruta']
  contador1_agua_bruta = agua_bruta['Contador 01: Leitura  (m³)']
  print(f'Contador 1 Água Bruta : tipo é: {type(contador1_agua_bruta)} e o valor é {contador1_agua_bruta}')
    
  agua_tratada = params['IFC050 Água Tratada']
  contador1_agua_tratada = agua_tratada['Contador 01: Leitura  (m³)  ']
  print(f'Contador 1 Água Tratada : tipo é: {type(contador1_agua_tratada)} e o valor é {contador1_agua_tratada}')
    
  soft_starter = params['SSW-07 Soft-Starter']
  potencia_soft_starter = soft_starter['Potência Aparente de Saída [KVA]']
  print(f'Potência Aparente de Saída Soft Starter : tipo é: {type(potencia_soft_starter)} e o valor é {potencia_soft_starter}')
  
  file = open("db_test.txt", "a+")
  file.write(f'{count};')
  file.write(f'{datetime.datetime.now()};')
  file.write(f'{contador1_agua_bruta};')
  file.write(f'{contador1_agua_tratada};')
  file.write(f'{potencia_soft_starter}\n') 
  file.close()
  

file = open("db_test.txt", "a+")
file.write(f'N_Aquisicao;Data | Hora;Contador 1 Agua Bruta;Contador 1 Agua Tratada;Potencia Soft-Starter\n')
file.close()


while True:
 
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
    if(int(timer)==timer_verif):   ## AQUI SE DEFINI
      counter = counter + 1
      
      params,status_node_params = get_node_params(token) 
      clean_data(params,counter)
      
      print(params)
      print('get params')
      print(f'contador = {counter} às {time}')
      time = datetime.datetime.now()

      if (status_node_params != 200):
        status=False
        print("STATUS NODE PARAMS ERROR")

  print('ERROR TO GET NODE PARAMS')


