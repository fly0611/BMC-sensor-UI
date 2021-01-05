import subprocess
import time

ipmi = r'E:\fiberhome\ipmitool-1.8.18\ipmitool.exe'
cmd = r'%s -I lanplus -U ADMIN -P ADMIN -H 10.73.37.170 sensor' % ipmi

def Time():
    return time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

flie_name = r'ipmitool_get_sensor_%s.csv' % Time()
def GetCommand(cmd):
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = data.stdout.readlines()
    return data

def Wfile(file):
    with open(flie_name,'a+') as f:
        f.write(file)

title = []
database = [] 
def GitDate(data):
    for i in data:
        data = bytes.decode(i).split('|')
        a = data[1].lstrip().rsplit()
        if data[1].lstrip().rsplit()[0].startswith(('na','0x')) == False:
            title.append(data[0].lstrip().rsplit()[0])
            database.append(data[1].lstrip().rsplit()[0])
    return title,database

#先获取cpu温度，如果cpu温度为N/A则等待，说明未近系统活开机中，
while True:
    data = GetCommand(cmd)
    cpu_temp = bytes.decode(data[0]).split('|')[1].lstrip().rsplit()
    if cpu_temp[0] != 'na':
        print('please 10s...')
        time.sleep(10)
        title,database = GitDate(data)
        title_count = len(title)
        title = []
        database = []
        break
    else:
        print('Please turn on the power.....')
        time.sleep(5)


flage = 0 
while True:
    data = GetCommand(cmd)
    title,database = GitDate(data)
    if flage == 0:
        t = 'TIME' + ',' + ','.join(title)
        print(t)
        Wfile(t + '\n')
        flage = 1

    if title_count == len(database):
        d = Time() +',' + ','.join(database)
        print(d)
        Wfile(d + '\n')
    title = []
    database = []
    time.sleep(1) 



