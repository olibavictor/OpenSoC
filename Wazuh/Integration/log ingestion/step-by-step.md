# Passo a passo
## Como integrar o Wazuh com qualquer tecnologia para ingestão de dados?

### **1) Avalie o contexto da integração.**
Vamos partir do ponto onde você já validou a real necessidade daquela integração. Aí você partiria para análise do contexto. Valide se no Wazuh já existem decodificadores e regras para aquela tecnologia. Mesmo que exista, ainda é importante validar se é exatamente aquilo que procuro. Exemplo: Pode ser que queira monitorar regras específicas de trafego do meu firewall, embora existam decodificadores e regras para aquela solução, só existem regras focadas em VPN e Auditoria.

### **2) Qual caminho seguir?**
Com a compreensão do contexto, decida qual a melhor alterativa.
- 2.1)  Caso não tenha nenhum decodificador ou regra, terá que desenvolve-los do zero, como aprendemos no curso. Busque exemplos do Log que será recebido pelo Wazuh e desenvolva os recurso com base nisso.
- 2.2) Caso exista decodificadores/regras ainda vale entender o que é mais viável. Customizar os recursos atuais ou desenvolve-los do zero? Você pode pegar exemplos dos logs que serão enviados e testa-los através da ferramenta "Ruleset Test" dentro da plataforma, assim terá uma visão do que o Wazuh já consegue fazer com aquele log. De repente, ele já até consegue decodificar os campos e precisa apenas de regras mais específicas.

### **3) Como capturar exemplos dos logs que quero ingerir na plataforma?**
Bom, aqui que realmente todo mundo acaba tendo problema, mas vou dar algumas opções.
- 3.1) A primeira opção é buscar exemplos na internet. É tranquilo encontrar esses exemplos para soluções amplamente usadas, como soluções de firewall ou dispositivos de rede no geral, servidores web, entre outros. Obviamente, atente-se a versão das tecnologias, formato de envio dos logs e etc, para garantir que o que você vai enviar para a plataforma segue o mesmo formato do log que vai usar de exemplo.
- 3.2) Aponte o envio da ferramenta para o servidor do wazuh, porém, para uma porta diferente e use o netcat para escutar na porta específica e receber os logs. Assim já terá exemplos dos logs reais que serão enviados. Aí já teria exemplos dos logs, seja para desenvolver decodificadores/regras a partir disso ou apenas para testar os recursos que ja estão presentes.
- 3.3) A terceira opção da um pouco mais de trabalho, mas pode ser uma opção em alguns casos. Você vai até as configurações do Wazuh e cria uma nova porta de escuta com o serviço <remote>. Essa configuração abrirá uma nova porta no servidor para receber os logs. Sem os decodificadores/regras adequadas, tudo será descartado, mas é possível capturar os eventos que são descartados pelo Wazuh. Você precisa habilitar o archives (logs descartados). Para fazer isso, vá até as configurações do servidor e procure pelos parâmetros `<logall>` e `<logall_json>` e altere de "no" para "yes". Depois disso você pode entrar no servidor wazuh e ler os logs /var/ossec/logs/archives/archives.log em tempo real para identificar os logs em texto simples que não foram processados corretamente pelo Wazuh. NÃO ESQUEÇA DE DESATIVAR AS CONFIGURAÇÕES ALTERADAS `<logall>` e `<logall_json>`.

### **4) Visualizando os eventos na plataforma Wazuh**
Depois de ter capturado os logs de exemplo e garantir que agora existem decodificadores e regras adequadas para aquela tecnologia  e ter testado várias possibilidades com "Ruleset Test", agra é hora de colocar em produção.
Para isso, você deve seguir parte do processo descrito na fase **3.3**. Você até pode configurar o envio para a mesma porta padrão 1514, mas recomendo sempre criar uma nova porta de escuta separada para ingerir logs via syslog, ainda mais quando terá um grande volume de eventos processados. Com a nova porta de escuta configurada e o envio configurada, agora você ja deveria começar a receber os eventos corretamente dentro da plataforma.

### **5) Ainda não estou recebendo os eventos dentro do Wazuh! E agora?**
Você só tem dois caminhos.  Ou realmente nenhum evento foi enviado durante aquele período, ou seus decodificadores e regras ainda não estão conseguindo processar os logs recebidos. Sendo assim, você deve voltar ao passo **3.3** e verificar se os logs estão sendo descartados. Se estiverem sendo descartados você deve revisar os decodificadores e regras novamente, realizando testes com "Ruleset Test". NÃO ESQUEÇA DE DESATIVAR AS CONFIGURAÇÕES ALTERADAS `<logall>` e `<logall_json>` no passo **3.3**.
