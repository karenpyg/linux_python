#!/usr/bin/env python3.10

from typing import List
from paramiko import AutoAddPolicy, RSAKey, SSHClient
from scp import SCPClient, SCPException
from os import system
from paramiko.auth_handler import AuthenticationException, SSHException
import logging

"""Client to interact with a remote host via SSH & SCP."""
class RemoteClient:

    def __init__(self,host: str,user: str,password: str,port :int, ssh_key_filepath: str,remote_path: str,):
                
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        logging.basicConfig(filename='dool.log', level=logging.DEBUG)
        # to prevent every function from calling connection 
        self.connection()


    # open connection to remote host
    # @property
    def connection(self):
        try:
            client = SSHClient()
            client.load_system_host_keys()

            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                self.host,
                username=self.user,
                password=self.password,
                port=self.port,
                key_filename=self.ssh_key_filepath,
                timeout=5000)
            #if neccesary uncomment the line below (to avoid multiple call to connection method)
            self.client = client
            return client
        except AuthenticationException as e:
            logging.error(
                f"AuthenticationException occurred; did you remember to generate an SSH key? {e}"
            )
        except Exception as e:
            logging.error(
                f"Unexpected error occurred while connecting to host: {e}"
            )

    def disconnect(self):
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()
    
    def execute_commands(self, commands: List[str]):
        """ results and status of the command execution can be seen in log """

        for cmd in commands:
            # if you are running the connection method once before this , then its all good
            # if you uncomment the self.client=client in connection func, then use this line
            stdin, stdout, stderr = self.client.exec_command(cmd)
            # stdin, stdout, stderr = self.connection.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            logging.info('-------------------------------------------------')
            for line in response:
                logging.info(
                    f"INPUT: {cmd}\n \
                    OUTPUT: {line}"
                    )

    # @property
    def scp(self) -> SCPClient:
        conn = self.connection()
        return SCPClient(conn.get_transport())

    def bulk_upload(self, local_filepaths: List[str], remote_fpath=None):
        """
        Upload files to a remote dir.
        the type casting(not the right term though!) done here needs the typing lib to be imported
        """
        try:
            b = self.scp()
            if remote_fpath:
                b.put(local_filepaths, remote_path=remote_fpath, recursive=True)
            else:
                b.put(local_filepaths, remote_path=self.remote_path , recursive=True)
            logging.info(
                f"Finished uploading {len(local_filepaths)} files to {self.remote_path} on {self.host}"
            )
        except SCPException as e:
            logging.error(
                f"SCPException during bulk upload: {e}"
            )
        except Exception as e:
            logging.error(
                f"Unexpected exception during bulk upload: {e}")

    def download_file(self, remote_filepath: str, local_path=None):
        """ filepath: Path to file hosted on remote server to fetch."""
        b = self.scp()
        if local_path:
            b.get(remote_filepath, local_path)
        else:
            b.get(remote_filepath)

# its better to copy the key by hand than execute system commands by code, 
# but the next two  function are doing this 
def get_ssh_key(ssh_key_filepath, ):
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

    """Fetch locally stored SSH key."""
    try:
        ssh_key = RSAKey.from_private_key_file(
            ssh_key_filepath
        )
        logging.info(
            f"Found SSH key at {ssh_key_filepath}"
        )
        return ssh_key
    except SSHException as e:
        logging.error(f"SSHException while getting SSH key: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while getting SSH key: {e}")

def upload_ssh_key(user, ssh_host, ssh_key_filepath, ):
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    try:
        system(
            f"ssh-copy-id -i {ssh_key_filepath}.pub {user}@{ssh_host}>/dev/null 2>&1"
        )
        logging.info(
            f"{ssh_key_filepath} uploaded to {ssh_host}"
        )
    except FileNotFoundError as e:
        logging.error(
            f"FileNotFoundError while uploading SSH key: {e}"
        )
    except Exception as e:
        logging.error(
            f"Unexpected error while uploading SSH key: {e}"
        )


ssh_host = 'ip_address_or_domain_name'
usr = 'user'
passwd = 'password'
# normally sshkey files are stored in ~/.ssh :
ssh_key_filepath = '/home/user/.ssh/id_rsa'
remote_path = '~/remote_path'


if __name__ == '__main__':
    rc = RemoteClient(host=ssh_host, user=usr, password=passwd, port=2122,
                ssh_key_filepath = ssh_key_filepath, remote_path = remote_path,)

    # for executing commands :
    # rc.execute_commands(['ls', 'pwd'])
    # for uploading things :
    # rc.bulk_upload(remote_fpath='/home/d/code/',local_filepaths=['~/cpp/file.cpp', '~/code/cpp/other_file.cpp'])
    # for downloading :
    # rc.download_file(remote_filepath='~/data/sth.py', local_path='~/code/python/')



