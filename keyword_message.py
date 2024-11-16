import random
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from database import products_collection
from handlers import show_options, handle_lihat_produk, handle_cara_pembelian, handle_cara_bayar

# Load responses from JSON
with open("responses.json", "r") as f:
    responses = json.load(f)

# Fungsi untuk menentukan sapaan berdasarkan waktu
def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Selamat pagi"
    elif 12 <= current_hour < 18:
        return "Selamat siang"
    else:
        return "Selamat malam"

# Fungsi rule untuk sapaan
async def greet_user(update, context):
    user_message = update.message.text.lower()
    greetings = ['halo', 'hi', 'selamat pagi', 'selamat siang', 'selamat malam', 'hey', 'hai']
    if any(greet in user_message for greet in greetings):
        greeting = get_greeting()
        await update.message.reply_text(f"{greeting} Latier! Selamat datang di Latitaka Borneo. Apa yang bisa kami bantu hari ini?")
        await show_options(update, context)
        return True
    return False

# Fungsi rule untuk produk
async def show_products(update, context):
    user_message = update.message.text.lower()
    if any(term in user_message for term in ['produk', 'daftar produk', 'lihat produk', 'tampilkan produk']):
        await handle_lihat_produk(update, context)
        return True
    return False

# Fungsi rule untuk cara pembelian
async def show_purchase_method(update, context):
    user_message = update.message.text.lower()
    keywords = ['cara beli', 'beli', 'pembelian', 'pesan', 'order', 'pemesanan', 'cara order', 'cara pesan']
    if any(keyword in user_message for keyword in keywords):
        await handle_cara_pembelian(update, context)
        return True
    return False

# Fungsi rule untuk cara pembayaran
async def show_payment_method(update, context):
    user_message = update.message.text.lower()
    keywords = ['cara bayar', 'bayar', 'metode pembayaran', 'transfer', 'pembayaran', 'rekening', 'cara membayar']
    if any(keyword in user_message for keyword in keywords):
        await handle_cara_bayar(update, context)
        return True
    return False

# Fungsi rule untuk produk spesifik dan manfaatnya
async def show_specific_product(update, context):
    user_message = update.message.text.lower()
    matched_product = None

    # Mencari produk dalam user_message yang sesuai dengan yang ada di responses.json
    for product in responses.keys():
        if product in user_message:
            matched_product = product
            break

    if matched_product:
        # Ambil deskripsi produk, manfaat, dan cara pengolahan
        product_description = responses[matched_product].get("description")
        product_benefits = responses[matched_product].get("manfaat")
        product_processing = responses[matched_product].get("cara pengolahan")

        # Jika user bertanya tentang manfaat
        if 'manfaat' in user_message or 'khasiat' in user_message:
            if isinstance(product_benefits, list) and product_benefits:
                # Kirim manfaat produk secara acak
                response = random.choice(product_benefits)
                await update.message.reply_text(response)
            else:
                await update.message.reply_text(f"Maaf, manfaat untuk {matched_product} belum tersedia.")
        elif 'cara pengolahan' in user_message or 'pengolahan' in user_message:
            if isinstance(product_processing, list) and product_processing:
                # Kirim cara pengolahan produk secara acak
                response = random.choice(product_processing)
                await update.message.reply_text(response)
            elif isinstance(product_processing, str) and product_processing:
                # Jika pengolahan hanya berupa string, kirim langsung
                await update.message.reply_text(product_processing)
            else:
                await update.message.reply_text(f"Maaf, cara pengolahan untuk {matched_product} belum tersedia.")
        else:
            # Jika tidak ada pertanyaan tentang manfaat atau cara pengolahan, kirim deskripsi produk
            if isinstance(product_description, list) and product_description:
                response = random.choice(product_description)
                await update.message.reply_text(response)
            elif isinstance(product_description, str) and product_description:
                await update.message.reply_text(product_description)
            else:
                await update.message.reply_text(f"Maaf, informasi lebih lanjut tentang {matched_product} belum tersedia.")
    else:
        await update.message.reply_text("Maaf, produk yang Anda cari tidak ditemukan.")
    return matched_product is not None

# Fungsi rule untuk ucapan terima kasih
async def respond_to_thanks(update, context):
    user_message = update.message.text.lower()
    thanks_terms = ['terima kasih', 'makasih', 'thank you']
    if any(term in user_message for term in thanks_terms):
        await update.message.reply_text("Sama-sama, Latier! Jika ada pertanyaan lain, jangan ragu untuk bertanya.")
        return True
    return False

# Fungsi utama yang menjalankan semua rule secara berurutan
async def handle_message(update, context):

    if await respond_to_thanks(update, context):
        return
    # Cek untuk pesan sapaan
    if await greet_user(update, context):
        return
    # Cek untuk melihat produk
    if await show_products(update, context):
        return
    # Cek untuk cara pembelian
    if await show_purchase_method(update, context):
        return
    # Cek untuk cara pembayaran
    if await show_payment_method(update, context):
        return
    # Cek untuk produk spesifik
    if await show_specific_product(update, context):
        return

    # Jika tidak ada aturan yang cocok, beri balasan umum
    await update.message.reply_text("Maaf, saya tidak mengerti. Apakah Anda ingin tahu tentang produk lain atau ada pertanyaan lainnya?")
    await show_options(update, context)