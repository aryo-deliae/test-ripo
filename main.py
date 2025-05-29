import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, app_commands
import arvestapi
from commandes import upload_image
from pdf2image import convert_from_path
from PIL import Image
from urllib.request import urlopen
from keep_alive import keep_alive

load_dotenv()

key_bot = os.getenv('BOT_KEY')
mail = os.getenv('MAIL')
password = os.getenv('PASS')

intents = discord.Intents.default()
intents.message_content = True

#client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)

racine = (os.getcwd())

@bot.event
async def on_ready():
    print(f'Je me suis bien connecté en tant que {bot.user}')

@bot.event
async def on_message(message):

    if message.content == "!o":
        lien_brut = str(message.attachments)
        upload_image(mail, password, lien_brut)
        await message.channel.send("image uploaded !")


    if message.content == "!pdf":
        
        ar = arvestapi.Arvest(mail, password)

        #Recuperation de la piece jointe 

        fichier = message.attachments
        
        chemin = os.path.join(racine,"img")

        for attachment in fichier :
            await attachment.save(attachment.filename)
            name = attachment.filename

        file_name = name.replace('.pdf', '')
        chemin = os.path.join(racine,name)

        # Conversion en JPEG
        image = convert_from_path(chemin, 72)
        os.remove(chemin)

        num_page = 0

        #Upload des medias sur Arvest
        for i, page in enumerate(image):
            img_name = f"{file_name}_page_{i + 1}.jpeg"
            output_path = os.path.join("file", img_name)
            page.save(output_path, 'JPEG')
            added_media = ar.add_media(path = output_path)
            os.remove(output_path)
            num_page += 1

        await message.channel.send(f"upload the pdf as {num_page} medias")
        
        medias = ar.get_medias()
        nom_manifest = file_name

        #Creation et upload du manifest
        medias_pdf_to_manifest(medias, nom_manifest, racine, ar)

        await message.channel.send("le pdf est devenu un manifest !")
        
#keep_alive()
bot.run(key_bot)
        
keep_alive()
bot.run(key_bot)

#Pour image = save l'image d'abord ?

#pdf to manifest = image direct upload sur arvest avant stockage + utilise fichier du mess

#SOLUTION MDP : ecrire dans l'environnement
