from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

import jmcomic
from jmcomic import *

option = jmcomic.create_option_by_file('D:\Librury\Desktop\AstrBotLauncher-0.2.0\AstrBot\data\plugins\astrbot_plugin_jmcomic\option.yml')
client = JmOption.default().new_jm_client()

def download(id: int):
    jmcomic.download_album(f'{id}', option)

def search_name(name: str, pag: int):
    page: JmSearchPage = client.search_site(search_query=name, page=pag)

    for album_id, title in page:
        print(f'[{album_id}]: {title}')

def search_id(id:int):
    page = client.search_site(search_query=f'{id}')
    album: JmAlbumDetail = page.single_album
    print(album.tags)

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):

    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("download")
    async def download_handler(self, event: AstrMessageEvent):
        """下载漫画指令"""
        message_str = event.message_str
        try:
            album_id = int(message_str.strip('/download '))
            yield event.plain_result(f"开始下载漫画 {album_id}...")
            download(album_id)
            pdf = Comp.File(file=f'download/{album_id}.pdf',name=f'{album_id}.pdf')
            yield event.chain_result([pdf])
        except ValueError:
            yield event.plain_result("请提供有效的漫画 ID")

    @filter.command("s_id")
    async def search_id_handler(self, event: AstrMessageEvent):
        message_str = event.message_str
        id = int(message_str.strip('/s_id '))
        page = client.search_site(search_query=f'{id}')
        album: JmAlbumDetail = page.single_album
        resolt = ''
        for i in album.tags:
            resolt += f'{i}\n'
        yield event.plain_result(resolt)
        
        

    @filter.command("s_name")
    async def search_name_handler(self, event: AstrMessageEvent):
        message_str = event.message_str
        name = message_str.split()
        page: JmSearchPage = client.search_site(search_query=name[1], page=int(name[2]))
        yield event.plain_result('正在搜索')
        resolt = ''

        for album_id, title in page:
            resolt += f'[{album_id}]: {title}\n'
        yield event.plain_result(resolt)

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
