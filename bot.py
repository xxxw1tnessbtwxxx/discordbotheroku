import asyncio
import math as _math
import os
import sqlite3
import sys
import time as _time
from asyncio import sleep
from sqlite3.dbapi2 import Date

import discord
from discord import embeds
from discord_components.dpy_overrides import send
import googletrans
from discord import Color, Embed, client, message, raw_models
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from discord.ext.commands.core import has_any_role
from discord.message import PartialMessage
from discord.utils import get, time_snowflake
from discord_components import Button, ButtonStyle, DiscordComponents
from googletrans import Translator
from discord import Member

from fullaccess import developersid, devlopersmoderid, moderatorsrole
from languages import LANGUAGES
from settings import settings

###############################
# ВСЕ КОМАНДЫ
###############################
allcommands = '`bothelp` - *Вызвать данное меню*\n`ping` - *Проверить, работает ли бот*'
noperms = 'У вас нет доступа.'

bot = commands.Bot(command_prefix=settings['PREFIX'])
bot.remove_command('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="{}'s info".format(member.name), description="Welcome too {}".format(member.guild.name))
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Roles", value=member.top_role)
    embed.add_field(name="Joined", value=member.joined_at)
    embed.add_field(name="Created", value=member.created_at)
    embed.set_thumbnail(url=member.avatar_url)
    inlul = client.get_channel(881586019655372883)

    await inlul.send(inlul, embed=embed)

# bot presence

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за сервером!\nhell.help"))
    print('Bot connected')

###############################
# CLEAR
###############################
@bot.command()
@commands.has_any_role(moderatorsrole)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    await ctx.send(f'Модератор <@{ctx.author.id}> успешно удалил ' + amount + ' сообщений с данного чата.')

###############################
# КОМАНДА ПИНГА
###############################
@bot.command()
async def ping(ctx):
    if ctx.author.id == 315507881959096322 or 315505638769819648:
        await ctx.send(f'🎾 **Pong!**\nchecked by dev: <@{ctx.author.id}>')
    else:
        await ctx.send('🎾 **Pong!**') # команда пинга

###############################
# МОДЕРАТОРСКИЕ КОМАНДЫ (НЕ ДОДЕЛАНО)
###############################
@bot.command()
@commands.has_permissions()
async def admhelp(ctx):
    await ctx.send("")
    pass

###############################
# ФУНКЦИЯ БАНА
###############################


###############################
# ФУНКЦИЯ МУТА
###############################
noreason = "Причина не указана"
@bot.command()
async def mute(ctx, user: discord.Member, time: int, reason = noreason):
    mutedone = f'<@{user.id}> получил блокировку чата на {time} минут по причине: {reason}. Блокировка чата была выдана модератором <@{ctx.author.id}>'
    moderators_role_ids = (882623183830802463, )
    role = user.guild.get_role(881929360456699964) # айди роли мута
    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await ctx.send(mutedone)
            await user.add_roles(role)
            await user.move_to(None)
            await asyncio.sleep(time * 60)
            await user.remove_roles(role)
            break
    else:
        await ctx.send(noperms)

###############################
# ФУНКЦИЯ РАЗМУТА
###############################
unmutenoreason = "Причина не указана"
@bot.command()
async def unmute(ctx, user: discord.Member, reason=unmutenoreason):
    unmutedone = "Meow."
    moderators_role_ids = (882623183830802463, ) # айди роли модеров
    muterole = user.guild.get_role(881929360456699964) # получение роли мута

    if muterole not in user.roles:
        await ctx.send('У пользователя нет мута!')
        return

    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await user.remove_roles(muterole)
            await ctx.send(unmutedone)
            break
    else:
        await ctx.send(noperms)

    
###############################
# ТЕСТОВЫЙ ЭМБЕД
###############################
@bot.command()
async def displayembed(ctx):
    embeddisplay = discord.Embed(
        title='Загловок',
        description = 'Описание',
        colour = discord.Colour.from_rgb(106, 192, 245),
    )
    embeddisplay.set_thumbnail(url="https://sun9-76.userapi.com/impg/VB4qXuJ0PadWeMhiShjiLSsjNRrv6USlEk2dJA/ShtcFSpl_Hc.jpg?size=512x512&quality=95&sign=6ef34ad883ecf71a3a32ee8b5063facf&type=album")
    await ctx.send(embed=embeddisplay)

###############################
# HELP
###############################
@bot.command()
async def bhelp(ctx):
    embed = discord.Embed (
        title = 'Вы успешно вызвали меню помощи!',
        description = 'Снизу вы сможете увидить список команд, которые сейчас существуют.\nНапомню, что префикс нашего бота - **hell.**',
        colour = discord.Colour.from_rgb(255, 182, 193),
        timestamp = ctx.message.created_at
        )

    await ctx.send(embed=embed)
    await ctx.send(allcommands)

###############################
# ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ (ДЛЯ РАЗРАБОВ)
###############################
@bot.command()
async def test(ctx, user: discord.Member):
    fmt = (f'<@{user.id}> присоединился на данный сервер {user.joined_at}\
            \nЕго ID: {user.id}.\
            \nЕго статус на данный момент:. Он имеет {1} роль(-ей).')
    developer_role_ids = (883348782413144094, )
    for role in ctx.author.roles:
        if role.id in developer_role_ids:
            await ctx.send(fmt)
            break
    else:
        await ctx.send(noperms)

###############################
# ВРЕМЕННАЯ РОЛЬ (НЕ ДОДЕЛАНА)
###############################
@bot.command() 
@commands.has_permissions(administrator=True)
async def temprole(ctx, user: discord.member, time):
    pass

bot.run(settings['TOKEN'])