import discord
from discord.ext import commands
import random as rn
import wikipedia
import requests
import json
import praw
import time

PREFIX = ["dm ", "DM ", "günaydı"]
client = commands.Bot(command_prefix=PREFIX, description="FARKETMEZ Mİ? You are goddamn right 😎.",
                      case_insensitive=True)
is_connected = False
waiting = 0.5

#fill these variables for meme command
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     username="",
                     password="",
                     user_agent="")


@client.event
async def on_ready():
    activity = discord.Game("dm help")
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print(client.user, "discorda bağlandı.")


@client.command()
async def meme(msg=""):
    """--> random meme yollar."""
    subreddit = rn.choice([reddit.subreddit("memes"), reddit.subreddit("nukedmemes"), reddit.subreddit("burdurland"),
                           reddit.subreddit("dankmemes"), reddit.subreddit("Cringetopia")])
    all = list()
    top = subreddit.top(limit=50)
    for i in top:
        all.append(i)
    rn_sub = rn.choice(all)
    name = rn_sub.title
    url = rn_sub.url
    em = discord.Embed(title=name, color=discord.Color.dark_green())
    em.set_image(url=url)
    await msg.channel.send(embed=em)



@client.command()
async def şaka(msg=""):
    """--> şakalar 🤣🤣🤣."""
    joke = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = json.loads(joke.text)
    await msg.channel.send(f"**{data['setup']}**\n\n||{data['punchline']}🤣🤣🤣||")


@client.command()
async def n(msg=""):
    await msg.channel.send("GÜNAYDIN SERVERLARIN")
    time.sleep(waiting)
    await msg.channel.send("EN GÜZELİ")
    time.sleep(waiting)
    await msg.channel.send("EN ÖZELİ")
    time.sleep(waiting)
    await msg.channel.send("EN SÜPERİ")
    time.sleep(waiting * 2)
    await msg.channel.send("NAPIYORSUN 😍")


@client.command()
async def join(ctx):
    """--> botu ses kanalına geçer."""
    global is_connected
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        is_connected = True
        await ctx.channel.send("Selamın aleyküm 😇")

    except:
        if is_connected:
            await ctx.channel.send("E kanaldayım ya 🤬!")
        else:
            await ctx.channel.send("Kanalda yoksun 🤬!")


@client.command()
async def vs(ctx):
    """--> rakipler ve silahlar üzerinden vs atar."""
    silahlar = open("silahlar.txt", "r", encoding='utf-8')
    rakipler = open("rakipler.txt", "r", encoding='utf-8')
    rakip_list = rakipler.read().split("\",\"")
    silah_list = silahlar.read().split("\",\"")
    versus = rn.sample(rakip_list, 2)
    weapon = rn.choice(silah_list)
    winner = rn.choice(versus)
    loser = [i for i in versus if not i == winner][0]
    await ctx.channel.send(
        f"{versus[0]} vs {versus[1]}\nSONUÇ: {loser}, rakibi {winner} tarafından {weapon} ile ödürüldü.")
    rakipler.close()
    silahlar.close()


@client.command()
async def eklesilah(ctx, *thing):
    """<silah ismi> --> silah ekler."""
    silahlar = open("silahlar.txt", "r", encoding='utf-8')
    silahlar_ekle = open("silahlar.txt", "a", encoding='utf-8')
    s_ekle_list = silahlar.read().split("\",\"")
    thing = ' '.join(thing)
    if not thing in s_ekle_list:
        silahlar_ekle.write("\",\"" + thing)
    else:
        await ctx.channel.send("E ekledim ya 🤬!")

    silahlar.close()
    silahlar_ekle.close()


@client.command()
async def eklerakip(ctx, *thing):
    """<rakip ismi> --> rakip ekler."""
    rakipler_ekle = open("rakipler.txt", "a", encoding='utf-8')
    rakipler = open("rakipler.txt", "r", encoding='utf-8')
    r_ekle_list = rakipler.read().split("\",\"")
    thing = ' '.join(thing)
    if not thing in r_ekle_list:
        rakipler_ekle.write("\",\"" + thing)
    else:
        await ctx.channel.send("E ekledim ya 🤬!")
    rakipler.close()
    rakipler_ekle.close()


@client.command()
async def gostersilah(ctx):
    """--> silahları gösterir."""
    silahlar = open("silahlar.txt", "r", encoding='utf-8')
    silahlar_l = silahlar.read().split("\",\"")
    silahlar_gosterilecek = "\n".join(silahlar_l)
    await ctx.channel.send("SİLAHLAR LİSTESİ:\n" + silahlar_gosterilecek)
    silahlar.close()


@client.command()
async def papağan(ctx, *message):
    """mesajı tekrar eder"""
    content = ' '.join(message)
    await ctx.channel.send(content)


@client.command(pass_context=True)
async def sil(ctx, amount=1):
    """<miktar> --> miktar kadar mesajı siler."""
    channell = ctx.message.channel
    messages = []
    async for message in channell.history(limit=int(amount) + 1):
        messages.append(message)
    await channell.delete_messages(messages)
    await ctx.channel.send(f'{amount} mesaj silindi.')
    time.sleep(0.5)
    messages = []
    async for message in channell.history(limit=1):
        messages.append(message)
    await channell.delete_messages(messages)


@client.command()
async def gosterrakip(ctx):
    """--> rakipleri gösterir."""
    rakipler = open("rakipler.txt", "r", encoding='utf-8')
    rakipler_l = rakipler.read().split("\",\"")
    rakipler_gosterilecek = "\n".join(rakipler_l)
    await ctx.channel.send("RAKİPLER LİSTESİ:\n" + rakipler_gosterilecek)
    rakipler.close()


@client.command()
async def leave(ctx=None):
    """--> botu ses kanalından atar."""
    global is_connected
    try:
        await ctx.voice_client.disconnect()
        is_connected = False
        await ctx.channel.send("Ben gidiyom bye 🤪")
    except:
        await ctx.channel.send("E çıktım ya 🤬!")


@client.command()
async def search(ctx, sth):
    """<aratılacak şey> --> wikipedia dan bir şey aratır."""
    wikipedia.set_lang('tr')
    pic = discord.Embed(color=discord.Color.dark_green())
    try:
        page = wikipedia.search(sth)
    except:
        page = wikipedia.search(sth)[0]
    summary = wikipedia.summary(page, sentences=rn.randint(3, 6))
    sth_page = wikipedia.page(page)
    sth_url = sth_page.images[0]
    pic.set_image(url="{}".format(sth_url))
    await ctx.channel.send(embed=pic)
    await ctx.channel.send(summary)


@client.command()
async def ehb(ctx):
    """<soru> --> sorulan soruya evet hayır ya da belki der"""
    answers = ["Evet.", "Hayır.", "Belki."]
    answer = rn.choice(answers)
    await ctx.channel.send(answer)


@client.command()
async def rps(ctx, message):
    """<rock/paper/scissors> --> taş kağıt makas oynar."""
    my_choice = ["rock", "paper", "scissors"][rn.randint(0, 2)]
    cnt = message
    if cnt == my_choice:
        await ctx.channel.send(f"berabere! hamlem: {my_choice}")
    elif (cnt == "rock" and my_choice == "scissors") or (cnt == "paper" and my_choice == "rock") or (
            cnt == "scissors" and my_choice == "paper"):
        await ctx.channel.send(f"kazandın helall😎! hamlem: {my_choice}")
    else:
        await ctx.channel.send(f"haha ben kazandım eziq 🤪! hamlem: {my_choice}")


@client.command()
async def versus(ctx, v1, v2, *v3):
    """<birici, ikinci,....> --> vs atar."""
    lst = [v1, v2] + list(v3)
    winner = rn.choice(lst)
    await ctx.channel.send("Kazanan: " + winner)


@client.command()
async def gn(ctx, member: discord.Member = None):
    """<@dcüyesi> --> iyi geceler diler."""
    if member == None:
        await ctx.channel.send(f"iyi geceler {ctx.author.display_name}")
    else:
        await ctx.channel.send(f"iyi geceler {member.display_name}")


@client.command()
async def çıkrala(ctx, *message):
    """--> çıkralar."""
    message = list(message)
    for i in range(len(message)):
        if not len(message[i]) <= 2:
            mes_list = list(message[i])
            mes_list[1], mes_list[2] = mes_list[2], mes_list[1]
            new_i = ''.join(mes_list)
            message[i] = new_i
    await ctx.channel.send(' '.join(message))


@client.command()
async def topla(ctx, left, right):
    """<num1 num2> --> İki sayı ya da kelimeyi toplar."""
    try:
        left = int(left)
        right = int(right)
    except:
        pass
    finally:
        await ctx.channel.send(left + right)

@client.command()
async def avatar(ctx, member: discord.Member = None):
    """<@dcüyesi> --> avatarı gösterir."""
    avatar = discord.Embed(color=discord.Color.dark_green())
    if member == None:
        avatar.set_image(url="{}".format(ctx.author.avatar_url))
    else:
        avatar.set_image(url="{}".format(member.avatar_url))
    await ctx.channel.send(embed=avatar)


@client.command()
async def nick(ctx, choice, *message):
    """<1/2 isim> --> şekilli nick üretir."""
    harf_dict1 = {'a': '𝓐', 'b': '𝓑', 'c': '𝓒', 'd': '𝓓', 'e': '𝓔', 'f': '𝓕', 'g': '𝓖', 'h': '𝓗', 'i': '𝓘',
                  'j': '𝓙', 'k': '𝓚', 'l': '𝓛', 'm': '𝓜', 'n': '𝓝', 'o': '𝓞', 'p': '𝓟', 'r': '𝓡', 's': '𝓢',
                  't': '𝓣', 'u': '𝓤', 'v': '𝓥', 'y': '𝓨', 'z': '𝓩'}

    harf_dict2 = {'a': 'ƛ', 'b': 'Ɓ', 'c': 'Ƈ', 'd': 'Ɗ', 'e': 'Є', 'f': 'Ƒ', 'g': 'Ɠ', 'h': 'Ӈ', 'i': 'Ɩ',
                  'j': 'ʆ', 'k': 'Ƙ', 'l': 'Լ', 'm': 'ℳ', 'n': 'Ɲ', 'o': 'Ơ', 'p': 'Ƥ', 'r': 'Ʀ', 's': 'Ƨ', 't': 'Ƭ',
                  'u': 'Ʋ', 'v': 'Ɣ', 'y': 'Ƴ', 'z': 'Ȥ'}
    message = " ".join([i for i in message])

    message = list(message.lower())
    res = ''
    if choice == '1':
        for i in message:
            if i in harf_dict1.keys():
                res += harf_dict1[i]
            else:
                res += i
    elif choice == '2':
        for i in message:
            if i in harf_dict2.keys():
                res += harf_dict2[i]
            else:
                res += i
    await ctx.channel.send(res)


@client.command()
async def puanla(ctx, thing):
    """<bir şey> --> 1/10 arası puan verir."""
    puan = rn.randint(1, 10)
    await ctx.channel.send(f"{puan}/10")


@client.command()
async def random(ctx):
    """--> 1-100 arası random sayı üretir."""
    num = rn.randint(1, 100)
    await ctx.channel.send(num)


client.run("YOUR TOKEN HERE")

