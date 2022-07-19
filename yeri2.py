# discord 모듈은 외부 모듈이기 때문에 cmd에서 pip하고 와야함
# itertools 모듈은 내장 모듈이기때문에 따로 pip하지 않아도 됨

## 모듈
import discord
from discord import message # 디스코드 모듈 불러오기
from discord.ext import commands, tasks # 명령어 확장팩 불러오기
from itertools import cycle # 상태 루프 걸때 필요한 팩

import time # 채팅 핑 만들때 필요한 모듈
import random # 로또와 게임 뽑기 만들기

from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

import youtube_dl

## 예리봇의 시작
bot = commands.Bot(command_prefix = "!") # 명령어 접두사 "!" 지정
token = "^^" # 내새끼 주민번호


## 봇이 online되면 제일 먼저 수행되는 것들
@bot.event
async def on_ready(): # on_ready 라는 함수를 생성하여, 봇이 실행되면 할 동작들을 넣어줌
    print("예리 일 할거야")
    print("=========================")
    print("제작자 : ***")
    print("leeby.dev@gmail.com")
    print("")
    change_status.start() # 상태표시 로테이션제 ^ _____ ^
    # await bot.change_presence(activity=discord.Game("예리는 말 안드뤄!"))
    # await bot.change_presence(activity=discord.Streaming(name="예리는", url="")) = 방송중 상태로 설정

# await bot.change_presence(activity=discord.Game("텍스트 넣어")) = 상태 메세지 설정
# await bot.change_presence(activity=discord.Game("텍스트 넣어"), status=discord.Status.상태) = 상태 설정
# 상태 - online = 온라인 / idle = 자리비움 / do_not_disturb = dnd = 다른 용무 중 / offline = 오프라인
# await bot.change_presence(activity=discord.Streaming(name="트위치 방송", url="트위치 링크")) = 방송중 상태로 설정
## 방송중 설정 사용하려면 코드를 교체해줘야함!

## 상태 설정 코드
# 상태 리스트를 만들어서 playing 변수에 넣어줌
playing = cycle(["예리는 착한 봇", "말 안드뤄!", "마카롱 옴뇸뇸", "롤 생각"])

# loop걸어줌
@tasks.loop(minutes=45)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(playing)))
# seconds=n : 초단위, minutes=n : 분단위, hours=n : 시간단위


## 서버핑 출력
@bot.command(aliases=["ping"])
async def 핑(ctx): # 핑 이라는 비동기 함수
    latancy = bot.latency # bot.latency를 latancy라는 변수 생성
    # latancy값을 ms단위에 맞게 1000을 곱하고, round로 소수점 첫째자리 반올림
    # f string을 이용하여 문구 출력
    await ctx.send(f"고것은 제 {round(latancy * 1000)} 번째 잔상입니다만") # 함수의 비동기 흐름이 멈추고 명령을 수행하는 데 소비하는 시간
         

## 사용자 말 따라하기
@bot.command()
async def 건의(ctx, *, content: str):
    await ctx.send(content)
    

## 노래
# 입장
@bot.command()
async def 공하(ctx):
    await ctx.author.voice.channel.connect()
    await ctx.channel.send("예리와써~")

# 퇴장
@bot.command()
async def 빠잉(ctx):
    for vc in bot.voice_clients:
        if vc.guild == ctx.guild:
            voice = vc
    await voice.disconnect()
    await ctx.channel.send("예리갈게~")
    

# 노래재생
@bot.command()
async def 재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    for vc in bot.voice_clients:
        if vc.guild == ctx.guild:
            voice = vc
            if not vc.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
                vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

                title = info("title")
                await ctx.channel.send(title + " 부르는중!")
            else:
                await ctx.send("노래가 이미 재생되고 있습니다!") 

## 로또번호 생성기
@bot.command()
async def 로또(ctx):
    lotto = range(1, 46)
    await ctx.send(f"{random.sample(lotto,6)} 당첨되면 예리한테 치킨 쏘기!")

## 연금 복권 번호 생성기
@bot.command()
async def 연금(ctx):
    lotto2 = random.random()
    await ctx.send(f"[{int(lotto2*1000000)}] 당첨되면 정기 구독하기!_!")

## 게임 추첨기
@bot.command()
async def 게임(ctx):
    game = ["롤", "배그", "블서", "로아", "테런", "크아"]
    await ctx.send(random.choices(game))

## 각종 명령어
@bot.command()
async def 사용법(ctx):
    text = "알아서 잘 써보시지! 😋"
    await ctx.send(embed = discord.Embed(title = "예리 사용법", description = text, color = 0x4641D9))

@bot.command()
async def 예리야(ctx):
    await ctx.send("왜 불러~")

# 특수기호를 쓰고 싶을때는 명령어를 미리 지정해준다.
@bot.command(name = "1234") # name = 명령어 지정
async def _1234(ctx):
    await ctx.send("5678")

# 명령어를 2개 이상으로 지정할때는, aliases=[]를 사용한다. (리스트 생성)
@bot.command(aliases=["뚱카롱"])
async def 마카롱(ctx):
    await ctx.send("마카롱 조하~")

@bot.command()
async def 잘했어(ctx):
    await ctx.send("희희")

@bot.command()
async def 일어나(ctx):
    await ctx.send("몇시야?")

@bot.command(aliases=["예리야 밥줘"])
async def 밥줘(ctx):
    await ctx.send("누구세요?")

@bot.command()
async def 일해(ctx):
    await ctx.send("싫엉!")

@bot.command()
async def 공주(ctx):
    await ctx.send("예리 왜 불렁 > _<")



bot.run(token)


