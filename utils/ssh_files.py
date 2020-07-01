import os, sys, re
import scp, paramiko

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = re.sub(r'\\', '/', SCRIPT_DIR)
SCRIPT_BASE_DIR = os.path.dirname(SCRIPT_DIR)
FILE_NAME = f'{os.path.splitext(os.path.basename(__file__))[0]}.log'
print(f'{SCRIPT_BASE_DIR}/{FILE_NAME}')

SERVER = '40.71.214.228'
USER = 'nvk'
PASSWD = 'password'

LOCAL_REPO_BASE='d:/nkhedkar/'
LOCAL_REPO_PY = f'{LOCAL_REPO_BASE}/remote_setup_files/azure-single-server1'

class SSHClientCls:
  def __init__(self):
    self.ssh = paramiko.SSHClient()
    # self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    self.ssh.connect(SERVER, username=USER, password=PASSWD)
    self.sftp = None

  def close_conn(self):
    self.ssh.close()
    print('Connection closed')

  def run_cmd(self, cmd):
    ssh_session = self.ssh.get_transport().open_session()
    if ssh_session.active:
      ssh_session.exec_command(cmd)
      buffer = (ssh_session.recv(4096)).decode("utf-8")
      print(buffer)
    return

  def open_ftp(self, use_scp=1):
    if not self.sftp:
      if not scp:
        self.sftp = self.ssh.open_sftp()
      else:
        self.sftp = scp.SCPClient(self.ssh.get_transport())

  def close_ftp(self):
    if self.sftp:
      self.sftp.close()

  def upload_files(self, local, to, close_ftp=0):
    self.open_ftp()

    self.sftp.put(local, to)
    if close_ftp:
      self.close_ftp()
    return

scc = SSHClientCls()
scc.run_cmd('pwd')
scc.run_cmd('ls -lth')
scc.run_cmd('sudo rm trusolid-worker-app_1.0.0-1.tar.gz')
scc.run_cmd('ls -lth')
scc.open_ftp(use_scp=1)
scc.upload_files(LOCAL_REPO_PY+'/trusolid-worker-app_1.0.0-1.tar.gz',
  '/home/gensteam/trusolid-worker-app_1.0.0-1.tar')
scc.close_ftp()
scc.run_cmd('ls -lth')
scc.close_conn()
