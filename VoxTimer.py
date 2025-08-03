import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import asyncio
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


load_dotenv()
from keep_alive import keep_alive
keep_alive()
CANAL_AUTORIZADO_ID = int(os.getenv("CANAL_AUTORIZADO_ID"))

evento_data = datetime(2025, 8, 8, 21, 30, 0, tzinfo=timezone.utc)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def contador(ctx):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        await ctx.send("🚫 Este comando só pode ser usado em <#1383957562696929342>")
        return

    mensagem = await ctx.send("⏳ Calculando tempo restante...")

    while True:
        agora = datetime.now(timezone.utc)
        tempo_restante = evento_data - agora

        if tempo_restante.total_seconds() <= 0:
            await mensagem.edit(content="🎉 O evento de Vox Sea já começou!")
            break

        dias = tempo_restante.days
        horas, resto = divmod(tempo_restante.seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        novo_texto = (
            f"⏳ Tempo restante até o lançamento de Vox Sea em **08/08 às 18:30 (BRT)**:\n"
            f"**{dias}** dias, **{horas}** horas, **{minutos}** minutos e **{segundos}** segundos."
        )

        await mensagem.edit(content=novo_texto)
        await asyncio.sleep(1)


bot.run(os.getenv("API_KEY"))
