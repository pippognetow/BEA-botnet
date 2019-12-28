import botogram
import time

def loadList(file, type):
    if type == "int":
        with open(file, "r") as file:
            list = [int(line.rstrip("\n")) for line in file]
    else:
        with open(file, "r") as file:
            list = [line.rstrip("\n") for line in file]
    return list
    
def loadVar(file):
    with open(file, "r") as file:
        var = str(file.read()).rstrip("\n")
    return var
    
def writeVar(file, var):
    with open(file, "w+") as file:
        file.write(str(var))

token = loadVar("token.txt")
bot = botogram.create(token)

if __name__ == "__main__":
    channelToken = loadVar("channelToken.txt")
    bots = loadList("assets/bots.txt", "str")
    tokens = loadList("assets/botstoken.txt", "str")
    nrOnline = 0
    btns = botogram.Buttons()
    id = loadVar("lastMessage.txt")
    try:
        bot.chat(channelToken).delete_message(id)
    except:
        pass
    mex = bot.chat(channelToken).send("🌐 Retrieving data...")
    for bot in bots:
        pos = returnPos(bots, bot)
        online, cpuUsage, resetData, resetTime = botnet_status(bot, tokens[pos])
        if online == True:
            nrOnline += 1
            bnts[int(pos/5)].callback("✅", "online", str(pos))
        else:
            bnts[int(pos/5)].callback("❌", "offline", str(pos))
    mex.edit("BOTNET STATUS\nBOTS: " + str(nrOnline) + "/" + str(len(bots)), attach=btns)
    writeVar("lastMessage.txt", mex.id)
    bot.chat(channelToken).pin_message(mex.id)
    
