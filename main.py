import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DEL SISTEMA Y LOGS
# ==========================================
logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("System_Core")

TOKEN = "8881399062:AAGnfsW0ITpj0VvFD4B84Jd8FlY77-9RXMI"
OWNER_ID = 7262260763
WHATSAPP = "https://wa.me/525551761906"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ==========================================
# SIMULACIÓN DE BASE DE DATOS / ESTADOS
# ==========================================
class UserManager:
    def __init__(self):
        self.users = {}

    def register_user(self, user_id, username, first_name):
        if user_id not in self.users:
            self.users[user_id] = {
                "username": username,
                "name": first_name,
                "status": "🔴 Free",
                "joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            logger.info(f"Nuevo usuario registrado: {first_name} (@{username}) - ID: {user_id}")
        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id, None)

db = UserManager()

# ==========================================
# GENERADORES DE INTERFAZ (TECLADOS)
# ==========================================
class Interfaces:
    
    @staticmethod
    def premium_menu():
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("💎 ADQUIRIR ACCESO PREMIUM", url=WHATSAPP),
            InlineKeyboardButton("⬅️ Retornar al Panel Central", callback_data="menu")
        )
        return kb

    @staticmethod
    def main_menu():
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("🏛️ ACTAS", callback_data="actas"),
            InlineKeyboardButton("🏥 IMSS", callback_data="imss")
        )
        kb.add(
            InlineKeyboardButton("🏠 INFONAVIT", callback_data="infonavit"),
            InlineKeyboardButton("🏢 SAT", callback_data="sat")
        )
        kb.add(
            InlineKeyboardButton("🚗 VEHÍCULOS", callback_data="vehiculos"),
            InlineKeyboardButton("💳 AFORES", callback_data="afores")
        )
        kb.add(
            InlineKeyboardButton("🔎 OTROS", callback_data="otros")
        )
        kb.add(
            InlineKeyboardButton("🛡️ MI PERFIL", callback_data="perfil")
        )
        return kb

    @staticmethod
    def generate_submenu(botones):
        kb = InlineKeyboardMarkup(row_width=1)
        for b in botones:
            kb.add(InlineKeyboardButton(b, callback_data="premium_lock"))
        kb.add(InlineKeyboardButton("⬅️ Volver al Menú Principal", callback_data="menu"))
        return kb

# ==========================================
# CATÁLOGO DE SERVICIOS
# ==========================================
MENU_ITEMS = {
    "actas": [
        "💠 ACTA NACIMIENTO",
        "💠 ACTA NACIMIENTO FOLIADA",
        "💠 ACTA NACIMIENTO CADENA",
        "💠 ACTA MATRIMONIO",
        "💠 ACTA DEFUNCIÓN",
        "💠 ACTA DIVORCIO"
    ],
    "imss": [
        "💠 SEMANAS COTIZADAS IMSS",
        "💠 VIGENCIA DERECHOS IMSS",
        "💠 NO DERECHOHABIENTE IMSS",
        "💠 NÚMERO IMSS",
        "💠 ALTA IMSS"
    ],
    "infonavit": [
        "💠 INFONAVIT DESBLOQUEO",
        "💠 INFONAVIT RECUPERAR",
        "💠 INFONAVIT HISTÓRICO",
        "💠 INFONAVIT RESUMEN"
    ],
    "sat": [
        "💠 RFC CURP GENÉRICO",
        "💠 RFC IDCIF",
        "💠 RFC CONVERTIR CURP",
        "💠 RFC CONSTANCIA ORIGINAL",
        "💠 RFC CONSTANCIA 2QR"
    ],
    "vehiculos": [
        "💠 PERMISO GUERRERO",
        "💠 REPUVE",
        "💠 CFE RECIBO"
    ],
    "afores": [
        "💠 AFORE AZTECA",
        "💠 AFORE COPPEL",
        "💠 AFORE BANAMEX",
        "💠 AFORE XXI"
    ],
    "otros": [
        "💠 CURP",
        "💠 RENAPO",
        "💠 DATOS GENERALES"
    ]
}

# ==========================================
# UTILIDADES VISUALES
# ==========================================
def simulate_processing(call, target_text, target_markup):
    """Crea un efecto visual de procesamiento en la interfaz del usuario."""
    processing_texts = [
        "🔄 <i>Estableciendo conexión segura...</i>",
        "🔐 <i>Desencriptando catálogo de servicios...</i>"
    ]
    
    try:
        # Mostramos una animación breve
        bot.edit_message_text(
            processing_texts[0],
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML"
        )
        time.sleep(0.4)
        
        # Entregamos el menú final
        bot.edit_message_text(
            target_text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=target_markup,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error en la simulación visual: {e}")


# ==========================================
# RUTAS Y CONTROLADORES (HANDLERS)
# ==========================================
@bot.message_handler(commands=["start"])
def start_command(message):
    nombre = message.from_user.first_name
    username = message.from_user.username or "Desconocido"
    user_id = message.from_user.id

    # Registrar en nuestra base de datos simulada
    user_data = db.register_user(user_id, username, nombre)

    texto = f"""
<b>N4 STYLEE SERVICES | PORTAL CENTRAL</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

Saludos, <b>{nombre}</b>. Bienvenido al sistema avanzado de gestión y consulta digital.

<b>👤 PANEL DE USUARIO:</b>
├ <b>ID de Red:</b> <code>{user_id}</code>
├ <b>Alias:</b> @{username}
└ <b>Estado de Membresía:</b> {user_data['status']}

🛡️ <i>Seleccione una bóveda de datos en el menú inferior para proceder. Tenga en cuenta que la extracción de información requiere credenciales de acceso.</i>
"""

    bot.send_message(
        message.chat.id,
        texto,
        reply_markup=Interfaces.main_menu()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_dispatcher(call):
    
    # --- MENÚ PRINCIPAL ---
    if call.data == "menu":
        texto_menu = "<b>📂 PORTAL CENTRAL ORIONXN</b>\n\nSeleccione la categoría de servicio que desea consultar:"
        simulate_processing(call, texto_menu, Interfaces.main_menu())

    # --- PERFIL DEL USUARIO ---
    elif call.data == "perfil":
        user_data = db.get_user(call.from_user.id)
        if not user_data:
            user_data = db.register_user(call.from_user.id, call.from_user.username, call.from_user.first_name)
            
        texto_perfil = f"""
<b>🛡️ CENTRO DE CONTROL | MI PERFIL</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 <b>Titular:</b> {user_data['name']}
🆔 <b>Identificador:</b> <code>{call.from_user.id}</code>
📅 <b>Fecha de Registro:</b> {user_data['joined']}

💳 <b>NIVEL DE ACCESO:</b> {user_data['status']}

<i>Su cuenta actual posee restricciones de lectura. Para visualizar y solicitar documentos, es imperativo actualizar al rango Premium.</i>
"""
        # Botón para volver
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("⬅️ Volver al Portal", callback_data="menu"))
        
        bot.edit_message_text(
            texto_perfil,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=kb,
            parse_mode="HTML"
        )

    # --- CATEGORÍAS DE SERVICIOS ---
    elif call.data in MENU_ITEMS:
        categoria = call.data.upper()
        texto_cat = f"<b>📂 BÓVEDA DE DATOS: {categoria}</b>\n\nSeleccione el documento específico:"
        kb_cat = Interfaces.generate_submenu(MENU_ITEMS[call.data])
        
        # Usamos el efecto visual solo para entrar a las categorías
        simulate_processing(call, texto_cat, kb_cat)

    # --- BLOQUEO PREMIUM (INTENTO DE COMPRA) ---
    elif call.data == "premium_lock":
        # Notificar al administrador en silencio
        try:
            nombre = call.from_user.first_name
            username = call.from_user.username or "Sin_Usuario"
            user_id = call.from_user.id

            alerta_admin = f"""
<b>🔔 ALERTA DE INTENTO DE ACCESO</b>

👤 <b>Usuario:</b> {nombre}
📌 <b>Alias:</b> @{username}
🆔 <b>ID:</b> <code>{user_id}</code>

El usuario intentó acceder a un documento restringido y recibió el bloqueo Premium. Posible cliente potencial.
"""
            bot.send_message(OWNER_ID, alerta_admin, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"No se pudo notificar al admin: {e}")

        # Mensaje para el usuario
        texto_bloqueo = """
<b>🛑 ACCESO RESTRINGIDO | PROTOCOLO DE SEGURIDAD</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

El documento solicitado se encuentra bajo encriptación. 

Se requiere una membresía <b>ORIONXN</b> activa para ejecutar esta consulta y procesar el trámite.

Contacte con la administración para elevar sus privilegios de cuenta.
"""
        bot.edit_message_text(
            texto_bloqueo,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=Interfaces.premium_menu(),
            parse_mode="HTML"
        )


# ==========================================
# INICIO DEL SERVIDOR BOT
# ==========================================
if __name__ == "__main__":
    logger.info("Inicializando protocolos de red...")
    logger.info("Bot ORIONXN conectado exitosamente a los servidores de Telegram.")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as err:
        logger.error(f"Falla crítica en el sistema de polling: {err}")
