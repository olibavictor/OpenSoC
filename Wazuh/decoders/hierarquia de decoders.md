## Hierarquia de decodificadores Wazuh

### Log1
```
2019/01/02 13:16:35 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"
```
### Exemplo decoder único
```
<decoder name="securityapp">
  <program_name>securityapp</program_name>
  <regex>(\w+): srcuser="(\.+)" action="(\.+)" dstusr="(\.+)"</regex>
  <order>type,srcuser,action,dstuser</order>
</decoder>
```

### Output
```
Apr 12 14:31:38 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"

**Phase 1: Completed pre-decoding.
        full event: 'Apr 12 14:31:38 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"'
        timestamp: 'Apr 12 14:31:38'
        hostname: 'hostname1'
        program_name: 'securityapp'

**Phase 2: Completed decoding.
        name: 'securityapp'
        action: 'called'
        dstuser: 'Alice'
        srcuser: 'Bob'
        type: 'INFO'
```

### Log2
```
Apr 01 19:21:24 hostname2 securityapp: INFO: action="logged on" srcuser="Bob"
```

### Exemplo de decodificador condicional
```
<decoder name="securityapp">
  <program_name>securityapp</program_name>
</decoder>

<decoder name="securityapp">
  <parent>securityapp</parent>
  <regex>^(\w+):</regex>
  <order>type</order>
</decoder>

<decoder name="securityapp">
  <parent>securityapp</parent>
  <regex>srcuser="(\.+)"</regex>
  <order>srcuser</order>
</decoder>

<decoder name="securityapp">
  <parent>securityapp</parent>
  <regex>action="(\.+)"</regex>
  <order>action</order>
</decoder>

<decoder name="securityapp">
  <parent>securityapp</parent>
  <regex>dstusr="(\.+)"</regex>
  <order>dstuser</order>
</decoder>
```

### Output
```
Dec 28 01:35:18 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"

**Phase 1: Completed pre-decoding.
        full event: 'Dec 28 01:35:18 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"'
        timestamp: 'Dec 28 01:35:18'
        hostname: 'hostname1'
        program_name: 'securityapp'

**Phase 2: Completed decoding.
        name: 'securityapp'
        action: 'called'
        dstuser: 'Alice'
        srcuser: 'Bob'
        type: 'INFO'


Apr 01 19:21:24 hostname2 securityapp: INFO: action="logged on" srcuser="Bob"

**Phase 1: Completed pre-decoding.
        full event: 'Apr 01 19:21:24 hostname2 securityapp: INFO: action="logged on" srcuser="Bob"'
        timestamp: 'Apr 01 19:21:24'
        hostname: 'hostname2'
        program_name: 'securityapp'

**Phase 2: Completed decoding.
        name: 'securityapp'
        action: 'logged on'
        srcuser: 'Bob'
        type: 'INFO'
```
