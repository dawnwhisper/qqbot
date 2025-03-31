from client import MyClient
from botpy.ext.cog_yaml import read
import botpy
import os

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    intents = botpy.Intents.none()
    intents.public_messages=True
    intents.public_guild_messages=True
    intents.guild_messages=True
    # intents.direct_message=True

    # 通过kwargs，设置需要监听的事件通道
    client = MyClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])