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

    @commands.command()
    async def set_start_roles(self, ctx, *roles: discord.Role):
        await self.bot.change_guild_settings(ctx.guild.id, "start_roles", [role.id for role in roles])
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новый список стартовых ролей.',
                        mention_author=False)

    @commands.command()
    async def ssr(self, ctx, *roles: discord.Role):
        await self.set_start_roles(ctx, *roles)

    @commands.command()
    async def set_news_role(self, ctx, role: discord.Role):
        await self.bot.change_guild_settings(ctx.guild.id, "news_role", role.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новую новостную роль.',
                        mention_author=False)

    @commands.command()
    async def snr(self, ctx, role: discord.Role):
        await self.set_news_role(ctx, role)

    @commands.command()
    async def set_admin_role(self, ctx, role: discord.Role):
        await self.bot.change_guild_settings(ctx.guild.id, "admin_role", role.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новую администраторскую роль.',
                        mention_author=False)

    @commands.command()
    async def sar(self, ctx, role: discord.Role):
        await self.set_admin_role(ctx, role)

    @commands.command()
    async def set_news_channel(self, ctx, channel: discord.TextChannel):
        await self.bot.change_guild_settings(ctx.guild.id, "news_channel", channel.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новый новостной канал.',
                        mention_author=False)

    @commands.command()
    async def snc(self, ctx, channel: discord.TextChannel):
        await self.set_news_channel(ctx, channel)

    @commands.command()
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        await self.bot.change_guild_settings(ctx.guild.id, "welcome_channel", channel.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новый приветственный канал.',
                        mention_author=False)

    @commands.command()
    async def swc(self, ctx, channel: discord.TextChannel):
        await self.set_welcome_channel(ctx, channel)

    @commands.command()
    async def set_logs_channel(self, ctx, channel: discord.TextChannel):
        await self.bot.change_guild_settings(ctx.guild.id, "logs_channel", channel.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новый канал для логов.',
                        mention_author=False)

    @commands.command()
    async def slc(self, ctx, channel: discord.TextChannel):
        await self.set_logs_channel(ctx, channel)

    @commands.command()
    async def set_private_room(self, ctx, channel: discord.VoiceChannel):
        await self.bot.change_guild_settings(ctx.guild.id, "private_room", channel.id)
        await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} установил новый канал для приваток.',
                        mention_author=False)

    @commands.command()
    async def spr(self, ctx, channel: discord.VoiceChannel):
        await self.set_private_room(ctx, channel)

    @commands.command()
    async def set_disable_setting(self, ctx, setting):
        success = await self.bot.change_guild_settings(ctx.guild.id, setting, None)
        if success:
            await ctx.reply(f'{ctx.author.name}#{ctx.author.discriminator} удалил настройку {setting}.',
                            mention_author=False)
        else:
            await ctx.reply(f'Настройки {setting} не существует.', mention_author=False)

    @commands.command()
    async def sds(self, ctx, settings):
        await self.set_disable_setting(ctx, settings)


async def setup(bot):
    await bot.add_cog(SettingsCog(bot))
