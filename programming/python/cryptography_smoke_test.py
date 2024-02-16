from __future__ import print_function

import getpass
import subprocess
import sys
import warnings
import _ssl

# Don't print out warnings from paramiko; it makes it easier to post text
# verbatim to public sites without redacting a ton of info.
warnings.filterwarnings("ignore")

import paramiko
import requests

try:
    input = raw_input
except NameError:
    pass

print("## ldd _ssl.__file__:")
subprocess.call(["ldd", _ssl.__file__])

print("## openssl version:")
subprocess.call(["openssl", "version"])

# Update the next three lines with your
# server's information

print("## paramiko")
host = "localhost"
username = getpass.getuser()
password = getpass.getpass("Password> ")

command = "uname -a; df"
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command(command)
sys.stdout.write(_stdout.read().decode())
client.close()

print("## requests:")
resp = requests.get("https://www.google.com")
resp.raise_for_status()
print("requests:\n", resp.text[:500])
