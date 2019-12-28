import requests, re

def botnet_status(username, token):
    online = True
    response = requests.get('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(username=username), headers={'Authorization': 'Token {token}'.format(token=token)})
    if response.status_code == 200:
        consoles = re.split(":|,",response.content.decode("UTF-8"))
        if len(consoles) == 1:
            online = False
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
    response = requests.get('https://eu.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(username=username), headers={'Authorization': 'Token {token}'.format(token=token)})
    if response.status_code == 200:
      data = re.split(",|:|{|}", response.content.decode("UTF-8"))
      cpuUsage = str(int(float(data[-2])))
      resetData = re.split("-",str(data[4])[1:-3])
      resetData = resetData[-1] +"-"+ resetData[1] +"-"+ resetData[0]
      resetTime = str(int(str(data[4])[-2:])+1) +":"+ data[5]
      return online, cpuUsage, resetData, resetTime
    else:
      print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

def download_requirements(username, token, level):
    response = requests.get('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(username=username), headers={'Authorization': 'Token {token}'.format(token=token)})
    if response.status_code == 200:
        consoles = re.split(":|,",response.content.decode("UTF-8"))
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
    id = consoles[1]
    obj = {"input":"pip3 install --user botogram2\n"}
    requests.post('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(username=username, id=id), headers={'Authorization': 'Token {token}'.format(token=token)}, data=obj)
    obj = {"input":"cd\nrm -rf BEA-botnet\ngit clone https://github.com/pippognetow/BEA-botnet\n"}
    requests.post('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(username=username, id=id), headers={'Authorization': 'Token {token}'.format(token=token)}, data=obj)
    obj = {"input":"cd BEA-botnet/BEA/bots\necho BOTOGRAM_TOKEN > assets/token.txt\necho CHANNEL_ID > assets/channelToken.txt\n"}
    requests.post('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(username=username, id=id), headers={'Authorization': 'Token {token}'.format(token=token)}, data=obj)
    if level == "master":
        username = "MASTER_BOT_USERNAME"
        token = "MASTER_BOT_API_ID"
        response = requests.get('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(username=username), headers={'Authorization': 'Token {token}'.format(token=token)})
        if response.status_code == 200:
            consoles = re.split(":|,",response.content.decode("UTF-8"))
        else:
            print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
        id = consoles[1]
        obj = {"input":"\3cd\nrm -rf BEA-botnet\ngit clone https://github.com/pippognetow/BEA-botnet\ncd BEA-botnet/BEA/master\necho BOTOGRAM_TOKEN > assets/token.txt\necho CHANNEL_ID > assets/channelToken.txt\necho 0 > assets/lastMessage.txt\npython3 main.py\n"}
        requests.post('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(username=username, id=id), headers={'Authorization': 'Token {token}'.format(token=token)}, data=obj)

def send_commands(username, token, commands):
    response = requests.get('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(username=username), headers={'Authorization': 'Token {token}'.format(token=token)})
    if response.status_code == 200:
        consoles = re.split(":|,",response.content.decode("UTF-8"))
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
    id = consoles[1]
    if commands == None:
        obj = {"input":"cd BEA-botnet/BEA/bots\npython3 main.py\ncd\n"}
    else:
        obj = {"input":commands}
    requests.post('https://eu.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(username=username, id=id), headers={'Authorization': 'Token {token}'.format(token=token)}, data=obj)
