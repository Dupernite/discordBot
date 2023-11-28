import json
import requests
import ipaddress
from discord import Bot, Intents, Interaction, Embed, Option

# Defina constantes de cores para mensagens incorporadas
verde = 0x00d26a
vermelho = 0xf8312f
amarelo = 0xf7cd64

# Função para obter o token do bot do arquivo de configuração
def obter_token():
    with open('config.json', 'r') as arquivo:
        dados = json.load(arquivo)
        return dados['token']

# Função para validar um endereço IP (com ou sem uma porta)
def validarIP(ip):
    try:
        if ':' in ip:  # se o endereço IP contém uma porta
            ip, porta = ip.split(':')  # divide o IP e a porta
            ipaddress.ip_address(ip)  # valida o IP
            if not 1 <= int(porta) <= 65535:  # valida a porta
                return False
        else:
            ipaddress.ip_address(ip)  # valida o IP
        return True
    except ValueError:
        return False

# Função para obter um valor do arquivo de configuração
def obter_do_config(nome, tipo):
    with open('config.json', 'r') as arquivo:
        dados = json.load(arquivo)
        return dados.get(nome, tipo)

# Função para atualizar o endereço IP no arquivo de configuração
def atualizar_ip_no_config(novo_ip):
    with open('config.json', 'r') as arquivo:
        dados = json.load(arquivo)

    dados['ip'] = novo_ip

    with open('config.json', 'w') as arquivo:
        json.dump(dados, arquivo)

# Função para obter a mensagem de status do servidor
def obter_mensagem():
    ip = obter_do_config('ip', None)
    versao = obter_do_config('versao', None)

    if obter_do_config('has_footer', None):
        rodape = obter_do_config('footer', None)

    if obter_do_config('has_thumbnail', None):
        miniatura = obter_do_config('thumbnail', None)

    if validarIP(ip):
        url = f"https://api.mcstatus.io/v2/status/{versao}/{ip}"
        headers = {
            "Accept": "application/json",
        }

        resposta = requests.get(url, headers=headers)
        if resposta.content:
            dados = resposta.json()
            isOnline = dados['online']
            if isOnline:
                jogadores_online = dados['players']['online']
                max_jogadores = dados['players']['max']
                versao = dados['version']['name']
                host = dados['host']
                porta = dados['port']
                embed = Embed(title="Servidor online! | 🟢",
                              description=f"**IP: ** ```{host}```**Porta: **```\n{porta}```\n**Jogadores Online: **```{jogadores_online}/{max_jogadores}```**Versão: **```{versao}```",
                              color=verde
                              )
                if obter_do_config('has_footer', None):
                    embed.set_footer(text=rodape)
                if obter_do_config('has_thumbnail', None):
                    embed.set_thumbnail(url=miniatura)
                return embed
            else:
                embed = Embed(title="Servidor offline! | 🔴",
                              description="O servidor está offline.",
                              color=vermelho
                              )
                if obter_do_config('has_footer', None):
                    embed.set_footer(text=rodape)

                if obter_do_config('has_thumbnail', None):
                    embed.set_thumbnail(url=miniatura)
                return embed
        else:
            embed = Embed(title="Erro! | ⚠️",
                          description="O servidor não respondeu! Aguarde um pouco e tente novamente!",
                          color=amarelo
                          )
            if obter_do_config('has_footer', None):
                embed.set_footer(text=rodape)
            if obter_do_config('has_thumbnail', None):
                embed.set_thumbnail(url=miniatura)
            return embed
    else:
        embed = Embed(title="Erro! | ⚠️",
                      description="O IP não foi configurado corretamente, peça ajuda a um STAFF!",
                      color=amarelo
                      )
        if obter_do_config('has_footer', None):
            embed.set_footer(text=rodape)
        if obter_do_config('has_thumbnail', None):
            embed.set_thumbnail(url=miniatura)
        return embed


# Cria uma instância do bot
bot = Bot(intents=Intents.default())


# Define um comando de barra para verificar o status do servidor
@bot.slash_command(name="status", description="veja o status do server!")
async def _status(interaction: Interaction):
    embed = obter_mensagem()
    await interaction.response.send_message(embed=embed)


# Define um comando de barra para operações de administração
@bot.slash_command(name="adm", description="comando apenas para administradores!")
async def _adm(interaction: Interaction, novo_ip: Option(str, "Digite novo IP", required=True)):
    roles_permitidos = obter_do_config('allowed_roles', [])
    roles_usuario = interaction.user.roles
    if obter_do_config('has_footer', None):
        rodape = obter_do_config('footer', None)

    if obter_do_config('has_thumbnail', None):
        miniatura = obter_do_config('thumbnail', None)

    if not any(role.id in roles_permitidos for role in roles_usuario):
        embed = Embed(title="Erro! | ⚠️",
                      description="Você não possui permissões suficientes para executar este comando!",
                      color=amarelo
                      )
        if obter_do_config('has_footer', None):
            embed.set_footer(text=rodape)

        if obter_do_config('has_thumbnail', None):
            embed.set_thumbnail(url=miniatura)
        await interaction.response.send_message(embeds=[embed])
        return

    i_ip = obter_do_config('ip', None)
    if validarIP(novo_ip):
        atualizar_ip_no_config(novo_ip)
        embed = Embed(title="IP alterado com sucesso! | ✅",
                      description=f"`{i_ip} --> {novo_ip}`\n\nPor favor, verifique se o IP está correto!",
                      color=verde
                      )
        if obter_do_config('has_footer', None):
            embed.set_footer(text=rodape)

        if obter_do_config('has_thumbnail', None):
            embed.set_thumbnail(url=miniatura)
        await interaction.response.send_message(embeds=[embed])
    else:
        embed = Embed(title="Erro! | ⚠️",
                      description="O IP não parece válido! Tente verificar novamente",
                      color=amarelo
                      )
        if obter_do_config('has_footer', None):
            embed.set_footer(text=rodape)

        if obter_do_config('has_thumbnail', None):
            embed.set_thumbnail(url=miniatura)
        await interaction.response.send_message(embeds=[embed])


token = obter_token()
bot.run(token)