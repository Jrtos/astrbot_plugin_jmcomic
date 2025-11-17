from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import jmcomic
from jmcomic import *

option = jmcomic.create_option_by_file('D:\work\Python\JMCoic\option.yml')
client = JmOption.default().new_jm_client()

def download(id: int) -> None:
    jmcomic.download_album(f'{id}', option)

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
            #download(album_id)
            yield event.plain_result(f"开始下载漫画 {album_id}...")
        except ValueError:
            yield event.plain_result("请提供有效的漫画 ID")

    @filter.command("search_id")
    async def search_id_handler(self, event: AstrMessageEvent):
        """按 ID 搜索漫画"""
        pass

    @filter.command("search_name")
    async def search_name_handler(self, event: AstrMessageEvent):
        """按名称搜索漫画"""
        pass

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
