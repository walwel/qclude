# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
from youdao_etc import youdao
from ldzt import orders
from ldzt import create_user
from ldzt import help

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is welwel view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "walwal" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument



    def POST(self):
        try:
            webData = web.data()
            #print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
		content = recMsg.Content
		if type(content).__name__ == "unicode":
            	    content = content.encode('UTF-8')
		print ("toUser",toUser,type(toUser),"content",content,type(content))
                if recMsg.MsgType == 'text':
		    #有道词典
		    if content[0] == 'y':
			content = youdao(content[1:]).encode('utf-8')
		    elif content == "test":
		    	content = "toUser>",toUser,"fromUser>",fromUser
		    elif content == "newm":
			print("new %s") % content
			create_user(toUser,1)
			content = "创建成功"
		    elif content == "newf":
			print("create %s") % content
			create_user(toUser,0)
                        content = "创建成功"
		    elif content == "help":
			content = help(toUser)
		    else:
			content = orders(toUser,content)
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
		    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
	    else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
