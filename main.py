import json
import requests
import ipaddress
from discord import Bot, Intents, Interaction, Embed, Option

# Define constantes de cores para mensagens incorporadas
green = 0x00d26a
red = 0xf8312f
yellow = 0xf7cd64


# Função para obter o token do bot do arquivo de configuração
def get_token():
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data['token']


# Função para validar um endereço IP (com ou sem uma porta)
def isValidIP(ip):
    try:
        if ':' in ip:  # se o endereço IP contém uma porta
            ip, port = ip.split(':')  # divide o IP e a porta
            ipaddress.ip_address(ip)  # valida o IP
            if not 1 <= int(port) <= 65535:  # valida a porta
                return False
        else:
            ipaddress.ip_address(ip)  # valida o IP
        return True
    except ValueError:
        return False


# Função para obter um valor do arquivo de configuração
def get_from_config(name, type):
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data.get(name, type)


# Função para atualizar o endereço IP no arquivo de configuração
def update_ip_in_config(new_ip):
    with open('config.json', 'r') as file:
        data = json.load(file)

    data['ip'] = new_ip

    with open('config.json', 'w') as file:
        json.dump(data, file)


# Função para obter a mensagem de status do servidor
def get_message():
    ip = get_from_config('ip', None)
    if isValidIP(ip):
        url = f"https://api.mcstatus.io/v2/status/bedrock/{ip}"
        headers = {
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.content:
            data = response.json()
            isOnline = data['online']
            if isOnline:
                online_players = data['players']['online']
                max_players = data['players']['max']
                version = data['version']['name']
                host = data['host']
                port = data['port']
                embed = Embed(title="Servidor online! | 🟢",
                              description=f"**IP: ** ```{host}```**Porta: **```\n{port}```\n**Jogadores Online: **```{online_players}/{max_players}```**Versão: **```{version}```",
                              color=green
                              )
                embed.set_footer(text="ToP - Bot")
                embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
                return embed
            else:
                embed = Embed(title="Servidor offline! | 🔴",
                              description="The server is offline.",
                              color=red
                              )
                embed.set_footer(text="ToP - Bot")
                embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
                return embed
        else:
            embed = Embed(title="Erro! | ⚠️",
                          description="O servidor não respondeu! Aguarde um pouco e tente novamente!",
                          color=yellow
                          )
            embed.set_footer(text="ToP - Bot")
            embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
            return embed
    else:
        embed = Embed(title="Erro! | ⚠️",
                      description="O IP não foi configurado corretamente, peça ajuda a um STAFF!",
                      color=yellow
                      )
        embed.set_footer(text="ToP - Bot")
        embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
        return embed


# Cria uma instância do bot
bot = Bot(intents=Intents.default())


# Define um comando de barra para verificar o status do servidor
@bot.slash_command(name="status", description="This is a test command.")
async def _test(interaction: Interaction):
    embed = get_message()
    await interaction.response.send_message(embed=embed)


# Define um comando de barra para operações de administração
@bot.slash_command(name="adm", description="Repeats your message.")
async def _echo(interaction: Interaction, ip_novo: Option(str, "Enter new IP", required=True)):
    allowed_roles = get_from_config('allowed_roles', [])
    user_roles = interaction.user.roles

    if not any(role.id in allowed_roles for role in user_roles):
        embed = Embed(title="Erro! | ⚠️",
                      description="Você não possui permissões suficientes para executar este comando!",
                      color=yellow
                      )
        embed.set_footer(text="ToP - Bot")
        embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
        await interaction.response.send_message(embeds=[embed])
        return

    i_ip = get_from_config('ip', None)
    if isValidIP(ip_novo):
        update_ip_in_config(ip_novo)
        embed = Embed(title="IP alterado com suscesso! | ✅",
                      description=f"`{i_ip} --> {ip_novo}`\n\nPor favor verifique se o IP esta correto!",
                      color=green
                      )
        embed.set_footer(text="ToP - Bot")
        embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
        await interaction.response.send_message(embeds=[embed])
    else:
        embed = Embed(title="Erro! | ⚠️",
                      description="O IP não parece válido! tente verificar novamente",
                      color=yellow
                      )
        embed.set_footer(text="ToP - Bot")
        embed.set_thumbnail(url="https://i.imgur.com/UteffyD.png")
        await interaction.response.send_message(embeds=[embed])


token = get_token()
bot.run(token)
