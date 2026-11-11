import os
import sys
import time
import json
import datetime
import requests
import re
from flask import Flask
from threading import Thread

# ==========================================
# ⚠️ الإعدادات الأساسية ⚠️
# ==========================================
TOKEN = "8249734110:AAHYupUxO35v-g43OXBspBBfYny7o12JnIc"
ADMIN_ID = 7527980889 
CHANNEL_ID = "True" 
CHANNEL_URL = "https://t.me/+3mFJy_Km72cxYWI0" 
SUPPORT_URL = "https://t.me/blak_st" 
EXCHANGE_RATE = 150 

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
USERS_FILE = "store_users.json"
STORE_FILE = "store_data_v29.json" 

ADMIN_STATES = {}
USER_STATES = {}
BOT_ACTIVE = True 
BOT_USERNAME = "YourBotUsername" 

# ==========================================
# 🌐 قاموس الترجمة (AR / EN)
# ==========================================
T = {
    "ar": {
        "choose_lang": "🌐 يرجى اختيار اللغة:\nPlease choose your language:",
        "welcome": "☠️ **أهلاً بك في BLACK STORE**\n\n> النظام جاهز...\n> اختر أداة الاختراق:",
        "btn_lang": "[ 🌐 English ]",
        "btn_wallet": "[ 👛 محفظتي ]",
        "btn_support": "[ 💬 الدعم الفني ]",
        "btn_search": "[ 🔍 بحث ]",
        "btn_ref": "[ 🎁 رابط الإحالة ]",
        "btn_pay": "[ 💳 شحن رصيد ]",
        "btn_admin": "[ ⚙️ لوحة تحكم المدير ]",
        "btn_status": "[ 🟢 حالة النظام ]",
        "btn_back": "🔙 العودة",
        "btn_buy": "💸 شراء الآن",
        "btn_home": "🏠 الرئيسية",
        "choose_pay": "💳 **اختر طريقة الدفع التي تريدها:**",
        "pay_syriatel": "💵 سيراتيل كاش",
        "pay_usdt": "🪙 USDT (SOON)",
        "pay_usdt_msg": "🪙 **USDT**\n\n(SOON)\n\nسيتم إضافة هذه الطريقة قريباً.",
        "wallet_info": "> **[ النظام متصل... ]**\n\n👤 **الرتبة:** {}\n💰 **الرصيد:** {}\n📉 **المصروف:** {}\n\n💵 *سعر الصرف: 150 ل.س*",
        "support_msg": "💬 للتواصل مع الإدارة:\n@blak_st",
        "ref_msg": "🎁 **رابط الاختراق الخاص بك:**\n`{}`",
        "out_of_stock": "❌ نفد من المخزن.",
        "no_balance": "❌ رصيدك غير كافٍ.\nرصيدك: {}\nالسعر: {}",
        "purchase_ok": "✅ **[ تم استلام طلبك بنجاح ]**\n\n📦 الخدمة: {}\n💵 المدفوع: {}\n\n🔑 **الكود الخاص بك:**\n\n{}",
        "send_file": "📁 جاري إرسال الملف المطلوب...",
        "choose_admin": "⚙️ لوحة التحكم:",
        "admin_add_sec": "➕ إضافة قسم",
        "admin_add_prod": "📦 إضافة منتج",
        "admin_users": "👤 إدارة العملاء",
        "admin_stats": "👥 سجل الدخول",
        "admin_fin": "📊 الأرباح",
        "admin_backup": "💾 نسخة احتياطية",
        "admin_pay_text": "📝 تعديل نص الدفع",
        "admin_pay_img": "🖼️ تعديل صورة الدفع",
        "admin_stop": "🔴 إيقاف النظام",
        "admin_start": "🟢 تشغيل النظام",
        "status_msg": "> **[ SYSTEM STATUS ]**\n\n🟢 جميع الأنظمة تعمل بكفاءة."
    },
    "en": {
        "choose_lang": "🌐 يرجى اختيار اللغة:\nPlease choose your language:",
        "welcome": "☠️ **Welcome to BLACK STORE**\n\n> System is ready...\n> Choose your tool:",
        "btn_lang": "[ 🌐 العربية ]",
        "btn_wallet": "[ 👛 My Wallet ]",
        "btn_support": "[ 💬 Support ]",
        "btn_search": "[ 🔍 Search ]",
        "btn_ref": "[ 🎁 Referral Link ]",
        "btn_pay": "[ 💳 Top-up ]",
        "btn_admin": "[ ⚙️ Admin Panel ]",
        "btn_status": "[ 🟢 System Status ]",
        "btn_back": "🔙 Back",
        "btn_buy": "💸 Buy Now",
        "btn_home": "🏠 Home",
        "choose_pay": "💳 **Choose payment method:**",
        "pay_syriatel": "💵 Syriatel Cash",
        "pay_usdt": "🪙 USDT (SOON)",
        "pay_usdt_msg": "🪙 **USDT**\n\n(SOON)\n\nThis method will be added soon.",
        "wallet_info": "> **[ System Connected... ]**\n\n👤 **Rank:** {}\n💰 **Balance:** {}\n📉 **Spent:** {}\n\n💵 *Exchange Rate: 150 SYP*",
        "support_msg": "💬 Contact Admin:\n@blak_st",
        "ref_msg": "🎁 **Your Referral Link:**\n`{}`",
        "out_of_stock": "❌ Out of stock.",
        "no_balance": "❌ Insufficient balance.\nYour balance: {}\nPrice: {}",
        "purchase_ok": "✅ **[ Purchase Successful ]**\n\n📦 Product: {}\n💵 Paid: {}\n\n🔑 **Your Code:**\n\n{}",
        "send_file": "📁 Sending file...",
        "choose_admin": "⚙️ Admin Panel:",
        "admin_add_sec": "➕ Add Section",
        "admin_add_prod": "📦 Add Product",
        "admin_users": "👤 Manage Users",
        "admin_stats": "👥 Login Log",
        "admin_fin": "📊 Revenue",
        "admin_backup": "💾 Backup",
        "admin_pay_text": "📝 Edit Payment Text",
        "admin_pay_img": "🖼️ Edit Payment Image",
        "admin_stop": "🔴 Stop System",
        "admin_start": "🟢 Start System",
        "status_msg": "> **[ SYSTEM STATUS ]**\n\n🟢 All systems operational."
    }
}

# ==========================================
# ⚠️ المتجر الشامل ⚠️
# ==========================================
DEFAULT_STORE = {
    "sections": {
        "best": {"name": "🔥 الأكثر مبيعاً", "products": ["v1", "v2", "v3", "v4", "w1", "w2"]},
        "phone_viruses": {"name": "🦠 فيروسات الهاتف", "products": ["v1", "v2", "v3", "v4"]},
        "format_files": {"name": "🧹 ملفات فرمطة", "products": []},
        "whatsapp": {"name": "💬 واتس اب", "products": ["w1", "w2", "w3", "w4", "w5", "w6", "w7"]}
    },
    "products": {
        "v1": {"name": "فيروس شلل 🐍🥱", "price": 5.0, "desc": "شلل وتجميد لجميع أنظمة التشغيل.", "stock": ["FILE_ID:BQACAgQAAxkBAAO_avH2sIXb6mBUi5rf_OkL3TtbJTkAApEIAIRh5BTTXUI7cGtrPY9BA"], "sales_count": 0},
        "v2": {"name": "فيروس هواتف ضار💀", "price": 5.0, "desc": "⌯ فيروس هواتف.\n⌯ شكل تطبيق انستا.\n⌯ لاتثبته بل اقنع الضحيه يثبه.\n⌯ عمل التطبيق: بمجرد الضغط على login سيتم حذف جميع بيانات الهاتف.", "stock": ["تواصل مع الإدارة: @blak_st"], "sales_count": 0},
        "v3": {"name": "فيروس فرمتة هاتف 🧹", "price": 5.0, "desc": "ملف خبيث يقوم بفرمتة هاتف الضحية بالكامل ومسح جميع البيانات بمجرد فتحه أو تثبيته.", "stock": ["تواصل مع الإدارة: @blak_st"], "sales_count": 0},
        "v4": {"name": "فيروس بوبجي موبايل 🎮", "price": 5.0, "desc": "⚠️ فايروس ؏ـلـى شكل لعبة ببجي موبايل مهكرة يقوم بفر ــمتت الهاتف ⚠️", "stock": ["تواصل مع الإدارة: @blak_st"], "sales_count": 0},
        "w1": {"name": "باند فنش نار بلاغين 😈", "price": 7.0, "desc": "بند فنش نار من بلاغين.", "stock": ["Sie können Ihren Computer mit Ihrem Computer verbinden συνεχώς και πώς τα αντιμετωπίζατε; Es ist nicht einfach, den Fehler zu beheben ούν έντονα το πουλί; Ich habe noch nie ein Buch gelesen, es ist nicht einfach, es zu tun 2000-1000 Tage, 2000-1000 Tage, 2000 bis 2000. Η διαδικασία είναι απλή (αν είσστε άνω των 22 ετών, πρέπει να εγγραφείτε στο ν ιστότοπότοπό μας) Παρακαλώ Σύνδεση μέσω WhatsApp: Εάν δεν σας πειράζει, εισαγάγετε πρ ώτα [1] και, στη συνέχεια, πατήστε παρατεταμένα τα παρακάτω στοιχεία επικοινωνω Weitere Informationen\n\n👇👇👇👇\nhttps://api.whatsapp.com/send?phone=+967"], "sales_count": 0},
        "w2": {"name": "فك التخمين 😈", "price": 6.0, "desc": "ثغره فك تخمين", "stock": ["ثغره فك تخمين\nجمـيلات الشـرڪة 🤺🖤\n\nsupport@support.whatsapp.com, android@support.whatsapp.com, smb@support.whatsapp.com, android_web@support.whatsapp.com, jan@whatsapp.com,press@whatsapp.com\n\nالمـوضوع🤺🖤\n\nУкраден, пропал, отгадайте, пожалуйста.\n\nالـڪـود 🤺🖤\n\nЗдравствуйте, команда поддержки WhatsApp Как будто моя учетная запись принадлежала компании WhatsApp, моя учетная запись была украдена, и когда я восстановил ее, я обнаружил, что она была украдена и исчезла. Пожалуйста, угадайте, какой у меня номер, и большое спасибо всем. кто видит, и моя группа цифровой поддержки (+994)"], "sales_count": 0},
        "w3": {"name": "باند فنش2025😈🦅", "price": 8.0, "desc": "باند فنش 2025 بأحدث الثغرات", "stock": ["Мир вам, отличная поддержка WhatsApp. Я отправляю вам это сообщение, потому что у меня есть номер человека, который распространяет коррупцию в WhatsApp и продает контрабанду, такую ​​как наркотики, гашиш и т. д. Он также насилует женщин в обмен на наркотики, а затем публикует порнографические видео в своих группах. Поэтому такое поведение нельзя терпеть. Необходимо принять все меры и быстро заблокировать номер от использования WhatsApp. Это номер ❌🚫👇\nhttps://api.whatsapp.com/send?phone=+"], "sales_count": 0},
        "w4": {"name": "فك باند مشدد😈", "price": 20.0, "desc": "كود فك حظر ارقام الواتساب ( فك مشدد )", "stock": ["جيميلات الدعم للواتساب \n\n\nandroid@whatsapp.com,\nandroid_web@support.whatsapp.com,\nsmb@support.whatsapp.com,\nandroid@support.whatsapp.com,\nsupport@whatsapp.com,\naccessibility@support.whatsapp.com,\nsmb_web@support.whatsapp.com,\nsmb-iphone@support.whatsapp.com,\niphone@support.whatsapp.com,\nwebclient_web@support.whatsapp.com,\niphone_web@support.whatsapp.com,\nbusinesscomplaints@support.whatsapp.com,\nsupport@support.whatsapp.com,\ngrievance_officer_wa@support.whatsapp.com,\n\n\nالموضوع \n\nXTB का व्हाट्सएप अकाउंट \"गलतफहमी\" के कारण गलत तरीके से निलंबित कर दिया गया था।\n\n\nالكود \n\n\nBem-vindo à maravilhosa empresa WhatsApp. Sou cliente de uma empresa de manutenção. Fui proibido de usar o WhatsApp oficial e não fiz nada que viole a política oficial do WhatsApp e trabalho online para o WhatsApp Business. Uso WhatsApp desde os 15 anos... tenho 30 e não recebi nada. Quando eu faço alguma coisa, esse grupo cancela mensagens falsas do WhatsApp e denuncia essas mensagens falsas. Eles usam versões não oficiais do WhatsApp e colocam meu número em um grupo interativo do WhatsApp e as pessoas denunciam meu número. número. Não fiz absolutamente nada e tudo o que está listado no meu número está relacionado ao meu trabalho em uma empresa de manutenção. Peço à grande empresa do WhatsApp e ao grande Sr. Mark que desbloqueiem meu número. Obrigado por apoiar a maravilhosa empresa WhatsApp. meu número é.\n\nترسل الكود بدون رقمك المحظور وبعدين علق الدعم لمدة 5 ساعات ورسل لهم رقمك المحظور برمز الدولة فقط (+) ويفتك باذن الله. لو ردو عليك ب طعن ترد عليهم بالكود دي برقمك المحظور \nBonjour l équipe d assistance WhatsApp, j ai des difficultés à me connecter. Je me suis connecté et j ai été confronté au problème du blocage de mon numéro par WhatsApp, mais je n ai rien fait pour bloquer mon numéro et je n ai rien fait qui viole les conditions d utilisation de WhatsApp. Veuillez lire mon cas et le envoyer au créateur de WhatsApp et résoudre le problème du blocage aléatoire des numéros sans aucune preuve. Il semble que votre système ait fonctionné contre moi, ou peut-être que des pirates informatiques utilisent des versions modifiées de WhatsApp dotées de boutons pour annuler les messages. Ces boutons affichent des messages et fournissent de faux rapports. Veuillez étudier mon sujet et le reconnaître avec tout le sérieux et l intérêt pour ce sujet et essayer d arrêter ces pirates informatiques et d empêcher la copie de WhatsApp. La modification viole vos conditions d utilisation. Veuillez débloquer mon numéro le plus tôt possible car j ai beaucoup de travail, je suis également médecin et j ai inventé une méthode de traitement qui profite aux patients hépatiques et j y ai enregistré les données mais en raison d une erreur ou d actions suspectes de leur part. pirates, mon numéro est bloqué. J ai de grands espoirs pour toi. Veuillez débloquer mon numéro pour que je puisse continuer. Mon travail consiste à fournir des traitements aux patients afin qu ils puissent aller mieux. J espère que mon numéro ne sera plus interdit, puni et que des mesures strictes seront prises contre ces pirates informatiques qui travaillent à utiliser ces choses pour nuire à la société. C est mon numéro (+967). Merci WhatsApp.\nلو ردو عليك ب التحلي بصبر ترسل الكود هاذا وكذه يتفك معاك عافيه عن الدعم ⚡️\n\nПожалуйста, не беспокойтесь об этом. אני משתמש בוואטסאפ הרשמי מאז 2012 Канун Нового года. Пожалуйста, не беспокойтесь об этом. Пожалуйста, не беспокойтесь об этом."], "sales_count": 0},
        "w5": {"name": "فك حظر باند ابا ـحي🔥", "price": 20.0, "desc": "ثغره فك حظر اباحي مضمون وربي فقط ترسل الثغرة من خمس جميلات جديدة والرقم ينفك خلال 10 دقائق", "stock": ["#تنبية الثغرات حق الفتح م تتوقف تجلس طول العمر م يجي واحد يكذب عليك ويقولك هذا الثغرة م توقف#\n\n\nالموضوع\nПожалуйста, деактивируйте мою учетную запись: +967777777777\n\nالرساله الكترونيه\n\nЗдравствуйте, пожалуйста, помогите мне. Я потерял свою личную карту, и у меня есть кое-что особенное в WhatsApp о банковских счетах и ​​личной информации.  Пожалуйста, удалите мою учетную запись или закройте мой номер WhatsApp.  Я потерял документ, подтверждающий право собственности на мой личный номер.  Пожалуйста, помогите немедленно: Это мой номер: +967777777777\n\nبعد مايردو عليك\nЗдравствуйте, служба поддержки WhatsApp, я украл свой телефон и прошу вас закрыть мою учетную запись, чтобы вор не нарушил условия вашего условного номера: +967777777777"], "sales_count": 0},
        "w6": {"name": "باند فك حظر انتهاك🔥", "price": 10.0, "desc": "فك الارقام الواتساب اذا رقمك محضور إنتهاك جرب هذا من خمسه جميلات رسله من خمسة جميلات جديدة والرقم ينفك خلال ساعه او نص ساعة مضمون وربي", "stock": ["مرحبآ فريق الدعم لقد قد تم حظر الرقم الخاص بي في الواتساب بدون سبب حيث انه أنا لم أنتهك ايا من سياسات وخصوصيات الواتساب وقام شخص يهدنني ان يقوم بحظر رقمي وقام هذا الشخص بتشغيل نسخه واتساب معدله وارسال صوره اباحيه وقام بعمل اعاده توجيه وهذا النسخه قامت بعمل ان انا الذي ارسل الصورة الاباحية وانا لم ارسل شئ قط ولقد قام هذا الشخص بعمل حظر وابلاغ لرقم الواتساب الخاص بي وقد حظر رقمي الواتساب وانا لم اقوم بعمل شئ أرجاء ازاله الحظر عن رقمي الواتساب لكي اتواصل مع اقربائي واصدقائي الرقم الخاص بي :967777777777+\n\n\n\n\n\nترسل هذا الرساله من خمس جميلات والرقم ينفك خلال ساعه وربي مضمون نار وربي"], "sales_count": 0},
        "w7": {"name": "ثغرة تبنيد حسبات غير مضمونة🔥", "price": 5.0, "desc": "الطريقه مش مضمون", "stock": ["ايميل الشركه :\n\nsupport@whatsapp.com\n\nالموضوع : مسروق /مفقود : الرجاء تعطيل حسابي +967\n\nوترسل علا طول ، بيوصل لـك رد من الشركه ترد لهم بالرقم بمفتاح الدوله بدون فواصل. مثلاً\n+967777777777\n\nهاكذا ترسل لهم الرقم 👆\n\n\nالطريقه مش مضمون"], "sales_count": 0}
    },
    "coupons": {},
    "settings": {
        "payment_text": "💳 **طرق الدفع المتاحة:**\n\n1️⃣ **سيرياتيل كاش:** `43920139`\n\n\n📌 **ملاحظة:**\nبعد إتمام التحويل، أرسل صورة الإشعار إلى المدير: @blak_st ليتم شحن رصيدك فوراً.\n\n⚠️ **بعد إرسال الصورة للمدير، سيتم شحن رصيدك فوراً.**",
        "payment_image": ""
    }
}

# --- سيرفر وهمي للاستضافة ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- دوال مساعدة ---
def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "settings" not in data: data["settings"] = default["settings"]
                if "payment_image" not in data["settings"]: data["settings"]["payment_image"] = ""
                return data
        except: pass
    return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def download_file_from_telegram(file_id, save_path):
    try:
        res = requests.get(BASE_URL + f"getFile?file_id={file_id}", timeout=10).json()
        if res.get("ok"):
            file_path = res["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            r = requests.get(file_url, timeout=15)
            with open(save_path, "wb") as f:
                f.write(r.content)
            return True
    except: pass
    return False

USERS = load_data(USERS_FILE, {})
STORE = load_data(STORE_FILE, DEFAULT_STORE)

def is_bot_open(): return True

def get_bot_username():
    global BOT_USERNAME
    try:
        res = requests.get(BASE_URL + "getMe", timeout=10).json()
        if res.get("ok"): BOT_USERNAME = res["result"]["username"]
    except: pass

def get_hacker_rank(spent):
    if spent >= 100: return "☠️ Zero-Day Legend"
    if spent >= 50: return "🕶️ Black Hat"
    if spent >= 20: return "💻 Script Kiddie"
    return "👶 Newbie"

def init_user(user_id, first_name="", username=""):
    user_id = str(user_id)
    if user_id not in USERS:
        USERS[user_id] = {
            "balance": 0.0, "spent": 0.0, "currency": "USD", 
            "purchases": [], "banned": False, "current_coupon": None,
            "invited": [], "used_referrals": 0, "lang": "ar", # اللغة الافتراضية
            "first_name": first_name, "username": username
        }
        save_data(USERS_FILE, USERS)
        send_message(ADMIN_ID, f"🔔 **[ اختراق جديد للنظام ]**\n👤 الهدف: {first_name}\n🆔 الآيدي: `{user_id}`")
    else:
        if "spent" not in USERS[user_id]: USERS[user_id]["spent"] = 0.0
        if "currency" not in USERS[user_id]: USERS[user_id]["currency"] = "USD"
        if "purchases" not in USERS[user_id]: USERS[user_id]["purchases"] = []
        if "current_coupon" not in USERS[user_id]: USERS[user_id]["current_coupon"] = None
        if "invited" not in USERS[user_id]: USERS[user_id]["invited"] = []
        if "used_referrals" not in USERS[user_id]: USERS[user_id]["used_referrals"] = 0
        if "lang" not in USERS[user_id]: USERS[user_id]["lang"] = "ar"
        if first_name: USERS[user_id]["first_name"] = first_name
        if username: USERS[user_id]["username"] = username

def format_currency(amount, currency):
    if currency == "SYP": return f"{int(amount * EXCHANGE_RATE)} ل.س"
    return f"{amount:.2f} $"

# --- دوال تلغرام ---
def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup: payload["reply_markup"] = reply_markup
    try: 
        res = requests.post(url, json=payload, timeout=10).json()
        if not res.get("ok"):
            payload.pop("parse_mode", None)
            requests.post(url, json=payload, timeout=10)
    except: pass

def send_photo(chat_id, photo_id, caption, reply_markup=None):
    if not photo_id:
        send_message(chat_id, caption, reply_markup)
        return
    url = BASE_URL + "sendPhoto"
    payload = {"chat_id": chat_id, "photo": photo_id, "caption": caption, "parse_mode": "Markdown"}
    if reply_markup: payload["reply_markup"] = reply_markup
    try:
        res = requests.post(url, json=payload, timeout=10).json()
        if not res.get("ok"):
            send_message(chat_id, caption, reply_markup)
    except:
        send_message(chat_id, caption, reply_markup)

def send_document(chat_id, doc_path_or_id, caption=""):
    url = BASE_URL + "sendDocument"
    if os.path.exists(doc_path_or_id):
        files = {'document': open(doc_path_or_id, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        try: requests.post(url, data=data, files=files, timeout=15)
        except: pass
    else:
        data = {'chat_id': chat_id, 'document': doc_path_or_id, 'caption': caption}
        try: requests.post(url, data=data, timeout=15)
        except: pass

def edit_message(chat_id, message_id, text, reply_markup=None):
    url = BASE_URL + "editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup: payload["reply_markup"] = reply_markup
    try: 
        res = requests.post(url, json=payload, timeout=10).json()
        if not res.get("ok"):
            payload.pop("parse_mode", None)
            requests.post(url, json=payload, timeout=10)
    except: pass

def answer_callback(callback_id, text="", show_alert=False):
    url = BASE_URL + "answerCallbackQuery"
    payload = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

# --- واجهات المستخدم ---
def get_lang_menu():
    return {"inline_keyboard": [
        [{"text": "🇸🇾 العربية", "callback_data": "lang_ar"}],
        [{"text": "🇬🇧 English", "callback_data": "lang_en"}]
    ]}

def get_reply_keyboard(user_id):
    lang = USERS.get(str(user_id), {}).get("lang", "ar")
    tr = T[lang]
    keyboard = []
    
    # الأقسام
    sections_buttons = [{"text": f"[ {sec['name']} ]"} for sid, sec in STORE.get("sections", {}).items() if sid != "best" or any(STORE["products"][p]["sales_count"] > 0 for p in sec["products"] if p in STORE["products"])]
    for i in range(0, len(sections_buttons), 2):
        keyboard.append(sections_buttons[i:i+2])
        
    keyboard.append([{"text": tr["btn_search"]}, {"text": tr["btn_wallet"]}])
    keyboard.append([{"text": tr["btn_pay"]}, {"text": tr["btn_support"]}])
    keyboard.append([{"text": tr["btn_ref"]}, {"text": tr["btn_lang"]}]) # زر تغيير اللغة
    
    if user_id == ADMIN_ID:
        keyboard.append([{"text": tr["btn_status"]}, {"text": tr["btn_admin"]}])
        
    return {"keyboard": keyboard, "resize_keyboard": True, "is_persistent": True}

def get_admin_menu(user_id):
    lang = USERS.get(str(user_id), {}).get("lang", "ar")
    tr = T[lang]
    toggle_text = tr["admin_stop"] if BOT_ACTIVE else tr["admin_start"]
    return {"inline_keyboard": [
        [{"text": tr["admin_add_sec"], "callback_data": "admin_add_sec"}, {"text": tr["admin_add_prod"], "callback_data": "admin_add_prod_secs"}],
        [{"text": tr["admin_users"], "callback_data": "admin_user_mgmt"}, {"text": tr["admin_stats"], "callback_data": "admin_stats"}],
        [{"text": tr["admin_fin"], "callback_data": "admin_fin_stats"}, {"text": tr["admin_backup"], "callback_data": "admin_backup"}],
        [{"text": tr["admin_pay_text"], "callback_data": "admin_edit_pay_text"}, {"text": tr["admin_pay_img"], "callback_data": "admin_edit_pay_img"}],
        [{"text": toggle_text, "callback_data": "admin_toggle_off" if BOT_ACTIVE else "admin_toggle_on"}]
    ]}

# --- باقي الوظائف ---
def get_section_products_menu(sec_id, user_id):
    lang = USERS.get(str(user_id), {}).get("lang", "ar")
    tr = T[lang]
    keyboard = []
    if sec_id == "best":
        all_prods = [(pid, p) for pid, p in STORE["products"].items() if p["sales_count"] > 0]
        if not all_prods: all_prods = list(STORE["products"].items())
        all_prods.sort(key=lambda x: x[1]["sales_count"], reverse=True)
        for pid, prod in all_prods[:5]:
            if len(prod["stock"]) > 0: keyboard.append([{"text": f"[+] {prod['name']} | {prod['price']}$", "callback_data": f"prod_{pid}"}])
    else:
        for pid in STORE["sections"][sec_id]["products"]:
            if pid in STORE["products"]:
                prod = STORE["products"][pid]
                stock_text = f"متوفر: {len(prod['stock'])}" if len(prod["stock"]) > 0 else "نفدت ❌"
                keyboard.append([{"text": f"[+] {prod['name']} | {prod['price']}$ | {stock_text}", "callback_data": f"prod_{pid}"}])
    
    keyboard.append([{"text": tr["btn_back"], "callback_data": "main_menu"}])
    return {"inline_keyboard": keyboard}

def get_product_menu(prod_id, sec_id, user_id):
    lang = USERS.get(str(user_id), {}).get("lang", "ar")
    tr = T[lang]
    prod = STORE["products"][prod_id]
    keyboard = []
    if len(prod["stock"]) > 0: keyboard.append([{"text": tr["btn_buy"], "callback_data": f"confirm_buy_{prod_id}"}])
    keyboard.append([{"text": tr["btn_back"], "callback_data": f"sec_{sec_id}"}])
    return {"inline_keyboard": keyboard}

def process_buy(chat_id, user_id, prod_id):
    lang = USERS.get(str(user_id), {}).get("lang", "ar")
    tr = T[lang]
    try:
        user_id = str(user_id)
        init_user(user_id)
        prod = STORE["products"][prod_id]
        
        if len(prod["stock"]) == 0:
            send_message(chat_id, tr["out_of_stock"]); return
            
        final_price = prod["price"]
        if USERS[user_id]["balance"] < final_price:
            cur = USERS[user_id]["currency"]
            send_message(chat_id, tr["no_balance"].format(format_currency(USERS[user_id]['balance'], cur), format_currency(final_price, cur)))
            return
            
        product_code = prod["stock"][0]
        USERS[user_id]["balance"] -= final_price
        USERS[user_id]["spent"] += final_price
        USERS[user_id]["purchases"].append({"item": prod["name"], "code": product_code})
        prod["sales_count"] += 1
        
        if not product_code.startswith("FILE_ID:"): prod["stock"].pop(0)
            
        save_data(USERS_FILE, USERS)
        save_data(STORE_FILE, STORE)
        
        if product_code.startswith("FILE_ID:"):
            send_message(chat_id, tr["purchase_ok"].format(prod['name'], format_currency(final_price, "USD"), "") + "\n" + tr["send_file"])
            send_document(chat_id, product_code.replace("FILE_ID:", ""))
        else:
            send_message(chat_id, tr["purchase_ok"].format(prod['name'], format_currency(final_price, "USD"), product_code))
            
        send_message(ADMIN_ID, f"💰 **[ عملية شراء ]**\n👤 العميل: {USERS[user_id].get('first_name', 'مجهول')}\n📦 المنتج: {prod['name']}\n💵 المبلغ: {final_price:.2f} $")
        
    except Exception as e: print(f"BUY ERROR: {e}", flush=True)

def show_wallet(chat_id, user_id):
    user_id = str(user_id)
    lang = USERS.get(user_id, {}).get("lang", "ar")
    tr = T[lang]
    cur, bal, spent = USERS[user_id]["currency"], USERS[user_id]["balance"], USERS[user_id]["spent"]
    rank = get_hacker_rank(spent)
    
    text = tr["wallet_info"].format(rank, format_currency(bal, cur), format_currency(spent, cur))
    send_message(chat_id, text)

# --- الحلقة الرئيسية ---
def main_loop():
    global BOT_ACTIVE, USERS, STORE
    get_bot_username()
    print("البوت يعمل الآن... (24/7 | عربي/إنجليزي)", flush=True)
    
    last_update_id = None
    while True:
        try:
            print(".", end="", flush=True) 
            res = requests.get(BASE_URL + "getUpdates", params={"timeout": 20, "offset": last_update_id}, timeout=30).json()
            if "result" in res:
                for update in res["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    try: 
                        user_obj = update.get("message", {}).get("from", {}) or update.get("callback_query", {}).get("from", {})
                        user_id = user_obj.get("id")
                        first_name = user_obj.get("first_name", "")
                        username = user_obj.get("username", "")
                        
                        if user_id: init_user(user_id, first_name, username)
                        
                        # استقبال الملفات من المدير
                        if user_id == ADMIN_ID and "document" in update.get("message", {}):
                            doc = update["message"]["document"]
                            if doc.get("file_name") in ["store_users.json", "store_data_v29.json"]:
                                if download_file_from_telegram(doc["file_id"], doc.get("file_name")):
                                    USERS = load_data(USERS_FILE, {})
                                    STORE = load_data(STORE_FILE, DEFAULT_STORE)
                                    send_message(user_id, "✅ **تم استعادة الملف بنجاح!**")
                            continue

                        if USERS.get(str(user_id), {}).get("banned") and user_id != ADMIN_ID:
                            continue

                        if not BOT_ACTIVE and user_id != ADMIN_ID:
                            if "message" in update: send_message(user_id, "⛔️ النظام تحت الصيانة / Maintenance.")
                            continue 

                        if "message" in update and "text" in update["message"]:
                            chat_id, text = update["message"]["chat"]["id"], update["message"]["text"]
                            lang = USERS.get(str(user_id), {}).get("lang", "ar")
                            tr = T[lang]
                            
                            if user_id == ADMIN_ID and user_id in ADMIN_STATES:
                                state = ADMIN_STATES[user_id]
                                if state == "WAIT_PAY_IMAGE":
                                    if "photo" in update["message"]:
                                        STORE["settings"]["payment_image"] = update["message"]["photo"][-1]["file_id"]
                                        save_data(STORE_FILE, STORE)
                                        del ADMIN_STATES[user_id]
                                        send_message(chat_id, "✅ **تم حفظ صورة الدفع بنجاح!**", get_admin_menu(user_id))
                                    else:
                                        del ADMIN_STATES[user_id]
                                        send_message(chat_id, "⚠️ تم إلغاء تعديل الصورة.")
                                elif state == "WAIT_PAY_TEXT":
                                    STORE["settings"]["payment_text"] = text
                                    save_data(STORE_FILE, STORE)
                                    del ADMIN_STATES[user_id]
                                    send_message(chat_id, "✅ **تم تحديث نص الدفع بنجاح!**", get_admin_menu(user_id))
                                elif state == "WAIT_SEC_NAME":
                                    STORE["sections"][f"sec_{int(time.time())}"] = {"name": text, "products": []}
                                    save_data(STORE_FILE, STORE)
                                    del ADMIN_STATES[user_id]
                                    send_message(chat_id, "✅ تم إضافة القسم.", get_reply_keyboard(user_id))
                                elif state.startswith("WAIT_PROD_"):
                                    sec_id = state.replace("WAIT_PROD_", "")
                                    parts = text.split("|")
                                    if len(parts) >= 4:
                                        try:
                                            prod_id = f"p_{int(time.time())}"
                                            STORE["products"][prod_id] = {"name": parts[0].strip(), "price": float(parts[1].strip()), "desc": parts[2].strip(), "stock": [parts[3].strip()], "sales_count": 0}
                                            STORE["sections"][sec_id]["products"].append(prod_id)
                                            save_data(STORE_FILE, STORE)
                                            del ADMIN_STATES[user_id]
                                            send_message(chat_id, "✅ تم إضافة المنتج بنجاح!", get_admin_menu(user_id))
                                        except Exception as err: send_message(chat_id, f"❌ خطأ: {err}")
                                elif state == "WAIT_BAN_ID":
                                    USERS[text.strip()]["banned"] = True; save_data(USERS_FILE, USERS); del ADMIN_STATES[user_id]; send_message(chat_id, "تم الحظر.", get_admin_menu(user_id))
                                elif state == "WAIT_UNBAN_ID":
                                    if text.strip() in USERS: USERS[text.strip()]["banned"] = False; save_data(USERS_FILE, USERS); send_message(chat_id, "تم فك الحظر.", get_admin_menu(user_id))
                                    del ADMIN_STATES[user_id]
                                elif state == "WAIT_ADD_BAL":
                                    try:
                                        parts = re.split(r'\s+', text.strip())
                                        if len(parts) == 2:
                                            target, amount = parts[0], float(parts[1])
                                            if target not in USERS: init_user(target)
                                            USERS[target]["balance"] += amount
                                            save_data(USERS_FILE, USERS)
                                            send_message(chat_id, f"✅ تمت إضافة {amount}$ لـ {target}.", get_admin_menu(user_id))
                                        del ADMIN_STATES[user_id]
                                    except Exception as e: send_message(chat_id, f"❌ خطأ: {e}"); del ADMIN_STATES[user_id]
                                elif state == "WAIT_DEDUCT_BAL":
                                    try:
                                        parts = re.split(r'\s+', text.strip())
                                        if len(parts) == 2:
                                            target, amount = parts[0], float(parts[1])
                                            if target in USERS:
                                                USERS[target]["balance"] = max(0, USERS[target]["balance"] - amount)
                                                save_data(USERS_FILE, USERS)
                                                send_message(chat_id, f"✅ تم سحب {amount}$ من {target}.", get_admin_menu(user_id))
                                        del ADMIN_STATES[user_id]
                                    except Exception as e: send_message(chat_id, f"❌ خطأ: {e}"); del ADMIN_STATES[user_id]
                                continue

                            if text.startswith("/start "):
                                referrer_id = text.split(" ")[1].strip()
                                if referrer_id != str(user_id) and str(user_id) not in USERS[referrer_id].get("invited", []):
                                    init_user(referrer_id)
                                    USERS[referrer_id]["invited"].append(str(user_id))
                                    save_data(USERS_FILE, USERS)
                                    send_message(referrer_id, f"🎉 **شخص جديد دخل عبر رابطك!**")
                                text = "/start"

                            # إذا كان المستخدم جديداً أو كتب /start لأول مرة
                            if text == "/start":
                                if "first_start" not in USERS[str(user_id)]:
                                    send_message(chat_id, T["ar"]["choose_lang"], get_lang_menu())
                                    USERS[str(user_id)]["first_start"] = True
                                    save_data(USERS_FILE, USERS)
                                else:
                                    send_message(chat_id, tr["welcome"], get_reply_keyboard(user_id))
                                continue

                            # الأزرار
                            if "محفظتي" in text or "Wallet" in text: show_wallet(chat_id, user_id); continue
                            elif "حالة النظام" in text or "Status" in text: send_message(chat_id, tr["status_msg"]); continue
                            elif "الدعم" in text or "Support" in text: send_message(chat_id, tr["support_msg"]); continue
                            elif "بحث" in text or "Search" in text: USER_STATES[user_id] = "WAIT_SEARCH"; send_message(chat_id, "🔍 Enter product name:"); continue
                            elif "رابط الإحالة" in text or "Referral" in text:
                                send_message(chat_id, tr["ref_msg"].format(f"https://t.me/{BOT_USERNAME}?start={user_id}")); continue
                            elif "تغيير اللغة" in text or "English" in text or "العربية" in text:
                                send_message(chat_id, T["ar"]["choose_lang"], get_lang_menu()); continue
                            elif "شحن رصيد" in text or "Top-up" in text or "طرق الدفع" in text:
                                kb = {"inline_keyboard": [[{"text": tr["pay_syriatel"], "callback_data": "pay_syriatel"}], [{"text": tr["pay_usdt"], "callback_data": "pay_usdt"}]]}
                                send_message(chat_id, tr["choose_pay"], kb); continue
                            elif "لوحة تحكم" in text or "Admin" in text and user_id == ADMIN_ID:
                                send_message(chat_id, tr["choose_admin"], get_admin_menu(user_id)); continue

                            # ✅ هنا تم إصلاح المشكلة: استقبال ضغطات أزرار الأقسام
                            for sid, sec in STORE.get("sections", {}).items():
                                # نتحقق من وجود اسم القسم داخل النص (لتجاهل الأقواس والإيموجي)
                                if sec['name'].split(' ', 1)[-1] in text:
                                    send_message(chat_id, f"📂 **{sec['name']}**", get_section_products_menu(sid, user_id))
                                    break

                            # البحث
                            if user_id in USER_STATES and USER_STATES[user_id] == "WAIT_SEARCH":
                                del USER_STATES[user_id]
                                found = [(pid, p) for pid, p in STORE["products"].items() if text.lower() in p["name"].lower()]
                                if found:
                                    kb = [[{"text": f"[+] {p['name']}", "callback_data": f"prod_{pid}"}] for pid, p in found]
                                    send_message(chat_id, "النتائج:", {"inline_keyboard": kb})
                                else: send_message(chat_id, "❌ لا توجد نتائج.")
                                continue

                        elif "callback_query" in update:
                            cb = update["callback_query"]
                            callback_id, chat_id, message_id, data = cb["id"], cb["message"]["chat"]["id"], cb["message"]["message_id"], cb["data"]
                            user_id = cb["from"]["id"]
                            lang = USERS.get(str(user_id), {}).get("lang", "ar")
                            tr = T[lang]

                            if data.startswith("lang_"):
                                answer_callback(callback_id)
                                new_lang = data.replace("lang_", "")
                                USERS[str(user_id)]["lang"] = new_lang
                                save_data(USERS_FILE, USERS)
                                edit_message(chat_id, message_id, T[new_lang]["welcome"])
                                send_message(chat_id, "✅", get_reply_keyboard(user_id))
                                continue

                            if data == "pay_syriatel":
                                answer_callback(callback_id)
                                pay_img = STORE.get("settings", {}).get("payment_image", "")
                                if pay_img: send_photo(chat_id, pay_img, STORE.get("settings", {}).get("payment_text", ""), {"inline_keyboard": [[{"text": tr["btn_back"], "callback_data": "pay_methods_menu"}]]})
                                else: send_message(chat_id, STORE.get("settings", {}).get("payment_text", ""), {"inline_keyboard": [[{"text": tr["btn_back"], "callback_data": "pay_methods_menu"}]]})
                                continue
                            elif data == "pay_usdt":
                                answer_callback(callback_id)
                                send_message(chat_id, tr["pay_usdt_msg"], {"inline_keyboard": [[{"text": tr["btn_back"], "callback_data": "pay_methods_menu"}]]})
                                continue
                            elif data == "pay_methods_menu":
                                answer_callback(callback_id)
                                kb = {"inline_keyboard": [[{"text": tr["pay_syriatel"], "callback_data": "pay_syriatel"}], [{"text": tr["pay_usdt"], "callback_data": "pay_usdt"}]]}
                                edit_message(chat_id, message_id, tr["choose_pay"], kb)
                                continue

                            # لوحة التحكم
                            if data == "admin_backup" and user_id == ADMIN_ID:
                                answer_callback(callback_id, "جاري الإرسال...")
                                send_document(chat_id, USERS_FILE, "المستخدمين")
                                send_document(chat_id, STORE_FILE, "المنتجات")
                                continue
                            elif data == "admin_edit_pay_text" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_PAY_TEXT"; edit_message(chat_id, message_id, "📝 أرسل النص الجديد:"); continue
                            elif data == "admin_edit_pay_img" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_PAY_IMAGE"; edit_message(chat_id, message_id, "🖼️ أرسل الصورة:"); continue
                            elif data == "admin_panel" and user_id == ADMIN_ID:
                                answer_callback(callback_id); edit_message(chat_id, message_id, "⚙️ لوحة التحكم:", get_admin_menu(user_id)); continue
                            elif data == "admin_fin_stats" and user_id == ADMIN_ID:
                                answer_callback(callback_id); send_message(chat_id, f"💰 الأرباح: {sum(u.get('spent', 0) for u in USERS.values()):.2f}$"); continue
                            elif data == "admin_stats" and user_id == ADMIN_ID:
                                answer_callback(callback_id)
                                last_50 = list(USERS.keys())[-50:]
                                txt = "👥 آخر 50 عضو:\n\n"
                                for i, u_id in enumerate(last_50, 1):
                                    txt += f"{i}. <a href='tg://user?id={u_id}'>{USERS[u_id].get('first_name','بدون')}</a> | <code>{u_id}</code>\n"
                                send_message(chat_id, txt, parse_mode="HTML"); continue
                            elif data == "admin_user_mgmt" and user_id == ADMIN_ID:
                                answer_callback(callback_id); edit_message(chat_id, message_id, "إدارة المستخدمين:", get_user_mgmt_menu()); continue
                            elif data == "admin_ban_user" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_BAN_ID"; send_message(chat_id, "أرسل ID:"); continue
                            elif data == "admin_unban_user" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_UNBAN_ID"; send_message(chat_id, "أرسل ID:"); continue
                            elif data == "admin_add_bal" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_ADD_BAL"; send_message(chat_id, "أرسل `ID المبلغ`:"); continue
                            elif data == "admin_deduct_bal" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_DEDUCT_BAL"; send_message(chat_id, "أرسل `ID المبلغ`:"); continue
                            elif data == "admin_add_sec" and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = "WAIT_SEC_NAME"; send_message(chat_id, "أرسل اسم القسم:"); continue
                            elif data == "admin_add_prod_secs" and user_id == ADMIN_ID:
                                answer_callback(callback_id)
                                kb = [[{"text": s["name"], "callback_data": f"admin_sel_{sid}"}] for sid, s in STORE["sections"].items()]
                                edit_message(chat_id, message_id, "اختر القسم:", {"inline_keyboard": kb}); continue
                            elif data.startswith("admin_sel_") and user_id == ADMIN_ID:
                                answer_callback(callback_id); ADMIN_STATES[user_id] = f"WAIT_PROD_{data.replace('admin_sel_', '')}"; send_message(chat_id, "أرسل: `الاسم | السعر | الوصف | الكود`"); continue
                            elif data == "admin_toggle_off" and user_id == ADMIN_ID:
                                BOT_ACTIVE = False; answer_callback(callback_id, "تم الإيقاف!"); edit_message(chat_id, message_id, "🔴 متوقف", get_admin_menu(user_id)); continue
                            elif data == "admin_toggle_on" and user_id == ADMIN_ID:
                                BOT_ACTIVE = True; answer_callback(callback_id, "تم التشغيل!"); edit_message(chat_id, message_id, "🟢 يعمل", get_admin_menu(user_id)); continue

                            # المتجر
                            if data == "main_menu":
                                answer_callback(callback_id); send_message(chat_id, "👇"); continue
                            elif data.startswith("sec_"):
                                answer_callback(callback_id); sec_id = data.replace("sec_", ""); edit_message(chat_id, message_id, f"📂 **{STORE['sections'][sec_id]['name']}**", get_section_products_menu(sec_id, user_id)); continue
                            elif data.startswith("prod_"):
                                answer_callback(callback_id); prod_id = data.replace("prod_", ""); prod = STORE["products"][prod_id]
                                current_sec = next((s for s, d in STORE["sections"].items() if prod_id in d["products"]), "best")
                                status = f"متوفر: {len(prod['stock'])}" if len(prod["stock"]) > 0 else "نفدت ❌"
                                edit_message(chat_id, message_id, f"📦 **{prod['name']}**\n\n📝 {prod['desc']}\n💵 {prod['price']}$\n📦 {status}", get_product_menu(prod_id, current_sec, user_id)); continue
                            elif data.startswith("confirm_buy_"):
                                prod_id = data.replace("confirm_buy_", ""); prod = STORE["products"][prod_id]
                                kb = {"inline_keyboard": [[{"text": "✅ تنفيذ", "callback_data": f"buy_{prod_id}"}], [{"text": "❌ إلغاء", "callback_data": f"prod_{prod_id}"}]]}
                                answer_callback(callback_id, "تأكيد الدفع", show_alert=True)
                                edit_message(chat_id, message_id, f"⚠️ هل أنت متأكد من شراء:\n{prod['name']}؟", kb); continue
                            elif data.startswith("buy_"):
                                answer_callback(callback_id, "جاري المعالجة...")
                                process_buy(chat_id, user_id, data.replace("buy_", ""))
                                continue
                                    
                    except Exception as inner_e: print(f"\nInner Loop Error: {inner_e}", flush=True); time.sleep(1)
        except Exception as outer_e: print(f"\nConnection Error: {outer_e}", flush=True); time.sleep(5)

if __name__ == '__main__':
    keep_alive() 
    main_loop()
