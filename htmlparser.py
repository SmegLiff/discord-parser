################## PUT INPUT / OUTPUT DIRECTORY HERE ###################

logdir = ""
resultdir = ""

####### CODE SPAGHETTI BELOW THIS LINE DON'T EVEN BOTHER TO LOOK ######


import os
from html.parser import HTMLParser

messageinfo = ["", "", "", "", "", ""] # high quality data processing
lastauthor = ["", "", ""] # ah yes this definitely makes sense
isMessage = False
isTimestamp = False
isReaction = False
nestedSpanCount = 0 # oh my god
nestedDivCount = 0 # i have accepted my fate
attachmentCount = 0 # rarely anyone uses multiple attachments on a single message tbh

def writeData():
    global messageinfo
    global lastauthor
    if messageinfo[0] == "":
        del messageinfo[0:4]
        messageinfo = lastauthor + messageinfo
    line = ""
    for value in messageinfo:
        line += "\'" + value + "\'" + ','
    line = line[:-1]
    line = line.replace("\n\n", "\n")
    line += "\n"
    result.write(line)
    lastauthor = messageinfo[0:4]
    messageinfo = ["", "", "", "", "", ""]

class MultiColliderSuperParser(HTMLParser): # fucking hell
    def handle_starttag(self, tag, attrs):
        global isMessage
        global isTimestamp
        global isReaction
        global nestedSpanCount
        global nestedDivCount
        global attachmentCount
        if tag == "span":
            if ('class', 'chatlog__author-name') in attrs:
                messageinfo[0] = attrs[2][1]
                messageinfo[1] = attrs[1][1]
            elif ('class', 'chatlog__timestamp') in attrs:
                isTimestamp = True
            elif ('class', 'markdown') in attrs:
                isMessage = True
            if isMessage:
                nestedSpanCount += 1 # hell.
        elif tag == "div":
            if ('class', 'chatlog__reactions') in attrs:
                isReaction = True
                nestedDivCount += 1
                attachmentCount = 0
            elif ('class', 'chatlog__attachment') in attrs:
                attachmentCount = 2 # Yes.
            elif ('class', 'chatlog__message') in attrs or ('class', 'chatlog__messages') in attrs: # two different things you see
                if messageinfo[3] != "":
                    writeData()
        elif tag == "img":
            if ('class', 'emoji emoji--small') in attrs and isReaction:
                messageinfo[5] += attrs[2][1]
                nestedDivCount += 1
        elif tag == "a":
            if attachmentCount > 0:
                messageinfo[4] += attrs[0][1] + ", "



                

    def handle_endtag(self, tag):
        global isMessage
        global isReaction
        global nestedSpanCount
        global nestedDivCount
        global attachmentCount
        if tag == "span" and isMessage:
            nestedSpanCount -= 1
            if nestedSpanCount == 0:
                isMessage = False
        if tag == "div" and isReaction:
            nestedDivCount -= 1
            if nestedDivCount == 0:
                isReaction = False
                messageinfo[5] = messageinfo[5][:-2]
        if tag == "div" and attachmentCount > 0:
            attachmentCount -= 1


    def handle_data(self, data):
        global isMessage
        global isTimestamp
        if isTimestamp: # immensely stupid way to find the message but it works so
            messageinfo[2] = data
            isTimestamp = False
        if isMessage: # ditto
            data = data.replace("\'", '\"')
            messageinfo[3] += data
        if isReaction: # ditto
            data = data.replace("\n", "")
            data = data.replace(" ", "")
            if data != "":
                messageinfo[5] += "(" + data + "), "

for filename in os.listdir(logdir):
    chatlog = open(logdir + "/" + filename, "r", encoding="utf8")
    result = open(resultdir + "/" + filename.strip("html") + "csv", "w", encoding="utf8")
    parser = MultiColliderSuperParser()
    parser.feed(chatlog.read())
    chatlog.close()
    result.close()
