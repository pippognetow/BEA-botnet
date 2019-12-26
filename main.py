import botogram
import requests
import socket

def loadVar(file):
    with open(file, "r") as file:
        var = str(file.read()).rstrip("\n")
    return var

token = loadVar("token.txt")
bot = botogram.create(token)

if __name__ == "__main__":
  channelToken = loadVar("channelToken.txt")
  IPAddr = socket.gethostbyname(socket.gethostname())
  ip = requests.get('https://checkip.amazonaws.com').text.strip()
  bot.chat(channelToken).send(str(IPAddr) + " | " + str(ip) + " listening!")
