import os
import pytz
import platform
import discord
import json
from playsound import playsound
from discord import Game
import asyncio
from datetime import datetime, timedelta, time
import colorama
from colorama import Fore, Back, Style
import random
import re
from brettYT import RandomVideo

"""
Initializing colorama for cross-platform color compatibility.
"""
colorama.init()

TOKEN = 'Token goes here'

#Work in progress
"""
inventory_dir = os.path.join(os.getcwd(), "Inventories")
async def get_inventory_file_path(username):
    # Returns a sanitized username filepath for a JSON inventory of cards.
    sanitized_username = "".join(c for c in username if c.isalnum() or c in (" ", "_")).rstrip()
    return os.path.join(inventory_dir, f"{sanitized_username}-inventory.json")

async def ensure_user_inventory_file(user):
    inventory_file_path = await get_inventory_file_path(user.name)
    if not os.path.exists(inventory_file_path):
        with open(inventory_file_path, "w", encoding="utf8") as file:
            json.dump([], file, indent=4)

async def handle_inventory_command(message):
    user = message.author
    inventory_file_path = await get_inventory_file_path(user.name)
    # Returns a loaded version of the user's inventory of cards.
    with open(inventory_file_path, 'r', encoding='utf8') as file:
        return json.load(file)

async def save_user_inventory(user, inventory):
    inventory_file_path = await get_inventory_file_path(user.name)
    with open(inventory_file_path, 'w', encoding='utf8') as file:
        json.dump(inventory, file, indent=4)

async def ensure_all_users_have_inventories(guild):
    for member in guild.members:
        if not member.bot:  # Skip bots
            await ensure_user_inventory_file(member)

async def get_cards_by_rarity(user, rarity, page):
    inventory = await handle_inventory_command(user)
    filtered_cards = [card for card in inventory if card['rarity'] == rarity]

    # Return empty if no cards found
    if not filtered_cards:
        return []

    # Pagination: Get the 5 cards for the requested page
    start_index = (page - 1) * 5
    end_index = start_index + 5

    return filtered_cards[start_index:end_index]
"""

def get_channel_id():
    server_choice = input("What server channel ID would you like to use? (P/T/L?): ").lower()
    if server_choice == "p":
        print(f"{Fore.GREEN}{Back.BLACK}Main Server Successfully Selected{Style.RESET_ALL}")
        return 1181491247186186261
    elif server_choice == "t":
        print(f"{Fore.GREEN}{Back.BLACK}Test Server Successfully Selected{Style.RESET_ALL}")
        return 1182112426573959271
    elif server_choice == "l":
        return 575736702321033227
    else:
        print("Please enter only valid options!")
        return get_channel_id()

CHANNEL_ID = get_channel_id()
CHRISTMAS_DATE = '2023-12-25'
BRETTCOMESHOME_DATE = '2023-12-14'
MESSAGE_TIME = time(0, 0)
intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.message_content = True
intents.guilds = True
intents.members = True

mountain_tz = pytz.timezone('US/Mountain')

client = discord.Client(intents=intents)

async def set_presence():
    await client.wait_until_ready()
    await client.change_presence(activity=Game("Bootcamp"))

async def daily_countdown():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    christmas_date = datetime.strptime(CHRISTMAS_DATE, '%Y-%m-%d').date()
    brettcomeshome_date = datetime.strptime(BRETTCOMESHOME_DATE, '%Y-%m-%d').date()

    while not client.is_closed():
        now = datetime.now(mountain_tz)
        today = now.date()

        if now.time() > MESSAGE_TIME:
            next_message_date = today + timedelta(days=1)
        else:
            next_message_date = today

        next_message_time = mountain_tz.localize(datetime.combine(next_message_date, MESSAGE_TIME))
        time_until_next_message = (next_message_time - now).total_seconds()

        if today < christmas_date:
            days_remaining_until_christmas = (christmas_date - today).days
            days_remaining_until_brettcomeshome = (brettcomeshome_date - today).days
            christmas_message = f"There are {days_remaining_until_christmas} days left until Christmas \ud83c\udf81"
            brettcomeshome_message = f"Brettman comes home today! \ud83c\udf81"
            await channel.send(christmas_message)
            await channel.send(brettcomeshome_message)
        else:
            message = "Merry Christmas! \ud83c\udf84\ud83c\udf81"
            await channel.send(message)

        await asyncio.sleep(time_until_next_message)

@client.event
async def on_ready():
    status = discord.Activity(type=discord.ActivityType.watching, name="the Drill Sergeant")
    await client.change_presence(activity=status)
    startup_files = ['Gamecube.wav', 'GTA4.wav', 'PS1.wav', 'Windows XP.wav', 'Xbox360.wav', 'PSP.wav']
    random_file = random.choice(startup_files)
    startup_sound = os.path.join(os.getcwd(), "Sound Effects", "Basic", "Startup", random_file)
    if platform.system() in ["Linux", "Windows"]:
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}Cannot play sound on the server.{Style.RESET_ALL}")
    else:
        playsound(startup_sound)
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{client.user} is ready.{Style.RESET_ALL}")

@client.event
async def on_message(message):
    now = datetime.utcnow()
    christmas_date = datetime.strptime(CHRISTMAS_DATE, '%Y-%m-%d').date()
    brettcomeshome_date = datetime.strptime(BRETTCOMESHOME_DATE, '%Y-%m-%d').date()
    today = now.date()
    days_remaining_until_christmas = (christmas_date - today).days
    days_remaining_until_brettcomeshome = (brettcomeshome_date - today).days
    history_path = os.path.join(os.getcwd(), "Text", "ChatHistory.json")
    image_url = None
    if message.author == client.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                image_url = attachment.url
                break

    print(f"Message received from {message.author}: {message.content}. Created at {message.created_at}, From: {message.guild}")

    if message.content in ["!dailycount", "!dc"]:
        message_count, image_count, emoji_count = await count_daily_messages_images_emojis()
        await message.channel.send(f"This is a work in progress function, it does not yet work.")
        await message.channel.send(
            f"**{message_count}** messages 📩\n**{image_count}** images 🖼️\n**{emoji_count}** emojis 😀\nCaptured today.")

    if message.content in ["!randomchat", "!rc"]:
        nickname_path = os.path.join(os.getcwd(), "Settings", "nicknames.json")
        with open(nickname_path, 'r', encoding='utf8') as file:
            name_mapping = json.load(file)
        with open(history_path, 'r', encoding='utf8') as file:
            chat_history = json.load(file)

        if chat_history:
            random_entry = random.choice(chat_history)
            date_string = random_entry.get('date', '')
            if date_string:
                date_string_no_tz = ' '.join(date_string.split()[:-1])
                date_object = datetime.strptime(date_string_no_tz, "%B %d, %Y at %I:%M %p")
                year = date_object.year

            author_of_random_entry = random_entry.get('author')
            total_messages = len(chat_history)
            author_count = sum(1 for entry in chat_history if entry.get('author') == author_of_random_entry)
            rarity = author_count / total_messages
            rarity_text = ""

            # Rarity categories
            rarity_colors = {
                'Blue': (0.02, '0x00BCFF'),
                'Purple': (0.005, '0x6D0CA6'),
                'Pink': (0.0008333, '0xFF0082'),
                'Red': (0.0002, '0xFF0000'),
                'Gold': (0, '0xF5FF00')
            }

            for rarity_name, (chance, color) in rarity_colors.items():
                if rarity > chance:
                    rarity_text = rarity_name
                    accent_color = int(color, 16)
                    break

            stattracknumber = random.randint(1, 10)

            name_mapping_dict = {list(item.keys())[0]: list(item.values())[0] for item in name_mapping}

            original_author = random_entry.get('author')
            author_display_name = name_mapping_dict.get(original_author, original_author)

            jump_url = f"https://discord.com/channels/{message.guild.id}/{random_entry['channel_id']}/{random_entry['message_id']}"

            card_data = {
                'author': author_display_name,
                'date': year,
                'rarity': rarity_text,
                'text': random_entry.get('text', ''),
                'jump_url': jump_url,
                'attachments': random_entry.get('attachments', []),
                'author_avatar': random_entry.get('author_avatar', None)
            }

            title_prefix = "★ " if stattracknumber == 1 else ""
            title = f"{title_prefix}Message from {author_display_name}"

            embed = discord.Embed(
                title=title,
                url=jump_url,
                color=accent_color
            )

            if random_entry.get('text', ''):
                embed.add_field(name="Message:", value=random_entry['text'], inline=True)
                embed.add_field(name=f"Date: {year}", value="", inline=False)
                embed.add_field(name=f"Rarity: {rarity_text}", value="", inline=True)
                embed.add_field(name=f"Author: {author_display_name}", value="", inline=False)
                footer_text = f"Stattrack {year} {author_display_name} Card" if stattracknumber == 1 else f"{year} {author_display_name} Card"
                embed.set_footer(text=footer_text)

                # Add text to the embed if available
                # embed.description = f"\n**{random_entry.get('text', 'No text available.')}**"

                # Set the author of the embed using the stored avatar URL
                author_avatar_url = random_entry.get('author_avatar', None)
                embed.set_author(name=random_entry.get('author'), icon_url=author_avatar_url)

                # Add a thumbnail
                thumbnail_url = "author_avatar_url"
                embed.set_thumbnail(url=author_avatar_url)

                # Try to set the timestamp of the embed
                try:
                    # Assuming the date is in the format: "December 06, 2023 at 11:48 AM MST"
                    embed.timestamp = datetime.strptime(random_entry['date'], "%B %d, %Y at %I:%M %p %Z")
                except ValueError:
                    # If there's an error parsing the date, you can choose to ignore it or handle it differently
                    print("Date format is incorrect or missing")

                # Set the image of the embed if there's an attachment that's an image
                attachments = random_entry.get('attachments', [])
                if attachments:  # Check if there are any attachments
                    embed.set_image(url=attachments[0])

                await message.channel.send(embed=embed)

    if message.content in ["!jn", "!ju", "!joeusername", "!joename"]:
        joe_usernames = ["JustJoe", "JoeTheMoose", "DaMoneyMan", "Patronic",
                         "Prism", "Patrism", "JoeTheOwl", "JoeDoesGaming",
                         "JoeThePerson", "FlameyHD", "Trash",
                         "Almost Not Trash", "Epic Penguin", "James Penguin",
                         "Freddy Fazbear", "DoctorPenguin10", "Average Joe",
                         "Joe Does Roblox"]
        await message.channel.send(f"Legend has it Joe's username was once:")
        await asyncio.sleep(0.5)
        await message.channel.send(f"**{random.choice(joe_usernames)}**")
        await asyncio.sleep(0.5)
        await message.channel.send(f"Wow...")

    if message.content in ["!pixelcinema", "!pc"]:
        random_video = RandomVideo("UCjh4c6EhOKX54Moj3Sir8EA", "Google API Key Here")
        video_link = random_video.get_random_video_link()
        await message.channel.send(video_link)

    if message.content in ["!rpf"]:
        random_video = RandomVideo("UCFJDWPMlZD5zQ6DGK6TT54w", "Google API Key Here")
        video_link = random_video.get_random_video_link()
        await message.channel.send(video_link)

    if message.content in ["!boxingbennett", "!bb"]:
        random_video = RandomVideo("UCykH7SSA4KfMz6VUWUX3Psg", "Google API Key Here")
        video_link = random_video.get_random_video_link()
        await message.channel.send(video_link)

    if re.findall(r"(?i)sayin", message.content):
        await message.channel.send("I know what you're sayin")

    if message.content.startswith("!verse"):
        match = re.match(r"!verse (\d+):(\d+)", message.content)
        if match:
            # Extracting numbers and forming the verse format with "Gamer " prefix
            number1, number2 = match.groups()
            verse_format = f"Gamer {number1}:{number2}"

            # Load the JSON data
            phrases_path = os.path.join(os.getcwd(), "Text", "GamerVerses.json")
            with open(phrases_path, 'r', encoding='utf-8') as file:
                verses = json.load(file)

            # Check if verse_format exists in any of the objects
            found_verse = None
            for v in verses:
                if v['verse'] == verse_format:
                    found_verse = v
                    break

            # Send the found verse or a fallback message
            if found_verse:
                message_text = f">>> 📜 **{found_verse['verse']}**  *\"{found_verse['text']}\" - {found_verse['author']}*$ \n{found_verse['date']}"
            else:
                message_text = "Verse not found. Please check the verse number."
            await message.channel.send(message_text)
        else:
            # Handle the case where no valid verse format is provided
            phrases_path = os.path.join(os.getcwd(), "Text", "GamerVerses.json")
            with open(phrases_path, 'r', encoding='utf-8') as file:
                verses = json.load(file)
            random_verse = random.choice(verses)
            message_text = f">>> 📜 **{random_verse['verse']}**  *\"{random_verse['text']}\" - {random_verse['author']}* \n{random_verse['date']}"
            await message.channel.send(message_text)

    if message.content.startswith("!re"):
        randomemoji_message = ""
        match = re.match(r"!re(\d+)", message.content)
        if match:
            numberoftimes = int(match.group(1))
            for x in range(numberoftimes):
                randomemoji_message += await get_random_custom_emoji()
        else:
            randomemoji_message += await get_random_custom_emoji()
        await message.channel.send(randomemoji_message)


    if message.content == "!allverses":
        phrases_path = os.path.join(os.getcwd(), "Text", "GamerVerses.json")
        with open(phrases_path, 'r', encoding='utf-8') as file:
            verses = json.load(file)
        for verse in verses:
            message_text = f">>> 📜 **{verse['verse']}**  *\"{verse['text']}\" - {verse['author']}* \n{verse['date']}"
            await message.channel.send(message_text)

    if message.content == "!addverse":
        phrases_path = os.path.join(os.getcwd(), "Text", "GamerVerses.json")

        # Ensure GamerVerses is loaded or initialized
        if os.path.exists(phrases_path) and os.path.getsize(phrases_path) > 0:
            with open(phrases_path, "r", encoding="utf-8") as file:
                GamerVerses = json.load(file)
        else:
            GamerVerses = []

        versenumber = await versenumberobtainer(message)
        versetext = await versetextobtainer(message)
        verseauthor = await verseauthorobtainer(message)
        versedate = formatted_date_with_ordinal()

        new_verse = {
            "verse": versenumber,
            "text": versetext,
            "author": verseauthor,
            "date": versedate
        }

        GamerVerses.append(new_verse)

        with open(phrases_path, "w", encoding="utf-8") as file:
            json.dump(GamerVerses, file, indent=4)

        await message.channel.send(f">>> 📜 **{versenumber}**  *\"{versetext}\" - {verseauthor}\n{versedate}*")
        await message.channel.send("Message saved successfully ✅.")

    if message.content == "!daysleft":
        await message.channel.send(f'There are {days_remaining_until_christmas + 1} days left until Christmas 🎁')

    if message.content.lower() == '!areyoualive':
        await message.channel.send("Yes, I'm here!")

    if message.content.startswith('!rps'):
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)

        await message.channel.send("Choose rock, paper, or scissors:")
        try:
            response = await client.wait_for('message', check=lambda m: m.author == message.author, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send("You took too long to respond!")
            return

        user_choice = response.content.lower()
        if user_choice not in choices:
            await message.channel.send("Invalid choice. Please choose rock, paper, or scissors.")
            return

        if user_choice == bot_choice:
            await message.channel.send(f"It's a tie! We both chose {bot_choice}. 🤝")
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            await message.channel.send(f"You win! I chose {bot_choice}. 🎉")
        else:
            await message.channel.send(f"I win! I chose {bot_choice}. 😄")

#Work in progress
async def count_daily_messages_images_emojis():
        # Read the JSON file
        history_path = os.path.join(os.getcwd(), "Text", "ChatHistory.json")
        with open(history_path, 'r', encoding='utf8') as file:
            message_logs = json.load(file)

        # Get current date in MST
        current_date = datetime.now(mountain_tz).strftime("%B %d, %Y")  # e.g., "December 30, 2019"

        # Debugging current date
        print(f"Current date: {current_date}")

        # Initialize counters
        daily_message_count = 0
        daily_image_count = 0
        daily_emoji_count = 0

        # Regex pattern for Discord emojis
        emoji_pattern = re.compile(r"<a?:.+?:\d+>")

        for log in message_logs:
            log_date = log["date"].split(' at ')[0]  # Extract date without time and timezone

            # Debugging log date
            print(f"Log date: {log_date}")

            if log_date == current_date:  # Match date
                daily_message_count += 1
                if log.get("attachments"):
                    daily_image_count += len(log["attachments"])
                emojis = emoji_pattern.findall(log["text"])
                daily_emoji_count += len(emojis)

        return daily_message_count, daily_image_count, daily_emoji_count

async def get_random_custom_emoji():
    # Retrieve emojis from a specific guild
    guild_id = 610260169225535497  # Replace with the relevant guild ID
    guild = discord.utils.get(client.guilds, id=guild_id)

    if guild and guild.emojis:
        random_emoji = random.choice(guild.emojis)
        return str(random_emoji)
    return None

async def count_daily_messages_images_emojis():
    # Read the JSON file
    history_path = os.path.join(os.getcwd(), "Text", "ChatHistory.json")
    with open(history_path, 'r', encoding='utf8') as file:
        message_logs = json.load(file)

    # Get current date in MST
    current_date = datetime.now(mountain_tz).strftime("%B %d, %Y")  # e.g., "December 30, 2019"

    # Debugging current date
    print(f"Current date: {current_date}")

    # Initialize counters
    daily_message_count = 0
    daily_image_count = 0
    daily_emoji_count = 0

    # Regex pattern for Discord emojis
    emoji_pattern = re.compile(r"<a?:.+?:\d+>")

    for log in message_logs:
        log_date = log["date"].split(' at ')[0]  # Extract date without time and timezone

        # Debugging log date
        print(f"Log date: {log_date}")

        if log_date == current_date:  # Match date
            daily_message_count += 1
            if log.get("attachments"):
                daily_image_count += len(log["attachments"])
            emojis = emoji_pattern.findall(log["text"])
            daily_emoji_count += len(emojis)

    return daily_message_count, daily_image_count, daily_emoji_count
async def get_random_custom_emoji():
    # Retrieve emojis from a specific guild
    guild_id = 610260169225535497  # Replace with the relevant guild ID
    guild = discord.utils.get(client.guilds, id=guild_id)

    if guild and guild.emojis:
        random_emoji = random.choice(guild.emojis)
        return str(random_emoji)
    return None

def ordinal_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return suffix

def formatted_date_with_ordinal():
    current_datetime = datetime.now()
    day = current_datetime.day
    formatted_date = current_datetime.strftime(f"%B {day}{ordinal_suffix(day)}, %Y")
    return formatted_date

async def versenumberobtainer(message):
    while True:
        await message.channel.send("Please provide your verse number (e.g., '123:45'): ")
        versenumber = await client.wait_for('message', check=lambda m: m.author == message.author)
        versenumberpattern = r'\d+:\d+'
        if not re.match(versenumberpattern, versenumber.content):
            await message.channel.send("Invalid format. Please try again (e.g., '123:45').")
        else:
            return versenumber.content

async def versetextobtainer(message):
    await message.channel.send("What is the text of your verse?")
    versetext = await client.wait_for('message', check=lambda m: m.author == message.author)
    if versetext:
        return versetext.content
    else:
        await message.channel.send("Something went wrong. Please try again.")

async def verseauthorobtainer(message):
    await message.channel.send("Who is the author of this verse?")
    versetext = await client.wait_for('message', check=lambda m: m.author == message.author)
    if versetext:
        return versetext.content
    else:
        await message.channel.send("Something went wrong. Please try again.")
async def logging_func(message):
    excluded_guild_id = 1088939691295920131
    if message.content.startswith('!') or message.author == client.user or \
       (message.guild and message.guild.id == excluded_guild_id):
        return

    new_log = {
        "author": str(message.author),
        "author_id": message.author.id,
        "author_avatar": str(message.author.avatar.url if message.author.avatar else message.author.default_avatar.url),
        "text": message.content,
        "attachments": [str(attachment.url) for attachment in message.attachments],
        "date": message.created_at.astimezone(mountain_tz).strftime("%B %d, %Y at %I:%M %p MST"),
        "server": str(message.guild) if message.guild else None,
        "message_id": message.id,
        "channel_id": message.channel.id,
        "mentions": [str(mention) for mention in message.mentions],
        "mention_roles": [str(role) for role in message.role_mentions],
        "mention_everyone": message.mention_everyone,
        "pinned": message.pinned,
        "tts": message.tts,
        "guild_name": str(message.guild.name) if message.guild else None,
        "guild_id": message.guild.id if message.guild else None,
        "webhook_id": message.webhook_id,
        "application": str(message.application.to_dict()) if message.application else None
    }

    with open(history_path, 'r', encoding='utf-8') as file:
        history = json.load(file)

    history.append(new_log)

    with open(history_path, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)

    await logging_func(message)

client.run(TOKEN)
