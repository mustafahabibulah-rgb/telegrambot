from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum


class LanguageModelEnum(str, Enum):
    es = "Español"
    en = "English"
    ar = "العربية"
    pt = "Português"
    bn = "বাংলা"
    id = "Bahasa Indonesia"
    ru = "Русский"
    ja = "日本語"
    pa = "ਪੰਜਾਬੀ"
    de = "Deutsch"


class LanguageCallback(CallbackData, prefix="language"):
    language: LanguageModelEnum


async def language_keyboard():
    builder = InlineKeyboardBuilder()

    for language in LanguageModelEnum:
        builder.button(
            text=language.value, callback_data=LanguageCallback(language=language.value).pack()
        )

    builder.adjust(3, 4)

    return builder.as_markup()
