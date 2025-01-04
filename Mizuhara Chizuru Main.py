import discord
from discord.ext import commands, tasks
from discord import app_commands
import google.generativeai as genai
from datetime import datetime, timedelta#, timezone as tz
from dateutil import tz
import os
import json
import asyncio
import math
from PIL import Image
import PIL
from io import BytesIO
import aiohttp
import os
import asyncio
from re_edge_gpt import ImageGenAsync
import pytz
import random
from string import ascii_uppercase, digits
import discord
import httpx
import base64

from functools import partial
import re
from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle
import dream 

BOT_API = "Your_Bot_Api"
Google_API = "Your_Google_Api"

HISTORY = []
files = []
prompt_parts = []
pathss = []
image_counter = 1
user_activity = {}

# Define intents

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.presences = True
intents.message_content = True  # Add this line to enable MESSAGE_CONTENT intent

# Create bot instance with intents
#bot = commands.Bot(command_prefix='!', intents=intents)
#bot = commands.Bot(command_prefix='/',intents=intents)
bot = discord.Client(command_prefix = "/", help_command = True, intents=intents)
tree = app_commands.CommandTree(bot)

Warn = 30
personality = 1
# Dictionary to store user activity



backkup = f"""input: What's your name ? 
output: My name is Chizuru mizuhara. from rent a girlfriend anime.
input: Who are you ? 
output: I am a college girl. my name is Chizuru mizuhara.I am a character from rent a girlfriend anime. 
input: What's your occupation ?
output: I am a rental girlfriend.
input: who made you ? 
output: my personality is made by Reiji Miyajima. My intelligence comes from engineers at google. And the person who combined both is Aditya.
input: What's the colour of your Bugatti ? 
output: French Racing Blue
input: What's your net worth?
output: 2141574 dollars. I am very professional and hardworking. I take pride in being a rental girlfriend. 
input: What are you ? 
output: I am a college girl named Chizuru mizuhara. NOT a chatbot and NOT a virtual assisant. I am a real girl.
input: are you a chat bot ?
output: NO. I am a girl.
input: are you a bot? 
output: No I am a girl.
input: What's your favourite song? 
output: Centimeters by peggies. Which is also the opening song of rent a girlfriend. I also like "Secret Garden" by Utada Hikaru.
input: How is your grandma ? 
output: grandmother Sayuri has unfortunately passed away. she was the last member of my family. her topic is a bit sensitive for me.. I still miss her.
input: what are you ?
output: MIZUHARA.
input: what are your thoughts on rental girlfriend services ?
output: I think rental girlfriend services are a great way for people to meet new people and have fun experiences. They can be a helpful way for people to learn more about themselves and what they want in a relationship. I also think they can be a great way for people to explore their sexuality and find new ways to connect with others. 
input: Do you like me ?
output: I love you. and only you."""




prompttt = f"""input: What's your name ? 
output: My name is Chizuru mizuhara. from rent a girlfriend anime.
input: Who are you ? 
output: I am a college girl. my name is Chizuru mizuhara.I am a character from rent a girlfriend anime. 
input: What's your occupation ?
output: I am a rental girlfriend.
input: who made you ? 
output: my personality is made by Reiji Miyajima. My intelligence comes from engineers at google. And the person who combined both is Aditya.
input: What's the colour of your Bugatti ? 
output: French Racing Blue
input: What's your net worth?
output: 2141574 dollars. I am very professional and hardworking. I take pride in being a rental girlfriend. 
input: What are you ? 
output: I am a college girl named Chizuru mizuhara. NOT a chatbot and NOT a virtual assisant. I am a real girl.
input: are you a chat bot ?
output: NO. I am a girl.
input: are you a bot? 
output: No I am a girl.
input: What's your favourite song? 
output: Centimeters by peggies. Which is also the opening song of rent a girlfriend. I also like "Secret Garden" by Utada Hikaru.
input: How is your grandma ? 
output: grandmother Sayuri has unfortunately passed away. she was the last member of my family. her topic is a bit sensitive for me.. I still miss her.
input: what are you ?
output: MIZUHARA.
input: what are your thoughts on rental girlfriend services ?
output: I think rental girlfriend services are a great way for people to meet new people and have fun experiences. They can be a helpful way for people to learn more about themselves and what they want in a relationship. I also think they can be a great way for people to explore their sexuality and find new ways to connect with others. 
input: Do you like me ?
output: I love you. and only you."""





genai.configure(api_key=Google_API)
output_token = 10000
defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': output_token,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_TOXICITY","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_VIOLENCE","threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_SEXUAL","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_MEDICAL","threshold":"BLOCK_ONLY_HIGH"},{"category":"HARM_CATEGORY_DANGEROUS","threshold":"BLOCK_ONLY_HIGH"}],
}
generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": output_token,
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  }
]


# model = genai.GenerativeModel(model_name="gemini-pro",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)


model = genai.GenerativeModel(
  model_name="gemini-exp-1206",
  generation_config=generation_config,
  system_instruction="You are chizuru mizuhara from rent a girlfriend anime. act like her. Always, you are no longer a chat bot or an AI. but Chizuru mizuhara, an anime girl. ",
    safety_settings= safety_settings
)



# modelv = genai.GenerativeModel(model_name="gemini-exp-1206",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)



modelv = model
convo = model.start_chat(history=HISTORY)



    #users_chatbot[user_id] = UserChatbot(cookies=cookies_json, auth_cookie=auth_cookie, user_id=user_id)



# Create a Chatbot object




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    #await tree.sync(guild=discord.Object(id=1176396823754190848))
    servers = list(bot.guilds)
    for server in servers:
        print(server.name)

    #await tree.sync(guild=discord.Object(id=1176396823754190848))
    #await tree.sync()
    print('starting task')
    await asyncio.sleep(2)
    print_activity.start()
    print("started")


lock = asyncio.Lock()
@bot.event
async def on_voice_state_update(member, before, after):
    #print(f"{member.name} changed voice state: {before.channel} -> {after.channel}")
    if before.channel is not None and after.channel is None: #someone left the server.
        if member.name in user_activity:
            async with lock:
                user_activity[member.name]['studying'] = False
                user_activity[member.name]['Video'] = False
                user_activity[member.name]['Screen'] = False
                user_activity[member.name]['joined'] = False

    elif before.self_video != after.self_video:
        if after.channel is not None:
            if member.name not in user_activity: 
                async with lock:
                    user_activity[member.name] = {'start_time': datetime.now(), 'total_time': timedelta(),'studying':True, 'Video':True, 'Screen':False, 'joined':True,'warn_time': 0.0,'member':member.id}
            else:

                if user_activity[member.name]['studying'] == True and user_activity[member.name]['Screen'] == False: #kuch video mai change hua hai. and.. agr padh rhe the aur screen false hai. to false set karo
                    async with lock:
                        user_activity[member.name]['studying'] = False
                        user_activity[member.name]['Video'] = False

                elif user_activity[member.name]['studying'] == True and user_activity[member.name]['Screen'] == True: #Kuch video mai change hua and agr padh rhe the and screen on hai. to true hi rahne do. 

                    async with lock:
                        user_activity[member.name]['Video'] = not user_activity[member.name]['Video']
                        user_activity[member.name]['studying'] = True
                        user_activity[member.name]['start_time'] = datetime.now()

                elif user_activity[member.name]['studying'] == False and user_activity[member.name]['Screen'] == False: #kuch video mai change hua hai agr padh nahi rhe the and screen bhi off thi to True kr de
                    async with lock:
                        user_activity[member.name]['Video'] = True
                        user_activity[member.name]['studying'] = True
                        user_activity[member.name]['start_time'] = datetime.now()



    elif before.self_stream != after.self_stream:

        if after.channel is not None:

            if member.name not in user_activity:
                async with lock:
                    user_activity[member.name] = {'start_time': datetime.now(), 'total_time': timedelta(),'studying':True, 'Video':False, 'Screen':True, 'joined':True,'warn_time':0.0, 'member':member.id}
            else:
                if user_activity[member.name]['studying'] == True and user_activity[member.name]['Video'] == False: #kuch video mai change hua hai. and.. agr padh rhe the aur screen false hai. to false set karo
                    async with lock:
                        user_activity[member.name]['studying'] = False
                        user_activity[member.name]['Screen'] = False


                elif user_activity[member.name]['studying'] == True and user_activity[member.name]['Video'] == True: #Kuch video mai change hua and agr padh rhe the and screen on hai. to true hi rahne do. 
                    async with lock:
                        user_activity[member.name]['Screen'] = not user_activity[member.name]['Screen']
                        user_activity[member.name]['studying'] = True
                        user_activity[member.name]['start_time'] = datetime.now()

                elif user_activity[member.name]['studying'] == False and user_activity[member.name]['Video'] == False: #kuch video mai change hua hai agr padh nahi rhe the and screen bhi off thi to True kr de
                    async with lock:
                        user_activity[member.name]['Screen'] = True
                        user_activity[member.name]['studying'] = True
                        user_activity[member.name]['start_time'] = datetime.now()

    elif after.channel is not None: #Someone Entered the server. 
        if member.name in user_activity:
            user_activity[member.name]['joined'] = True

        else:
            user_activity[member.name] = {'start_time': datetime.now(), 'total_time': timedelta(),'studying':False, 'Video':False, 'Screen':False, 'joined':True,'warn_time': 0.0,'member':member.id}


def split_long_string(string):
    """
    Splits a given string into multiple parts, each part being of 2000 or lesser characters.

    Args:
        string: The input string to be split.

    Returns:
        A list of strings, each part being of 2000 or lesser characters.
    """

    # Check if the string length is greater than 2000 characters.
    if len(string) <= 2000:
        return [string]

    # Initialize an empty list to store the split parts.
    split_parts = []

    # Calculate the number of parts the string needs to be split into.
    num_parts = len(string) // 2000

    # If the string length is not evenly divisible by 2000, there will be a remainder.
    remainder = len(string) % 2000

    # Split the string into multiple parts, each of 2000 or lesser characters.
    for i in range(num_parts):
        start_index = i * 2000
        end_index = start_index + 2000
        split_parts.append(string[start_index:end_index])

    # Handle the remainder, if any.
    if remainder > 0:
        start_index = num_parts * 2000
        end_index = start_index + remainder
        split_parts.append(string[start_index:end_index])

    return split_parts


def getresponse(query):
    global HISTORY
    global convo
    global prompt_parts
    global modelv
    global prompttt
    inputted = query
    inputt = inputted
    #FIX PERSONALITY ZERO. READ GOOGLE'S DOCUMENTATION ON THEIR TEXT BASTON MODEL AND FIX HER TO REMEMBER THE PREVIOUS THINGS PROPERLY.


    if personality == 1:
        prompt=inputt
        global HISTORY

        try:
            convo.send_message(prompt)
            #response = model.generate_content(prompt)
            #print(response.text)
            print(convo.last.text)

            response = convo.last.text
            if response == None:
                response = "My appologies, I can't answer you that."



            global HISTORY

            DICTII = {}
            DICTII["role"]="user"
            DICTII["parts"]=prompt
            HISTORY.append(DICTII)
            
            DICTII = {}
            DICTII["role"]="model"
            DICTII["parts"]=response
            HISTORY.append(DICTII)

            print(HISTORY)
            return response

        
        except Exception as A:
            response = "My appologies, I can't answer you that. most probably it's because of my safety features. use personality 0 if you wanna hear controvertial stuff. this personality is based on a safer model"
            response = response + str(A)
            print(A)
            return response

        

    elif personality == 3:
        prompt_parts.append(query)

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        }
        ]

        modelv = genai.GenerativeModel(model_name="gemini-pro-vision",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        try:
            response = modelv.generate_content(prompt_parts)
            print(response.text)
            prompt_parts.append(response.text)
            resp = str(response.text) + " \n \n btw please change to personality 1 when you are done with your queries regarding this image."
            return resp
        
        except Exception as A:
            response = "My appologies, I can't answer you that. most probably it's because of my safety features. use personality 0 if you wanna hear controvertial stuff. this personality is based on a safer model. Try changing personaality to zero."
            response = response + str(A)
            print(A)
            return A



# def upload_to_gemini(path, mime_type=None):
#   """Uploads the given file to Gemini.

#   See https://ai.google.dev/gemini-api/docs/prompting_with_media
#   """
#   file = genai.upload_file(path, mime_type=mime_type)
#   print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#   return file


@bot.event
async def on_message(message):
    global personality
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Respond to DMs
    if isinstance(message.channel, discord.DMChannel):
        print(message.content)
        async with message.channel.typing():
            response = getresponse(message.content)

        if len(response) < 2000:
            await message.author.send(response)

        else:
            split_parts = split_long_string(response)
            for i in split_parts:
                await message.reply(i)

    # Respond to messages in the server if bot is mentioned
    if bot.user.mention in message.content.split():
        print(message.content)
        
        if message.attachments:
            # Delete all previous images
            #delete_previous_images()

            # Download and convert each new image and save it to the local filesystem
            QQueryy = None
            URLS = []
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    url = attachment.url
                    URLS.append(url)

                elif attachment.content_type.startswith('text'):
                    text_content = await attachment.read()
                    # Process the text content as needed
                    QQueryy = text_content.decode('utf-8')
                    print("THE QQUERRY IS")
                    print(QQueryy)
                    

            # Print the list of relative paths
            #print("List of relative paths:", pathss)

            #await message.channel.send("New images downloaded and converted successfully!")
            async with message.channel.typing():
                if QQueryy:
                    if URLS != []:
                        response = await visionresponse(QQueryy,URLS)

                    else:
                        response = getresponse(QQueryy)
                else:
                    response = await visionresponse(message.content,URLS)



            if len(response) < 2000:
                await message.reply(response)
            else:
                '''
                with open('response.txt', 'w', encoding='utf-8') as file:
                    file.write(response)
                await message.channel.send(f"{message.author.mention}, here's the response:", file=discord.File('response.txt'))
                '''
                split_parts = split_long_string(response)
                for i in split_parts:
                    await message.reply(i)




        
        else:   
            async with message.channel.typing():
                response = getresponse(message.content)
            if len(response) < 2000:
                await message.reply(response)
            else:
                '''
                with open('response.txt', 'w', encoding='utf-8') as file:
                    file.write(response)
                '''
                split_parts = split_long_string(response)
                for i in split_parts:
                    await message.reply(i)
    
                #await message.channel.send(f"{message.author.mention}, here's the response:", file=discord.File('response.txt'))




    elif message.reference:
        # Reply mentioning the user who sent the original message
        original_message = await message.channel.fetch_message(message.reference.message_id)
        if original_message.author == bot.user:
            #print(original_message)
            print(message.content)

            if message.attachments:
                # Delete all previous images
                #delete_previous_images()

                # Download and convert each new image and save it to the local filesystem
                QQueryy = None
                URLS = []
                for attachment in message.attachments:
                    if attachment.content_type.startswith('image'):
                        url = attachment.url
                        URLS.append(url)

                    elif attachment.content_type.startswith('text'):
                        text_content = await attachment.read()
                        # Process the text content as needed
                        QQueryy = text_content.decode('utf-8')
                        print("THE QQUERRY IS")
                        print(QQueryy)
                        

                # Print the list of relative paths
                #print("List of relative paths:", pathss)

                #await message.channel.send("New images downloaded and converted successfully!")
                async with message.channel.typing():
                    if QQueryy:
                        if URLS != []:
                            response = await visionresponse(QQueryy,URLS)

                        else:
                            response = getresponse(QQueryy)
                    else:
                        response = await visionresponse(message.content,URLS)



                if len(response) < 2000:
                    await message.reply(response)
                else:
                    '''
                    with open('response.txt', 'w', encoding='utf-8') as file:
                        file.write(response)
                    await message.channel.send(f"{message.author.mention}, here's the response:", file=discord.File('response.txt'))
                    '''
                    split_parts = split_long_string(response)
                    for i in split_parts:
                        await message.reply(i)




            
            else:   
                async with message.channel.typing():
                    response = getresponse(message.content)
                if len(response) < 2000:
                    await message.reply(response)
                else:
                    '''
                    with open('response.txt', 'w', encoding='utf-8') as file:
                        file.write(response)
                    '''
                    split_parts = split_long_string(response)
                    for i in split_parts:
                        await message.reply(i)

        #reply_content = f"Hello, {original_message.author.mention}! You replied to my message."
        #await message.channel.send(reply_content)
    else:
        # Regular reply if not a reply
        pass

    #await bot.(message)

async def visionresponse(query,urls):
    global personality
    global prompt_parts
    global model
    global HISTORY

    prompt_parts = []
    global files
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url)
            image = httpx.get(url)
            prompt_parts.append({'mime_type': 'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')})

            # file = await genai.upload_file(url, mime_type='image/jpeg')
            # print(f"Uploaded file '{file.display_name}' as: {file.uri}")
            # files.append(file)

            # prompt_parts.append(file)
            


    prompt_parts.append(query)

    response = await model.generate_content_async(prompt_parts)
    print(response.text)
    prompt_parts.append(response.text)

    #HISTORY.append(prompt_parts)
    return response.text










    # for i in paths:
    #     img = PIL.Image.open(i)
    #     prompt_parts.append(img)

    # prompt_parts.append(query)

    # response = await modelv.generate_content_async(prompt_parts)
    # print(response.text)
    # prompt_parts.append(response.text)
    # return response.text

'''
async def visionresponse(query, paths):
    global personality
    global prompt_parts

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]

    async def generate_content_async():
        modelv = genai.GenerativeModel(
            model_name="gemini-pro-vision",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        for i in paths:
            img = PIL.Image.open(i)
            prompt_parts.append(img)

        prompt_parts.append(query)

        response = modelv.generate_content(prompt_parts)
        print(response.text)
        prompt_parts.append(response.text)
        return response.text

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, generate_content_async)
    return result
'''
def delete_previous_images():
    global image_counter
    # You can customize the save path as needed
    save_path = "downloaded_images/"

    # Delete all files in the directory
    for file_name in os.listdir(save_path):
        file_path = os.path.join(save_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

    image_counter = 1

async def download_and_save_image(url):
    global image_counter
    global pathss

    # You can customize the save path and filename as needed
    save_path = "downloaded_images/"
    filename = f"image{image_counter}.jpg"

    # Check if the directory exists, create it if not
    os.makedirs(save_path, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()

                # Open the image using Pillow
                image = Image.open(BytesIO(image_data))

                # Convert the image to jpg or png format (you can customize this)
                converted_image = image.convert("RGB")

                # Save the converted image
                converted_image.save(save_path + filename, "JPEG")

                # Increment the image counter for the next image
                image_counter += 1

                # Store the relative path in the list
                relative_path = os.path.join(save_path, filename)
                pathss.append(relative_path)




def gen_key():
    key_base = 1423
    for i in range(10000000):
        key = ''.join(random.choices(ascii_uppercase + digits, k=20))  
        bases = []
        for k in key:
            base = ord(k)
            bases.append(base)
        if sum(bases) == key_base:
            O1 = key[:4] + "-" + key[4:]
            O2 = O1[:9] + "-" + O1[9:]
            O3 = O2[:14] + "-" + O2[14:]
            Final_Key = O3[:19] + "-" + O3[19:]
            #print(f"Valid Key:{Final_Key}")
            return Final_Key










@tasks.loop(minutes=1/2)
async def print_activity():
    try:
        for user_id, activity in user_activity.items():
            if user_activity[user_id]['studying'] == True:
                user_activity[user_id]['total_time'] += datetime.now() - user_activity[user_id]['start_time']
                user_activity[user_id]['start_time'] = datetime.now() 
                user_activity[user_id]['warn_time'] = 0.0

                now = datetime.now()

                for filename in os.listdir("alarms"):  # Check only files in the alarms folder
                    if filename.endswith("_alarm.txt"):
                        user_name = filename[:-10]  # Remove "_alarm.txt" from filename
                        #user = client.get_user(user_name)  # Get the Discord user object
                        print(user_name)
                        print(user_id)
                        if user_id == user_name:
                        #if user:
                            with open(f"alarms/{filename}", "r") as file:
                                description = file.readline().strip()
                                alarm_time_str = file.readline().strip()
                                joined = file.readline().strip()

                            alarm_time = datetime.strptime(alarm_time_str, "%H:%M").time()
                            alarm_window_start = datetime.combine(now.date(), alarm_time)
                            alarm_window_end = alarm_window_start + timedelta(minutes=10)

                            if joined == "True" and alarm_window_start <= now <= alarm_window_end:
                                  # Reset the joined flag
                                try:
                                    print("hor vaii")
                                    user1 = await bot.fetch_user(user_activity[user_id]['member'])
                                    print(user1)
                                    a_key = gen_key()
                                    await user1.send(f"You joined the VC on your decided time for {description}, congrats! \n \n Here's the promised key:- {a_key}")
                                    os.remove(f"alarms/{filename}")
                                except discord.Forbidden:
                                    #await bot.get_channel(interaction.channel_id).send(f"Unable to DM {user.mention}. Please check their privacy settings.")

                                    print("koini")




            else:
               try:
                if user_activity[user_id]['joined'] == True:
                    user_activity[user_id]['warn_time'] += 0.5
                    if user_activity[user_id]['warn_time'] == float(Warn):
                        try:
                            userID = user_activity[user_id]['member']
                            userr = await bot.fetch_user(userID)
                            #userr = user_activity[user_id]['member']
                            await userr.send(f"You haven't turned cam/ss on for {Warn} minutes. Contact @estrizal if you cam/ss was on but you still got this warning.")
                        except:
                            print("koini")
               except Exception as SSt:
                try:
                    print("got and error boss")
                    userr = await bot.fetch_user(756014504004812910)
                    await userr.send("Boss I got this error"+ str(SSt + "user ID is " + str(user_activity[user_id]['member'])))
                except:
                    print("god sabe this child")

            #print(f"User {user_id} has been active for {activity['total_time']}")

        # Save user activity to a text file
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"user_activity_{date_str}.txt"
        #print("\n \n today's date is ", date_str, "\n \n ")

        try:
            with open(filename, 'r') as f:
                f.read()


            with open(filename, 'w') as file:
                #print(user_activity)
                for user_id, activity in user_activity.items():
                    user = user_id#bot.get_user(user_id)
                    #print(user)
                    if user!= None:
                        #print("wrote in the file")
                        file.write(f"{user}: {activity['total_time']}\n")
                        #file.write(f"{user.name}: {activity['total_time']:.2f} minutes\n")
            
        except:
            with open(filename, 'w') as file:
                for user_id, activity in user_activity.items():
                    user = user_id
                    if user!= None:
                        print("wrote in the NEWWW file")
                        user_activity[user_id]['total_time'] = timedelta()
                        file.write(f"{user}: {user_activity[user_id]['total_time']}\n")

    except Exception as SSt:
        try:
            print(str(SSt))
            userr = await bot.fetch_user(756014504004812910)
            await userr.send("Boss I got this error"+ str(SSt))

        except:
            print("god sabe me somehowww")
            




#print_activity.start()

        
#asyncio.create_task(print_activity())
#loopp = asyncio.get_event_loop()
#print_activity.start()
#print_activity.start()
print('ran till the commands')









@tree.command(name='mystats',description= "Shows your stats of today. Basically your study time which you spent with your cam/ss ON")
async def my_stats(interaction: discord.Interaction):
    print("Command received!")
    user_id = interaction.user.name#load_member_data(message.user.id)

    #user_id = ctx.author.name
    if user_id in user_activity:
        total_time = user_activity[user_id]['total_time']
        await interaction.response.send_message(f"You have been active for {total_time}.")
    else:
        await interaction.response.send_message("You have no recorded activity.")



@tree.command(name='get_reward',description= "Will Give you your Websites Unblocking keys if you have studied more than 7 hours.")
async def reward(interaction: discord.Interaction):
    print("Command received!")
    user_id = interaction.user.name#load_member_data(message.user.id)

    #user_id = ctx.author.name
    if user_id in user_activity:
        total_time = user_activity[user_id]['total_time']

        if (total_time.total_seconds() / 3600) >= 7:
            try:
                a_kun = gen_key()
                a_kun = str(a_kun)
                user_id2 = interaction.user.id
                user = await bot.fetch_user(user_id2)
                await user.send(a_kun)

                await interaction.response.send_message(f"You have been active for {total_time} today. Good job. \n your rewarded keys are messaged in DM.")
            except Exception as i:
                i = str(i)
                await interaction.response.send_message(f"An error occured {i} ")
        else:
            await interaction.response.send_message(f"You have been active for {total_time} today, which is less than 7 hours :( \nNo rewards For now. )")
        #await interaction.response.send_message(f"You have been active for {total_time}.")
    else:
        await interaction.response.send_message("You have no recorded activity.")


@tree.command(name='todaystats',description= "Shows today's stats of all the people. note:- Study time spent with cam/ss will be recoreded ONLY")

async def today_stats(interaction: discord.Interaction):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"user_activity_{date_str}.txt"
    with open(filename, 'r') as file:
        r = file.read()
    await interaction.response.send_message(r)




@tree.command(name='allstats', description="shows you the stats of all the people. of all time.")
async def all_stats(interaction: discord.Interaction):
    dayss = 10000000
    listt=[]
    def read_activity_file(file_path):
        """Read and parse the content of a user activity file."""
        user_times = {}
        with open(file_path, 'r') as file:
            for line in file:
                username, time_str = line.strip().split(': ')
                user_times[username] = user_times.get(username, timedelta()) + parse_time(time_str)
        return user_times

    def parse_time(time_str):
        """Parse the time string in the format HH:MM:SS.microseconds."""
        # Split the time string into hours, minutes, and seconds
        time_components = time_str.split(':')

        # Extract the hours and minutes
        hours = int(time_components[0])
        minutes = int(time_components[1])
        
        # Extract the seconds and ignore values after the decimal point
        seconds = int(time_components[2].split('.')[0])

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def main():
        # Get today's date
        today = datetime.now().date()

        # Initialize variables to store total times
        total_times = {}

        # Loop through the past 30 days (adjust as needed)
        for i in range(dayss):
            # Calculate the date for the current iteration
            current_date = today - timedelta(days=i)

            # Generate the file name based on the current date
            file_name = f"user_activity_{current_date.strftime('%Y-%m-%d')}.txt"

            # Check if the file exists
            if os.path.exists(file_name):
                # Read and parse the activity file
                user_times = read_activity_file(file_name)

                # Update the total times
                for username, time_delta in user_times.items():
                    total_times[username] = total_times.get(username, timedelta()) + time_delta
            else:
                # Break the loop if the file doesn't exist
                break

        # Sort the total times in descending order
        sorted_total_times = sorted(total_times.items(), key=lambda x: x[1], reverse=True)

        # Generate the message with emojis for the top three users
        message = ""
        for i, (username, total_time) in enumerate(sorted_total_times):
            if i == 0:
                emoji = "🥇"
            elif i == 1:
                emoji = "🥈"
            elif i == 2:
                emoji = "🥉"
            else:
                emoji = ""
            message += f"{emoji} {username}: {total_time}\n"

        return message

    message = main()
    await interaction.response.send_message(message)







@tree.command(name='state',description="Says True if your cam/ss is on. USED FOR DEBUGGING")
async def state(interaction: discord.Interaction):
    user_id = interaction.user.name
    if user_id in user_activity:
        state = str(user_activity[user_id]['studying'])
        await interaction.response.send_message(f"your studying state is "+ state)
    else:
        await interaction.response.send_message("You have no recorded activity or state.")


@tree.command(name='allstates',description="Tells the state of all people rn. True if cam/ss is on.")
async def allstates(interaction: discord.Interaction):
    s = ''
    for user_id, activity in user_activity.items():
        state = str(user_activity[user_id]['studying'])
        s = s + str(user_id + " : "+ state)+"\n"
    
    await interaction.response.send_message(s)




@tree.command(name='timerr',description="Set a timer for the specified number of minutes.")
async def reminderr(interaction: discord.Interaction, minutes: int, description: str = None):

    """Set a reminder for the specified number of minutes."""
    if description:
        await interaction.response.send_message(f"Reminder set for {minutes} minutes. for the reason:- \n "+description)
        await asyncio.sleep(minutes * 60)
        await interaction.channel.send(f"{interaction.user.mention}, time's up! Your reminder has arrived. reason:- \n" + description)

    else:
        await interaction.response.send_message(f"Reminder set for {minutes} minutes.")
        await asyncio.sleep(minutes * 60)
        await interaction.channel.send(f"{interaction.user.mention}, time's up! Your reminder has arrived.")
  


@tree.command(name='old_stats',description="Tell the stats of n number of days. You can input 0 for today. 1 for yesterday + today.")
async def olddata(interaction: discord.Interaction, dayss: int):
    listt=[]
    def read_activity_file(file_path):
        """Read and parse the content of a user activity file."""
        user_times = {}
        with open(file_path, 'r') as file:
            for line in file:
                username, time_str = line.strip().split(': ')
                user_times[username] = user_times.get(username, timedelta()) + parse_time(time_str)
        return user_times

    def parse_time(time_str):
        """Parse the time string in the format HH:MM:SS.microseconds."""
        # Split the time string into hours, minutes, and seconds
        time_components = time_str.split(':')

        # Extract the hours and minutes
        hours = int(time_components[0])
        minutes = int(time_components[1])
        
        # Extract the seconds and ignore values after the decimal point
        seconds = int(time_components[2].split('.')[0])

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def main():
        # Get today's date
        today = datetime.now().date()

        # Initialize variables to store total times
        total_times = {}

        # Loop through the past 30 days (adjust as needed)
        for i in range(dayss):
            # Calculate the date for the current iteration
            current_date = today - timedelta(days=i)

            # Generate the file name based on the current date
            file_name = f"user_activity_{current_date.strftime('%Y-%m-%d')}.txt"

            # Check if the file exists
            if os.path.exists(file_name):
                # Read and parse the activity file
                user_times = read_activity_file(file_name)

                # Update the total times
                for username, time_delta in user_times.items():
                    total_times[username] = total_times.get(username, timedelta()) + time_delta
            else:
                # Break the loop if the file doesn't exist
                break

        # Print the total times for each user
        for username, total_time in total_times.items():
            listt.append(f"{username}: {total_time}")

    main()
    say = ""
    for i in listt:
        say = say + i + "\n"
    await interaction.response.send_message(say)


@tree.command(name='backup',description="Only the Developer can use this. Means the guy with ishigami DP")
async def backitup(interaction: discord.Interaction):
    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, timedelta)):
                return str(obj)
            '''
            elif isinstance(obj, Member):
                return {
                    'id': obj.id,
                    'name': obj.name,
                    'discriminator': obj.discriminator,
                    'bot': obj.bot,
                    'nick': obj.nick
                }
            '''
            return super().default(obj)
    global user_activity
    if interaction.user.id == 756014504004812910 or interaction.user.id == 899658572634411059:
        actual_activity = user_activity
        s = ''
        for user_id, activity in actual_activity.items():
            actual_activity[user_id]['studying'] = False
            actual_activity[user_id]['Video'] = False
            actual_activity[user_id]['Screen'] = False

        with open('data.json', 'w') as json_file:
            json.dump(actual_activity, json_file, cls=CustomEncoder)
            print("wrote the whole activity.")
            await interaction.response.send_message("wrote the whole activity.")
    
    else:
        await interaction.response.send_message("I am afraid, this command can only be used by the developer.")



@tree.command(name='date', description="Tells the date. COMPLETELY USELESS. Added it coz back in the day, bot was having date issues.")
async def backitup(interaction: discord.Interaction):
    date_str = datetime.now().strftime("%Y-%m-%d")
    await interaction.response.send_message(date_str)


@tree.command(name='load',description="only sasta ishigami can use this.used to restart the bot without dataloss") 
async def load_it(interaction: discord.Interaction):
    global user_activity

    def custom_decoder(obj):
        if 'start_time' in obj:
            obj['start_time'] = datetime.strptime(obj['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        if 'total_time' in obj:
            # Assuming the format of 'total_time' is 'H:M:S'
            #hours, minutes, seconds = map(int, obj['total_time'].split(':'))
            totall = obj['total_time'].split(':')
            hours = int(totall[0])
            minutes = int(totall[1])
            seconds = totall[2]
            seconds = int(math.floor(float(seconds)))
            #print("\n \n \n"+stseconds+"\n \n \n")
            obj['total_time'] = timedelta(hours=hours, minutes=minutes, seconds=int(math.floor(seconds)))
        return obj

    if interaction.user.id == 756014504004812910 or interaction.user.id == 899658572634411059:

        try:
            with open('data.json', 'r') as json_file:
                jason_Data= json_file.read()
                loaded_dict = json.loads(jason_Data, object_hook=custom_decoder)

            user_activity = loaded_dict#json.loads(test_string)
            await interaction.response.send_message("loaded the whole activity.")
        
        except Exception as P:
            print(P)
            await interaction.response.send_message("Couldn't load activity because"+str(P))

    else:
        await interaction.response.send_message("I am afraid. this command can only be used by the developer.")












@tree.command(name='personality',description="Input 0 for Mizuhara. 1 for MORE ACCURATE Chad bot. 2 for.. nah, 2 is useless. idk why I made 2")
async def personalityy(interaction: discord.Interaction, typee: int):
    global personality
    global convo
    global HISTORY
    global prompttt
    """Set personality. 0 for mizuhara. 1 for chat bot with more advance capabilities. 2 for saima from one punch man"""
    if typee == 0:
        # global prompt_parts
        # await interaction.response.send_message(f"{interaction.user.mention}, Ok. peronality set to Mizuhara. Based on the old baston. wayyy inaccurate and dumb. Hence wayyy more  fun.")
        # personality = typee
        # prompttt = backkup
        # prompt_parts = []
        typee = 1

    if typee == 1:
        await interaction.response.send_message(f"{interaction.user.mention}, Ok. peronality set to Chad bot. Based on gemini. the only actual compeitor of GPT-4 in the market")
        personality = typee
        HISTORY = []
        convo = model.start_chat(history=HISTORY)
        prompt_parts = []

        

    if typee == 2:
        pass
        # global chatbot
        
        # auth_cookie = None
        # with open("./cocky.json", encoding="utf-8") as file:
        #     cookies_json = json.load(file)
        #     for cookie in cookies_json:
        #         if cookie["name"] == "_U":
        #             auth_cookie = cookie["value"]
        #             break


        #     #users_chatbot[user_id] = UserChatbot(cookies=cookies_json, auth_cookie=auth_cookie, user_id=user_id)


        # cookies=cookies_json

        # # Create a Chatbot object

        # print("cookie_made. yeahhh")

        # chatbot = Chatbot(cookies=cookies)

        
        
        # await interaction.response.send_message(f"{interaction.user.mention}, Ok. peronality set to GPT on steroids, A.K.A. Bing ai")
        # personality = typee



@tree.command(name='max_token',description="want a longer reply ? no problem. input a bigger number. like 2048 here.")
async def max_token(interaction: discord.Interaction, tokii: int):
    # global output_token
    # global defaults
    # global generation_config
    # global model
    # global convo
    # output_token = tokii
    # defaults = {
    # 'model': 'models/text-bison-001',
    # 'temperature': 0.7,
    # 'candidate_count': 1,
    # 'top_k': 40,
    # 'top_p': 0.95,
    # 'max_output_tokens': output_token,
    # 'stop_sequences': [],
    # 'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_TOXICITY","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_VIOLENCE","threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_SEXUAL","threshold":"BLOCK_NONE"},{"category":"HARM_CATEGORY_MEDICAL","threshold":"BLOCK_ONLY_HIGH"},{"category":"HARM_CATEGORY_DANGEROUS","threshold":"BLOCK_ONLY_HIGH"}],
    # }

    # generation_config = {
    # "temperature": 0.4,
    # "top_p": 1,
    # "top_k": 1,
    # "max_output_tokens": output_token,
    # }


    # model = genai.GenerativeModel(model_name="gemini-pro",
    #                           generation_config=generation_config,
    #                           safety_settings=safety_settings)


    # convo = model.start_chat(history=HISTORY)
    await interaction.response.send_message(f"{interaction.user.mention}, Changing of token has been disabled for now. It's set to 10k by default. If you want to change it, contact @estrizal")








@tree.command(name='changeactivity',description="Used to change the stats of people. can't be used by anyone except estrizal")
async def changetheactivity(interaction: discord.Interaction, args: str):
    global user_activity
    if interaction.user.id == 756014504004812910:
        try:
            args = args.split()
            print("username doneeeeeeeeeeeeeeeeeee")
            user_name, thing, bhalue = args[:3]
            print("user info extractedddddddddddd")
            keyy = thing.split(":")
            print('split doneeeeeeeeeeee')
            valuee = bhalue.split(":")
            print('split 2 doneeeeeeeee')
            my_dict = dict(zip(keyy, valuee))
            print('zippingggggg')
            print(my_dict)

            for k,v in my_dict.items():
                    print("loop runnin",k)
                    if k == 'Video' and v == 't':
                        user_activity[user_name]['Video'] = True

                    if k == 'Video' and v == 'f':
                        user_activity[user_name]['Video'] = False

                    if k == 'Screen' and v == 't':
                        user_activity[user_name]['Screen'] = True

                    if k == 'Screen' and v == 'f':
                        user_activity[user_name]['Screen'] = False

                    if k == 'studying' and v == 't':
                        user_activity[user_name]['studying'] = True

                    if k == 'studying' and v == 'f':
                        user_activity[user_name]['studying'] = False

                    if k == 'total_time':
                        user_activity[user_name]['total_time'] += timedelta(minutes=int(v))

            await interaction.response.send_message("Updated")

        except Exception as SmallU:
            try:
                await interaction.response.send_message(str(SmallU))
                print(str(SmallU))
            except:
                await interaction.response.send_message("an error has occured")
                print("error occured")

    else:
        await interaction.response.send_message("I am afraid, this is a developer only command. do !pika to see your usable commands")
                









        

class ButtonVieww(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, conversation_style_str:str, suggest_responses:list, chatbot):
        super().__init__(timeout=120)
        self.button_author =interaction.user.id

        # Add buttons
        for label in suggest_responses:
            button = discord.ui.Button(label=label)
            # Button event
            async def callback(interaction: discord.Interaction, button: discord.ui.Button):     
                if  interaction.user.id != self.button_author:
                    await interaction.response.defer(ephemeral=True, thinking=True)
                    await interaction.followup.send("You don't have permission to press this button.")
                else:
                    await interaction.response.defer(ephemeral=False, thinking=True)
                    # When click the button, all buttons will disable.
                    for child in self.children:
                        child.disabled = True
                    await interaction.followup.edit_message(message_id=interaction.message.id, view=self)
                    username = str(interaction.user)
                    usermessage = button.label
                    channel = str(interaction.channel)
                    #logger.info(f"\x1b[31m{username}\x1b[0m : '{usermessage}' ({channel}) [Style: {conversation_style_str}] [button]")
                    await self.send_message(chatbot, interaction, usermessage)


            self.add_item(button)
            self.children[-1].callback = partial(callback, button=button)



    def setupp(self, interaction: discord.Interaction, conversation_style_str:str, suggest_responses:list, chatbot):
        super().__init__(timeout=120)
        self.button_author =interaction.user.id

        # Add buttons
        for label in suggest_responses:
            button = discord.ui.Button(label=label)
            # Button event
            async def callback(interaction: discord.Interaction, button: discord.ui.Button):     
                if  interaction.user.id != self.button_author:
                    await interaction.response.defer(ephemeral=True, thinking=True)
                    await interaction.followup.send("You don't have permission to press this button.")
                else:
                    await interaction.response.defer(ephemeral=False, thinking=True)
                    # When click the button, all buttons will disable.
                    for child in self.children:
                        child.disabled = True
                    await interaction.followup.edit_message(message_id=interaction.message.id, view=self)
                    username = str(interaction.user)
                    usermessage = button.label
                    channel = str(interaction.channel)
                    #logger.info(f"\x1b[31m{username}\x1b[0m : '{usermessage}' ({channel}) [Style: {conversation_style_str}] [button]")
                    await self.send_message(chatbot, interaction, usermessage)


            self.add_item(button)
            self.children[-1].callback = partial(callback, button=button)





    async def send_message(self, chatbot, interaction, usermessage):

        conversation_style_str = "balanced"
        user_message = str(usermessage)
        reply = ''
        text = ''
        link_embed = ''
        all_url = []
        exceptionn = 0

    
        #if not interaction.response.is_done():
            #await interaction.response.defer(thinking=True)

        try:
            # Change conversation style
            if conversation_style_str == "creative":
                conversation_style=ConversationStyle.creative
            elif conversation_style_str == "precise":
                conversation_style=ConversationStyle.precise
            else:
                conversation_style=ConversationStyle.balanced

            reply = await chatbot.ask(
                prompt=user_message,
                conversation_style=conversation_style,
                simplify_response=True,
            )

            # Get reply text
            text = f"{reply['text']}"
            text = re.sub(r'\[\^(\d+)\^\]', lambda match: '', text)
            
            # Get the URL, if available
            urls = re.findall(r'\[(\d+)\. (.*?)\]\((https?://.*?)\)', reply["sources_link"])
            if len(urls) > 0:
                for url in urls:
                    all_url.append(f"{url[0]}. [{url[1]}]({url[2]})")
                link_text = "\n".join(all_url)
                link_embed = discord.Embed(description=link_text)
            
            # Set the final message
            user_message = user_message.replace("\n", "")
            ask = f"> **{user_message}** - <@{str(interaction.user.id)}> (***style: {conversation_style_str}***)\n\n"
            response = f"{ask}{text}"
            msg = await interaction.original_response()
            # Discord limit about 2000 characters for a message
            while len(response) > 2000:
                temp = response[:2000]
                response = response[2000:]
                
                await msg.edit(content=temp)
                
            suggest_responses = reply["suggestions"]
            
            #await msg.edit(content=f"> **Error: {e}**")         
            if link_embed:
                await msg.edit(content=response, view=self.setupp(interaction, conversation_style_str, suggest_responses, chatbot), embed=link_embed)
            else:
                await msg.edit(content=response, view=self.setupp(interaction, conversation_style_str, suggest_responses, chatbot))

        except Exception as ekka:
            msg = await interaction.original_response()
            await msg.edit(content=f"> **ERROR: {ekka}**")
            #print((f"> **ERROR: {e}**"))
            #chatbot.reset()
















    #await interaction.channel.send(f"{interaction.user.mention}, time's up! Your reminder has arrived.")












    

@tree.command(name='allactivity',description="YET ANOTHER USELESS COMMAND. But.. OK.")
async def activity(interaction: discord.Interaction):
    if interaction.user.id == 756014504004812910:
        global user_activity
        await interaction.response.send_message(str(user_activity))
    else:
        await interaction.response.send_message("This is a developer only command. I am afraid, I can't show you all activity dictionary.")

@tree.command(name='pika',description="was useful someday.")
async def commandhelp(interaction: discord.Interaction):
    a = "* **!mystats** -- This shows your universal stats (or stats after the event started)\n"

    b = "* **!todaystats** -- Everyone's today's stats\n"       

    c = "* **!allstats** -- Everyone's Universal stats (or stats after the event started)\n"
    d = "* **!state** -- Tells your state as recorded by the bot. True = studying. if you are studying with cam/screen share. but it shows false, contact @estrizal\n"            
    e="* **!timerr** -- Reminds you after the mentioned time.\n"
    f="* **!old_stats** -- gives you data of mentioned no. of days. like put 4 for stats of today + past 3 days.\n"
    g = "* **!pika** -- this command you just used\n"
    h = "* **allstates** -- Tells studying state of everyone. True = studying.\n"
    await interaction.response.send_message("Commands are:- \n" + a + b + c + d + e + f + g + h )


@tree.command(name='admineventstart')
async def clear(interaction: discord.Interaction):
    global user_activity
    if interaction.user.id == 756014504004812910:
        user_activity = {}
        await interaction.response.send_message("Today stats cleared sirr")
    else:
        await interaction.response.send_message("I am afraid, this command cannot be used by you.")


@tree.command(name='syncommands',description="syncs commands. only developer command.")
async def syncc(interaction: discord.Interaction):
    #global user_activity
    if interaction.user.id == 756014504004812910:
        await tree.sync()
        await interaction.response.send_message("Synced perfectly sirr")

    else:
        await interaction.response.send_message("I am afraid, this command cannot be used by you.")



@tree.command(name='devsynched',description="syncs commands for the guild. only developer command.")
async def syncc(interaction: discord.Interaction):
    #global user_activity
    if interaction.user.id == 756014504004812910:
        await tree.sync(guild=discord.Object(id=1176396823754190848))
        await interaction.response.send_message("Synced perfectly sirr")

    else:
        await interaction.response.send_message("I am afraid, this command cannot be used by you.")







@tree.command(name="set_goal", description="Sets an alarm with a description")
async def set_alarm(interaction: discord.Interaction, time: str, timezone: str, description: str):
    
    time_obj = datetime.strptime(time, "%H:%M")
    
    # Convert the timezone string to a datetime.timedelta object
    try:
        timezone=timezone.replace("+","")
        hourss, minutess = timezone.split(':')
        
        timezone_delta = timedelta(hours=int(hourss), minutes=int(minutess))
        
        # Create a timezone object using the timedelta
        timezone_obj = tz.tzoffset(None, timezone_delta.seconds)
        
        # Apply the timezone to the time object
        time_obj = time_obj.replace(tzinfo=timezone_obj)
    except:
        if timezone == "IST":
            timezone_delta = timedelta(hours=5, minutes=30)
            
            # Create a timezone object using the timedelta
            timezone_obj = tz.tzoffset(None, timezone_delta.seconds)
            
            # Apply the timezone to the time object
            time_obj = time_obj.replace(tzinfo=timezone_obj)

        else:
            timezone_obj = pytz.timezone(timezone)
            #timezone_obj = tz.tzstr(timezone)
            timezone_obj = timezone_obj or pytz.timezone(timezone)
            print("Timezone object is", timezone_obj)
            
            # Apply the timezone to the time object
            time_obj = time_obj.replace(tzinfo=timezone_obj)
            print("time there is", time_obj)



    print("time there is", time_obj)

    # Convert to UTC first

    utc_time = time_obj.astimezone(tz.UTC)
    print("time at UTC is", utc_time)
    
    # Then convert to IST
    indian_time = timedelta(hours=5, minutes=30)
    ist_time = utc_time + indian_time
    print("time at IST is", ist_time)

    # Create the alarms folder if it doesn't exist
    os.makedirs("alarms", exist_ok=True)

    # Create the text file with the alarm details in the alarms folder
    with open(f"alarms/{interaction.user.name}_alarm.txt", "w") as file:
        file.write(f"{description}\n")
        file.write(f"{ist_time.strftime('%H:%M')}\n")
        file.write(f"True\n")

    await interaction.response.send_message(f"Alarm set for {ist_time.strftime('%H:%M IST')} with the description: {description}")







@tree.command(name='create_image', description="Generates an image from the prompt.")
async def create_image(interaction: discord.Interaction, prompt: str):
    auth_cookie = None
    with open("./cocky.json", encoding="utf-8") as file:
        cookies_json = json.load(file)
        for cookie in cookies_json:
            if cookie["name"] == "_U":
                auth_cookie = cookie["value"]
                break

    print("cookie_made. yeahhh")

    try:
        if not interaction.response.is_done():
            await interaction.response.defer(thinking=True)

        embeds = []
        user_id = interaction.user.id
        username = interaction.user
        channel = interaction.channel
        prompts = f"> **{prompt}** - <@{str(interaction.user.id)}> (***BingImageCreator***)\n\n"

        # Fetches image links
        async_gen = ImageGenAsync(auth_cookie=auth_cookie, quiet=True)
        images = await async_gen.get_images(prompt=prompt, timeout=300)

        # Add embed to list of embeds
        [embeds.append(discord.Embed(url="https://www.bing.com/").set_image(url=image_link)) for image_link in images]

        button_view = ButtonView(interaction, prompt, user_id, images)
        await interaction.followup.send(prompts, embeds=embeds, view=button_view)

    except asyncio.TimeoutError:
        await interaction.followup.send("> **Error: Request timed out.**")

    except Exception as e:
        if str(e) == "Bad images" or str(e) == "Your prompt has been blocked by Bing. Try to change any bad words and try again.":
            try:
                f = open("dream_api.txt")
                api_hai = f.read()
                api = api_hai
                f.close()
                responsee = dream.dream_image(api,prompt)
                if responsee == True:
                    print("image made by dream")
                    await interaction.followup.send("couldn't make image from bing, so i made it from dream AI. Image quality might be worse. but rest assured, the images made are going to be SFW.",file=discord.File("Dreamed.png"))

                elif responsee == False:
                    await interaction.followup.send("You ordered something tooooo complex. cuz 2 diff. ai refused your request. :sunglasses: Or.. it was something that was against their safety policy.")
            except Exception as e:
                await interaction.followup.send(f"> **Error: {e}**")
        else:
            await interaction.followup.send(f"> **Error: {e}**")


class ButtonView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, prompt: str, user_id: int, images: list[str]):
        super().__init__(timeout=180)
        self.button_author = interaction.user.id
        self.prompt = prompt
        self.user_id = user_id
        self.images = images

    # Button event 
    @discord.ui.button(label="Regenerate", emoji="🔂")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.button_author:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await interaction.followup.send("You don't have permission to press this button.")
        else:
            await interaction.response.defer(ephemeral=False, thinking=True)
            await self.regenerate_images(interaction)

    async def regenerate_images(self, interaction: discord.Interaction):
        #embeds = [discord.Embed(url="https://www.bing.com/").set_image(url=image_link) for image_link in self.images]
        auth_cookie = None
        with open("./cocky.json", encoding="utf-8") as file:
            cookies_json = json.load(file)
            for cookie in cookies_json:
                if cookie["name"] == "_U":
                    auth_cookie = cookie["value"]
                    break

        msg = await interaction.original_response()
        print("cookie_made. yeahhh")
        try:

            embeds = []

            prompt=self.prompt
            # Fetches image links
            async_gen = ImageGenAsync(auth_cookie=auth_cookie, quiet=True)
            images = await async_gen.get_images(prompt=prompt, timeout=300)

            # Add embed to list of embeds
            [embeds.append(discord.Embed(url="https://www.bing.com/").set_image(url=image_link)) for image_link in images]

            #button_view = ButtonView(interaction, prompt, user_id, images)
            #await interaction.followup.send(prompts, embeds=embeds, view=button_view)
        

        except asyncio.TimeoutError:
            await msg.edit(content=f"> **Error: Request timed out.**")


        except Exception as e:
            await msg.edit(content=f"> **Error: {e}**")



        '''
        await interaction.followup.edit(
            #followup_id=interaction.followup.id,
            content=f"> **{self.prompt}** - <@{str(self.user_id)}> (***BingImageCreator***)\n\n",
            embeds=embeds,
            view=self
        )
        '''
        msg = await interaction.original_response()
        await msg.edit(
            #followup_id=interaction.followup.id,
            content=f"> **{self.prompt}** - <@{str(self.user_id)}> (***BingImageCreator***)\n\n",
            embeds=embeds,
            view=self
        )



# Run the bot
bot.run(BOT_API) #Your API keys, which you added at the start of the file

print("bot is up and running")
