#!/usr/bin/python3

import socket
import time

remote_host = 'endereco_do_servidor'  #Substitua pelo endereço do servidor syslog
remote_port = 514  #Porta padrão do syslog

syslog_msg = f'{message}'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.sendto(syslog_msg.encode(), (remote_host, remote_port))
    print('Mensagem syslog enviada com sucesso.')
except Exception as e:
    print('Erro ao enviar mensagem syslog:', e)
finally:
    sock.close()
