import os
import json
import datetime

import s3FileOperation
import sendHttpRequest

token = os.environ["TELEGRAM_BOT_TOKEN"]
chatId1 = os.environ["TELEGRAM_CHAT_ID"]
chatId2 = os.environ["TELEGRAM_CHAT_ID_FOR_ERRORMESSAGE"]



def ypsilon_handler(event, context, token):
    print("==startYpsilon_handler")
    
    chatId = chatId1
    resBody_json = sendHttpRequest.getChat(token, chatId)
    if "title" in resBody_json["result"]:
        title = resBody_json["result"]["title"]
    
    resBody_json = sendHttpRequest.getChatMemberCount(token, chatId)
    chatMemberCount = resBody_json["result"]
    print("chatMemberCount == "+str(chatMemberCount))
    
    fileName = "XFFSRheinNeckar-memberlist/XFFSRheinNeckar-memberlist.json"
    memberList = s3FileOperation.downloadAndReadFile(fileName)
    print("==memberListDownloaded")
    print(type(memberList))
    
    memberList_dict = json.loads(memberList)
    print("==convertedToMemberist_dict")
    print(type(memberList_dict))
    
    numberOfMember = len(memberList_dict)
    print("==numberOfMember: "+str(numberOfMember))
    print(type(numberOfMember))
    
    messageText = "chatMemberCount: "+str(chatMemberCount)+"人、numberOfMember: "+str(numberOfMember)+"人"
    chatId = chatId2
    messageThreadId = None
    sendHttpRequest.sendMessage(token, chatId, messageThreadId, messageText)
    chatId = chatId1
    
    fileName = "empty.json"
    memberList2 = s3FileOperation.downloadAndReadFile(fileName)
    print("==memberListDownloaded")
    print(type(memberList2))
    
    memberList2_dict = json.loads(memberList2)
    print("==convertedToMemberist2_dict")
    print(type(memberList2_dict))
    
    for numberOfMember in range(len(memberList_dict)):
        userId = memberList_dict[numberOfMember]["user_id"]
        print("==userId: "+str(userId))
        print(type(userId))

        resBody_json = sendHttpRequest.getChatMember(token, chatId, userId)
        print(type(resBody_json))

        if resBody_json["ok"] == False:
            messageText = "user ID: " + str(userId) +  " not found in " + title + " (group ID: " + str(chatId) + ")."
            chatId = chatId2
            messageThreadId = None
            sendHttpRequest.sendMessage(token, chatId, messageThreadId, messageText)
            chatId = chatId1
            
            userName = ""
            firstName = ""
            lastName = ""
            status = "not found"
            
        else:
            if "username" in resBody_json["result"]["user"]:
                userName = resBody_json["result"]["user"]["username"]
            else:
                userName = ""
            if "first_name" in resBody_json["result"]["user"]:
                firstName = resBody_json["result"]["user"]["first_name"]
            else:
                firstName = ""
            if "last_name" in resBody_json["result"]["user"]:
                lastName = resBody_json["result"]["user"]["last_name"]
            else:
                lastName = ""
            status = resBody_json["result"]["status"]
            
        userInfo = {
            "user_id":userId,
            "username":userName,
            "first_name":firstName,
            "last_name":lastName,
            "status":status
        }
    
        memberList2_dict.append(userInfo)
        print("==appendUserInfo")
        print(json.dumps(memberList2_dict))
        
    dateNow = datetime.datetime.now()
    dateNowJST = dateNow + datetime.timedelta(hours=+9)
    timestamp = dateNowJST.strftime("%Y%m%d%H%M")
    
    newFileContents = json.dumps(memberList2_dict, ensure_ascii=False, indent=4)
    print("==newFileContents")
    fileName = "XFFSRheinNeckar-memberlist/XFFSRheinNeckar-memberlist"+timestamp+".json"
    s3FileOperation.writeAndUploadFile(newFileContents, fileName)


    print("==endYpsilon_handler")
    return
