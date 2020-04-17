################## PUT INPUT / OUTPUT DIRECTORY HERE ###################

logdir = ""
resultdir = ""

####### CODE SPAGHETTI BELOW THIS LINE DON'T EVEN BOTHER TO LOOK ######

import os

def CSVCroncher():
    text = csv.read()
    textlist = text.split("\'\n\'")
    header = ""
    for item in textlist:
        # item = "\'" + item + "\'"
        chatinfo = item.split("\',\'")
        if  ("[" + chatinfo[2] + "]\n") != header:
            header = "\n[" + chatinfo[2] + "] " + chatinfo[1] + "\n"
            result.write(header)
        result.write(chatinfo[3] + "\n")
        if chatinfo[4] != "":
            attachments = chatinfo[4].split(",")
            for attachment in attachments:
                vibecheck = attachment.replace("\n", "")
                vibecheck = vibecheck.replace(" ", "")
                if vibecheck != "":
                    result.write("Attachment: " + attachment + "\n")
    

for filename in os.listdir(logdir):
    csv = open(logdir + "/" + filename, "r", encoding="utf8")
    result = open(resultdir + "/" + filename.strip("csv") + "txt", "w", encoding="utf8")
    CSVCroncher()
    csv.close()
    result.close()