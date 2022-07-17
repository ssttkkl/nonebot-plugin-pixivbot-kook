import json
from typing import Optional

from nonebot import get_bot
from nonebot.adapters.kaiheila import MessageSegment, Bot, Message
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.enums import BlockAction
from nonebot_plugin_pixivbot.postman import Postman as BasePostman, PostmanManager
from nonebot_plugin_pixivbot.postman.model.illust_message import IllustMessageModel
from nonebot_plugin_pixivbot.postman.model.illust_messages import IllustMessagesModel

from .illust_card import make_illust_card
from .post_destination import PostDestination


@context.require(PostmanManager).register
class Postman(BasePostman[int, int]):
    @classmethod
    def adapter(cls) -> str:
        return "kaiheila"

    @staticmethod
    async def make_illust_msg(model: IllustMessageModel) -> Optional[Message]:
        bot: Bot = get_bot()

        image_url = await bot.upload_file(("img.jpg", model.image, "image/jpeg"))
        block_msg = None

        if model.block_action is not None:
            if model.block_action == BlockAction.no_image:
                image_url = None
                block_msg = model.block_message
            elif model.block_action == BlockAction.completely_block:
                return Message(model.block_message)
            elif model.block_action == BlockAction.no_reply:
                return None

        card = make_illust_card(model, image_url, block_msg)
        card_json = json.dumps(card)
        return Message(MessageSegment.Card(card_json))

    async def send_plain_text(self, message: str,
                              *, post_dest: PostDestination):
        await post_dest.post(Message(message))

    async def send_illust(self, model: IllustMessageModel,
                          *, post_dest: PostDestination):
        message = await self.make_illust_msg(model)
        if message:
            await post_dest.post(message)

    async def send_illusts(self, model: IllustMessagesModel,
                           *, post_dest: PostDestination):
        for x in model.flat():
            await self.send_illust(x, post_dest=post_dest)


__all__ = ("Postman",)
