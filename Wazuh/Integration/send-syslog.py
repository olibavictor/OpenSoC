import socket
import time

# Configurações do servidor syslog remoto
remote_host = 'endereco_do_servidor'  # Substitua pelo endereço do servidor syslog
remote_port = 514  # Porta padrão do syslog

# Nível de severidade e mensagem a serem enviados
severity = 'info'
message = 'Exemplo de mensagem syslog enviada via Python'

# Formato da mensagem syslog PRI - '<PRI> TIMESTAMP HOSTNAME APPNAME MSGID'
# Definindo o PRI com base no nível de severidade
pri = 13  # Calculado como 10 * Facility + Severity
pri = pri << 3  # Deslocamento para a esquerda de 3 bits

# Criando a mensagem syslog completa
current_time = time.strftime('%b %d %H:%M:%S')
hostname = socket.gethostname()
appname = 'python_script'
msgid = '-'
syslog_msg = f'<{pri}> {current_time} {hostname} {appname} {msgid} - {severity.upper()}: {message}'

# Criando um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Enviando a mensagem para o servidor syslog remoto
    sock.sendto(syslog_msg.encode(), (remote_host, remote_port))
    print('Mensagem syslog enviada com sucesso.')
except Exception as e:
    print('Erro ao enviar mensagem syslog:', e)
finally:
    sock.close()
