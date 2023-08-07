### Teste

Alguma coisa

```

## Mensagens

2019/01/02 13:16:00 hostname1 securityapp: INFO: srcuser="Bob" action="called" dstusr="Alice"
2019/01/02 13:17:00 hostname1 securityapp: INFO: action="logged on" srcuser="Bob"

## Exemplo regra única

<group name="securityapp, custom,">
  <rule id="1337" level="3">
    <decoded_as>securityapp</decoded_as>
		<field name="action">called</field>
    <description>User called</description>
  </rule>
</group>

## Exemplo de regra condicional

<group name="securityapp, custom,">
  <rule id="1337" level="0">
    <decoded_as>securityapp</decoded_as>
		<description>SecurityApp Group Messages</description>
  </rule>

  <rule id="1338" level="3">
    <if_sid>1337</if_sid>
		<field name="action">called</field>
    <description>User called</description>
  </rule>

  <rule id="1339" level="3">
    <if_sid>1337</if_sid>
		<field name="action">logged on</field>
    <description>User logged on</description>
  </rule>

</group>
```
