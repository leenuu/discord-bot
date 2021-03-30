import discord 
from datetime import datetime
import urllib.request
from fake_useragent import UserAgent
from main_ver2 import bank
from discord.ext import commands 

app = commands.Bot(command_prefix='>') 
bot = bank()
items = { 1 : '경고 1회 차감권', 2 : '[고인물](칭호)', 3 : '[흑우](칭호)', 4 : '[대마법사](칭호)', 5 : '[RMT],[EMT],[PMT](칭호, 택1)', 6 : '[쇼타콘],[로리콘],[중2병](칭호, 택1)', 7 : '[얀데레].[츤데레],[도짓코](칭호, 택1)', 8 : '[페이몬],[혐],[비밀친구](칭호, 택1)', 9 : '[뉴비](칭호)', 10 : '[덕후](칭호)'}


@app.event 
async def on_ready(): 
    print('연결 완료!') 
    await app.change_presence(status=discord.Status.online, activity=None) 


async def logs(message):
    ua = UserAgent()
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', str(ua.chrome))]
    urllib.request.install_opener(opener)
    user = f'<@!{message.author.id}>'
    if message.attachments == []:
        msg = f'{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))} <{message.channel}> <{message.author.id}> : msg "{message.content}"' + '\n'
        bot.log_channel_user_add(str(message.channel) ,msg, user)

    else:
        for urls in message.attachments:
            urllib.request.urlretrieve(urls.url,f'img/{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))}-{message.author.id}-{urls.filename}')

            msg = f'{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))} <{message.channel}> <{message.author.id}> : msg "{message.content}" , img {str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))}-{message.author.id}-{message.attachments.filename} ' + '\n'
            bot.log_channel_user_add(str(message.channel) ,msg, user)
        
        
    
@app.event 
async def on_message(message): 
    await app.process_commands(message)
    # print(bot.data)
    await logs(message)
    return


@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 만들기(message):
    user = f"<@!{message.author.id}>"
    log = f'{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))} log: {user} 님이 계좌를 만들었습니다.'

    if bot.new_bank_user(user) == 0:
        bot.log_server_add(log)
        await message.channel.send(f'{user} 님이 계좌를 만들었습니다.')
    
    else:
        await message.channel.send(f'{user} 님은 이미 계좌가 있습니다.')


@app.command() 
@commands.has_role("은행원")
async def 관리(message): 
    user = f'<@!{message.author.id}>'
    name = message.message.content.split(' ')[1]
    money = int(message.message.content.split(' ')[2])

    if '!' not in name:
        name = f'<@!{name[2:len(name)-1]}>'

    if  bot.manage(name, money) == 1:
        await message.channel.send('존재하지 않는 유저입니다.') 

    else:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))} log: {user}님이 {name} 님의 덕후 코인을 {money}만큼 추가했습니다')
        await message.channel.send(f'{name} 님의 덕후 코인을 {money} :coin: 만큼 추가했습니다.') 

@관리.error
async def 관리_error(t, err):
    if isinstance(err, commands.MissingRole):
        await t.send('당신은 권한이 없습니다.') 
    if isinstance(err, commands.CommandInvokeError):
        await t.send('명령어를 다시 확인해주세요.') 


@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 구매(message):
    user_id = f'<@!{message.author.id}>'
    item_num = int(message.message.content.split(' ')[1])
    ch = bot.buy(user_id, item_num)
    channel = message.channel
    if ch == 1:
        await channel.send(f'{user_id}님 돈이 부족합니다.') 

    elif ch == 0:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))} log: {user_id} 님이  {items[item_num]} 을 구매 하셨습니다.')
        await channel.send(f'{user_id}님이 {items[item_num]} 을 구매 하셨습니다.')

    elif ch == -1:
        await channel.send(f'{user_id}님의 계좌가 존재하지 않습니다.')

@구매.error
async def 구매_error(t, err):
    if isinstance(err, commands.CommandInvokeError):
        await t.send('명령어를 다시 확인해주세요.') 


@app.command() 
@commands.has_role("은행원")
async def 저장(t): 
    bot.save_data()
    await t.send('데이터  저장 완료!')
    bot.log_save()
    await t.send('로그 저장 완료!')

@저장.error
async def 저장_error(t, err):
    if isinstance(err, commands.MissingRole):
        await t.send('당신은 권한이 없습니다.') 
        

@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 상점품목(t):
    embed = discord.Embed(title="덕후 은행 상점", description="덕후 코인으로 살 수 있는 품목 입니다.", color=0x62c1cc)
    embed.add_field(name=">1 경고 1회 차감권 ", value="1000 코인", inline=True)
    embed.add_field(name=">2 [고인물](칭호)", value="800 코인", inline=True)
    embed.add_field(name=">3 [흑우](칭호)", value="600 코인", inline=True)
    embed.add_field(name=">4 [대마법사](칭호) ", value="550 코인", inline=True)
    embed.add_field(name=">5 [RMT],[EMT],[PMT](칭호, 택1)", value="500 코인", inline=True)
    embed.add_field(name=">6 [쇼타콘],[로리콘],[중2병](칭호, 택1)", value="400 코인", inline=True)
    embed.add_field(name=">7 [얀데레].[츤데레],[도짓코](칭호, 택1)", value="350 코인", inline=True)
    embed.add_field(name=">8 [페이몬],[혐],[비밀친구](칭호, 택1)", value="300 코인", inline=True)
    embed.add_field(name=">9 [뉴비](칭호)", value="100 코인", inline=True)
    embed.add_field(name=">10 [덕후](칭호)", value="50 코인", inline=True)
    await t.send(embed=embed)


@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">출첵 ", value="출석 체크를 합니다.", inline=False)
    embed.add_field(name=">출첵확인 ", value="출석 체크한 횟수를 보여줍니다.", inline=False)
    embed.add_field(name=">만들기 ", value="덕후 코인을 할당받는 계좌를 만듭니다.", inline=False)
    embed.add_field(name=">코인확인 ", value="유저의 현재 소지하는 덕후 코인을 확인합니다.", inline=False)
    embed.add_field(name="> ", value="유저의 현재 소지하는 덕후 코인을 확인합니다.", inline=False)
    await t.send(embed=embed)


@app.command() 
@commands.has_role("은행원")
async def 관리도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">관리 (유저멘션) (추가 또는 빼고 싶은 만큼의 돈) ", value="멘션한 유저의 돈을 더하거나 뺍니다.", inline=False)
    embed.add_field(name=">저장 ", value="정보를 저장합니다.", inline=False)
    embed.add_field(name=">유저확인 (유저멘션) ", value="유저의 ID값을 가져옵니다.", inline=False)
    embed.add_field(name=">이름확인 (id) ", value="유저의 ID값으로 유저이름을 알려줍니다. (멘션됨).", inline=False)
    embed.add_field(name=">변환 ", value="텍스트 파일로 로그를 출력 합니다.", inline=False)
    embed.add_field(name=">상점품목 ", value="덕후 코인으로 살 수 있는 품목을 보여줌니다.", inline=False)
    await t.send(embed=embed)


app.run('')
