# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import paddlehub as hub
import time
import random

model = hub.Module(name="plato-mini")

talk = on_command("chat",rule=to_me(), priority=5)
talkself = on_command("自言自语", rule=to_me(), priority=5)
about = on_command("about", rule=to_me(), priority=5)

@talk.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  
    if args:
        state["msg"] = args  # 如果用户发送了参数则直接赋值

@talk.got("msg", prompt="你好，我是陈睿")
async def talking(bot: Bot, event: Event, state = T_State):
    msg = state['msg']
    with model.interactive_mode(max_turn=20):
        while True:
            if random.randint(1,10) == 4:
                reply = "[CQ:image,file=https://https://cdn.jsdelivr.net/gh/C4a15Wh/RuiBot-Images@main/ChenRui-" + random.randint(0,74) + ".jpg?raw=true,id=40000]"
            elif msg not in "stop":
                reply = model.predict(msg)[0]
                await talk.reject(reply)
            else:
                await talk.finish("再见，叔叔只想给老色批们一个快乐老家。")
                break

@talkself.handle()
async def handle_first_receive(bot: Bot,event: Event, state: T_State):
    args = str(event.get_message()).strip()  
    if args:
        state["num"] = args  # 如果用户发送了参数则直接赋值

@talkself.got("num", prompt="请问需要几轮对话（一次问答为一轮）")
async def talkingself(bot: Bot, event: Event, state = T_State):
    num = int(state["num"])
    i=0
    msg = "你好"
    with model.interactive_mode(max_turn=3):
        while True:
            if i == num or i > num:
                await talk.finish("本次对话已结束，请节制使用")
                break
            await talk.send(msg)
            msg1 = model.predict(msg)[0]
            await talk.send(msg1)
            msg = model.predict(msg1)[0]
            i+=1

@about.receive()
async def _(bot: Bot, event: Event, state: T_State):
    await about.send("="*30+"\nアトリは、高性能ですから！\n"+"-"*30+"\n睿叔叔Bot Ver.0.1.0\nCopyright 2021 Stariver Project All Rights Reserved.")