import discord
import os
import requests
from discord.ext import commands
from deepgram import Deepgram

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

DISCORD_BOT_TOKEN = '<your discord bot token here>'
DEEPGRAM_API_KEY = '<your deepgram api key here>'

dg_client = Deepgram(DEEPGRAM_API_KEY)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is online and ready.')

@bot.event
async def on_message(message):
    print(f'Got a message {message}')
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.ogg') or attachment.filename.endswith('.mp3') or attachment.filename.endswith('.wav') or attachment.filename.endswith('.m4a'):
                print("message seems to have audio attachment")
                audio_url = attachment.url
                transcription = await transcribe_audio(audio_url)

                print(f"Transcription {transcription}")

                # Create a thread for the message
                thread = await message.create_thread(
                    name=f"Transcription",
                    auto_archive_duration=60
                )

                # Send the transcription in the thread
                await send_long_message(thread, transcription)


async def send_long_message(channel, message):
    max_length = 2000
    while len(message) > max_length:
        # Find the last space within the max_length limit
        split_index = message.rfind(' ', 0, max_length)
        if split_index == -1:
            split_index = max_length

        # Send the part up to the split point
        await channel.send(message[:split_index])
        # Remove the part that was sent
        message = message[split_index:].lstrip()

    # Send any remaining part of the message
    await channel.send(message)

async def transcribe_audio(audio_url):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()

        audio_bytes = response.content

        source = {
            'buffer': audio_bytes,
            'mimetype': 'application/octet-stream'
        }

        response = await dg_client.transcription.prerecorded(source, {'smart_format': 'true', 'model': 'whisper-large'})
        print("deepgram response", response)
        paragraphs = response['results']['channels'][0]['alternatives'][0]['paragraphs']

        return response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']
    except Exception as e:
        print(f'Error transcribing audio: {e}')
        return 'Failed to transcribe audio.'

bot.run(DISCORD_BOT_TOKEN)
