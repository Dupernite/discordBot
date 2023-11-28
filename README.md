# Como utilizar?
Para utilizar este Bot é nescessário preencher a 'config.json', nela você precisará colocar o Token do bot e também dizer se quer ter Footer e Thumbnail em suas mensagens ( caso queira, modifique as informações do footer ou da thumbnail )

```JSON:config.json
{
  "token": "TOKEN",
  "ip": "IP",
  "allowed_roles": [965360361521938442, 1117830793121759393],
  "version": "bedrock",

  "has_footer": "true",
  "footer": "ToP - Bot",

  "has_thumbnail": "true",
  "thumbnail": "https://i.imgur.com/UteffyD.png"
}
```
# Comandos:
* **/status** - pode ser usado por todos para verificar o status atual do servidor.
* **/adm** [new ip] - só pode ser usado pelos cargos definidos em “allowed_roles” e é usado para alterar o IP.
