import discord
from discord.ext import commands

import sys
import os

sys.path.insert(1, os.path.abspath(".."))

from lib.funcs import *


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = 'Серверные'
        self.adminOnly = True
        print(f"{self.category} команды инициализированы!")

    @commands.command(aliases=['ssr', 'set_sr'])
    async def set_start_roles(self, ctx, *roles: discord.Role):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "start_roles", [role.id for role in roles])
        await ctx.channel.send(f"{ctx.author.name}#{ctx.author.discriminator} установил новый список стартовых ролей:\n "
                               f"{', '.join([f'<@&{role.id}>' for role in roles])}",
                               mention_author=False)

    @commands.command(aliases=['snr', 'set_nr'])
    async def set_news_role(self, ctx, role: discord.Role):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "news_role", role.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новую новостную роль:\n'
                               f'<@&{role.id}>',
                               mention_author=False)

    @commands.command(aliases=['sar', 'set_ar'])
    async def set_admin_role(self, ctx, role: discord.Role):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "admin_role", role.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новую администраторскую роль:\n'
                               f'<@&{role.id}>',
                               mention_author=False)

    @commands.command(aliases=['snc', 'set_nc'])
    async def set_news_channel(self, ctx, channel: discord.TextChannel):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "news_channel", channel.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новый новостной канал:\n'
                               f'<#{channel.id}>',
                               mention_author=False)

    @commands.command(aliases=['swc', 'set_wc'])
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "welcome_channel", channel.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новый приветственный канал:\n'
                               f'<#{channel.id}>',
                               mention_author=False)

    @commands.command(aliases=['slc', 'set_lc'])
    async def set_logs_channel(self, ctx, channel: discord.TextChannel):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "logs_channel", channel.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новый канал для логов:\n'
                               f'<#{channel.id}>',
                               mention_author=False)

    @commands.command(aliases=['spr', 'set_pr'])
    async def set_private_room(self, ctx, channel: discord.VoiceChannel):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        await self.bot.change_guild_settings(ctx.guild.id, "private_room", channel.id)
        await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} установил новый канал для приваток:\n'
                               f'<#{channel.id}>',
                               mention_author=False)

    @commands.command(aliases=['sds', 'set_ds'])
    async def set_disable_setting(self, ctx, setting):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        success = await self.bot.change_guild_settings(ctx.guild.id, setting, None)
        if success:
            await ctx.channel.send(f'{ctx.author.name}#{ctx.author.discriminator} удалил настройку {setting}.',
                                   mention_author=False)
        else:
            await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')
            return

    @commands.command(aliases=['gs', 'get_st'])
    async def get_settings(self, ctx):
        if await self.bot.check_is_admin(ctx.guild, ctx.author) is False:
            await ctx.add_reaction('\N{THUMBS DOWN SIGN}')
            return

        await ctx.message.delete()

        config_table = await self.bot.load_data(ctx.guild.id, self.bot.datatypes[0])
        text = f"**Роли:**\n" \
               f"**Администраторская:** <@&{config_table['admin_role']}>\n" \
               f"**Новостная:** <@&{config_table['news_role']}>\n" \
               f"**Начальные:** {', '.join([f'<@&{role}>' for role in config_table['start_roles']])}\n" \
               f"\n**Каналы:**\n" \
               f"**Новостной:** <#{config_table['news_channel']}>\n" \
               f"**Приветственный:** <#{config_table['welcome_channel']}>\n" \
               f"**Для логов:** <#{config_table['logs_channel']}>\n" \
               f"**Для приваток:** <#{config_table['private_room']}>\n" \

        await ctx.channel.send(text, mention_author=False)


async def setup(bot):
    await bot.add_cog(SettingsCog(bot))
