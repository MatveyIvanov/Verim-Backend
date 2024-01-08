import re
from typing import Tuple

from services.entries import ContentType


YOUTUBE_REGEX = re.compile(
    r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?"
)
TIKTOK_REGEX = re.compile(
    r"https:\/\/(?:m|www|vm)?\.?tiktok\.com\/((?:.*\b(?:(?:usr|v|embed|user|video)\/|\?shareId=|\&item_id=)(\d+))|\w+)"
)
VK_REGEX = re.compile(r"http(?:s?):\/\/(?:www\.)?vk.com/video.*")
TWITCH_REGEX = re.compile(r"(?:https:\/\/)?clips\.twitch\.tv\/(\S+)/i")


def clean_url_and_get_content_type(url: str) -> Tuple[str, ContentType | None]:
    regex_map = {
        ContentType.YOUTUBE: YOUTUBE_REGEX,
        ContentType.TIKTOK: TIKTOK_REGEX,
        ContentType.VK: VK_REGEX,
        ContentType.TWITCH: TWITCH_REGEX,
    }
    for type, regex in regex_map.items():
        if (match := re.match(regex, url)) is not None:
            return match.group(), type
    return url, None
