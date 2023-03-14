import asyncio
from lib.funcs import *

main_bot = Bot(command_prefix='#', intents=discord.Intents.all(), help_command=None)


@main_bot.event
async def on_ready():
    await main_bot.check_data_folder()


@main_bot.event
async def on_message(msg):
    level_up = await main_bot.change_member_stats(msg.author.id, msg.guild.id, 1, 0.5 * (len(msg.content) * 0.1))
    if level_up:
        await msg.add_reaction('🆙')

    await main_bot.process_commands(msg)


@main_bot.event
async def on_raw_reaction_add(payload):
    guild = main_bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    member = guild.get_member(payload.user_id)

    await main_bot.on_reaction_message(member, payload.emoji, guild, msg.id, give_type=0)


@main_bot.event
async def on_raw_reaction_remove(payload):
    guild = main_bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    member = guild.get_member(payload.user_id)

    await main_bot.on_reaction_message(member, payload.emoji, guild, msg.id, give_type=1)


async def main():
    async with main_bot:
        await main_bot.start("")


asyncio.run(main())
