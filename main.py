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
        #fichier = message.attachment
        #upload_pdf(fichier, xxxxx, mail, password)
        #await message.channel.send("le pdf est devenu un manifest !")

        file = str(message.attachments)

        if file.find("url='") > 0:
                  cible = file.find("url='")
                  cible2 = file.find("'>]")
                  link = file[cible+5:cible2]

        if file.find("filename='") > 0:
                  cible = file.find("' url")
                  cible2 = file.find("filename='")
                  name = file[cible2+10:cible]

        file_name = name.replace('.pdf', '')

        # Conversion en JPEG
        image = convert_from_path(link, 72)

        for i, page in enumerate(image):
            img_name = f"{file_name}_page_{i + 1}.jpeg"
            output_path = os.path.join("img", img_name)
            page.save(output_path, 'JPEG')
            added_media = ar.add_media(path = output_path)
            os.remove(output_path)

        await message.channel.send("pdf uploadé !")
        
keep_alive()
bot.run(key_bot)

#Pour image = save l'image d'abord ?

#pdf to manifest = image direct upload sur arvest avant stockage + utilise fichier du mess

#SOLUTION MDP : ecrire dans l'environnement