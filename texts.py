import os
from dotenv import load_dotenv

load_dotenv()
DEV_CHAT_ID = os.getenv('DEV_CHAT_ID')


send_contact = {
    "es": "Pulsa fijar, elige `contactos` y envía el contacto de la persona con la que quieres hablar.",
    "en": "Tap pin, choose `contacts`, and send the contact of the person you want to talk to.",
    "ar": "اضغط على التثبيت، اختر `جهات الاتصال`، ثم أرسل جهة اتصال الشخص الذي تريد التحدث معه.",
    "pt": "Toque em fixar, escolha `contatos` e envie o contato da pessoa com quem você quer conversar.",
    "bn": "পিন এ চাপ দিন, `contacts` নির্বাচন করুন এবং যার সঙ্গে কথা বলতে চান তার কন্ট্যাক্ট পাঠান।",
    "id": "Ketuk sematkan, pilih `kontak`, lalu kirim kontak orang yang ingin kamu ajak bicara.",
    "ru": "Нажми закрепить, выбери `контакты` и отправь контакт человека, с которым хочешь общаться.",
    "ja": "ピンをタップして「連絡先」を選び、話したい相手の連絡先を送ってください。",
    "pa": "ਪਿਨ 'ਤੇ ਟੈਪ ਕਰੋ, `contacts` ਚੁਣੋ ਅਤੇ ਉਸ ਵਿਅਕਤੀ ਦਾ ਸੰਪਰਕ ਭੇਜੋ ਜਿਸ ਨਾਲ ਤੁਸੀਂ ਗੱਲ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ।",
    "de": "Tippe auf Anheften, wähle `Kontakte` und sende den Kontakt der Person, mit der du chatten möchtest.",
}

group_msg = {
    "es": "Este bot solo funciona en chats privados.",
    "ru": "Бот работает только в приватных чатах.",
    "en": "Bot works only in private chats.",
    "ar": "البوت يعمل فقط في المحادثات الخاصة.",
    "pt": "O bot funciona apenas em conversas privadas.",
    "bn": "বট শুধুমাত্র ব্যক্তিগত চ্যাটে কাজ করে।",
    "id": "Bot hanya bekerja di chat pribadi.",
    "ja": "ボットはプライベートチャットでのみ機能します。",
    "pa": "ਬੋਟ ਕੇਵਲ ਪਰਦੇਦਾਰ ਚੈਟ ਵਿੱਚ ਕੰਮ ਕਰਦਾ ਹੈ।",
    "de": "Der Bot funktioniert nur in privaten Chats.",
}

group_link = {
    "es": "Enlace al grupo: {invite_link}",
    "en": "Group link: {invite_link}",
    "ar": "رابط المجموعة: {invite_link}",
    "pt": "Link do grupo: {invite_link}",
    "bn": "গোপনীয় গ্রুপের লিঙ্ক: {invite_link}",
    "id": "Tautan grup: {invite_link}",
    "ru": "Ссылка на группу: {invite_link}",
    "ja": "グループリンク: {invite_link}",
    "pa": "ਗੁਰੂਤਾ ਗ੍ਰੁਪ ਲਿੰਕ: {invite_link}",
    "de": "Gruppenlink: {invite_link}",
}

user_joined_group = {
    "es": "El usuario <a href='tg://user?id={user_id}'>{user_name}</a> se unió al grupo {group_link}",
    "en": "User <a href='tg://user?id={user_id}'>{user_name}</a> joined the group {group_link}",
    "ar": "المستخدم <a href='tg://user?id={user_id}'>{user_name}</a> انضم إلى المجموعة {group_link}",
    "pt": "O usuário <a href='tg://user?id={user_id}'>{user_name}</a> entrou no grupo {group_link}",
    "bn": "ব্যক্তি <a href='tg://user?id={user_id}'>{user_name}</a> গ্রুপ {group_link} এ যোগ দিলেন",
    "id": "Pengguna <a href='tg://user?id={user_id}'>{user_name}</a> bergabung ke grup {group_link}",
    "ru": "Пользователь <a href='tg://user?id={user_id}'>{user_name}</a> присоединился, ссылка на группу {group_link}",
    "ja": "ユーザー <a href='tg://user?id={user_id}'>{user_name}</a> がグループ {group_link} に参加しました",
    "pa": "ਵਿਅਕਤੀ <a href='tg://user?id={user_id}'>{user_name}</a> ਗ੍ਰੁਪ {group_link} ਵਿੱਚ ਸ਼ਾਮਲ ਹੋਇਆ",
    "de": "Benutzer <a href='tg://user?id={user_id}'>{user_name}</a> hat der Gruppe {group_link} beigetreten",
}

no_group_found = {
    "es": f"No se encontraron grupos vacíos, contacte al administrador <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "en": f"No empty groups found, contact the admin <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "ar": f"لا توجد مجموعات فارغة, يرجى الاتصال بالمسؤول <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "pt": f"Nenhum grupo vazio encontrado, contate o administrador <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "bn": f"কোনো গ্রুপ খালি নেই, অ্যাডমিনকে যোগাযোগ করুন <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "id": f"Tidak ada grup kosong, hubungi admin <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "ru": f"Нет свободных групп, обратитесь к админу <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "ja": f"空のグループが見つかりません、管理者に連絡してください <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "pa": f"ਕੋਈ ਖੁੱਲਾ ਗ੍ਰੁਪ ਨਹੀਂ ਲੱਭਿਆ, ਮਾਰਚ ਦਾਤਾ ਨਾਲ ਸੰਪਰਕ ਕਰੋ <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
    "de": f"Keine leeren Gruppen gefunden, kontaktieren Sie den Administrator <a href='tg://user?id={DEV_CHAT_ID}'>@bikmetle</a>",
}