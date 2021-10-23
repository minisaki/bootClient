from enum import Enum


class FacebookAction(Enum):
    LIKE = 1
    COMMENT = 2
    SHARE = 3
    LOGIN = 4
    LOGOUT = 5
    NEW_FEED = 6
    GET_COOKIE = 8
    POST_GROUP = 9


class YoutubeAction(Enum):
    LIKE = 1
    COMMENT = 2
    VIEW = 3


class TypeControl(Enum):
    HARDWARE = 1
    APP = 2


class WebsiteType(Enum):
    FACEBOOK = 1
    YOUTUBE = 2
    TIKTOK = 3
    SHOPPE = 4

