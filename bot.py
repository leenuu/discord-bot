import discord 
from datetime import datetime
from main import bank
from discord.ext import commands 

app = commands.Bot(command_prefix='>') 
bot = bank()

#####################################################################################################
@app.event 
async def on_ready(): 
    print(app.user.name, 'has connected to Discord!') 
    await app.change_presence(status=discord.Status.online, activity=None) 
    print("ready")

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 관리(t, *, name_money): 
    name = name_money.split(' ')[0]
    money = name_money.split(' ')[1]
    if bot.manage(name, money) == 1:
        await t.send('존제하지 않는 유저입니다.') 

    else:
        bot.log_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {name} 님의 덕후 코인을 {money}만큼 추가했습니다')
        await t.send(f'{name} 님의 덕후 코인을 {money} :coin: 만큼 추가했습니다.') 

# @관리.error
# async def 관리_error(t, err):
#     if isinstance(err, commands.MissingRole):
#         await t.send('당신은 권한이 없습니다.') 
#     if isinstance(err, commands.CommandInvokeError):
#         await t.send('명령어를 다시 확인해주세요.') 


#####################################################################################################

@app.command() 
@commands.has_any_role("은행 고객원", "은행원")
async def 만들기(message):
    name = f'<@!{message.author.id}>'
    if bot.add_user(name) == 1:
        await  message.channel.send(f'{name} 님 이미 계좌가 있습니다.')

    else:
        bot.log_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {name} 님 계좌를 추가했습니다')
        await message.channel.send(f'{name} 님의 계좌를 추가했습니다.') 

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 저장(t): 
    bot.save()
    await t.send('데이터 저장 완료!')
    bot.log_save()
    await t.send('로그 저장 완료!')

@저장.error
async def 저장_error(t, err):
    if isinstance(err, commands.MissingRole):
        await t.send('당신은 권한이 없습니다.') 

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 유저확인(t, *, ur): 
    name = ur.replace("<@!", "").replace(">", "")
    await t.send(name)

@유저확인.error
async def 유저확인_error(t, err):
    if isinstance(err, commands.MissingRole):
        await t.send('당신은 권한이 없습니다.') 

#####################################################################################################

@app.command() 
@commands.has_any_role("은행 고객원", "은행원")
async def 코인확인(message): 
    name = f'<@!{message.author.id}>'
    await message.channel.send(f'{name}님의 현재 덕후 코인은 {bot.cheack(name)} :coin: 입니다.')

@코인확인.error
async def 코인확인_err(t, err):
    if isinstance(err,commands.CommandInvokeError):
        await t.send('존제하지 않는 유저입니다.') 

#####################################################################################################

@app.command() 
@commands.has_any_role("은행원" , "은행 고객원")
async def 구매(t, *, item):
    pass

#####################################################################################################

@app.command() 
async def test(message):
    print(f'<@!{message.author.id}>')
    channel = message.channel
    await channel.send(f'<@!{message.author.id}>') 

#####################################################################################################

@app.command() 
@commands.has_any_role("은행원" , "은행 고객원")
async def 도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">만들기 ", value="덕후 코인을 할당받는 계좌를 만듬니다.", inline=False)
    embed.add_field(name=">코인확인 ", value="유저의 현제 소지하는 덕후 코인을 확인합니다.", inline=False)
    await t.send(embed=embed)

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 관리도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">관리 (유저맨션) (추가 또는 빼고싶은 만큼의 돈)", value="맨션한 유저의 돈을 더하거나 뺌니다.", inline=False)
    embed.add_field(name=">저장", value="정보를 저장합니다.", inline=False)
    embed.add_field(name=">유저확인 (유저맨션)", value="유저의 ID값을 가져옵니다.", inline=False)
    await t.send(embed=embed)

#####################################################################################################



app.run('ODA1MDI4MjMzOTIxNDI5NTc0.YBU69w.c6zQyOi5qJ6YnXfNAwCCmsQboV8')

