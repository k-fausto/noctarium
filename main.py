import os
import logging 
import re
import discord
from random import randint
from time import sleep
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
embed_image = "https://i.postimg.cc/XYZKSJYw/img-2026-06-15-23-29-39-Photoroom.png"
embed_color = discord.Colour(0).from_str("0x8a2b44")

# Roles y necesidades específicas de configuraciones previas.
cultista_id = 1511176662195245209
noctista_id = 1511176220916715600

class MyBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        

    async def on_message(self, message):

        # Se ejecuta esto para evitar bucles infinitos.
        if message.author == self:
            return
        
        # Esta sección únicamente es para el primer comando que quiero ponerle a los usuarios
        # una vez se unen al servidor y mandan un mensaje.

        if message.channel.id == 1511177456252620911:
             await asignar_cultista(message)

        print(f'Message from {message.author}: {message.content}')

        await self.process_commands(message)

    async def process_commands(self, message):
        if message.author.id == self.user.id:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

bot = MyBot(command_prefix='⛧', intents=intents)

# Comandos personalizados.

@bot.command()
async def ping(ctx):
    """ Ping para comprobar que el bot funciona.
    """
    await ctx.send('pong!')

@bot.command() 
async def roll(ctx, *, arg):
    """ Comando para tirar dados. 
    Recibe la tirada en formato: (Número de dados)d(Caras de cada dado) + (Valor a sumar/restar)
    Independiente de los espacios.
    """

    # Este regex parte en cuatro grupos el argumento del comando:
    # Grupo 1: Número de dados.
    # Grupo 2: Caras de cada dado.
    # Grupo 3: Signo.
    # Grupo 4: Valor a sumar/restar.

    regex_tirada = r"^([0-9]+)d([0-9]+)(?:\s*([+-])\s*([0-9]+))?"
    tirada = re.search(regex_tirada, arg) # Comprobamos que el formato sea válido.

    if tirada: 

        # En este trozo recuperamos los grupos de cada cosa.
        numero_de_dados = int(tirada.group(1)) 
        caras = int(tirada.group(2))
        
        if "+" == tirada.group(3):
            inmediato = int(tirada.group(4))
        elif "-" == tirada.group(3):
            inmediato = (-1) * int(tirada.group(4))
        else:
            inmediato = 0

    else:
        print("Runa mal trazada...")
        return
    
    # En el caso de que todo salga bien, se envía este mensaje, y tras ello, tantas veces como dados se hayan tirado, se escriben.
    # Se tiene cuidado en la presentación de modo que no aparezca un feo "+ 0" en el caso de que el número a sumar sea 0.
    await ctx.send("⛧ Corre la sangre...")

    for i in range(numero_de_dados):
        sleep(0.5)
        resultado = randint(1, caras)
        mostrar_resultado = f"⛧ {resultado}" if  inmediato == 0 else (f"⛧ {resultado} + {inmediato} = {resultado+inmediato}" if inmediato > 0 else f"⛧ {resultado} - {-1*inmediato} = {resultado+inmediato}")
        await ctx.send(mostrar_resultado)
        
@bot.command()
async def whisp(ctx, *, arg):
    """ Envía un mensaje en cualquier canal.
        Admite un id de canal y un mensaje.
        ⛧whisp 132473298 string
    """
    print(ctx.author.roles)
    if noctista_id in [x.id for x in ctx.author.roles]:
        canal, mensaje = arg.split(" ", 1)
        await ctx.guild.get_channel(int(canal)).send(mensaje)

@bot.command()
async def p(ctx):

    """ Define un prototipo estándar de cómo será la mayoría de hechizos.
    """
    
    dados = 6
    caras = 34
    inmediato = 0
    
    embed_title = " "
    flavortext = "__Kýrie, eléison, christe eléison__"
    embed_flavortext = "⠀\n\n" + flavortext +" \n" + f"`{dados}d{caras}`"

    for i in range(dados):
        resultado = randint(dados, caras)
        mostrar_resultado = f" ⛧ {resultado}" if  inmediato == 0 else (f"⛧ {resultado} + {inmediato} = {resultado+inmediato}" if inmediato > 0 else f"⛧ {resultado} - {-1*inmediato} = {resultado+inmediato}")
        embed_flavortext += mostrar_resultado

    embed_test = discord.Embed(title=embed_title, description=embed_flavortext, color=embed_color).set_thumbnail(url=embed_image)


    # await ctx.send(flavortext)
    # await ctx.send(mostrar_resultado)
    await ctx.send(embed=embed_test)

@bot.command()
async def respuesta(ctx, *, arg):
    
    if arg.lower() == "tres" or arg == "3":
        embed_color = discord.Colour(0).from_str("0x8a2b44")
        embed_respuesta = discord.Embed(title="Divinación", description="*Exitosa.*", color=embed_color).set_thumbnail(url=embed_image)
        await ctx.send(embed=embed_respuesta)
    else:
        embed_color = discord.Colour(0).from_str("0x8a2b44")
        embed_respuesta = discord.Embed(title="Divinación", description="*Fallida.*", color=embed_color).set_thumbnail(url=embed_image)
        await ctx.send(embed=embed_respuesta)

# Comandos auxiliares.

async def asignar_cultista(message):
    # Esta es la forma de conseguir el rol teniendo el ID.
            rol_cultista = message.guild.get_role(cultista_id)

            if rol_cultista:
                try:
                    await message.author.add_roles(rol_cultista)
                    print(f"Añadido a {message.author}")
                except:
                    print("Error de jerarquía de roles o bien de HTTPS")
            else:
                print("El rol no existe")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
