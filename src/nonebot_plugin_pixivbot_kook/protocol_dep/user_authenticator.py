from nonebot_plugin_pixivbot.protocol_dep import UserAuthenticator as BaseUserAuthenticator

from nonebot_plugin_pixivbot_kook.postman import PostDestination


class UserAuthenticator(BaseUserAuthenticator):
    async def group_admin(self, post_dest: PostDestination) -> bool:
        # 搞不懂怎么实现
        return True
