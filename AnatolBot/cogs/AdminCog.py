import discord
from discord import Color
from discord.ext import commands

import sys
import os

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Администраторские'
        self.adminOnly = True
        print(f"{self.category} команды инициализированы!")

    @commands.command(aliases=['news', 'nw'])
    async def send_news(self, ctx, *text):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        config_table = await self.bot.load_data(ctx.guild.id, self.bot.datatypes[0])

        text = "- " + " ".join([str(word) for word in text])

        embed = discord.Embed(title="Новости", description=text, color=0x36393e)
        embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.display_avatar.url)

        if config_table["news_channel"] is not None:
            news_channel = ctx.guild.get_channel(config_table["news_channel"])
            await news_channel.send(embed=embed)

        if config_table["news_role"] is not None:
            news_role = ctx.guild.get_role(config_table["news_role"])
            for member in ctx.guild.members:
                if news_role in member.roles and not member.bot:
                    await member.send(embed=embed)

        await ctx.message.delete()

    @commands.command(aliases=['cl', 'clr'])
    async def clear(self, ctx, count):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        embed = discord.Embed(title="Очистка чата", description=f"Очищено {count} сообщений", color=0x36393e)
        embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator, icon_url=ctx.author.display_avatar.url)

        await ctx.channel.purge(limit=int(count) + 1)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['rm', 'react_msg'])
    async def reaction_message(self, ctx):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        def check_reaction_valid(reaction, user):
            return user == ctx.author

        def check_message_valid(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # FIRST MESSAGE
        reaction_message_text = ctx.message.content[len(self.bot.prefix) + len(ctx.invoked_with) + 1::]

        text = f'**Текст будущего сообщения:**\n*{reaction_message_text}*.' \
               f'\nЕсли хотите продолжить настройку сообщения, нажмите \N{THUMBS UP SIGN}, ' \
               f'если нет, то \N{THUMBS DOWN SIGN}'

        reaction_message_creating = await ctx.channel.send(text, mention_author=False)

        await reaction_message_creating.add_reaction('\N{THUMBS UP SIGN}')
        await reaction_message_creating.add_reaction('\N{THUMBS DOWN SIGN}')

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_reaction_valid)

        await reaction_message_creating.delete()

        if reaction.emoji == "\N{THUMBS DOWN SIGN}":
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        # FIRST MESSAGE

        # SECOND MESSAGE
        text = f"**Вы решили продолжить настройку!**\n" \
               f"Чтобы установить роли и соответствующие реакции, вводите поочередно их по шаблону ниже:" \
               f"\n*\N{THUMBS DOWN SIGN} : @Роль1 | \N{THUMBS UP SIGN} : @Роль2 | ...*"

        reaction_message_creating = await ctx.channel.send(text, mention_author=False)

        message = await ctx.bot.wait_for('message', check=check_message_valid)
        reaction_message_roles = message.content.replace(" ", "").split("|")

        await message.delete()
        await reaction_message_creating.delete()

        # SECOND MESSAGE

        # THIRD MESSAGE
        text = f"**Вы установили реакции и роли для них!**\n" \
               f"Проверьте, все ли верно и нажмите \N{THUMBS UP SIGN} и сообщение с реакциями будет создано, " \
               f"в ином случае нажмите \N{THUMBS DOWN SIGN}! " \
               f"Неправильно введенные реакции не будут добавлены в сообщение." \
               f"\n**Текст сообщения:** \n*{reaction_message_text}*" \
               f"\n**Реакции и роли:** \n{', '.join(reaction_message_roles[0:])}"

        reaction_message_creating = await ctx.channel.send(text, mention_author=False)

        await reaction_message_creating.add_reaction('\N{THUMBS UP SIGN}')
        await reaction_message_creating.add_reaction('\N{THUMBS DOWN SIGN}')

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_reaction_valid)

        await reaction_message_creating.delete()

        if reaction.emoji == "\N{THUMBS DOWN SIGN}":
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        # THIRD MESSAGE

        # SAVING REACTION

        reaction_message = await ctx.channel.send(f"{reaction_message_text}")
        reaction_table = []

        for role in reaction_message_roles:
            role = role.split(":")
            role[1] = await self.bot.clear_format_id(role[1])
            if ctx.guild.get_role(role[1]) is None:
                continue
            role = [role[0], role[1]]
            reaction_table.append(role)
            await reaction_message.add_reaction(role[0])

        await self.bot.change_role_reaction(reaction_message.id, ctx.guild.id, reaction_table)

        # SAVING REACTION


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
