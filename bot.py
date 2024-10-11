import discord
from discord.ext import commands
import chess
from bot_logic import *
import os
import random
import urllib.request
import json
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
KEY = os.getenv('KEY_YOUTUBE')

bot = commands.Bot(command_prefix='$', intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hi!")

@bot.command()
async def bye(ctx):
    await ctx.send(":(")

@bot.command()
async def password(ctx):
    await ctx.send(gen_pass(10))

@bot.command()
async def smile(ctx):
    await ctx.send(gen_emodji())

@bot.command()
async def coin(ctx):
    await ctx.send(flip_coin())

@bot.command()
async def meme(ctx):
    memes = random.choice(os.listdir("images"))
    with open(f'images/{memes}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="usuario")
    await member.add_roles(role)
    await member.send(f"¡Bienvenido {member.name}! Se te ha asignado el rol {role.name}.")

@bot.command()
async def like(ctx):
    mensaje = await ctx.send("Reacciona con 👍 para obtener el rol 'like'.")
    await mensaje.add_reaction('👍')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.emoji == '👍':
        role = discord.utils.get(user.guild.roles, name="like")
        if role:
            await user.add_roles(role)
            await user.send("¡Te hemos añadido el rol 'like'!")
        else:
            await user.send("El rol 'like' no existe. Por favor, informa al administrador.")

@bot.command(name='subs')
async def subscriptores(ctx, username):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={username}&key={KEY}"
    data = urllib.request.urlopen(url).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    response = f"{username} tiene {int(subs):,d} suscriptores!"
    await ctx.send(response)

@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokemon)
        if result.text == "Not Found":
            await ctx.send("Pokemon no Encontrado")
        else:
            image_url = result.json()['sprites']['front_default']
            await ctx.send(image_url)
    except Exception as e:
        print("Error: ", e)

@poke.error
async def poke_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Falta el nombre del pokemon")

litros_por_minuto = 5.5

ideas = [
    "Reutiliza objetos antes de tirarlos. Piensa si pueden tener un nuevo uso.",
    "Recicla adecuadamente: separa los residuos correctamente (papel, plástico, vidrio, orgánico).",
    "Crea compost con desechos orgánicos en lugar de tirarlos a la basura.",
    "Ahorra energía apagando luces cuando no las uses.",
    "Reduce el consumo de agua: toma duchas más cortas y arregla fugas en tu hogar.",
    "Compra productos hechos con materiales reciclados siempre que sea posible.",
    "Utiliza transporte sostenible: camina, usa bicicleta o transporte público en lugar de vehículos privados."
]

def calcular_consumo_agua(tiempo_minutos):
    return tiempo_minutos * litros_por_minuto

@bot.command()
async def agua(ctx, tiempo: float):
    consumo = calcular_consumo_agua(tiempo)
    await ctx.send(f"Si dejas la llave abierta por {tiempo} minutos, gastaras aproximadamente {consumo} litros de agua.")

@bot.command()
async def idea(ctx):
    idea_aleatoria = random.choice(ideas)
    await ctx.send(f"💡 Idea para reciclar y reducir la contaminación: {idea_aleatoria}")

bot.run(TOKEN)