import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler
from handlers import handle_callback_query
from keyword_message import handle_message
from handlers import (
    handle_lihat_produk,
    handle_produk_detail,
    handle_cara_bayar,
    handle_cara_pembelian,
    handle_kembali_ke_menu
)

# Load .env
load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')

if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_token).build()

    # Handler untuk pesan "halo" dan lain-lain
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Handler untuk tombol lihat produk
    callback_handler = CallbackQueryHandler(handle_lihat_produk, pattern='lihat_produk')
    application.add_handler(callback_handler)

    # Handler untuk tombol produk yang akan menampilkan detail produk
    application.add_handler(CallbackQueryHandler(handle_produk_detail, pattern='^produk_'))

    # Handler untuk cara pembayaran
    application.add_handler(CallbackQueryHandler(handle_cara_bayar, pattern='^cara_bayar$'))

    # Handler untuk cara pembelian
    application.add_handler(CallbackQueryHandler(handle_cara_pembelian, pattern='^cara_pembelian$'))

    # Handler untuk kembali ke menu utama
    application.add_handler(CallbackQueryHandler(handle_kembali_ke_menu, pattern='^menu_utama$'))

    # Tambahkan handler untuk callback_query
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Menjalankan bot
    application.run_polling()