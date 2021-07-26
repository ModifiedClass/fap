# 查看服务器信息
# pipenv install paramiko
#/etc/server.ini为默认去查询的ip
import paramiko

""" 
@app.route('/display_server_info', methods=['GET', 'POST'])
def display_server_info():
    ip = []
    p = re.compile(r'(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)')
    if request.method == 'POST'and p.findall(request.form['searchip']):
        ip = p.findall(request.form['searchip'])
    else:
        for line in open('/etc/server.ini'):
            temp = line.replace('\n', '')
            ip.append(temp)
    info = []
    for i in range(0, len(ip)):
        info.append(collect_info(ip[i], 'root', 'xxxxx', 22))
    return render_template('display_server_info.html',info = info, ip = ip) 
"""


#获取远程服务器的信息，主机名等
def collect_info(ip, user, pkey, port):
    info = {}
    ip = ip
    user = user
    pkey = pkey
    port = port

    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()

    ssh.connect(ip, port, user, pkey=key)
    (stdin, stdout, stderr) = ssh.exec_command('hostname')
    hostname = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command('cat /proc/cpuinfo |grep "processor"|wc -l')
    cpuinfo = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command("free -m|grep 'Mem:'|awk '{print $2}'")
    meminfo = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command("uptime |awk -F':' '{print $NF}'")
    loadavg = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command("getenforce")
    getenforce = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command("ulimit -n")
    ulimit = stdout.read()
    (stdin, stdout, stderr) = ssh.exec_command("cat /etc/redhat-release")
    release = stdout.read()
    ssh.close()
    info['hostname'] = hostname
    info['cpuinfo'] = cpuinfo
    info['meminfo'] = meminfo
    info['getenforce'] = getenforce
    info['ulimit'] = ulimit
    info['loadavg'] = loadavg
    info['release'] = release
    return info