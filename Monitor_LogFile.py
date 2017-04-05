# coding=utf-8
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import linecache
import Send_Mail
from warnings import catch_warnings


#**********配置开始***************
search_keywords = ["ERROR", "Exception","Debug"]  # 搜索关键字
area = 50  # 截取关键字的前50行、后50行
sleep_time = 60  # 搜索频率时间，如等待60秒，进行下一次搜索
logfile = "c:/debug.log.2016-09-17.log"  # 搜索日志文件
outfile = "c:/error.log"  # 生成查找后关键字文件

smtpserver = 'smtp.qiye.163.com'  # 邮件服务器
sender_username = ''  # 邮件发送者账号
sender_password = ''  # 邮件发送者密码

mail_to = ["xxxx.sz@mopon.cn"]  # 邮件接受人
mail_cc = []  # 邮件接受人
mail_bcc = []


#**********配置结束***************




attachment = [outfile] 
subject = "系统错误日志信息"
msg_body = ""
# 获取文件最大行数
def get_file_max_line(file_path):
    max_count = 0;
    with open(file_path) as file:
        for line in file:
            max_count = max_count + 1
    return max_count

#获取错误行号
def get_error_line(file_path, start_line, end_line, error_keys):
    error_index = "";
    error_index_lists=[]
    for index in range(len(error_keys)):
        for lines_num in range(start_line,end_line):
            lines_str=linecache.getline(file_path,lines_num)
            if(search_keywords[index].upper() in lines_str.upper()):
                error_index_lists.append(lines_num)
               
   
    return error_index_lists


# 计算起始行号和结束行号
def get_error_start_end_line(file_path, line_NO, area):
    file_line_count = get_file_max_line(file_path)
    start_line = 0 if line_NO - area <= 0 else line_NO - area; 
    end_line = line_NO + area if line_NO + area < file_line_count else file_line_count; 
    return start_line, end_line
     

# 通过行号获取指定文件内容
def get_file_content(file_path, start_line, end_line):
    temp_str = "";
    linecache.checkcache(file_path)
    str = linecache.getlines(file_path)[start_line:end_line]
    for iTxt in str:
        temp_str = temp_str + iTxt
    
    linecache.clearcache()  # 清理缓存   
    return temp_str
def Send_Email():
    SendEmail2(sender_username, sender_password, subject, msg_body, mail_to, mail_cc, mail_bcc, attachment, smtpserver)
    
    
    
    
def SendEmail2(sender, password, subject, msg_body, mail_to=[], mail_cc=[], mail_bcc=[], attachment=[], smtpserver="smtp.qiye.163.com"):
    #******************统计用例结果********************
    msg_body = "Hi All<br>" 
    msg_body = msg_body + '&nbsp; &nbsp;<span style="font-weight:bold;">系统错误信息，详情请查验附件，请勿回复！</span><br>'

    message = MIMEMultipart()
    message.attach(MIMEText(msg_body, 'html', 'utf-8'))  # 邮件体
    # 添加附件
    try:
        attLen = len(attachment)
    except:
        print "请正确输入附件路径"
    if(attLen > 0):
        for i in range(0, attLen):
            att_str = attachment[i]
            if isinstance(att_str, basestring):
                att_str_arr = att_str.split("/")
                att = MIMEText(open(att_str, 'rb').read(), 'plain', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename=' + att_str_arr[len(att_str_arr) - 1]
                message.attach(att)
            

    if mail_to:
        message["To"] = ",".join(mail_to)
    if mail_cc:
        message["Cc"] = ",".join(mail_cc)
    if mail_bcc:
        message["Bcc"] = ",".join(mail_bcc)
    if len(mail_cc) > 0:
        mail_to = mail_to + mail_cc
    if len(mail_bcc) > 0:
        mail_to = mail_to + mail_bcc
    receiver = mail_to
    message["from"] = sender

    # subject = '幸福蓝海自动化测试报告'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, message.as_string())
        
    except Exception , e:
        print e
     
    finally:
        smtp.quit() 
        


#获取错误日志，生成文件，发送邮件
def get_error_log():
    max_old = get_file_max_line(logfile);
    print "max_old ",max_old
    while (True):
        try:
            time.sleep(sleep_time);
            max_new = get_file_max_line(logfile);
             
            error_line_list = get_error_line(logfile, max_old, max_new, search_keywords)
            if len(error_line_list)<=0:
                continue
            try:
                if(os.path.exists(outfile)):
                    os.remove(outfile)
            except:
                print ""
            new_file = open(outfile, 'wt') 
            for line_no in error_line_list:
                line = get_error_start_end_line(logfile, line_no, area)
                content = get_file_content(logfile, line[0], line[1])
                new_file.write(content)
            new_file.flush()
            new_file.close()
            Send_Email()
            max_old = max_new
            print "max_old ",max_old
            print "max_new ",max_new
        except Exception , e:
            print e
if __name__ == "__main__":
   get_error_log()
      




