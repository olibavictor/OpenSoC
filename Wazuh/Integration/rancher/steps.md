# Ingestão de logs Rancher
Homologado na versão 2.6.14

### 1) Instale o "logging"
Apps > Charts > Logging > Install

Após a instalação, o menu "Logging" pode levar alguns poucos minutos até aparecer.

### 2) Configure o ClusterOutput usando o arquivo "cluster_output.yml" presente neste repositório.
Faça a alteração do endereço remoto para onde serão enviado os logs

### 3) Configure o ClusterFlow usando o arquivo "cluster_flow.yml" presente neste repositório.
Por padrão a configuração irá encaminhar todos os logs do cluster. Posteriormente você pode alterar isso.

A configuração pode levar alguns poucos minutos para ter efeito. O mesmo se aplica a alterações futuras.

### 4) Adicione o decodificador "0002-rancher-web-decoder.xml" presente nesse repositório no Wazuh que está recebendo as mensagens.
O nome do decoder deve se manter exatamente o mesmo para que funcione de maneira adequada. O Wazuh processa os decoders por ordem alfabética e precisamos que ele seja processado antes do decoder json padrão.
