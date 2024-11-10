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
async def handle_lihat_produk(update, context):
    try:
        # Mengonversi hasil query ke dalam list agar dapat diiterasi
        produk_list = await products_collection.find().to_list(length=None)

        # Melakukan iterasi pada produk_list
        for produk in produk_list:
            # Contoh, mencetak nama produk (pastikan field sesuai dengan yang ada di MongoDB)
            await update.message.reply_text(f"Nama Produk: {produk.get('nama')}\nHarga: {produk.get('harga')}")

    except Exception as e:
        # Memastikan bahwa reply_text hanya dipanggil jika update.message tidak None
        if update.message:
            await update.message.reply_text("Terjadi kesalahan saat mengambil daftar produk. Silakan coba lagi nanti.")
        else:
            print("Error: update.message tidak ditemukan.")

        # Logging error untuk debugging
        print(f"Error: {e}")

# Fungsi untuk menampilkan detail produk yang dipilih
async def handle_produk_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    produk_id = query.data.split('_')[1]

    try:
        produk = products_collection.find_one({"_id": ObjectId(produk_id)})
        if produk:
            detail_produk = f"{produk['name']}\n\nDeskripsi: {produk['description']}\nHarga: Rp {produk['price']:,}\nStok: {produk['stock']} buah"
            keyboard = [
                [InlineKeyboardButton("Cara Pembelian", callback_data='cara_pembelian')],
                [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=detail_produk, reply_markup=reply_markup)
        else:
            await query.edit_message_text(text="Detail produk tidak ditemukan.")
    except Exception as e:
        await query.edit_message_text(text="Terjadi kesalahan saat mengambil detail produk. Silakan coba lagi nanti.")
        print(f"Error: {e}")

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