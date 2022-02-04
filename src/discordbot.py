from discord.ext import commands #type:ignore
import cv2 as cv #type:ignore
import discord #type:ignore
import os

from detector import Detector
from webscrape import get_tenor
from consts import EPILEPSY_DETECTION_REACTIONS

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=discord.Status.invisible)
    print(f'{bot.user} connected')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    """
    checks the first attachment of every message, if a video exists in its place,
    perform a detection analysis, otherwise just pass
    
    if nothing was attached, there may still possibly be a tenor that was sent; that will be checked
    """
    if message.author == bot.user:
        return
    
    attachments = message.attachments
    file_mdta = ''
    if not attachments:
        message_text: str = message.content

        if message_text.startswith('https://tenor.com/'): #if true, message text would be the wanted link
            # check for epilepsy in this gif through webscraping

            file_mdta = get_tenor(link=message_text)
            gif = cv.VideoCapture(file_mdta)
            check = Detector(gif).epilepsy()
            # print(check)
            if check:
                for reaction in EPILEPSY_DETECTION_REACTIONS:
                    await message.add_reaction(reaction)
            
            gif=None # killing the opencv control over this gif file to be able to delete the file
            os.remove(file_mdta)

        return # once the analysis of a theoretical gif is done, 
               # or if the message doesn't have any attachments or tenor links, pass this message

    video = message.attachments[0]
    if video.content_type != 'video/mp4':
        return

    file_name = video.filename
    if os.path.isfile(file_name):
        file_name = f'T{file_name}'
        await video.save(file_name)
    else: 
        await video.save(file_name)

    check = Detector(cv.VideoCapture(file_name)).epilepsy()
    if check:
        for reaction in EPILEPSY_DETECTION_REACTIONS:
            await message.add_reaction(reaction)

    os.remove(file_name)




@bot.command()
async def bruh(ctx):
    await ctx.send(bot.user)

TOKEN = "[ADD_YOUR_TOKEN_HERE]"
bot.run(TOKEN)
