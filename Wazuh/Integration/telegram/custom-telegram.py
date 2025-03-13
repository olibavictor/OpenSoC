#!/usr/bin/env python

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

#CHAT_ID="xxxx"
CHAT_ID=""

# Read configuration parameters
alert_file = open(sys.argv[1])
hook_url = sys.argv[3]


# Read the alert file
alert_json = json.loads(alert_file.read())
alert_file.close()

# Extract data fields
alert_level = alert_json['rule']['level'] if 'level' in alert_json['rule'] else "N/A"
title = alert_json['rule']['description'] if 'description' in alert_json['rule'] else "N/A"
description = alert_json['full_log'] if 'full_log' else "N/A"
groups = alert_json['rule']['groups'] if 'groups' in alert_json['rule'] else "N/A"
rule_id = alert_json['rule']['id'] if 'id' in alert_json['rule'] else "N/A"
agent = alert_json['agent']['name'] if 'name' in alert_json['agent'] else "N/A"

# Generate request
message = f"""🚨 *Alerta:* {title}

*Nível de Alerta:* {alert_level}
*Agente:* {agent}
*Regra:* {rule_id}
*Grupo:* {groups}

*Descrição:* {description}
"""

msg_data = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
}

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


# Send the request
requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

sys.exit(0)
