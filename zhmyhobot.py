import telebot
import os
from PIL import Image

bot = telebot.TeleBot("Your_Token")


@bot.message_handler(commands=["ping"])
def send_welcome(message):
    bot.reply_to(message, "Чпоньк!")


@bot.message_handler(commands=["d", "distort"])
def distortion(m):
    if not m.reply_to_message:
        return
    m = m.reply_to_message
    if not m.photo:
        if not m.sticker:
            if not m.document:
                return
            else:
                if not m.document.mime_type.startswith("image/"):
                    return
                else:
                    file_id = m.document.file_id
                    file_name = f"{file_id}.{m.document.mime_type.split('/')[1]}"
        else:
            if m.sticker.is_animated:
                return
            else:
                file_id = m.sticker.file_id
                file_name = f"{file_id}.webp"
    else:
        file_id = m.photo[-1].file_id
        file_name = f"{file_id}.jpg"
    file_path = bot.get_file(file_id).file_path
    file_bytes = bot.download_file(file_path)
    with open(file_name, "wb") as file:
        file.write(file_bytes)
    im = Image.open(file_name).convert("RGB")
    width, height = im.size
    im.save(file_name)
    cmd = f"convert {file_name} -liquid-rescale 60x60%! -resize {width}x{height}\! {file_name}"
    os.system(cmd)
    file = open(file_name, "rb")
    bot.send_photo(m.chat.id, file)
    file.close()
    os.remove(file_name)


bot.polling()
