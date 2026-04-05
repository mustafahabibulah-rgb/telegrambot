from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum


class LanguageModelEnum(str, Enum):
    spanish = "Español"
    english = "English"
    arabic = "العربية"
    portuguese = "Português"
    bangla = "বাংলা"
    indonesian = "Bahasa Indonesia"
    russian = "Русский"
    japanese = "日本語"
    punjabi = "ਪੰਜਾਬੀ"
    german = "Deutsch"


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
