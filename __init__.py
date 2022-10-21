import cv2
import numpy as np
import base64

import aiohttp
import asyncio
from threading import Thread
from os import path

from hoshino.typing import CQEvent
import hoshino
from hoshino import Service, priv

from .img_mix import mix

sv_help = '''
[混合] +序号+图片1+图片2
[查模板] +序号
'''.strip()
sv = Service('图片混合',help_=sv_help, bundle='娱乐')

MASK_FOLDER = "images\\mask\\"
OUT_FOLDER = "images\\ouput"
_dir = path.dirname(__file__)+"\\"


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
    

async def download(url):
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                content = await resp.read()
                return content
    except:
        return False


def cv2_to_base64(img):
    img = cv2.imencode('.jpg', img)[1]
    image_code = str(base64.b64encode(img))[2:-1]

    return image_code


async def get_img(black_url, white_url, idx, bot, ev: CQEvent):   
    mask_file = _dir + MASK_FOLDER+f"{idx}.jpg"
    output_dir = _dir + OUT_FOLDER

    if not path.exists(mask_file):
        await bot.send(ev,"不存在该模板")
        return 

    p = await download(black_url)
    q = await download(white_url)
    if not (p and q):
        await bot.send(ev, "下载图片失败")
        return
    
    black_img = cv2.imdecode(np.frombuffer(p, np.uint8), cv2.IMREAD_COLOR)
    white_img = cv2.imdecode(np.frombuffer(q, np.uint8), cv2.IMREAD_COLOR)
    mask_img = cv2.imread(mask_file, cv2.IMREAD_COLOR)

    size = (black_img.shape[1], black_img.shape[0])
    white_img = cv2.resize(white_img, size, interpolation=cv2.INTER_CUBIC)
    mask_img = cv2.resize(mask_img, size, interpolation=cv2.INTER_CUBIC)

    img = mix(black_img, white_img, mask_img, output_dir)
    base64_str = cv2_to_base64(img)
    img =  'base64://' + base64_str
    mycontent = f'''混合结果
[CQ:image,file={img}]'''
    await bot.send(ev,mycontent)
    


@sv.on_prefix('混合')
async def mix_init(bot, ev: CQEvent): 
    content=ev.message
    if len(content) != 3:
        return
    idx=content.extract_plain_text()
    if idx=='':
        idx=1
    else:
        idx=int(idx)
    code1=content[1]["data"]
    code2=content[2]["data"]
    black_url = code1.get("url")
    white_url = code2.get("url")
    if black_url and white_url:
        await bot.send(ev, "混合中")
        new_loop = asyncio.new_event_loop()
        t = Thread(target=start_loop, args=(new_loop,))
        t.start()
        coroutine1=get_img(black_url, white_url, idx, bot, ev)
        asyncio.run_coroutine_threadsafe(coroutine1,new_loop)
    else:
        await bot.send(ev, "参数错误")


@sv.on_prefix('查模板')
async def mix_init(bot, ev: CQEvent): 
    idx=ev.message.extract_plain_text()
    if idx=='':
        await bot.send(ev, "参数错误")
        return
    mask_file = _dir + MASK_FOLDER+f"{idx}.jpg"
    if path.exists(mask_file):
        mycontent = f'''模板{idx}
[CQ:image,file=file:///{mask_file}]'''
        await bot.send(ev,mycontent)
    else:
        await bot.send(ev,"不存在该模板")
        

@sv.on_prefix('添加模板')
async def add_mask(bot,ev:CQEvent):
    if not priv.check_priv(ev, priv.SUPERUSER):
        return

    content=ev.message
    name = content.extract_plain_text().strip()
    if name=='':
        await bot.send(ev, "参数错误")
        return
    
    mask_file = _dir + MASK_FOLDER+f"{name}.jpg"

    if path.exists(mask_file):
        await bot.send(ev,"已存在该模板")
        return 

    img_url=content[1]["data"].get("url")
    if img_url == None:
        await bot.send(ev,'请附带mask图片~')
        return

    p = await download(img_url)
    img = cv2.imdecode(np.frombuffer(p, np.uint8), cv2.IMREAD_COLOR)
    mask_file = _dir + MASK_FOLDER+f"{name}.jpg"
    cv2.imwrite(mask_file, img)
    await bot.send(ev,'模板已添加~')

