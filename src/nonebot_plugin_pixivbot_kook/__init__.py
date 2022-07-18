"""
nonebot-plugin-pixivbot-kook

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/ssttkkl/nonebot-plugin-pixivbot-kook
"""

# ======= register Postman and PostDestination =======
from .postman import Postman, PostDestinationFactory

# =============== register protocol_dep ===============
from .protocol_dep.user_authenticator import UserAuthenticator
