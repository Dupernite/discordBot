# How to use?
To use this Bot, you need to fill in the 'config.json'. In it, you will need to put the Bot's Token and also specify if you want to have a Footer and Thumbnail in your messages (if you want, modify the footer or thumbnail information)

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
# Commands:
* **/status** - can be used by everyone to check the current server status.
* **/adm** [new ip] - can only be used by the roles set on "allow_roles" and is used to change the IP.
