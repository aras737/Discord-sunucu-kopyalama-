import discord
import asyncio
import colorama
from colorama import Fore, Style
from serverclone import Clone

# Mac/Selfbot uyumlu başlatma
client = discord.Client()

print(f"{Fore.RED}cimidi - Sunucu Klonlama Başlatılıyor...{Style.RESET_ALL}")

token = input('Token Giriniz:\n > ').strip()
guild_s = input('Kopyalanacak Sunucu ID:\n > ').strip()
guild_to_id = input('Hedef Sunucu ID:\n > ').strip()

@client.event
async def on_ready():
    print(f"Giriş Başarılı: {client.user}")
    
    guild_from = client.get_guild(int(guild_s))
    guild_to = client.get_guild(int(guild_to_id))
    
    if not guild_from or not guild_to:
        print(f"{Fore.RED}Hata: Sunucu bulunamadı! ID'leri kontrol et.{Style.RESET_ALL}")
        return

    print("Klonlama işlemi başlıyor, lütfen bekleyin...")
    
    try:
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)
        print(f"{Fore.GREEN}İşlem Başarıyla Tamamlandı!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Bir hata oluştu: {e}{Style.RESET_ALL}")
    
    await asyncio.sleep(5)
    await client.close()

client.run("MTM5NDU3NDM4MDM5NDIyMTcxOQ.GAxvb2.wzJ8R40gij9uTtcnuVrIQG3fGDDzapbVD1JauM")