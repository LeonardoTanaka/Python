from multiprocessing.dummy.connection import Client
import re
import discord
import datetime
import requests
import random

from discord import colour
from discord.embeds import Embed
from random import choice
from discord.ext import commands, tasks


bot = commands.Bot("!")

cat_gifs = ["https://c.tenor.com/2v1aDCelTJgAAAAM/cat-cats.gif", "https://c.tenor.com/NFjEeHbk-zwAAAAM/cat.gif",
            "https://c.tenor.com/TXiaUZI-FGwAAAAM/hi.gif", "https://c.tenor.com/KFAzIs8FX4AAAAAM/barbanne-canele.gif",
            "https://c.tenor.com/gpOAug6iMFUAAAAM/cute-cat-cat.gif", "https://c.tenor.com/9TepkeounC4AAAAM/cat-angry.gif",
            "https://c.tenor.com/ZhfMGWrmCTcAAAAM/cute-kitty-best-kitty.gif", "https://c.tenor.com/2l-_G98Q1KUAAAAM/cat-shocked.gif",
            "https://c.tenor.com/GVqnsWqyGDYAAAAM/jjackson-cat.gif", "https://c.tenor.com/pb_Fg9KHdbEAAAAM/kitty-review-cat.gif",
            "https://c.tenor.com/bK1qpWGyQKkAAAAM/kitty.gif", "https://c.tenor.com/uzWDSSLMCmkAAAAM/cute-cat-oh-yeah.gif",
            "https://c.tenor.com/cwSkPoAkPy0AAAAM/cat-run.gif", "https://c.tenor.com/FysdcUSAQekAAAAM/angry-cat-furious-cat.gif",
            "https://c.tenor.com/_1avvWbL32oAAAAM/cat-dog.gif", "https://c.tenor.com/vN9EaApDdqgAAAAM/cat-licking-itself-what.gif",
            "https://i.imgur.com/DL583a3.gif", "https://i.imgur.com/TLlkJV3.gif",
            "https://i.imgur.com/4wQP9s9.gif", "https://i.imgur.com/OOVmdwa.gif",
            "https://i.imgur.com/Ji0IMvT.gif", "https://i.imgur.com/MoEWqyg.gif",
            "https://i.imgur.com/GnoeBna.gif", "https://i.imgur.com/ejYeUMS.gif",
            "https://i.imgur.com/YEDIlJg.gif", "https://i.imgur.com/AtV11yd.gif",
            "https://i.imgur.com/K17aOHq.gif", "https://i.imgur.com/Rz8MExe.gif"]

kiss_gifs = ["https://imgur.com/e0ep0v3.gif", "https://data.whicdn.com/images/354014869/original.gif",
             "https://aniyuki.com/wp-content/uploads/2021/07/aniyuki-anime-gif-kiss-8.gif", "https://i.gifer.com/3OM7C.gif",
             "https://i.gifer.com/3OM7I.gif","https://i.gifer.com/3OM7J.gif",
             "https://i.gifer.com/3OM7K.gif", "https://i.gifer.com/3OM7M.gif",
             "https://i.gifer.com/3OM7N.gif", "https://i.gifer.com/3OM7O.gif",
             "https://i.gifer.com/3OM7P.gif", "https://i.gifer.com/3OM7Q.gif",
             "https://animesher.com/orig/1/101/1012/10125/animesher.com_kirito-asuna-couple-sword-art-online-1012512.gif",
             "https://acegif.com/wp-content/uploads/anime-kiss-28.gif", "https://cutewallpaper.org/21/best-anime-kisses/Top-30-Kiss-Scene-GIFs-Find-the-best-GIF-on-Gfycat.gif",
             "https://acegif.com/wp-content/uploads/anime-kissin-13.gif", "https://acegif.com/wp-content/uploads/anime-kiss-37.gif",
             "https://c.tenor.com/Ypqd43UbTC8AAAAC/yuri.gif", "https://c.tenor.com/HCdZGf6l-JoAAAAC/kiss-toradora.gif",
             "https://c.tenor.com/oZ04B4Fj8GgAAAAC/anime-kiss.gif","https://https://s8.gifyu.com/images/ezgif.com-gif-makerd7af62fa53722b6b.gif"]

hugs_gifs = ["https://i.pinimg.com/originals/49/63/96/496396c91a4f6827ee8a87c2582ec746.gif", "https://c.tenor.com/Q-RjY3zuBcsAAAAd/anime-kiss.gif",
             "https://cutewallpaper.org/21/cute-anime-hug/Cute-anime-girl-hug-gif-9-At-GIF-Images-Download.gif",
             "https://Pd2sMiVr09YAAAAC/hug-anime-hug.gif", "https://c.tenor.com/u-jPAbdv8XwAAAAC/naofumi-iwatani-tate-no-yuusha-no-nariagari.gif",
             "https://c.tenor.com/Ei1Gg8dZLf8AAAAd/nezuko-chan-hug.gif", "https://c.tenor.com/8MZVGsjAO58AAAAd/hug-natsu.gif",
             "https://imgur.com/5JLSy.gif", "https://i.gifer.com/GAMC.gif","https://c.tenor.com/H7i6GIP-YBwAAAAd/a-whisker-away-hug.gif",
             "https://i.pinimg.com/originals/a1/64/6c/a1646c77119633b484ba98fc90613f15.gif", "https://i.pinimg.com/originals/40/ce/8e/40ce8e420750f0289c4daa00c6496e00.gif",
             "https://i.pinimg.com/originals/bb/84/1f/bb841fad2c0e549c38d8ae15f4ef1209.gif","https://c.tenor.com/dE8m3GiIUZkAAAAd/rascal-does-not-dream-of-bunny-girl-senpai-seishun-buta-yar%C5%8D.gif",
             "https://66.media.tumblr.com/e7ba49430f457536c2b77b9ddf101cda/tumblr_ojqz920XHo1qcsnnso1_500.gif",
             "https://i.kym-cdn.com/photos/images/original/000/643/197/e63.gif","https://c.tenor.com/Cuh9WL0xklIAAAAC/anime-hug.gif",
             "https://c.tenor.com/EHuOeZVV1jkAAAAC/anime-hug.gif", "https://i.pinimg.com/originals/0c/bc/37/0cbc377124f2f91d76277160b5803372.gif"]

hentai_gifs= ["https://xgifsbr.com/wp-content/uploads/2020/12/sexo-hentai-33.gif", "https://xgifsbr.com/wp-content/uploads/2020/12/sexo-hentai-32.gif",
              "https://xgifsbr.com/wp-content/uploads/2020/12/sexo-hentai-27.gif"]

blow_job_gifs = ["https://i0.wp.com/www.hentairing.com/thumb/1/blowjob-in-the-toilet-hentai-gif.gif", "https://25.media.tumblr.com/tumblr_mdn44pt4dQ1rd3iwlo1_500.gif", "http://www.hentairider.com/media/images/5/hot-red-head-hentai/hot-red-head-hentai-269726.gif"]


player1 = ""

player2 = ""

turn = ""

gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Those Eyes - New West"))

    print(f"Estou pronto! Estou conectado como {bot.user}")
    current_time.start()

    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "palavrão" in message.content:
        await message.channel.send(
            f"Por favor, {message.author.name}, não ofenda os demais usuários!")
        
        await message.delete()
        
    await bot.process_commands(message)



@bot.command(name="oi")
async def send_hello(ctx):
    name = ctx.author.name
    
    response = "Olá, " +name
    
    await ctx.send(response)
    
@bot.command(name="calcular")
async def calculate_expression(ctx, *expression):
    expression = "".join(expression)
    
    print(expression)
    
    response = eval(expression)
    
    await ctx.send("A resposta é: " + str(response))
    
@bot.command()
async def binance(ctx, coin, base):
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}")
    
        data = response.json()
        price = data.get("price")
    
        if price:
            await ctx.send(f"O valor do par {coin}/{base}")
        else:
            await ctx.send(f"O par {coin}/{base} é inválido")
    except Exception as error:
        await ctx.send("Ops... Deu algum erro!")
        print(error)
        
@bot.command(name="yukio")
async def secret(ctx):
    
    frasesYukio = ("Eu te amo muito, Sofia!",
                "Sofia, você é minha pessoa preferida no mundo.",
                "Tem um mestre que libera uma mina pra você entrar.",
                "Deixa eu entrar no seu templo secreto, amor?",
                "Não fica triste amor, você é linda.",
                "Espero que você saiba que pertence a mim, cada centímetro do seu corpo, cada pedacinho do seu coração, só eu posso te tocar, beijar e te fazer delirar a noite.",
                "Bora gf?",
                "Amor você é muito linda,gostosa,maravilhosa e uma pessoa incrível, quero passar o resto da minha vida com você.",
                "Você é tipo sinal vermelho, eu repeito, mas tô louco pra avançar.",
                "Toda vez que você fica feliz, quem se apaixona mais sou eu.",
                "Deixa eu entrar na sua caverna secreta e fazer sua cachoeira cair.",
                "Deixa eu te mostrar que depressão não é única coisa grande que eu tenho.",
                "Sim, você é minha dona, e eu sou seu cachorrinho.",
                "Au au",
                "Fofinho é meu pau")

    fraseYukio = choice(frasesYukio)
    await ctx.send(fraseYukio)
    
@bot.command(name="sofia")
async def secret(ctx):
    
    frasesSofia = ("Eu te amo muito, muitinho, Yukio lindo!",
                   "Eu faço fofinho",
                   "Velho",
                   "Eu te amo mais a cada dia",
                   "Manda foto do pau",
                   "Eu não sou fofa, sou dark",
                   "Você é muito gostoso,lindo e fofo",
                   "Gay, muito gay",
                   "Tô tímida",
                   "Yuki, você é muito fofo",
                   "Você vai ser meu first blood",
                   "Amo sua voz e seu sorriso",
                   "Casa comigo",
                   "Meu gadinho gostoso",
                   "Você me deixa toda fraca e bobinha",
                   "Mandar foto sem camisa when",
                   "Me xinga na cama, me enforcar, me bate, me come",
                   "Podia ser você destruindo meu útero em vez da cólica",
                   "Você é muito nerd, amor")

    fraseSofia = choice(frasesSofia)
    await ctx.send(fraseSofia)
    
    


    


       
@bot.command("cat")
async def cat(ctx):
    embed = discord.Embed(
        colour = (discord.Colour.random())
        
    )
    embed.set_image(url=(random.choice(cat_gifs)))
    
    await ctx.send(embed=embed)
    
@bot.command("kiss")
async def kiss(ctx, member:discord.Member):
    embed = discord.Embed(
        colour = (discord.Colour.random()),
       
        description =f"{ctx.author.mention} kisses {member.mention}"
        
        
        
    )
    embed.set_image(url=(random.choice(kiss_gifs)))
    
    await ctx.send(embed=embed)
    
@bot.command("hug")
async def kiss(ctx, member:discord.Member):
    embed = discord.Embed(
        colour = (discord.Colour.random()),
       
        description =f"{ctx.author.mention} hugs {member.mention}"
        
        
        
    )
    embed.set_image(url=(random.choice(hugs_gifs)))
    
    await ctx.send(embed=embed)
    
    
@bot.command("fap")
async def fap(ctx, member:discord.Member):
    embed = discord.Embed(
        colour = (discord.Colour.random()),
       
        description =f"{ctx.author.mention} fucks {member.mention}"
        
        
        
    )
    embed.set_image(url=(random.choice(hentai_gifs)))
    
    await ctx.send(embed=embed)

@bot.command("bj")
async def fap(ctx, member:discord.Member):
    embed = discord.Embed(
        colour = (discord.Colour.random()),
       
        description =f"{ctx.author.mention} gave {member.mention} a blowjob"
        
        
        
    )
    embed.set_image(url=(random.choice(blow_job_gifs)))
    
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount):
        messages.append(message)
    await channel.delete_messages(messages)
    
    

@bot.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        #print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " +board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        #determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It's <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It's <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board [pos - 1] = mark
                count += 1

                #print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + "Wins!")
                elif count >= 9:
                    await ctx.send("It's a tie!")

                #switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1

            else:
                await ctx.send("Be sure to choose a number between 1 and 9.")
        else:
            await ctx.send("It's your turn.")
    else:
        await ctx.send("Please start a new game using !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True
        

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention players (ie. <@975832996336767016).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter a number.")

    

@bot.command()
async def rps(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global count
    global p1Points
    global p2Points

    player1 = p1
    player2 = p2

    p1Points = 0
    p2Points = 0
    rpsGame = ["rock", "paper", "scissors"]
    
    await ctx.send(f"Rock, paper or scissors?")

    def checkP1(msg):
        
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame
        
    def checkP2(m):
        return m.author == p2 and m.channel == ctx.channel and m.content.lower() in rpsGame
        
    p1_choice = (await bot.wait_for('message', check=checkP1)).content

    p2_choice = (await bot.wait_for('message', check=checkP2)).content

    if p1_choice == 'rock':
        if p2_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'paper':
            p2Points += 1
            await ctx.send(f'Nice try, but I won that time!!\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'scissors':
            p1Points +=1
            await ctx.send(f"Aw, you beat me. It won't happen again!\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}")

    elif p1_choice == 'paper':
        if p2_choice == 'rock':
            p1Points +=1
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: { p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\Player 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'scissors':
            p2Points +=1
            await ctx.send(f"Aw man, you actually managed to beat me.\nPlayer 1 choice:: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}")

    elif p1_choice == 'scissors':
        if p2_choice == 'rock':
            p2Points +=1
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'paper':
            p1Points +=1
            await ctx.send(f'Bruh. >: |\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}')
        elif p2_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.\nPlayer 1 choice: {p1_choice}\nPlayer 2 choice: {p2_choice}\nPlayer 1 points: {p1Points}\nPlayer 2 points: {p2Points}")

    

@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention players (ie. <@975832996336767016).")

   
@tasks.loop(hours=1)
async def current_time():
    now = datetime.datetime.now()
    
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    
    channel = bot.get_channel(963986516365955146)
    
    await channel.send("Data atual: " + now)
    

bot.run("OTc1ODMyOTk2MzM2NzY3MDE2.GJUYhH.oUt-AiBoIbK3ag1kIOOnDNEeUE67Amyft5y1DU")