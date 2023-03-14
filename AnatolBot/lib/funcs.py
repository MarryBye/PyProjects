import discord
from discord.ext import commands
import time
import json
import sys
import os


# Decorator to send logs automatically
async def send_log(func):
    def wrapper(*args, **kwargs):
        log_text, guild_id = func(*args, **kwargs)
        print(log_text, guild_id)

    return wrapper


class Bot(commands.Bot):
    def __init__(self, command_prefix=">", intents=discord.Intents.all(), help_command=None):
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=help_command)
        self.prefix = command_prefix
        self.data_folder = "data"
        self.datatypes = ("guild_config", "members_config", "reactions_config")

    async def save_data(self, guild_id, datatype, data):
        with open(f"{self.data_folder}/{guild_id}/{datatype}.json", 'w', encoding="UTF-8") as config_file:
            json.dump(data, config_file, ensure_ascii=False, indent=6)

    async def load_data(self, guild_id, datatype):
        with open(f"{self.data_folder}/{guild_id}/{datatype}.json", 'r', encoding="UTF-8") as config_file:
            content = json.load(config_file)
            config_file.close()
            return content

    async def check_guild_folders(self):
        print("Запускаю проверку папок серверов...")
        start_tables = {
            self.datatypes[0]: {
                "start_roles": None,
                "news_role": None,
                "admin_role": None,
                "news_channel": None,
                "welcome_channel": None,
                "logs_channel": None,
                "private_room": None
            },
            self.datatypes[1]: {
                self.user.id: {
                    "messages_count": 0,
                    "level": 0,
                    "experience": 0
                }
            },
            self.datatypes[2]: {}
        }
        for guild in self.guilds:
            guild_folder = f"{self.data_folder}/{guild.id}"
            if os.path.isdir(guild_folder):
                continue
            os.mkdir(guild_folder)
            for datatype in self.datatypes:
                await self.save_data(guild.id, datatype, start_tables[datatype])
        print("Проверка папок серверов окончена!")

    async def check_data_folder(self):
        print(f"Запускаю проверку корневой папки...")
        if not os.path.isdir(self.data_folder):
            os.mkdir(self.data_folder)
            print("Корневая папка восстановлена!\n")
            await self.check_guild_folders()
        print("Проверка корневой папки окончена!")

    async def check_is_admin(self, guild, member):
        guild_config = await self.load_data(guild.id, self.datatypes[0])
        admin_role_data = guild_config["admin_role"]
        admin_role = None
        if admin_role_data is not None:
            admin_role = guild.get_role(admin_role_data)
        return guild.owner.id == member.id or member.guild_permissions.administator or admin_role in member.roles

    async def check_is_role_reaction(self, guild_id, message_id):
        message_id = str(message_id)

        config_table = await self.load_data(guild_id, self.datatypes[2])

        return message_id in config_table

    async def change_guild_settings(self, guild_id, setting, data):
        guild_id = str(guild_id)

        config_table = await self.load_data(guild_id, self.datatypes[0])

        if setting not in config_table:
            return False

        config_table[setting] = data
        await self.save_data(guild_id, self.datatypes[0], config_table)
        return True

    async def change_role_reaction(self, message_id, guild_id, reaction_table):
        message_id = str(message_id)
        config_table = await self.load_data(guild_id, self.datatypes[2])

        config_table[message_id] = reaction_table

        await self.save_data(guild_id, self.datatypes[2], config_table)

    async def change_member_stats(self, member_id, guild_id, msgs, exp):
        member_id = str(member_id)
        level_up = False
        config_table = await self.load_data(guild_id, self.datatypes[1])

        if str(member_id) not in config_table:
            config_table[str(member_id)] = {
                "messages_count": 0,
                "level": 1,
                "experience": 0,
            }

        config_table_member = config_table[str(member_id)]
        config_table_member["messages_count"] += msgs
        config_table_member["experience"] += exp

        if config_table_member["experience"] >= config_table_member["level"] * 25:
            config_table_member["level"] += 1
            config_table_member["experience"] = 0
            level_up = True

        await self.save_data(guild_id, self.datatypes[1], config_table)

        return level_up

    async def on_reaction_message(self, member, reaction, guild, message_id, give_type=0):
        message_id = str(message_id)
        guild_id = str(guild.id)
        reaction = str(reaction)

        config_table = await self.load_data(guild_id, self.datatypes[2])

        if message_id in config_table:
            message_table = config_table[message_id]
            for role in message_table:
                if role[0] != reaction:
                    continue
                role = member.guild.get_role(role[1])
                if give_type == 0:
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)
                break

    async def load_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    @staticmethod
    async def clear_format_id(uid):
        return int(uid.replace("<", "").replace(">", "").replace("&", "").replace("@", ""))

    async def setup_hook(self):
        await self.load_extensions()

