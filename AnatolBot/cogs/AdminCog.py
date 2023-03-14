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

    @commands.command()
    async def reaction_message(self, ctx):
        command = ctx.message

        if await self.bot.check_is_admin(command.guild, command.author) is False:
            await command.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        def check_reaction_valid(reaction, user):
            return user == command.author

        def check_message_valid(message):
            return message.author == command.author and message.channel == command.channel

        # FIRST MESSAGE
        reaction_message_text = command.content[len(self.bot.prefix) + len("reaction_message") + 1::]

        text = f'**Текст будущего сообщения:**\n*{reaction_message_text}*.' \
               f'\nЕсли хотите продолжить настройку сообщения, нажмите \N{THUMBS UP SIGN}, ' \
               f'если нет, то \N{THUMBS DOWN SIGN}'

        reaction_message_creating = await ctx.reply(text, mention_author=False)

        await reaction_message_creating.add_reaction('\N{THUMBS UP SIGN}')
        await reaction_message_creating.add_reaction('\N{THUMBS DOWN SIGN}')

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_reaction_valid)

        await reaction_message_creating.delete()

        if reaction == "\N{THUMBS DOWN SIGN}":
            return

        # FIRST MESSAGE

        # SECOND MESSAGE
        text = f"**Вы решили продолжить настройку!**\n" \
               f"Чтобы установить роли и соответствующие реакции, вводите поочередно их по шаблону ниже:" \
               f"\n*\N{THUMBS DOWN SIGN} : @Роль1 | \N{THUMBS UP SIGN} : @Роль2 | ...*"

        reaction_message_creating = await ctx.reply(text, mention_author=False)

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

        reaction_message_creating = await ctx.reply(text, mention_author=False)

        await reaction_message_creating.add_reaction('\N{THUMBS UP SIGN}')
        await reaction_message_creating.add_reaction('\N{THUMBS DOWN SIGN}')

        reaction, user = await ctx.bot.wait_for('reaction_add', check=check_reaction_valid)

        await reaction_message_creating.delete()

        if reaction == "\N{THUMBS DOWN SIGN}":
            return

        # THIRD MESSAGE

        # SAVING REACTION
        await command.delete()

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
