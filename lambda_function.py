import os

import ypsilon_function
import sendHttpRequest

token = os.environ["TELEGRAM_BOT_TOKEN"]


def lambda_handler(event, context):

    returnData =  {
        "statusCode": 200
    }

    try:
        ypsilon_function.ypsilon_handler(event, context, token)
        
    except Exception:
        import traceback
        traceback.print_exc()
        
        #エラー通知を投げる
        chatId = os.environ["TELEGRAM_CHAT_ID_FOR_ERRORMESSAGE"]
        messageThreadId = None
        messageText = "memberlist-update-functionがエラー出してます"
        sendHttpRequest.sendMessage(token, chatId, messageThreadId, messageText)

    print("==endLamdaHandler")
    print(returnData)
    return returnData
