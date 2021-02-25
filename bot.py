import discord 
from datetime import datetime
import urllib.request
from fake_useragent import UserAgent
from main import bank
from discord.ext import commands 

global base_ch
app = commands.Bot(command_prefix='>') 
bot = bank()
items = { 1 : '경고 1회 차감권', 2 : '[고인물](칭호)', 3 : '[흑우](칭호)', 4 : '[대마법사](칭호)', 5 : '[RMT],[EMT],[PMT](칭호, 택1)', 6 : '[쇼타콘],[로리콘],[중2병](칭호, 택1)', 7 : '[얀데레].[츤데레],[도짓코](칭호, 택1)', 8 : '[페이몬],[혐],[비밀친구](칭호, 택1)', 9 : '[뉴비](칭호)', 10 : '[덕후](칭호)'}
base_ch = ''

#####################################################################################################

@app.event 
async def on_ready(): 
    print(app.user.name, 'has connected to Discord!') 
    await app.change_presence(status=discord.Status.online, activity=None) 
    print("ready")


#####################################################################################################



@app.event 
async def on_message(message): 
    # print(message.attachments[0].filename)  
    # print(message.attachments[0].url)
    
    await app.process_commands(message)
    if message.author == app.user:
        return

    try:
        ua = UserAgent()
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', str(ua.chrome))]
        urllib.request.install_opener(opener)
        for urls in message.attachments:
            urllib.request.urlretrieve(urls.url,f'img/{str(datetime.today().strftime("%Y %m %d %H %M %S"))} {message.author.id} {urls.filename}')

        msg = f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} <{message.channel}> <{message.author.id}> : msg "{message.content}" , img {str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))}-{message.author.id}-{message.attachments[0].filename} ' + '\n'
        bot.log_channel_add(str(message.channel) ,msg)

    except IndexError:
        msg = f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} <{message.channel}> <{message.author.id}> : msg "{message.content}"' + '\n'
        bot.log_channel_add(str(message.channel) ,msg)
        # print(msg)
    
#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 이름확인(message): 
    name = f'<@!{message.author.id}>'
    await message.channel.send(name)

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 역할설정(message):
    print(base_ch.members)

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 설정(message): 
    global base_ch
    base_ch = message.channel
    await base_ch.send('설정 완료!')

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 관리(message): 
    # print(message.message.content)

    ur = f'<@!{message.author.id}>'
    name = message.message.content.split(' ')[1]
    money = message.message.content.split(' ')[2]

    if '!' not in name:
        name = f'<@!{name[2:len(name)-1]}>'
    #     print(name)

    # print(ur, name, money) 
    if bot.manage(name, money) == 1:
        await message.channel.send('존재하지 않는 유저입니다.') 

    else:
        # print(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {ur}님이 {name} 님의 덕후 코인을 {money}만큼 추가했습니다')
        bot.log_server_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {ur}님이 {name} 님의 덕후 코인을 {money}만큼 추가했습니다')
        await message.channel.send(f'{name} 님의 덕후 코인을 {money} :coin: 만큼 추가했습니다.') 

@관리.error
async def 관리_error(t, err):
    if isinstance(err, commands.MissingRole):
        await t.send('당신은 권한이 없습니다.') 
    if isinstance(err, commands.CommandInvokeError):
        await t.send('명령어를 다시 확인해주세요.') 


#####################################################################################################

@app.command() 
@commands.has_any_role("은행 고객님", "은행원")
async def 만들기(message):
    name = f'<@!{message.author.id}>'
    if bot.add_user(name) == 1:
        await  message.channel.send(f'{name} 님 이미 계좌가 있습니다.')

    else:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {name} 님 계좌를 추가했습니다')
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
async def 변환(t): 
    bot.conversion()
    await t.send('변환 완료!')

@변환.error
async def 변환_error(t, err):
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
@commands.has_any_role("은행 고객님", "은행원")
async def 코인확인(message): 
    name = f'<@!{message.author.id}>'
    if bot.cheack(name) == -1:
        await message.channel.send(f'{name}님의 현재 계좌가 없습니다.')
    else:
        await message.channel.send(f'{name}님의 현재 덕후 코인은 {bot.cheack(name)} :coin: 입니다.')

@코인확인.error
async def 코인확인_err(t, err):
    if isinstance(err,commands.CommandInvokeError):
        await t.send('존재하지 않는 유저입니다.') 

#####################################################################################################

@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 구매(message):
    user_id = f'<@!{message.author.id}>'
    item_num = int(message.message.content.split(' ')[1])
    # print(f'{user_id} {item_num}') 
    ch = bot.buy(user_id, item_num)
    channel = message.channel
    if ch == 1:
        await channel.send('돈이 부족합니다.') 
    elif ch == 0:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {user_id} 님이  {items[item_num]} 을 구매 하셨습니다.')
        print(f'{user_id}님이 {items[item_num]} 을 구매 하셨습니다.')
        await channel.send(f'{user_id}님이 {items[item_num]} 을 구매 하셨습니다.') 

#####################################################################################################

@app.command() 
async def 출첵(message):
    name = f'<@!{message.author.id}>'
    channel = message.channel
    ch = bot.attend(name)
    if ch == 0:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {name} 님이 출석했습니다.')
        print(f'<@!{message.author.id}> 출석')
        await channel.send(f'{name}님 출석! {bot.data[name][3]}회 출석했습니다.') 

    elif ch == 2:
        bot.log_server_add(f'{str(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))} log: {name} 님이 출석했습니다. 5코인 추가 되었습니다.')
        print(f'<@!{message.author.id}> 출석')
        await channel.send(f'{name}님 출석! {bot.data[name][3]}회 출석했습니다. 5코인 추가 되었습니다.') 
    
    elif ch == 1:
        print('이미 출석했습니다.')
        await channel.send(f'{name}님 이미 출석했습니다.') 

#####################################################################################################

@app.command() 
async def 출첵확인(message):
    name = f'<@!{message.author.id}>'
    channel = message.channel
    await channel.send(f'<@!{message.author.id}> 님 출석횟수는 {bot.data[name][3]} 입니다.') 

#####################################################################################################

@app.command() 
async def test(message):
    print(f'<@!{message.author.id}>')
    channel = message.channel
    await channel.send(f'<@!{message.author.id}>') 

#####################################################################################################

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

#####################################################################################################

@app.command() 
@commands.has_any_role("은행원" , "은행 고객님")
async def 도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">출첵 ", value="출석 체크를 합니다.", inline=False)
    embed.add_field(name=">출첵확인 ", value="출석 체크한 횟수를 보여줍니다.", inline=False)
    embed.add_field(name=">만들기 ", value="덕후 코인을 할당받는 계좌를 만듭니다.", inline=False)
    embed.add_field(name=">코인확인 ", value="유저의 현재 소지하는 덕후 코인을 확인합니다.", inline=False)
    await t.send(embed=embed)

#####################################################################################################

@app.command() 
@commands.has_role("은행원")
async def 관리도움(t):
    embed = discord.Embed(title="덕후 은행", description="디스코드 덕후 코인봇 입니다.", color=0x62c1cc)
    embed.add_field(name=">관리 (유저멘션) (추가 또는 빼고 싶은 만큼의 돈)", value="멘션한 유저의 돈을 더하거나 뺍니다.", inline=False)
    embed.add_field(name=">저장", value="정보를 저장합니다.", inline=False)
    embed.add_field(name=">유저확인 (유저멘션)", value="유저의 ID값을 가져옵니다.", inline=False)
    embed.add_field(name=">이름확인 (id)", value="유저의 ID값으로 유저이름을 알려줍니다. (멘션됨).", inline=False)
    embed.add_field(name=">변환", value="텍스트 파일로 로그를 출력 합니다.", inline=False)
    await t.send(embed=embed)

#####################################################################################################

app.run('')
