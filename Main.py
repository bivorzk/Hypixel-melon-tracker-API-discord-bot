import requests
import discord
import schedule
import time

API_KEY = "13e5fabc-b88d-4846-85b0-d2acdd49cff7"

uuid_list = ["5cbcea5767a74c1ebb5d2c3c91a25246"]  # Add your UUIDs here

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

channel_id = "770377475007709224"  # Replace with the ID of the channel where you want to send the melon slice data

def get_melon_slices(uuid):
    hypixel_api = 'https://api.hypixel.net/skyblock/profiles'
    response = requests.get(hypixel_api, params={'key': API_KEY, 'uuid': uuid})
    data = response.json()

    # Get melon slice data
    if "profiles" in data:
        melon_slices = data["profiles"][0]["members"][uuid]["collection"].get("MELON", 0)
        return melon_slices
    else:
        return None

def send_melon_slices():
    global uuid_list
    for uuid in uuid_list:
        username = get_username_from_uuid(uuid)
        melon_slices = get_melon_slices(uuid)
        if melon_slices is not None:
            message = f"{username}'s Melon Slices: {melon_slices}"
        else:
            message = f"Failed to get {username}'s melon slice data."
        channel = client.get_channel(int(channel_id))
        channel.send(message)

def get_username_from_uuid(uuid):
    response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    data = response.json()
    if "name" in data:
        return data["name"]
    else:
        return None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Schedule the melon slice data to be sent every day at 12:00 PM
    schedule.every().day.at("12:00").do(send_melon_slices)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

    if message.content.startswith('!add_uuid'):
        args = message.content.split()[1:]
        if len(args) == 0:
            await message.channel.send("ird be a szándékolt minecraft nevet akit hozzáakarsz adni a listához.")
        else:
            username = args[0]
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
            if response.status_code == 200:
                data = response.json()
                uuid = data["id"]
                uuid_list.append(uuid)
                await message.channel.send(f"Sikeresen hozzá lett adva {username} a listához.")
            else:
                await message.channel.send(f"Nem sikerult hozzádni a listához {username}. Kérlek ellenorizd a helyesirásod.")


client.run("MTA0Njc4ODcxNzQxMjYyNjUxMg.G67Q3T.06onQ-3VH0VlkJOy0soTXojqMSn3NqyJubDvcQ")
