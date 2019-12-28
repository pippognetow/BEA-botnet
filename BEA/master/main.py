import botogram
import time
from status import botnet_status, send_commands, download_requirements

def returnPos(list, id):
    pos = 0
    for item in list:
        if id == item:
            pos = list.index(item)
            break
    return pos

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

token = loadVar("assets/token.txt")
bot = botogram.create(token)

@bot.command("excec")
def excec(chat, message, args):
    bots = loadList("assets/botslist.txt", "str")
    tokens = loadList("assets/botstokens.txt", "str")
    if len(args) > 0:
        for instance in bots:
            pos = returnPos(bots, instance)
            mex = chat.send("<code>Worker " + str(pos+1) + "</code>\nExcecuting...")
            send_commands(instance, tokens[pos], " ".join(args))
            mex.delete()
    else:
        for instance in bots:
            pos = returnPos(bots, instance)
            mex = chat.send("<code>Worker " + str(pos+1) + "</code>\nExcecuting...")
            send_commands(instance, tokens[pos], None)
            mex.delete()
    chat.send("Done")

@bot.command("update")
def update(chat, message, args):
    bots = loadList("assets/botslist.txt", "str")
    tokens = loadList("assets/botstokens.txt", "str")
    if len(args) > 0:
        if args[0] == "master":
            for instance in bots:
                pos = returnPos(bots, instance)
                mex = chat.send("<code>Worker " + str(pos+1) + "</code>\nDownloading Files...")
                download_requirements(instance, tokens[pos], "master", pos)
                mex.delete()
    else:
        for instance in bots:
            pos = returnPos(bots, instance)
            mex = chat.send("<code>Worker " + str(pos+1) + "</code>\nDownloading Files...")
            download_requirements(instance, tokens[pos], None, pos)
            mex.delete()

@bot.command("whoslistening")
def whoslistening(chat, message):
    channelToken = loadVar("assets/channelToken.txt")
    bots = loadList("assets/botslist.txt", "str")
    tokens = loadList("assets/botstokens.txt", "str")
    nrOnline = 0
    btns = botogram.Buttons()
    id = loadVar("assets/lastMessage.txt")
    try:
        bot.chat(channelToken).delete_message(id)
    except:
        pass
    mex = bot.chat(channelToken).send("🌐 Retrieving data...")
    for instance in bots:
        pos = returnPos(bots, instance)
        online, cpuUsage, resetData, resetTime = botnet_status(instance, tokens[pos])
        if online == True:
            nrOnline += 1
            btns[int(pos/5)].callback("✅", "online", str(pos))
        else:
            btns[int(pos/5)].callback("❌", "offline", str(pos))
    mex.edit("BOTNET STATUS\nBOTS: " + str(nrOnline) + "/" + str(len(bots)), attach=btns)
    writeVar("assets/lastMessage.txt", mex.id)
    bot.chat(channelToken).pin_message(mex.id)
    bot.chat(channelToken).delete_message(mex.id + 1)

@bot.callback("goback")
def goback(chat, message):
    bots = loadList("assets/botslist.txt", "str")
    tokens = loadList("assets/botstokens.txt", "str")
    nrOnline = 0
    btns = botogram.Buttons()
    message.edit("🌐 Retrieving data...")
    for instance in bots:
        pos = returnPos(bots, instance)
        online, cpuUsage, resetData, resetTime = botnet_status(instance, tokens[pos])
        if online == True:
            nrOnline += 1
            btns[int(pos/5)].callback("✅", "online", str(pos))
        else:
            btns[int(pos/5)].callback("❌", "offline", str(pos))
    message.edit("BOTNET STATUS\nBOTS: " + str(nrOnline) + "/" + str(len(bots)), attach=btns)

@bot.callback("online")
def online(query, chat, message, data):
    bots = loadList("assets/botslist.txt", "str")
    tokens = loadList("assets/botstokens.txt", "str")
    btns = botogram.Buttons()
    btns[0].callback("Go Back", "goback")
    message.edit("🌐 Retrieving data...")
    online, cpuUsage, resetData, resetTime = botnet_status(bots[int(data)], tokens[int(data)])
    message.edit("<code>Worker " + str(int(data) + 1) + "</code>\n<b>USER:</b> <code>" + bots[int(data)] + "</code>\n<b>USAGE:</b> " + cpuUsage + " seconds\n<b>RESET @ </b>" + resetTime, attach=btns)

@bot.callback("offline")
def offline(query, chat, message):
    query.send("❌ Bot Offline")

if __name__ == "__main__":
    bot.run()
