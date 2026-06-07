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

# Roles y necesidades específicas de configuraciones previas.
cultista_id = 1511176662195245209

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

        # Retransmitir mi mensaje de un canal secreto a otro distinto. Si cumple la sintaxis,
        # separa en dos el mensaje: el canal al que debe ir, y el conttenido que enviar.
        elif message.channel.id == 1513025537331953716:
             enviar_mensaje_desde_susurro(message)
            


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
    await ctx.send('pong!')

@bot.command() # Comando para tirar dados. Recibe la tirada en formato "(Número de dados)d(Caras de cada dado) + (Valor a sumar/restar), sin importar los espacios.
async def roll(ctx, *, arg):

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
        print("Comando mal usado...")
        return
    
    # En el caso de que todo salga bien, se envía este mensaje, y tras ello, tantas veces como dados se hayan tirado, se escriben.
    # Se tiene cuidado en la presentación de modo que no aparezca un feo "+ 0" en el caso de que el número a sumar sea 0.
    await ctx.send("⛧ Corre la sangre...")

    for i in range(numero_de_dados):
        sleep(0.5)
        resultado = randint(1, caras)
        mostrar_resultado = f"⛧ {resultado}" if  inmediato == 0 else (f"⛧ {resultado} + {inmediato} = {resultado+inmediato}" if inmediato > 0 else f"⛧ {resultado} - {-1*inmediato} = {resultado+inmediato}")
        await ctx.send(mostrar_resultado)
        
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

async def enviar_mensaje_desde_susurro(message):
    if "⛧" in message.content:   
        try: 
            # Es improtanate convertir el canal en int, se saca como str.
            canal_a_enviar, mensaje_a_enviar = message.content.split("⛧")
            await message.guild.get_channel(int(canal_a_enviar)).send(mensaje_a_enviar)
        except Exception as e:
            print(e)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
