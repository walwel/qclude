#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
import smtplib  
import time
from email.mime.text import MIMEText  
 
def send_mail(to_list,sub,content):
    mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
    mail_user="fsh_walwal"                           #用户名  
    mail_pass="658250..qq"                             #密码      
    mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com 
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)                            #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
if __name__ == "__main__":
    mailto_list=['1205376237@qq.com']           #收件人(列表)
    warning='''时间：%s
    空闲：12
    使用：13
    故障：12
    ''' % time.strftime("%c")   
    for i in range(1):                             #发送1封，上面的列表是几个人，这个就填几  
        if send_mail(mailto_list,"浴室故障提示",warning):  #邮件主题和邮件内容   
            print "done!"  
        else:  
            print "failed!" 
