from discord.ext import commands #type:ignore
import cv2 as cv #type:ignore
import discord #type:ignore
from typing import Annotated, Any, Union
import os

from keyvars.consts import EPILEPSY_DETECTION_REACTIONS, GIF_DANG_TRIG_REQ, GIF_DRAM_PIX_CHANGE
from keyvars.mytypes import DiscordMessageReactions
from webscrape import get_tenor
from detector import Detector

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready() -> None:
	await bot.change_presence(status=discord.Status.invisible)
	print(f'{bot.user} connected')

@bot.event
async def on_message(message: Any) -> Annotated[None, 'or', DiscordMessageReactions]:
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

		if message_text.startswith('https://tenor.com/'):
			# if true, the link to webscrape would be the message

			# check for epilepsy in this gif through webscraping
			file_mdta = get_tenor(link=message_text)
			gif = cv.VideoCapture(file_mdta)
			check = Detector(gif).epilepsy(
				is_gif=True, 
				dramatic_pixel_change=GIF_DRAM_PIX_CHANGE,
				danger_trigger_requirement=GIF_DANG_TRIG_REQ
			)
			# print(check)

			if check:
				for reaction in EPILEPSY_DETECTION_REACTIONS:
					await message.add_reaction(reaction)
			
			gif=None # killing the opencv control over this gif file to be able to delete the file
			os.remove(file_mdta)

		return # enough has been analyzed or avoid a plain text message

	video = message.attachments[0]
	if video.content_type != 'video/mp4':
		return

	file_name = video.filename
	if os.path.isfile(file_name):
		file_name = f'T{file_name}'
		await video.save(file_name)
	else: 
		await video.save(file_name)

	# readjust for .mp4 since the gifs changed adjustments
	check = Detector(cv.VideoCapture(file_name)).epilepsy()
	if check:
		for reaction in EPILEPSY_DETECTION_REACTIONS:
			await message.add_reaction(reaction)

	os.remove(file_name) # can be done before doing discord reactions




@bot.command()
async def bruh(ctx):
	await ctx.send(bot.user)

TOKEN = "[ADD_YOUR_TOKEN_HERE]"
bot.run(TOKEN)
