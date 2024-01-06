import pathlib
import random
import urllib.request
from asyncio import sleep

import aiohttp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

headers = {
    "Token": "eyJhbGciOiJIUzI1NiIsImtpZCI6IjFlYWZPREQ3d3dodHFGVXgiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzA1MTUzMjE2LCJpYXQiOjE3MDQ1NDg0MTYsImlzcyI6Imh0dHBzOi8vaGxobW1rcHVncnVrbmVmc3R0bHIuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjM1Y2QxZTAzLTRhMDAtNDEyMy1hNGFmLTQ3MmM2MjQ3MTc3NiIsImVtYWlsIjoiZGFzaGtpbi5kaW1hMjAwM0BnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6Imdvb2dsZSIsInByb3ZpZGVycyI6WyJnb29nbGUiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0toZERKM0lNclNNVnpOV2ZydWhXQV9iVTZyc3FFelB5djlscmtrQjdsbT1zOTYtYyIsImVtYWlsIjoiZGFzaGtpbi5kaW1hMjAwM0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoi0JTQvNC40YLRgNC40Lkg0JTQsNGI0LrQuNC9IiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6ItCU0LzQuNGC0YDQuNC5INCU0LDRiNC60LjQvSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0toZERKM0lNclNNVnpOV2ZydWhXQV9iVTZyc3FFelB5djlscmtrQjdsbT1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTExMzU3MTAwNTEyMjY3ODAyNDQwIiwic3ViIjoiMTExMzU3MTAwNTEyMjY3ODAyNDQwIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3MDQ1NDg0MTZ9XSwic2Vzc2lvbl9pZCI6ImQ2ZWFiOWM5LTFhMGYtNGQ1Yi1hMDU2LTk3MmVkMzBmNGYzNCJ9.uZsIGPqQquu-9YZeWLFCtJ27sNISXBzSnW3SGbtXZBA",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://app.supermeme.ai/text-to-meme"
}


async def get_memes(prompt):
    payload = {"imageCount": 3, "inputLanguage": "en", "maxDimension": 500, "text": prompt}
    async with aiohttp.ClientSession(headers=headers) as session:
        # counter = 0
        while True:
            async with session.post('https://app.supermeme.ai/api/meme/text-to-meme', data=payload) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    print(await resp.text())
                    return {}
                # else:
                #     print(resp.text)
                #     await sleep(3)
                #     counter += 1


async def process_response(prompt):
    memes_response = await get_memes(prompt)
    if not memes_response:
        return ""
    else:
        random_pick = random.randint(0, 3)
        meme_to_send = memes_response['response']['results'][random_pick]
        img_base64 = await draw_meme(meme_to_send)
        return img_base64


async def draw_meme(meme_info):
    urllib.request.urlretrieve(meme_info['image_name'], f"{meme_info['id']}.png")
    img = Image.open(f"{meme_info['id']}.png")
    size = meme_info['width'], meme_info['height']
    img.thumbnail(size, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    for caption in meme_info['captions']:
        current_h, pad = caption['y'], 10
        font = ImageFont.truetype('impact.ttf', caption['fontSize'])
        para = get_wrapped_text(caption["text"].upper(), font, meme_info['width'])
        for line in para:
            font = ImageFont.truetype('impact.ttf', caption['fontSize'])
            w, h = draw.textsize(line, font=font)
            draw.text(((meme_info['width'] - w) / 2, current_h), line, font=font, stroke_width=2, stroke_fill='black')
            current_h += h + pad

    img = img.convert("RGB")
    im2 = Image.open(pathlib.Path("mac_watermark.png"))
    watermark_size = (meme_info['width']//10)*1.5
    im2.thumbnail((watermark_size, watermark_size))
    w2, h2 = im2.size
    img.paste(im2, (0, (meme_info['height'] - h2) // 2), im2)
    img.save(f"{meme_info['id']}.png", format="PNG")
    return f"{meme_info['id']}.png"


def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return lines
