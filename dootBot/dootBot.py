import time
import random
import re

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import string

serv_ip = "coop.test.adtran.com"
serv_port = 6667
channel = "#test"

try:
    with open("../admin_ip.txt", "r") as infile:
        admin_ip = infile.readline().strip()
except (IOError):
    admin_ip = ""
finally:
    if admin_ip != "":
        print("Admin IP: " + admin_ip)
    else:
        print("WARNING: No Admin IP recognized")

class dootBot(irc.IRCClient):
    nickname = "dootBot"

    def signedOn(self):
        self.join(channel)
        self.__user_list = []
        self.__last_response = 0
        self.__ignore = []
        self.__channel = channel
        print("Channel: " + self.__channel)

        with open("bot_list.txt", 'r') as infile:
            for each in infile:
                self.__ignore.append(each.strip())

        self.__user_list = []

    def luserClient(self, info):
        print(info)

    def userJoined(self, user, channel):
        print("JOINED:", channel, user)
        if user not in self.__user_list:
            self.__user_list.append(user.lower())

    def userLeft(self, user, channel):
        print("LEFT:", channel, user)
        if user in self.__user_list:
            self.__user_list.remove(user.lower())

    def userQuit(self, user, quitMessage):
        print("QUIT:", user)
        if user in self.__user_list:
            self.__user_list.remove(user.lower())

    def userRenamed(self, oldname, newname):
        print(oldname, "is now known as", newname.lower())
        if oldname in self.__user_list:
            self.__user_list.remove(oldname.lower())

        if newname not in self.__user_list:
            self.__user_list.append(newname.lower())

    def privmsg(self, user, channel, message):
        temp_time = time.time()
        if user not in self.__user_list:
            self.__user_list.append(user.lower())

        print(channel, user, message)
        if (temp_time - self.__last_response > 5) or user.split("@")[1] == admin_ip:
            user_name = user.split("!")[0]
            user_ip = user.split("@")[1]

            # ignore list
            if user_name in self.__ignore:
                return

            # pm privilages
            if (channel == self.nickname):
                if user_ip != admin_ip:
                    return
                else:
                    m = re.match(r"(\w+) (\w+)", message)
                    if m:
                        if m.group(1) == "mute":
                            if m.group(2) not in self.__ignore:
                                self.__ignore.append(m.group(2))
                        if m.group(1) == "unmute":
                            if m.group(2) in self.__ignore:
                                self.__ignore.remove(m.group(2))
                    else:
                        self.msg(self.__channel, message)
                    return
            for word in message.split():
                # strip punctuations and lowercase word
                if word == "":
                    pass

                # match rip
                elif re.search(r"(\brip\b)", message.lower()):
                    responses = ["rip", "ripperonie", "merry RIP-mas", "ripripripriprip", "RIP"]
                    self.msg(channel, random.choice(responses))
                    self.__last_response = temp_time
                    return

                # doot doot
                elif re.search(r"(\bdoot\b)", message.lower()):
                    numDoots = message.count("doot")
                    if numDoots > 70:
                        responses = ["...no", "ano", "BOI", "stahp", "Bruh chill"]
                        self.msg(channel, random.choice(responses))
                        return
                    self.describe(channel, "doot " + "doot " * numDoots)
                    self.__last_response = temp_time
                    return

                # achoo
                elif re.search(r"(\bachoo\b|\bsneeze\b|\basneeze\b)", message.lower()):
                    responses = ["bless you %s", "hands %s a tissue"]
                    self.describe(channel, random.choice(responses) % user_name)
                    self.__last_response = temp_time
                    return

                # :hr:
                elif re.search(r"(\b\:hr\:\b|\bhr\b)", message.lower()):
                    responses = ["HR", "BECKY", "MEGAN", "HR HR HR HR"]
                    self.msg(channel, random.choice(responses))
                    self.__last_response = temp_time
                    return

                # show me de way
                elif re.search(r"(\bwey\?*\.*\:*\b)", message.lower()):
                    responses = ["Sho me de wey", "Dat is not de wey", "DIS IS DE WEY", "Where is our queen?", "R u duh queen?"]
                    chance = random.randint(1,100)
                    if chance <= 75:
                        self.msg(channel, random.choice(responses))
                    else:
                        chance = random.randint(1,100)
                        if chance <= 50:
                            self.describe(channel, "cluck " * random.randint(1,20))
                        else:
                            self.describe(channel, "bwah " * random.randint(1,20))
                    self.__last_response = temp_time
                    return

                # # ip test
                # elif re.match(r"test", message.lower()):
                #     print(user.split("@")[1], admin_ip)
                #     if user.split("@")[1] == admin_ip:
                #         self.msg(channel, user.split("!")[0] + random.choice(["is duh queen!", "knows de wey"]))
                #     else:
                #         self.msg(channel, user.split("!")[0] + random.choice(["is duh false queen!", "is not de wey", "spit on the false queen!"]))
                #     return

                # # bless you
                # elif not self.__d.check(word):
                #     chance = random.randint(1,100)
                #     print("CATCH:", word, "chance: " + str(chance))
                #     responses = ["bless you %s", "hands %s a tissue"]
                #     if (chance <= 20):
                #         self.describe(channel, random.choice(responses) % user)
                #         self.__last_response = temp_time
                #     return

                else:
                    return




def main():
    f = protocol.ClientFactory()
    f.protocol = dootBot

    reactor.connectTCP(serv_ip, serv_port, f)
    reactor.run()


if __name__ == "__main__":
    main()

'''
TODO
- add a admin mute command
- do a unmute command too
- make sure mute is done on host name
'''
