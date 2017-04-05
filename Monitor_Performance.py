#coding=utf-8
import psutil
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import time


#***********配置开始***************
cpu_limit_rate=80;#设置内存发送邮件的最大使用率阀值
mem_limit_rate=80 #设置内存发送邮件的最大使用率阀值
monitor_time=60 #获取cpu，内存使用率间隔时间

smtpserver = 'smtp.qiye.163.com'
sender_username = ''
sender_password = ''
subject="知景区测试服务器CPU或内存告警"
mail_to=["xxxx.sz@mopon.cn"]
mail_cc=["xxxx.sz@mopon.cn"]
#***********配置结束***************



 
msg_body="Hi All<br>" 
msg_body=msg_body+'&nbsp; &nbsp;<span style="font-weight:bold;">系统CPU、内存信息，请勿回复！</span><br>'
mail_cc=[]
mail_bcc=[]
attachment=[] 

mem_rate=0;
cpu_rate=0;

def getMemorystate(): 
    #svmem(total=8436072448L, available=3321212928L, percent=60.6, used=5114859520L, free=3321212928L)
    return  psutil.virtual_memory()[2]


def getCpuState(): 
    #svmem(total=8436072448L, available=3321212928L, percent=60.6, used=5114859520L, free=3321212928L)
    #print psutil.cpu_percent(interval=1, percpu=True)
        #print psutil.cpu_percent(interval=1)
    return psutil.cpu_percent(interval=1);
   

def Send_Email():
    SendEmail2(sender_username,sender_password,subject,msg_body,mail_to,mail_cc,mail_bcc,attachment,smtpserver)

def SendEmail2(sender,password,subject,msg_body,mail_to = [],mail_cc = [],mail_bcc = [],attachment =[],smtpserver = "smtp.qiye.163.com"):
    msg_body=msg_body+'&nbsp; &nbsp;<span style="font-weight:bold;">CPU使用率：</span>'+str(mem_rate)+"%<br>"
    msg_body=msg_body+'&nbsp; &nbsp;<span style="font-weight:bold;">Memory使用率：</span>'+"<font color=#2E8B57>"+str(cpu_rate)+"%</font><br>"
    message = MIMEMultipart()
    
    message.attach(MIMEText(msg_body, 'html', 'utf-8')) #邮件体
    #添加附件
    try:
        attLen=len(attachment)
    except:
        print "请正确输入附件路径"
    if(attLen>0):
        for i in range(0,attLen):
            att_str=attachment[i]
            if isinstance(att_str,basestring):
                att_str_arr=att_str.split("/")
                att=MIMEText(open(att_str, 'rb').read(), 'plain', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename='+att_str_arr[len(att_str_arr)-1]
                message.attach(att)
            

    if mail_to:
        message["To"] = ",".join(mail_to)
    if mail_cc:
        message["Cc"] = ",".join(mail_cc)
    if mail_bcc:
        message["Bcc"] = ",".join(mail_bcc)
    if len(mail_cc)>0:
        mail_to = mail_to + mail_cc
    if len(mail_bcc)>0:
        mail_to = mail_to + mail_bcc
    receiver=mail_to
    message["from"] = sender

    #subject = '幸福蓝海自动化测试报告'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, message.as_string())
        
    except Exception ,e:
        print e
     
    finally:
        smtp.quit() 
        
        
def monitor_info():       
    global cpu_rate
    global mem_rate
    while(True):
        cpu_rate=getCpuState()
        mem_rate=getMemorystate()
        if(cpu_rate>cpu_limit_rate or mem_rate>=mem_limit_rate):
            Send_Email()
        time.sleep(monitor_time)
if __name__ == "__main__":
    monitor_info()
      


