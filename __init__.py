import time
import socket
import logging
from typing import List, Union
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException

logger = logging.getLogger(__name__)

class ServerError(Exception):
    """
    An exception class for exceptional behavior that occurs while working with servers.
    """
    pass

class MySSHClient(object):
    """
        Client to communicate with remote servers via SSH
    """

    def __init__(self, host: str, port: str, user: str , ssh_key: str) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.ssh_key = ssh_key
        self.client = None
        self.session = None
        self.conn_attempts = 10

    def __exit__(self) -> None:
        self._disconnect()

    def _connect(self) -> SSHClient:
        """
            Open connection to remote server
        """
        if self.session is None:
            for tries in range(self.conn_attempts):
                try:
                    self.client = SSHClient()
                    self.client.load_system_host_keys()
                    self.client.set_missing_host_key_policy(AutoAddPolicy())
                    self.client.connect(
                        self.host,
                        self.port,
                        username=self.user,
                        key_filename=self.ssh_key,
                        look_for_keys=True,
                        timeout=5000
                    )
                    break
                except (AuthenticationException,  SSHException) as e:
                    logger.error(f'Unable to authenticate with remote server: {e}')
                    raise e
                except (socket.error, EOFError):
                    logger.error(f'Connection refused, retrying...')
                    time.sleep(tries + 1)
            else:
               raise ValueError(f'Connection refused {self.session_attempts} times, giving up')
        return self.client

     def _disconnect(self) -> None:
        """
            Close SSH connection
        """
        self.client.close()

    def send_commands_to_server(self, commands: Union[str, list]):
        """
            Execute multiple commands to the server

            :param commands: Linux commands
            :type commands: List[str]
        """
        self.session = self._connect()
        cmd = '; '.join(commands)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        result = (stdout.read().decode('utf-8').splitlines())
        return result
