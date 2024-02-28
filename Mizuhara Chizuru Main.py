import discord
from discord.ext import commands, tasks
from discord import app_commands
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

from functools import partial
import re
from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle
import dream 
import jailbreak



user_activity = {}

# Define intents

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.presences = True
intents.message_content = True  # Add this line to enable MESSAGE_CONTENT intent


bot = discord.Client(command_prefix = "/", help_command = True, intents=intents)
tree = app_commands.CommandTree(bot)

Warn = 30

# Dictionary to store user activity


auth_cookie = None
with open("./cocky.json", encoding="utf-8") as file:
    cookies_json = json.load(file)
    for cookie in cookies_json:
        if cookie["name"] == "_U":
            auth_cookie = cookie["value"]
            break
cookies=cookies_json

    #users_chatbot[user_id] = UserChatbot(cookies=cookies_json, auth_cookie=auth_cookie, user_id=user_id)




# Create a Chatbot object

print("cookie_made. yeahhh")

chatbot = Chatbot(cookies=cookies)







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
    await asyncio.sleep(8)
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






@bot.event
async def on_message(message):
    global personality
    mess = message
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Respond to DMs
    if isinstance(message.channel, discord.DMChannel):
        print(message.content)
        async with message.channel.typing():
            print(message.content)
            gg = await message.reply("<a:mizuhara:1205591287886250076>")#"<a:3129kitty:1196499415632969798>")
            mess = message
            response = await jailbreak.send_messagee(message.content,gg,mess)
            if response == False:
                if message.content == "terminate":
                    jailbreak.ter()

                
                await message.author.send("already responding. please wait.")

    # Respond to messages in the server if bot is mentioned
    if bot.user.mention in message.content.split():
        print(message.content)
        
        if message.attachments:
            # Delete all previous images
            """
            delete_previous_images()

            # Download and convert each new image and save it to the local filesystem
            for attachment in message.attachments:
                url = attachment.url
                await download_and_save_image(url)

            # Print the list of relative paths
            print("List of relative paths:", pathss)

            await message.channel.send("New images downloaded and converted successfully!")
            async with message.channel.typing():
                response = visionresponse(message.content,pathss)
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
            """
            try:
                attachment = message.attachments[0]
                print(attachment.url)
                image_url = attachment.url
                async with message.channel.typing():
                    print(message.content)
                    gg = await message.reply("<a:mizuhara:1205591287886250076>")
                    response = await jailbreak.send_messagee(message.content,gg,mess,image_url)
                    if response == False:
                        await gg.edit(content="ALREADY RESPONDING")
            except Exception as p:
                await gg.edit(content=f"exception happened {p}")





        
        else:   
            async with message.channel.typing():
                print(message.content)
                gg = await message.reply("<a:mizuhara:1205591287886250076>")
                response = await jailbreak.send_messagee(message.content,gg,mess)
                if response == False:
                    if message.content == "terminate":
                        jailbreak.ter()

                    
                    await message.author.send("already responding. please wait.")

        
                #await message.channel.send(f"{message.author.mention}, here's the response:", file=discord.File('response.txt'))




    elif message.reference:
        # Reply mentioning the user who sent the original message
        original_message = await message.channel.fetch_message(message.reference.message_id)
        if original_message.author == bot.user:
            #print(original_message)
            print(message.content)


            if message.attachments:
                # Delete all previous images
                """
                delete_previous_images()

                # Download and convert each new image and save it to the local filesystem
                for attachment in message.attachments:
                    url = attachment.url
                    await download_and_save_image(url)

                # Print the list of relative paths
                print("List of relative paths:", pathss)

                await message.channel.send("New images downloaded and converted successfully!")
                async with message.channel.typing():
                    response = await visionresponse(message.content,pathss)

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
                
                """
                try:
                    attachment = message.attachments[0]
                    print(attachment.url)
                    image_url = attachment.url
                    async with message.channel.typing():
                        print(message.content)
                        gg = await message.reply("<a:mizuhara:1205591287886250076>")
                        response = await jailbreak.send_messagee(message.content,gg,mess,image_url)
                        if response == False:
                            await gg.edit(content="ALREADY RESPONDING")
                except Exception as p:
                    await gg.edit(content=f"exception happened {p}")




            else:
                async with message.channel.typing():
                    original_message = await message.channel.fetch_message(message.reference.message_id)
                    if original_message.author == bot.user:
                        #print(original_message)
                        print(message.content)
                        gg = await message.reply("<a:mizuhara:1205591287886250076>")
                        response = await jailbreak.send_messagee(message.content,gg,mess)
                        if response == False:
                            if message.content == "terminate":
                                jailbreak.ter()

                            
                            await message.author.send("already responding. please wait.")


        #reply_content = f"Hello, {original_message.author.mention}! You replied to my message."
        #await message.channel.send(reply_content)
    else:
        # Regular reply if not a reply
        pass

    #await bot.(message)




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


@tree.command(name='reset_chat',description= "Resets the chat. self explainatory.")
async def reset(interaction: discord.Interaction):
    print("Command received!")
    user_id = interaction.user.name#load_member_data(message.user.id)

    jailbreak.reset()
    await interaction.response.send_message(f"CHAT RESET Success.")



@tree.command(name='personality_shift',description="Changes personality according to the description you give.")
async def persona(interaction: discord.Interaction, description: str):

    """Changes personality according to how you define it."""
    jailbreak.define_personality(description)
    await interaction.response.send_message(f"Personality Reset Success.")
  
@tree.command(name='style_shift',description="Choose interaction style. 1 for balanced. 2 for creative. 3 for precise.")
async def changestyle(interaction: discord.Interaction, style: int):

    """Changes style of responses. balanced,creative,precise."""
    if style == 1 or style == 2 or style == 3:
        jailbreak.change_style(style)
        pit = ""
        if style == 1:
            pit = 'balanced'
        if style == 2:
            pit = 'creative'
        if style == 3:
            pit = 'precise'
        await interaction.response.send_message(f"Response style changed to {pit}")
    

    else:
        await interaction.response.send_message(f"ENTER THE NUMBER FROM 1 TO 3 ONLY.")
  




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






@tree.command(name='changeactivity',description="Used to change the stats of people. can't be used.")
async def changetheactivity(interaction: discord.Interaction, args: str):
    global user_activity
    if interaction.user.id == 756014504004812910 or interaction.user.id == 899658572634411059:
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
                        if int(v) < 0:
                            v = int(v)
                            v = v*(-1)
                            user_activity[user_name]['total_time'] -= timedelta(minutes=int(v))
                        
                        else:
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
                




    

@tree.command(name='allactivity',description="YET ANOTHER USELESS COMMAND. But.. OK.")
async def activity(interaction: discord.Interaction):
    if interaction.user.id == 756014504004812910 or 899658572634411059:
        global user_activity
        await interaction.response.send_message(str(user_activity))
    else:
        await interaction.response.send_message("This is a developer only command. I am afraid, I can't show you all activity dictionary.")

@tree.command(name='pika',description="was useful someday.")
async def commandhelp(interaction: discord.Interaction):
    await interaction.response.send_message("Commands are:- ")
    a = "* **!mystats** -- This shows your universal stats (or stats after the event started)\n"

    b = "* **!todaystats** -- Everyone's today's stats\n"       

    c = "* **!allstats** -- Everyone's Universal stats (or stats after the event started)\n"
    d = "* **!state** -- Tells your state as recorded by the bot. True = studying. if you are studying with cam/screen share. but it shows false, contact @estrizal\n"            
    e="* **!timerr** -- Reminds you after the mentioned time.\n"
    f="* **!old_stats** -- gives you data of mentioned no. of days. like put 4 for stats of today + past 3 days.\n"
    g = "* **!pika** -- this command you just used\n"
    h = "* **allstates** -- Tells studying state of everyone. True = studying.\n"
    await interaction.response.send_message(a + b + c + d + e + f + g + h )


@tree.command(name='admineventstart')
async def clear(interaction: discord.Interaction):
    global user_activity
    if interaction.user.id == 756014504004812910 or 899658572634411059:
        user_activity = {}
        await interaction.response.send_message("Today stats cleared sirr")
    else:
        await interaction.response.send_message("I am afraid, this command cannot be used by you.")


@tree.command(name='syncommands',description="syncs commands. only developer command.")
async def syncc(interaction: discord.Interaction):
    #global user_activity
    if interaction.user.id == 756014504004812910 or 899658572634411059:
        await tree.sync()
        await interaction.response.send_message("Synced perfectly sirr")

    else:
        await interaction.response.send_message("I am afraid, this command cannot be used by you.")



@tree.command(name='devsynched',description="syncs commands for the guild. only developer command.")
async def syncc(interaction: discord.Interaction):
    #global user_activity
    if interaction.user.id == 756014504004812910 or 899658572634411059:
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

    #auth_cookie = "1rEjo-NyvZNzyj-hwD0zzSx9yWTyiiAvA1crOOmtXlz9c0oDPQpLLBtgtTbwhpnwcwJJaYMvDNW84Fg3iPe4jMOdz7u5HjrKZq7fekz7eLqypY1nmRynVCcUqNc0ZsZvesJ10fSftJXzlljumBRZkEjGjdxxZwIrAoaOKy-CuZuFKNInByBwh6IdUbfY-6cRJroZ4bjEU6_aKBu9DHJL9PfFU33WwJGpBh8R4CfArySY"
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



bot.run("NEVER GONNA GIVE YOU up")

print("bot is up and running")
