from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bson import ObjectId
from database import products_collection
from constants import cara_bayar, cara_pembelian

# Fungsi untuk menampilkan opsi awal kepada pengguna
async def show_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Lihat Produk", callback_data='lihat_produk')],
        [InlineKeyboardButton("Cara Pembayaran", callback_data='cara_bayar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)

# Fungsi untuk kembali ke menu utama
async def handle_kembali_ke_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Lihat Produk", callback_data='lihat_produk')],
        [InlineKeyboardButton("Cara Pembayaran", callback_data='cara_bayar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    await query.answer()
    await query.edit_message_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)

# Fungsi untuk menampilkan daftar produk dari MongoDB
async def handle_lihat_produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received update: {update}")  # Menambahkan log untuk melihat update yang diterima
    if update.message:
        # Ambil produk dari MongoDB dengan async query
        try:
            produk_cursor = products_collection.find()  # Ini adalah AsyncIOMotorCursor
            produk_list = await produk_cursor.to_list(length=None)  # Convert cursor ke list

            if produk_list:
                # Kirim pesan dengan daftar produk
                produk_names = [produk['nama'] for produk in produk_list]  # Ambil nama produk dari daftar
                produk_text = "\n".join(produk_names)
                await update.message.reply_text(f"Berikut daftar produk kami:\n{produk_text}")
            else:
                await update.message.reply_text("Maaf, tidak ada produk yang tersedia.")
        except Exception as e:
            await update.message.reply_text("Terjadi kesalahan saat mengambil daftar produk. Silakan coba lagi nanti.")
            print(f"Error: {e}")
    else:
        print("Error: Tidak ada pesan yang diterima.")


# Fungsi untuk menampilkan detail produk yang dipilih
async def handle_lihat_produk(update: Update, context: CallbackContext):
    # Cek apakah update adalah callback_query
    if update.callback_query:
        # Log callback query untuk debugging
        print(f"Received callback query: {update.callback_query.data}")

        # Pastikan bahwa data callback_query adalah 'lihat_produk'
        if update.callback_query.data == 'lihat_produk':
            try:
                # Ambil produk dari MongoDB dengan async query
                produk_cursor = products_collection.find()  # AsyncIOMotorCursor
                produk_list = await produk_cursor.to_list(length=None)  # Convert cursor ke list

                if produk_list:
                    # Kirim pesan dengan daftar produk
                    produk_names = [produk['nama'] for produk in produk_list]  # Ambil nama produk
                    produk_text = "\n".join(produk_names)
                    await update.callback_query.message.reply_text(f"Berikut daftar produk kami:\n{produk_text}")
                else:
                    await update.callback_query.message.reply_text("Maaf, tidak ada produk yang tersedia.")
            except Exception as e:
                await update.callback_query.message.reply_text("Terjadi kesalahan saat mengambil daftar produk. Silakan coba lagi nanti.")
                print(f"Error: {e}")

            # Menghindari bot untuk mengulang respons callback dengan 'answer_callback_query'
            await update.callback_query.answer()

        else:
            await update.callback_query.answer("Opsi yang dipilih tidak dikenali.")

# Fungsi untuk menampilkan cara pembayaran
async def handle_cara_bayar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=cara_bayar, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text=cara_bayar, reply_markup=reply_markup)

# Fungsi untuk menampilkan cara pembelian
async def handle_cara_pembelian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=cara_pembelian, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text=cara_pembelian, reply_markup=reply_markup)

# Memastikan callback_query diproses dengan benar
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu_utama':
        await handle_kembali_ke_menu(update, context)
    elif query.data == 'lihat_produk':
        await handle_lihat_produk(update, context)
    elif query.data.startswith('produk_'):
        await handle_produk_detail(update, context)
    elif query.data == 'cara_bayar':
        await handle_cara_bayar(update, context)
    elif query.data == 'cara_pembelian':
        await handle_cara_pembelian(update, context)