#coding:utf-8
import MySQLdb
import time
'''user mode change'''
#connetc mysqldb
def open_db():
    try:
        conn = MySQLdb.connect(
            host = "localhost",
            user = "root",
            passwd = "662906..qqfsh",
            port = 3306,
            db = "dlzt",
            charset = "utf8",
        )
        cursor = conn.cursor()
        return conn,cursor
    except:
        print(">>>failed to connect mysql")

#update db
def update_db(conn, cursor, sql):
    sta = cursor.execute(sql)
    conn.commit()
    return sta

#close db
def close_db(conn,cursor):
    cursor.close()
    conn.close()
#chick position
def chick_position(type,mode):
    conn_node, cursor_node = open_db()
    csql = 'select position from node where stat=1 and mode=%d' % mode
    number = cursor_node.execute(csql)
    if number > 0:
        if type:
            post = cursor_node.fetchall()
            Usql = "update node set stat=%d where position=%d" % (2,post[0][0])
	    update_db(conn_node, cursor_node, Usql)
            close_db(conn_node, cursor_node)
            print("返回空位号%d" % post[0][0])
            return post[0][0]
        else:
            return number
    else:
        close_db(conn_node, cursor_node)
        print("无空位，返回NULL")
        return 'null'
#chick_user
def chick_user(user_name):
    conn_node, cursor_node = open_db()
    sql = 'select count,ctimes,position,mode from users where user_name="%s"' % user_name
    exist = cursor_node.execute(sql)
    print(exist,type(exist),exist==1L)
    if exist == 1:
        count, ctimes, position,mode = cursor_node.fetchall()[0]
        print("用户存在")
        return count, ctimes, position, mode
    else:
        #print("用户不存在")
        return 'n','n','n','n'
#解锁
def release_pos(user_name):
    conn_u,cursor_u = open_db()
    csql = "select ctimes,mode,position from users where user_name='%s'" % user_name
    print ("sql ", )
    cursor_u.execute(csql)
    print("release")
    ctimes,mode,position = cursor_u.fetchall()[0]
    if time.time()-ctimes > 30:
	print "time:",time.time(),"ctimes",ctimes
	return "你未占位"
    else:
	rsql = "update node set stat=1 where mode=%d and position=%d" % (mode,position)
	if cursor_u.execute(rsql):
	    conn_u.commit()
	    close_db(conn_u,cursor_u)
	    return "位置%d解锁成功" % position
	else:
	    close_db(conn_u,cursor_u)
	    return "位置%d解锁失败" % position
    

#help
def help(user_name):
    level = get_level(user_name)
    if level == 0:
	return """查询空位指令：c
预定空位指令：m
解锁预定：q
注：预定成功后，返回置物柜编号，置物柜预留10分钟，超出时间后解除锁定。"""
    elif level == 1:
	return """查询所有当前置物柜使用状态指令：stat
查询所有故障置物柜标号：get bad"""
    elif level == 2:
	return """查询所有当前置物柜使用状态指令：stat
查询所有故障置物柜标号：get bad
显示所有管理员账号：show admin
添加管理员：chmod 1 username
删除管理员：chmod 0 username
注：添加管理员是，该管理员必须已经注册；删除某管理员时执行者权限必须高于该管理员。"""
# get admin level
def get_level(user_name):
    conn_node, cursor_node = open_db()
    show_admin = "select admin from users where user_name='%s'" % user_name
    cursor_node.execute(show_admin)
    level = cursor_node.fetchall()[0][0]
    close_db(conn_node, cursor_node)
    #print "level>>", level
    return level

# change level mdoe = 0,1,2
def chmod(user_name, mode):
    conn_node, cursor_node = open_db()
    change_sql = "update users set admin=%d where user_name='%s'" % (int(mode), user_name)
    cursor_node.execute(change_sql)
    conn_node.commit()
    close_db(conn_node, cursor_node)
    #print "mode>>", mode

#create a user
def create_user(user_name,mode):
    print("begain create %s") % user_name
    create_conn, create_cursor = open_db()
    create_user_sql = "insert into users value ('%s',%d, %d, %d, %d, %d)" % (user_name, 1, 0, 0, mode,0)
    update_db(create_conn, create_cursor, create_user_sql)
    close_db(create_conn, create_cursor)
    print("create is done")

#get_post
def user_get_post(user_name):
    if 8 <= int(time.strftime('%H')) <= 21:
        conn, cursor = open_db()
        print "this is a test"
	count, ctimes, position, mode = chick_user(user_name)
        if isinstance(count, (int,long)):
	    print "2 this a test"
	    if (time.time() - ctimes) < 30:
                #print "你已预定，位置为%d" % position
                return "你已预定，位置为%d" % position
	    elif count > 3:
                #print "今天使用次数达3次,"
                return "今天使用次数达3次"
            else:
		print "3 this is a test "
                post = chick_position(1,mode)
                if post == "null":
                    print "无剩余位置，请稍后再试"
                    return "无剩余位置，请稍后再试"
                elif isinstance(post, (int,long)):
                    print("4 this is a test")
		    Usql = "update users set count=count+1,ctimes=%f,position=%d where user_name='%s'" % (time.time(), post, user_name)
                    update_db(conn, cursor, Usql)
                    print "你的位置为%d,10分钟内有效" % post
                    return "你的位置为%d,10分钟内有效" % post
        else:
            return """用户信息不存在，
            请输入'newm'创建男士账号，
            或输入'newf'创建女士账号
            [注：此账号将会您影响之后的使用，且一旦创建不可修改，请如实填写]"""
    else:
        print "不在营业时间（8:00-17:00）,稍后再试。"
        return "不在营业时间（8:00-17:00）,稍后再试。"

#users order
def orders(user_name,input_str):
    conn,cursor = open_db()
    get_admin = "select user_name from users where admin>0"
    cursor.execute(get_admin)
    admins = cursor.fetchall()
    #是否注册
    count, ctimes, position, mode = chick_user(user_name)
    if count == 'n':
        return """用户信息不存在，
        请输入'newm'创建男士账号，
        或输入'newf'创建女士账号
        [注：此账号将会您影响之后的使用，且一旦创建不可修改，请如实填写]"""
    #是否是管理员
    admin = [a[0] for a in admins]
    if type(user_name).__name__ != 'unicode':
        user_name = user_name.decode('utf-8')
    if user_name in admin:
        if  input_str == 'stat':
            conn.commit()
            stat_sql = "select stat,mode from node"
            cursor.execute(stat_sql)
            stat_data = cursor.fetchall()
            stat_m = [s[0] for s in stat_data if s[1] == 1]
            stat_f = [s[0] for s in stat_data if s[1] == 1]
            return """男浴中故障%d个，空闲%d个，预定%d个，使用%d个；
            女浴中故障%d个，空闲%d个，预定%d个，使用%d个。""" % (stat_m.count(0),stat_m.count(1),stat_m.count(2),stat_m.count(3),stat_f.count(0),stat_f.count(1),stat_f.count(2),stat_f.count(3))
        if input_str == "get bad":
            conn.commit()
            bad_sql = "select position,mode from node where stat=0"
            cursor.execute(bad_sql)
            pos_data = cursor.fetchall()
            pos_m = [s[0] for s in pos_data if s[1] == 1]
            pos_f = [s[0] for s in pos_data if s[1] == 0]
            return "男浴故障有"+str(pos_m)+"女浴故障有"+str(pos_f)
        if input_str == "show admin":
            if get_level(user_name) == 2:
                return admin
            else:
                return "权限不足"
        if input_str[:5] == "chmod":
            if get_level(user_name) == 2:
                input_str = input_str.split(' ')
                if int(input_str[1]) not in [0,1]:
                    return "权限值不在[0,1]之内"
                elif chick_user(input_str[2])[0] == 'n':
                    return "所输用户不存在"
                elif input_str[2] ==  user_name:
                    return("禁止修改自己的权限")
                else:
                    chmod(input_str[2],input_str[1])
                    return "修改成功"
            else:
                return "权限不足"
        else:
            return "未知指令"

    #是否申权
    elif input_str == 'change':
        chmod(user_name,1)
        return "修改成功"
    elif input_str == "m":
        return user_get_post(user_name)
        # 查看空位
    elif input_str == "c":
        return "浴室还有"+str(chick_position(0,mode))+"个空位"
    elif input_str == "q":
	print ("q order")
	return release_pos(user_name)
    else:
        return("未知指令")


if __name__ == "__main__":
    while(1):
        input_str = input("your content>>>")
        user_name = input("your user_name>>>")
        print orders(user_name, input_str)
