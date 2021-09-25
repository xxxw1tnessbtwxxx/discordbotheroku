import asyncio
from inspect import EndOfBlock
import math as _math
import os
import sqlite3
import sys
import time as _time
from asyncio import sleep
from sqlite3.dbapi2 import Date
from typing import Text

import discord
from discord import embeds
from discord import colour
from discord import activity
from discord.abc import User
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
import time

from languages import LANGUAGES
from settings import settings

import datetime

###############################
# ВСЕ ОТВЕТЫ НА СООБЩЕНИЯ
###############################
allcommands = (
    f'`help` - **Вызвать данное меню**\n\
`ping` - **Проверить, работает ли бот**\n\
`kiss @mention` - **Поцеловать пользователя**\n\
`beat @mention` - **Избить пользователя**\n\
`slap @mention` - **Дать пощечину пользователю**\n\
`embrance @mention` - **Обнять пользователя**\n\
`info @mention` - **Получить информацию о пользователе** p.s чтобы получить информацию о себе, нужно упомянуть себя.\n\n\
`@mention` обозначает упоминание пользователя через собачку')

moderandadmallcommands = (
    f'Команды модерации: \n\n\
    `mute @mention time reason` - **амутить пользователя**.\n\
    `unmute @mention reason` - **размутить пользователя**.\n\
    `clear кол-во` - **очистить чат.**\n\
    `kick @mention reason` - **кикнуть пользователя**\n\n\
    Команды разработчиков: \n\n\
    `getadminfo` - **получить админскую информацию о пользователе**.\n\
    `change_+arguments` - **изменить активность бота, доступные аргументы:**\n\
    `game, listen, watch, custom, competing`\n\n\
    ')

noperms = 'Вы не достойны =)'
noreason = "Причина не указана"
unmutenoreason = "Причина не указана"
serverthumbnaill = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/efb7c4cd-c7d6-418d-9db6-f75208869a2b/da1wjzr-0feabb93-8ca3-4ad2-b2da-b88ef35e1839.png/v1/fill/w_900,h_547,q_75,strp/hel__goddess_of_the_underworld_by_lesluv-da1wjzr.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9lZmI3YzRjZC1jN2Q2LTQxOGQtOWRiNi1mNzUyMDg4NjlhMmIvZGExd2p6ci0wZmVhYmI5My04Y2EzLTRhZDItYjJkYS1iODhlZjM1ZTE4MzkucG5nIiwid2lkdGgiOiI8PTkwMCIsImhlaWdodCI6Ijw9NTQ3In1dXX0.1C_bgNxJJCiAa0bzAiowlxwqgdLsr9eoRfIfs603Hx0'
bot_version = 'Версия бота: 1.0'
default_footer_text = 'С уважением, команда Hellheim!  ' + bot_version
topdoings = 'Вы не можете применять модераторские действия к участникам, которые имеют роли выше вашей.'


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
bot = commands.Bot(command_prefix=commands.when_mentioned_or(settings['PREFIX']), intents=intents)
bot.remove_command("help")

conn = sqlite3.connect('serverbase.db')
cursor = conn.cursor()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="в борьбе за сервером!\nhell.help"))
    print('Bot connected')


class AllEvents:
    @bot.event
    async def on_message_delete(message):
        hellbotname = 'Hellbot'
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        deletefooter = ('<' + st + '>')
        deleteeditlogchannel = bot.get_channel(890149373059686420)
        deletelogembed = discord.Embed(
            title=f'message remove by {message.author.name}',
            description=f'{message.author.name} delete message: ' + message.content + f'{message.channel.mention}',
            colour = discord.Colour.from_rgb(255, 0, 0)
        )
        deletelogembed.set_footer(text=deletefooter)
        for hellbot in message.author.name:
            if message.author.name not in hellbotname:
                await deleteeditlogchannel.send(embed=deletelogembed)
                break
    
    @bot.event
    async def on_member_join(user):
        if cursor.execute(f'SELECT id FROM users WHERE id = {user.id}').fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES ('{user}'), {user.id}, 0,")
            conn.commit()
        else:
            pass
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


    @bot.event
    async def on_member_remove(user: discord.Member):
        guild = user.guild
        leavelogchannel = bot.get_channel(888695834328305705)
        channel = bot.get_channel(888709127499558932)
        await leavelogchannel.send(f'{user} leave. id: {user.id}')
        await channel.send(f'Пользователь `{user.id}` покинул наш сервер :(\nДата его присоединения на сервер: `{user.joined_at}`.\nТеперь на сервере {guild.member_count} участников.')

    @bot.event
    async def on_message_edit(before, after):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        editfooter = ('<' + st + '>')
        deleteeditlogchannel = bot.get_channel(890149373059686420)
        editlogembed = discord.Embed(
            title=f'message edited by {before.author.name}',
            description=f"{before.author.mention} edited a message in {before.channel.mention}.\n\nOld: - {before.content}\nNew: - {after.content}",
            colour = discord.Colour.from_rgb(255, 0, 0)
        )
        editlogembed.set_footer(text=editfooter)
        await deleteeditlogchannel.send(embed=editlogembed)



class ChangePresence:
    @bot.command()
    async def presence_game(ctx):
        presencechannel = bot.get_channel(890913610501599272)
        gameactivity = discord.Game(name="hell.help")
        for role in ctx.author.roles:
            if role.id in developer_role_ids:
                await bot.change_presence(status=discord.Status.idle, activity=gameactivity)
                await presencechannel.send(f'presence changed to `game` by {ctx.author.mention}')
                await ctx.send(f'Разработчик {ctx.author.mention} успешно сменил мою активность на `game`.')
                break

        else:
            await ctx.send(noperms)

    @bot.command()
    async def presence_listen(ctx):
        presencechannel = bot.get_channel(890913610501599272)
        for role in ctx.author.roles:
            if role.id in developer_role_ids:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Голоса участников! - hell.help"))
                await presencechannel.send(f'presence changed to `listen` by {ctx.author.mention}')
                await ctx.send(f'Разработчик {ctx.author.mention} успешно сменил мою активность на `listen`.')
                break
        else:
            await ctx.send(noperms)

    @bot.command()
    async def presence_watch(ctx):
        for role in ctx.author.roles:
            presencechannel = bot.get_channel(890913610501599272)
            if role.id in developer_role_ids:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за сервером!\nhell.help"))
                await presencechannel.send(f'presence changed to `watch` by {ctx.author.mention}')
                await ctx.send(f'Разработчик {ctx.author.mention} успешно сменил мою активность на `watch`.')
                break
        else:
            await ctx.send(noperms)

    @bot.command()
    async def presence_custom(ctx):
        for role in ctx.author.roles:
            presencechannel = bot.get_channel(890913610501599272)
            if role.id in developer_role_ids:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="за сервером!\nhell.help"))
                await presencechannel.send(f'presence changed to `custom` by {ctx.author.mention}')
                await ctx.send(f'Разработчик {ctx.author.mention} успешно сменил мою активность на `custom`.')
                break
        else:
            await ctx.send(noperms)

    @bot.command()
    async def presence_competing(ctx):
        presencechannel = bot.get_channel(890913610501599272)
        for role in ctx.author.roles:
            if role.id in developer_role_ids:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="борьбе за сервер!\nhell.help"))
                await presencechannel.send(f'presence changed to `competing` by {ctx.author.mention}')
                await ctx.send(f'Разработчик {ctx.author.mention} успешно сменил мою активность на `competing`.')
                break
        else:
            await ctx.send(noperms)

class Moderation:
    @bot.command()
    async def clear(ctx, amount=None):
        for role in ctx.author.roles:
            if role.id in moderators_role_ids:
                nick = ctx.author.nick if (ctx.author.nick) else ctx.author.name
                clearlogchannel = bot.get_channel(890142915484078101)
                await ctx.channel.purge(limit=int(amount))
                clearembed = discord.Embed(
                    title=f"Очистка сообщений от модератора {nick}.",
                    description =f"Модератор {nick} успешно удалил с чата {amount} сообщений.",
                    colour = discord.Colour.from_rgb(106, 192, 245)
                )
                clearembed.set_thumbnail(url=serverthumbnaill)
                clearembed.set_footer(text=default_footer_text)
                clearembed.set_image(url='https://thumbs.gfycat.com/DelayedHardFattaileddunnart-max-1mb.gif')
                await ctx.send(embed=clearembed, delete_after = 10.0)
                await clearlogchannel.send(f'{ctx.author.mention} удалил {amount} сообщений из {ctx.channel.mention}')
                break
        else:
            await ctx.send(noperms)


    @bot.command()
    async def admhelp(ctx):
        admhelpembed = discord.Embed(
            title="Меню команд модерации успешно вызвано.",
            description=moderandadmallcommands
        )
        admhelpembed.set_thumbnail(url=serverthumbnaill)
        admhelpembed.set_footer(text=default_footer_text)
        for role in ctx.author.roles:
            if role.id in moderators_role_ids:
                await ctx.send(embed=admhelpembed)
                break
        else:
            await ctx.send(noperms)
    
    @bot.command()
    async def kick(ctx, user: discord.Member, reason = noreason):
        kickdone = f'{user.mention} был **изгнан** модератором {ctx.author.mention} по причине: **{reason}**.'
        kicklogchannel = bot.get_channel(888714438369247262)

        if user.top_role >= ctx.author.top_role:
            await ctx.send(topdoings)
            return

        for role in ctx.author.roles:
            if role.id in moderators_role_ids:
                await user.kick(reason = reason)
                await ctx.send(kickdone)
                await kicklogchannel.send(f'{user.mention} get kicked by {ctx.author.mention} by reason {reason}')
                break      

        for role in ctx.author.roles:
            if role.id not in moderators_role_ids:
                await ctx.send(noperms)
                break
    
    @bot.command()
    async def mute(ctx, user: discord.Member, time: int, reason = noreason):
        mutedone = f'{user.mention} получил блокировку чата на **{time}** минут по причине: **{reason}**. Блокировка чата была выдана модератором {ctx.author.mention}'
        muterole = user.guild.get_role(887354612934389870)
        mutelogchannel = bot.get_channel(888713534622560336)

        if user.top_role >= ctx.author.top_role:
            await ctx.send(topdoings)
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

        for role in ctx.author.roles:
            if role.id not in moderators_role_ids:
                await ctx.send(noperms)
                break

    @bot.command()
    async def unmute(ctx, user: discord.Member, reason=unmutenoreason):
        unmutedone = f"Блокировка была снята модератором <@{ctx.author.id}>. Причина: {reason}."
        muterole = user.guild.get_role(887354612934389870)
        mutelogchannel = bot.get_channel(888713534622560336)

        if user.top_role >= ctx.author.top_role:
            await ctx.send(topdoings)
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

    @bot.command()
    async def getadminfo(ctx, user: discord.Member):
        getinfochannel = bot.get_channel(890879427704131594)
        warninggetinfochannel = bot.get_channel(890880021714046986)
        admembedinfo = discord.Embed(
            title="Вы успешно вызвали админскую информацию о пользователе!",
            description=(f'{user.mention} присоединился на сервер `{user.joined_at}.`\n\n\
            Его ID: {user.id}\n\
            Ник на сервере: {user.nick}\n\
            Ник в дискорде: {user.name}\n\
            Его разрешения: {user.guild_permissions}\n\
            Список его ролей:\n {user.roles}\n\n\
            Его самая высокая роль: {user.top_role}\n')
        )
        admembedinfo.set_thumbnail(url=serverthumbnaill)
        admembedinfo.set_footer(text=default_footer_text)
        
        for role in ctx.author.roles:
            if role.id in developer_role_ids:
                await ctx.send(embed=admembedinfo)
                await getinfochannel.send(f'{ctx.author.mention} получил админскую информацию о пользователе {user.mention}')
                break
        else:
            await warninggetinfochannel.send(f'{ctx.author.mention} попытался получить админскую информацию о пользователе {user.mention}')
            await ctx.send(noperms)

    @bot.command()
    async def members(ctx):
        for role in ctx.author.roles:
            if role.id in developer_role_ids:
                for guild in bot.guilds:
                    for member in guild.members:
                        membersembed = discord.Embed(
                            title="Список всех участников:",
                            description=guild.guild_members
                        )
                        await ctx.send(embed=membersembed)
                        break
                    else:
                        await ctx.send(noperms)

class OtherCommands:
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
                await ctx.send(f'Информация по последнему пингу была отправлена в канал {pinglogchannel.mention}')
                await pinglogchannel.send('last latency = ' + str(bot.latency))
                break
        else:
            await ctx.send(f'🎾 **Pong!**')


class Fun:
    @bot.command()
    async def kiss(ctx, user: discord.Member):
        authornick = ctx.author.nick if (ctx.author.nick) else ctx.author.name
        usernick = user.nick if (user.nick) else user.name
        kissembed = discord.Embed(
            title=(f" Пользователь {authornick} поцеловал {usernick} 💋"),
            colour = discord.Colour.from_rgb(255, 20, 147)
        )
        kissembed.set_image(url='https://lifeo.ru/wp-content/uploads/gif-anime-kisses-35.gif')
        await ctx.send(embed=kissembed)

    @bot.command()
    async def embrace(ctx, user: discord.Member):
        authornick = ctx.author.nick if (ctx.author.nick) else ctx.author.name
        usernick = user.nick if (user.nick) else user.name
        embraceembed = discord.Embed(
            title=(f" Пользователь {authornick} обнял {usernick} 💑"),
            colour = discord.Colour.from_rgb(255, 20, 147)
        )
        embraceembed.set_image(url='https://im0-tub-ru.yandex.net/i?id=60c844ddb529237a2af34e6ea359b66d&n=13')
        await ctx.send(embed=embraceembed)

    @bot.command()
    async def slap(ctx, user: discord.Member):
        authornick = ctx.author.nick if (ctx.author.nick) else ctx.author.name
        usernick = user.nick if (user.nick) else user.name
        slapembed = discord.Embed(
            title=(f" Пользователь {authornick} дал пощечину {usernick} 👏"),
            colour = discord.Colour.from_rgb(255, 20, 147)
        )
        slapembed.set_image(url='https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif')
        await ctx.send(embed=slapembed)

    @bot.command()
    async def beat(ctx, user: discord.Member):
        authornick = ctx.author.nick if (ctx.author.nick) else ctx.author.name
        usernick = user.nick if (user.nick) else user.name
        beatembed = discord.Embed(
            title=(f" Пользователь {authornick} избил {usernick} 👏"),
            colour = discord.Colour.from_rgb(255, 20, 147)
        )
        beatembed.set_image(url='https://i.gifer.com/P44M.gif')
        await ctx.send(embed=beatembed)





    
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
async def help(ctx):
    bothelp = discord.Embed(
        title = 'Вы успешно вызвали меню помощи!',
        description = 'Снизу вы сможете увидить список команд, которые сейчас существуют.\nНапомню, что префикс нашего бота - **hell.**',
        colour = discord.Colour.from_rgb(255, 182, 193),
        timestamp = ctx.message.created_at
        )
    bothelp.set_footer(text=default_footer_text)
    bothelp.set_thumbnail(url=serverthumbnaill)
    bothelp.add_field(name="Вот список команд: \n", value=allcommands)
    await ctx.send(embed=bothelp)


@bot.command()
async def info(ctx, user: discord.Member):
    userinfochannel = bot.get_channel(890879754914381824)
    embedinfo = discord.Embed(
        title="Вы успешно вызвали информацию о пользователе!",
        description=(f'{user.mention} присоединился на сервер `{user.joined_at}.`\n\
        Его ID: {user.id}')
    )
    embedinfo.set_thumbnail(url=serverthumbnaill)
    embedinfo.set_footer(text=default_footer_text)
    await ctx.send(embed=embedinfo)
    await userinfochannel.send(f'{ctx.author.mention} получил информацию о пользователе {user.mention}')


###############################
# ВРЕМЕННАЯ РОЛЬ (НЕ ДОДЕЛАНА)
###############################
@bot.command()
async def temprole(ctx, user: discord.member, time):
    pass

bot.run(settings['TOKEN'])