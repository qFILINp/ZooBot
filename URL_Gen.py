import urllib.parse
from token_data import name_bot


async def generate_vk_share_url(photo_url, caption):
    post_text = f"Я только что прошёл интересный тест! \nВот мои результаты: {caption}. \nПройди и ты https://t.me/{name_bot}"
    encoded_text = urllib.parse.quote(post_text)
    vk_url = f"https://vk.com/share.php?url={photo_url}&title={encoded_text}"
    return vk_url
