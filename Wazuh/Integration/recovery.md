# Recovery alerts.json

O primeiro passo para realizar a recuperação de eventos antigos é trazer os arquivos compactados para dentro do ambiente (servidor manager).

### Compactar os arquvios antigos e enviar para novo servidor

```
cd /var/ossec/logs/alerts/{ano}/
tar -cvf ossec-alerts-{ano}.tar {mes1} {mes2} {mes3}
```

### Dentro do servidor wazuh, coloque os arquivos dentro da estrutura.
```
cd /tmp
mkdir -p logs/alerts/{ano}
tar -xf ossec-alerts-{ano}.tar -C logs/alerts/{ano}
```

### Baixo o script de recuperação
```
curl -o recovery.py https://raw.githubusercontent.com/olibavictor/OpenSoC/refs/heads/main/Wazuh/Integration/recovery.py
chmod +r recovery.py
```

### Ajustar configuração do filebeat
```
nano /usr/share/filebeat/module/wazuh/alerts/manifest.yml
#Adicione /tmp/recovery.json
```
manifest.yml deve ficar assim:
```
module_version: 0.1

var:
  - name: paths
    default:
      - /var/ossec/logs/alerts/alerts.json
      - /tmp/recovery.json
  - name: index_prefix
    default: wazuh-alerts-4.x-

input: config/alerts.yml

ingest_pipeline: ingest/pipeline.json
```
Reinicie o serviço do filebeat
```
systemctl restart filebeat
```

### Execute o comando abaixo para iniciar o processo de restore
```
nohup ./recovery.py -eps 500 -min 2023-06-10T00:00:00 -max 2023-06-18T23:59:59 -o /tmp/recovery.json -log ./recovery.log -sz 2.5 &
```
> nohup garante que mesmo encerrando a sessão remota o processo de restore seguirá rodando.

> -min: data de inicio do restore <altere conforme necessidade>
> -max: data limite do restore <altere conforme necessidade>

Após o incio do proceso, você pode ler o arquivo recovery.log para validar o o andamento do restore.
