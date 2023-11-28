import json
import requests
import ipaddress
from discord import Bot, Intents, Interaction, Embed, Option

# Define color constants for embedded messages
green = 0x00d26a
red = 0xf8312f
yellow = 0xf7cd64

# Function to get the bot token from the configuration file
def get_token():
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data['token']

# Function to validate an IP address (with or without a port)
def isValidIP(ip):
    try:
        if ':' in ip:  # if the IP address contains a port
            ip, port = ip.split(':')  # split the IP and the port
            ipaddress.ip_address(ip)  # validate the IP
            if not 1 <= int(port) <= 65535:  # validate the port
                return False
        else:
            ipaddress.ip_address(ip)  # validate the IP
        return True
    except ValueError:
        return False

# Function to get a value from the configuration file
def get_from_config(name, type):
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data.get(name, type)

# Function to update the IP address in the configuration file
def update_ip_in_config(new_ip):
    with open('config.json', 'r') as file:
        data = json.load(file)

    data['ip'] = new_ip

    with open('config.json', 'w') as file:
        json.dump(data, file)

# Function to get the server status message
def get_message():
    ip = get_from_config('ip', None)
    version = get_from_config('version', None)

    if get_from_config('has_footer', None):
        footer = get_from_config('footer', None)

    if get_from_config('has_thumbnail', None):
        thumnail = get_from_config('thumbnail', None)

    if isValidIP(ip):
        url = f"https://api.mcstatus.io/v2/status/{version}/{ip}"
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
                embed = Embed(title="Server online! | 🟢",
                              description=f"**IP: ** ```{host}```**Port: **```\n{port}```\n**Online Players: **```{online_players}/{max_players}```**Version: **```{version}```",
                              color=green
                              )
                if get_from_config('has_footer', None):
                    embed.set_footer(text=footer)
                if get_from_config('has_thumbnail', None):
                    embed.set_thumbnail(url=thumnail)
                return embed
            else:
                embed = Embed(title="Server offline! | 🔴",
                              description="The server is offline.",
                              color=red
                              )
                if get_from_config('has_footer', None):
                    embed.set_footer(text=footer)

                if get_from_config('has_thumbnail', None):
                    embed.set_thumbnail(url=thumnail)
                return embed
        else:
            embed = Embed(title="Error! | ⚠️",
                          description="The server did not respond! Wait a bit and try again!",
                          color=yellow
                          )
            if get_from_config('has_footer', None):
                embed.set_footer(text=footer)
            if get_from_config('has_thumbnail', None):
                embed.set_thumbnail(url=thumnail)
            return embed
    else:
        embed = Embed(title="Error! | ⚠️",
                      description="The IP was not correctly configured, ask a STAFF for help!",
                      color=yellow
                      )
        if get_from_config('has_footer', None):
            embed.set_footer(text=footer)
        if get_from_config('has_thumbnail', None):
            embed.set_thumbnail(url=thumnail)
        return embed


# Create a bot instance
bot = Bot(intents=Intents.default())


# Define a slash command to check server status
@bot.slash_command(name="status", description="Check the server status!")
async def _status(interaction: Interaction):
    embed = get_message()
    await interaction.response.send_message(embed=embed)


# Define a slash command for administration operations
@bot.slash_command(name="adm", description="This is an Admin's only command!")
async def _adm(interaction: Interaction, new_ip: Option(str, "Enter new IP", required=True)):
    allowed_roles = get_from_config('allowed_roles', [])
    user_roles = interaction.user.roles
    if get_from_config('has_footer', None):
        footer = get_from_config('footer', None)

    if get_from_config('has_thumbnail', None):
        thumnail = get_from_config('thumbnail', None)

    if not any(role.id in allowed_roles for role in user_roles):
        embed = Embed(title="Error! | ⚠️",
                      description="You do not have sufficient permissions to execute this command!",
                      color=yellow
                      )
        if get_from_config('has_footer', None):
            embed.set_footer(text=footer)

        if get_from_config('has_thumbnail', None):
            embed.set_thumbnail(url=thumnail)
        await interaction.response.send_message(embeds=[embed])
        return

    i_ip = get_from_config('ip', None)
    if isValidIP(new_ip):
        update_ip_in_config(new_ip)
        embed = Embed(title="IP successfully changed! | ✅",
                      description=f"`{i_ip} --> {new_ip}`\n\nPlease check if the IP is correct!",
                      color=green
                      )
        if get_from_config('has_footer', None):
            embed.set_footer(text=footer)

        if get_from_config('has_thumbnail', None):
            embed.set_thumbnail(url=thumnail)
        await interaction.response.send_message(embeds=[embed])
    else:
        embed = Embed(title="Error! | ⚠️",
                      description="The IP does not seem valid! Try checking again",
                      color=yellow
                      )
        if get_from_config('has_footer', None):
            embed.set_footer(text=footer)

        if get_from_config('has_thumbnail', None):
            embed.set_thumbnail(url=thumnail)
        await interaction.response.send_message(embeds=[embed])


token = get_token()
bot.run(token)