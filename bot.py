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
from discord import colour
from discord.flags import Intents
from discord_components.dpy_overrides import send
from discord import Color, Embed, client, message, raw_models
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from discord.ext.commands.core import has_any_role
from discord.message import PartialMessage
from discord.utils import get, time_snowflake
from discord_components import Button, ButtonStyle, DiscordComponents
from discord import Member

from fullaccess import developersid, devlopersmoderid, moderatorsrole
from languages import LANGUAGES
from settings import settings

import datetime as DT

###############################
# ВСЕ ОТВЕТЫ НА СООБЩЕНИЯ
###############################
allcommands = (
    f'`bhelp` - *Вызвать данное меню*\n\
`ping` - *Проверить, работает ли бот*')


noperms = 'Вы не достойны =)'
noreason = "Причина не указана"
unmutenoreason = "Причина не указана"
serverthumbnaill = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/efb7c4cd-c7d6-418d-9db6-f75208869a2b/da1wjzr-0feabb93-8ca3-4ad2-b2da-b88ef35e1839.png/v1/fill/w_900,h_547,q_75,strp/hel__goddess_of_the_underworld_by_lesluv-da1wjzr.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9lZmI3YzRjZC1jN2Q2LTQxOGQtOWRiNi1mNzUyMDg4NjlhMmIvZGExd2p6ci0wZmVhYmI5My04Y2EzLTRhZDItYjJkYS1iODhlZjM1ZTE4MzkucG5nIiwid2lkdGgiOiI8PTkwMCIsImhlaWdodCI6Ijw9NTQ3In1dXX0.1C_bgNxJJCiAa0bzAiowlxwqgdLsr9eoRfIfs603Hx0'
bot_version = 'Версия бота: 1.0'
default_footer_text = 'С уважением, команда Hellheim!  ' + bot_version
topmute = 'Вы не можете применять модераторские действия к участникам, которые имеют роли выше вашей.'


###############################
# СПИСОК ВСЕХ ID РОЛЕЙ
###############################

developer_role_ids = (887356276286300190, )
moderators_role_ids = (887356276286300190, 887353276339716098)
guild = 881585936742383626

###############################


intents_list = ('guilds', 'members', 'emojis', 'messages', 'reactions')
intent_data = {intent: True for intent in intents_list}
intents = discord.Intents(**intent_data)
bot = commands.Bot(command_prefix=settings['PREFIX'], intents=intents)

# bot presence

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за сервером!\nhell.help"))
    print('Bot connected')

###########################################
# MEMBER JOIN + LEAVE + GIVE ROLE WHEN JOIN
@bot.event
async def on_member_join(user):
    footertext = "С уважением, команда разработчиков Hellheim! " + bot_version
    logchannel = bot.get_channel(888695823687381022)
    channel = bot.get_channel(888709127499558932)
    guild = channel.guild
    embedjoin = discord.Embed(
        title = f'Добро пожаловать в Hellheim, {user}! Ты уже {guild.member_count} участник!',
        description = ('Ты попал на сервер, оформление которого составлено по скандинавской мифологии, как и собственно роли на этом сервере.\n'\
        'Сервер постоянно обновляется, добавляются новые фишки, убираются бесполезные.\n'\
        'У нас добрая и отзывчивая администрация, которая поможет/ответит на вопрос в любой момент!\n'\
        'Мы очень рады, что ты присоединился именно к нам, мы не подведем <3'),
        colour = discord.Colour.from_rgb(255, 182, 193)
    )
    embedjoin.set_footer(text=footertext)
    embedjoin.set_thumbnail(url=serverthumbnaill)
    await channel.send(embed=embedjoin)
    await logchannel.send(f'{user} join')

###########################################


###############################
# CLEAR
###############################
@bot.command()
async def clear(ctx, amount=None):
    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f'Модератор <@{ctx.author.id}> успешно удалил ' '**'+ amount + ' сообщений** с данного чата.', delete_after=4.0)
            break
    else:
        await ctx.send(noperms)

###############################
# КОМАНДА ПИНГА
###############################

@bot.command()
async def ping(ctx):
    latency = "Задержка (ping) " + str(bot.latency)
    pinglogchannel = bot.get_channel(888706125510361129)
    for role in ctx.author.roles:
        if role.id in developer_role_ids:
            pingembed = discord.Embed(
                title=f'🎾 **Pong!**',
                description = f"Работоспособность успешно проверена разработчиком {ctx.author}",
                colour = discord.Colour.from_rgb(106, 192, 245)
            )
            pingembed.set_footer(text=latency)
            await ctx.send(embed=pingembed)
            await ctx.send(f'Информация по последнему пингу была отправлена в канал #all-pings-by-dev')
            await pinglogchannel.send('last latency = ' + str(bot.latency))
            break
    else:
        await ctx.send(f'🎾 **Pong!**')

###############################
# МОДЕРАТОРСКИЕ КОМАНДЫ (НЕ ДОДЕЛАНО)
###############################

@bot.command()
async def admhelp(ctx):
    await ctx.send("")
    pass

###############################
# ФУНКЦИЯ КИКА
###############################
@bot.command()
async def kick(ctx, user: discord.Member, reason = noreason):
    kickdone = f'{user.mention} был **изгнан** модератором {ctx.author.mention} по причине: **{reason}**.'
    kicklogchannel = bot.get_channel(888714438369247262)

    if ctx.author.top_role <= user.top_role:
        await ctx.send(topmute)
        return

    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await user.kick(reason = reason)
            await ctx.send(kickdone)
            await kicklogchannel.send(f'{user.mention} get kicked by {ctx.author.mention} by reason {reason}')
            break
    else:
        await ctx.send(noperms)

###############################
# ФУНКЦИЯ МУТА
###############################
@bot.command()
async def mute(ctx, user: discord.Member, time: int, reason = noreason):
    mutedone = f'{user.mention} получил блокировку чата на **{time}** минут по причине: **{reason}**. Блокировка чата была выдана модератором {ctx.author.mention}'
    muterole = user.guild.get_role(887354612934389870)
    mutelogchannel = bot.get_channel(888713534622560336)

    if user.top_role >= ctx.author.top_role:
        await ctx.send(topmute)
        return

    if muterole in user.roles:
        await ctx.send("Пользователь уже замучен.")
        return

    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await ctx.send(mutedone)
            await mutelogchannel.send(f'{user.mention} muted by {ctx.author.mention} by reason {reason}')
            await user.add_roles(muterole)
            await asyncio.sleep(time * 60)
            await user.remove_roles(muterole)
            break
    else:
        await ctx.send(noperms)

###############################
# ФУНКЦИЯ РАЗМУТА
###############################
@bot.command()
async def unmute(ctx, user: discord.Member, reason=unmutenoreason):
    unmutedone = f"Блокировка была снята модератором <@{ctx.author.id}>. Причина: {reason}."
    muterole = user.guild.get_role(887354612934389870)
    mutelogchannel = bot.get_channel(888713534622560336)

    if user.top_role >= ctx.author.top_role:
        await ctx.send(topmute)
        return

    if muterole not in user.roles:
        await ctx.send('У пользователя нет мута!')
        return

    for role in ctx.author.roles:
        if role.id in moderators_role_ids:
            await user.remove_roles(muterole)
            await ctx.send(unmutedone)
            await mutelogchannel.send(f'{user.mention} unmuted by {ctx.author.mention} by reason {reason}')
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
    embeddisplay.set_thumbnail(url=serverthumbnaill)
    await ctx.send(embed=embeddisplay)

###############################
# HELP
###############################
@bot.command()
async def bhelp(ctx):
    creator = bot.get_user(315507881959096322)
    bothelp = discord.Embed(
        title = 'Вы успешно вызвали меню помощи!',
        description = 'Снизу вы сможете увидить список команд, которые сейчас существуют.\nНапомню, что префикс нашего бота - **hell.**',
        colour = discord.Colour.from_rgb(255, 182, 193),
        timestamp = ctx.message.created_at
        )
    bothelp.set_footer(text=default_footer_text)
    bothelp.set_thumbnail(url=serverthumbnaill)

    await ctx.send(embed=bothelp)
    await ctx.send(allcommands)

###############################
# ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ (ДЛЯ РАЗРАБОВ)
###############################
@bot.command()
async def test(ctx, user: discord.Member):
    fmt = (f'<@{user.id}> присоединился на данный сервер {user.joined_at}\
            \nЕго ID: {user.id}.\
            \nЕго статус на данный момент:. Он имеет {1} роль(-ей).')
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