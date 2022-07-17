from abc import ABC, abstractmethod
from typing import Optional

from nonebot import get_bot
from nonebot.adapters.kaiheila import Message, Bot
from nonebot.adapters.kaiheila.event import ChannelMessageEvent, PrivateMessageEvent, Event
from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.postman import PostDestination as BasePostDestination, \
    PostDestinationFactory as BasePostDestinationFactory
from nonebot_plugin_pixivbot.utils.nonebot import get_adapter_name


class PostDestination(BasePostDestination[str, str], ABC):
    @property
    def adapter(self) -> str:
        return get_adapter_name()

    @abstractmethod
    async def post(self, msg: Message):
        raise NotImplementedError()


class PrivatePostDestination(PostDestination):
    def __init__(self, *, user_id: str,
                 quote_message_id: Optional[str] = None):
        self._user_id = user_id
        self.quote_message_id = quote_message_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def group_id(self) -> Optional[str]:
        return None

    async def post(self, message: Message):
        bot: Bot = get_bot()
        await bot.send_private_msg(user_id=self.user_id, message=message, quote=self.quote_message_id)


class ChannelPostDestination(PostDestination):
    def __init__(self, *, user_id: Optional[str] = None,
                 channel_id: str,
                 quote_message_id: Optional[str] = None):
        self._user_id = user_id
        self.channel_id = channel_id
        self.quote_message_id = quote_message_id

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def group_id(self) -> str:
        """
        其实是channel_id
        """
        return self.channel_id

    async def post(self, message: Message):
        bot: Bot = get_bot()
        await bot.send_channel_msg(channel_id=self.channel_id, message=message, quote=self.quote_message_id)


@context.register_singleton()
class PostDestinationFactory(BasePostDestinationFactory[str, str]):
    def build(self, user_id: Optional[str], group_id: Optional[str]) -> PostDestination:
        if group_id is None:
            return PrivatePostDestination(user_id=user_id)
        else:
            return ChannelPostDestination(user_id=user_id, channel_id=group_id)

    def from_event(self, event: Event) -> PostDestination:
        if isinstance(event, ChannelMessageEvent):
            return ChannelPostDestination(user_id=event.author_id,
                                          channel_id=event.target_id,
                                          quote_message_id=event.msg_id)
        elif isinstance(event, PrivateMessageEvent):
            return PrivatePostDestination(user_id=event.author_id,
                                          quote_message_id=event.msg_id)
        else:
            raise ValueError("invalid event type: " + str(type(event)))
