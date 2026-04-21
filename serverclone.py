import discord
from colorama import Fore, init, Style

# Renkleri başlat
init()

def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Silinen Rol: {role.name}")
            except Exception:
                print_warning(f"Rol Silinemedi (Atlanıyor): {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [role for role in guild_from.roles if role.name != "@everyone"]
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Oluşturulan Rol: {role.name}")
            except Exception:
                print_warning(f"Rol Oluşturulamadı (Atlanıyor): {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Silinen Kanal: {channel.name}")
            except Exception:
                print_warning(f"Kanal Silinemedi (Atlanıyor): {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for category in guild_from.categories:
            try:
                overwrites_to = {}
                for key, value in category.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role:
                        overwrites_to[role] = value
                new_category = await guild_to.create_category(
                    name=category.name,
                    overwrites=overwrites_to)
                await new_category.edit(position=category.position)
                print_add(f"Oluşturulan Kategori: {category.name}")
            except Exception:
                print_warning(f"Kategori Oluşturulamadı (Atlanıyor): {category.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        # Metin Kanalları
        for channel_text in guild_from.text_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel_text.category.name) if channel_text.category else None
                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role:
                        overwrites_to[role] = value
                
                await guild_to.create_text_channel(
                    name=channel_text.name,
                    overwrites=overwrites_to,
                    position=channel_text.position,
                    topic=channel_text.topic,
                    slowmode_delay=channel_text.slowmode_delay,
                    nsfw=channel_text.nsfw,
                    category=category)
                print_add(f"Oluşturulan Metin Kanalı: {channel_text.name}")
            except Exception:
                print_warning(f"Metin Kanalı Atlandı: {channel_text.name}")

        # Ses Kanalları
        for channel_voice in guild_from.voice_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel_voice.category.name) if channel_voice.category else None
                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role:
                        overwrites_to[role] = value
                
                await guild_to.create_voice_channel(
                    name=channel_voice.name,
                    overwrites=overwrites_to,
                    position=channel_voice.position,
                    bitrate=channel_voice.bitrate,
                    user_limit=channel_voice.user_limit,
                    category=category)
                print_add(f"Oluşturulan Ses Kanalı: {channel_voice.name}")
            except Exception:
                print_warning(f"Ses Kanalı Atlandı: {channel_voice.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            await guild_to.edit(name=guild_from.name)
            print_add(f"Sunucu ismi güncellendi: {guild_to.name}")
        except:
            print_warning("Sunucu ismi güncellenemedi.")

        # Sadece bu kısmı hata vermemesi için sağlama aldım
        try:
            icon_asset = getattr(guild_from, 'icon_url', getattr(guild_from, 'icon', None))
            if icon_asset:
                icon_image = await icon_asset.read()
                await guild_to.edit(icon=icon_image)
                print_add("Sunucu simgesi güncellendi.")
        except:
            print_warning("Simge kopyalanamadı, devam ediliyor.")