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

not_authorized_group = {
    "es": "El bot no tiene permisos para funcionar en este grupo, por favor contacte al administrador",
    "en": "The bot does not have permissions to work in this group, please contact the administrator",
    "ar": "البوت ليس لديه صلاحيات للعمل في هذه المجموعة، يرجى الاتصال بالمسؤول",
    "pt": "O bot não tem permissões para funcionar nesse grupo, por favor contate o administrador",
    "bn": "বট এই গ্রুপে কাজ করতে অনুমতি নেই, অ্যাডমিনকে যোগাযোগ করুন",
    "id": "Bot tidak memiliki izin untuk bekerja di grup ini, silakan hubungi administrator",
    "ru": "Бот не имеет разрешений для работы в этой группе, обратитесь к администратору",
    "ja": "ボットはこのグループで機能する権限がないため、管理者に連絡してください",
    "pa": "ਬੋਟ ਇਹ ਗ੍ਰੁਪ ਵਿੱਚ ਕੰਮ ਕਰਨ ਦਾ ਅਨੁਮਤੀ ਨਹੀਂ ਹੈ, ਮਾਰਚ ਦਾਤਾ ਨਾಲ ਸੰਪਰਕ ਕਰੋ",
    "de": "Der Bot hat keine Berechtigungen für die Arbeit in dieser Gruppe, kontaktieren Sie den Administrator",
}


choose_language = {
    "es": "Elige tu idioma",
    "en": "Choose your language",
    "ar": "اختر اللغة الخاصة بك",
    "pt": "Escolha o idioma de você",
    "bn": "আপনার ভাষা বাছাই করুন",
    "id": "Pilih bahasa Anda",
    "ru": "Выберите свой язык",
    "ja": "あなたの言語を選択してください",
    "pa": "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ",
    "de": "Wählen Sie Ihre Sprache",
}


not_group_sender = {
    "es": "No tienes permisos para cambiar el idioma de este grupo, por favor contacte al administrador",
    "en": "You do not have permissions to change the language of this group, please contact the administrator",
    "ar": "ليس لديك صلاحيات لتغيير اللغة في هذه المجموعة، يرجى الاتصال بالمسؤول",
    "pt": "Você não tem permissões para alterar o idioma deste grupo, por favor contate o administrador",
    "bn": "আপনি এই গ্রুপের ভাষা পরিবর্তন করতে অনুমতি নেই, অ্যাডমিনকে যোগাযোগ করুন",
    "id": "Anda tidak memiliki izin untuk mengubah bahasa grup ini, silakan hubungi administrator",
    "ru": "У вас нет разрешений для изменения языка в этой группе, обратитесь к администратору",
    "ja": "このグループの言語を変更する権限がありません、管理者に連絡してください",
    "pa": "ਤੁਸੀਂ ਇਹ ਗ੍ਰੁਪ ਦਾ ਭਾਸ਼ਾ ਬਦਲਣ ਦਾ ਅਨੁਮਤੀ ਨਹੀਂ ਹੈ, ਮਾਰਚ ਦਾਤਾ ਨਾਲ ਸੰਪਰਕ ਕਰੋ",
    "de": "Sie haben keine Berechtigungen, um die Sprache in dieser Gruppe zu ändern, kontaktieren Sie den Administrator",
}


language_changed = {
    "es": "El idioma del grupo ha sido cambiado a {language}",
    "en": "The language of the group has been changed to {language}",
    "ar": "تم تغيير اللغة في المجموعة إلى {language}",
    "pt": "O idioma do grupo foi alterado para {language}",
    "bn": "গ্রুপের ভাষা পরিবর্তিত হয়েছে {language}",
    "id": "Bahasa grup telah diubah ke {language}",
    "ru": "Язык группы изменен на {language}",
    "ja": "グループの言語が変更されました {language}",
    "pa": "ਗ੍ਰੁਪ ਦਾ ਭਾਸ਼ਾ ਬਦਲ ਗਿਆ ਹੈ {language}",
    "de": "Die Sprache der Gruppe wurde auf {language} geändert",
}

recipient_not_set_language = {  
    "es": "El usuario <a href='tg://user?id={user_id}'>{full_name}</a> no ha configurado el idioma, por favor pídele que lo configure",
    "en": "The user <a href='tg://user?id={user_id}'>{full_name}</a> has not set the language, please ask them to set it",
    "ar": "المستخدم <a href='tg://user?id={user_id}'>{full_name}</a> لم يحدد اللغة، يرجى أن تطلب منه تحديدها",
    "pt": "O usuário <a href='tg://user?id={user_id}'>{full_name}</a> não definiu o idioma, por favor peça para ele defini-lo",
    "bn": "ব্যক্তি <a href='tg://user?id={user_id}'>{full_name}</a> ভাষা নির্ধারণ করেননি, দয়া করে তাকে ভাষা নির্ধারণ করতে বলুন",
    "id": "Pengguna <a href='tg://user?id={user_id}'>{full_name}</a> belum mengatur bahasa, silakan minta dia untuk mengaturnya",
    "ru": "Пользователь <a href='tg://user?id={user_id}'>{full_name}</a> не установил язык, попросите его установить язык",
    "ja": "ユーザー <a href='tg://user?id={user_id}'>{full_name}</a> は言語を設定していません。言語を設定するよう依頼してください",
    "pa": "ਵਿਅਕਤੀ <a href='tg://user?id={user_id}'>{full_name}</a> ਨੇ ਭਾਸ਼ਾ ਸੈਟ ਨਹੀਂ ਕੀਤੀ, ਕਿਰਪਾ ਕਰਕੇ ਉਹਨਾਂ ਨੂੰ ਇਹ ਸੈਟ ਕਰਨ ਲਈ ਕਹੋ",
    "de": "Der Benutzer <a href='tg://user?id={user_id}'>{full_name}</a> hat keine Sprache eingestellt, bitte bitten Sie ihn, eine Sprache einzustellen",
}
