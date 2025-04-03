import asyncio
import os
import botpy
from botpy import logging
from botpy.logging import DEFAULT_FILE_HANDLER
from botpy.message import GroupMessage, Message, C2CMessage
import datetime

from api import process_request

# 创建logs目录
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# 使用当前日期格式化日志文件名
today = datetime.datetime.now().strftime("%Y-%m-%d")
log_filename = f"botpy-{today}.log"
log_filepath = os.path.join(log_dir, log_filename)

# 配置默认文件处理器
DEFAULT_FILE_HANDLER["filename"] = log_filepath

# 获取日志记录器
_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(message)
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=process_request(message)
            )

    async def on_c2c_message_create(self, message: C2CMessage):
        _log.info(f"收到私信消息：{message.content}")
        await message._api.post_c2c_message(
            openid=message.author.user_openid, 
            msg_type=0, msg_id=message.id, 
            content=f"我收到了你的消息：{message.content}"
        )

