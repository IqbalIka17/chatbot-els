import streamlit as st
import google.generativeai as genai
import os

# ================================
# 1. MUAT DATA TOKO
# ================================
def load_store_data_txt(file_path="store_data.txt"):
    if not os.path.exists(file_path):
        st.error(f"File {file_path} tidak ditemukan.")
        st.stop()
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

STORE_INFO = load_store_data_txt()


# ================================
# 2. KONFIG GEMINI
# ================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")


# ================================
# 3. STYLE CHAT (iMessage)
# ================================
st.markdown("""
<style>

body {
    background-color: #ffffff;
}

.chat-container {
    max-width: 650px;
    margin: auto;
}

.user-bubble {
    background-color: #007AFF;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px;
    max-width: 80%;
    text-align: right;
    margin-left: auto;
    font-size: 16px;
    line-height: 1.4;
}

.bot-bubble {
    background-color: #E5E5EA;
    color: black;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px;
    max-width: 80%;
    text-align: left;
    margin-right: auto;
    font-size: 16px;
    line-height: 1.4;
}

</style>
""", unsafe_allow_html=True)


# ================================
# 4. FUNSI CHAT
# ================================
def ask_gemini(user_msg):
    prompt = f"""
Kamu adalah chatbot Customer Service untuk toko laptop ASUS bernama ELS.ID.

Gunakan informasi berikut untuk menjawab semua pertanyaan:
{STORE_INFO}

Aturan:
- Jawab dengan bahasa Indonesia yang ramah.
- Berikan info harga, stok, spek, rekomendasi bila diminta.
- Jangan gunakan Markdown, tidak boleh ** ** dan tidak boleh bullet *.
- Jika produk tidak ada di daftar, jawab tidak tersedia.
- Jangan pernah keluar dari konteks data toko.

Pertanyaan pengguna:
{user_msg}
"""

    response = model.generate_content(prompt)
    return response.text.strip()


# ================================
# 5. HISTORY CHAT
# ================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "msg": "Halo! Ada yang bisa saya bantu hari ini? 😊"}
    ]


# ================================
# 6. HEADER
# ================================
st.title("🖥️ ELSBOT - Customer Service Laptop ASUS Semarang")
st.write("Selamat datang! Saya siap membantu Anda 😊")

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)


# ================================
# 7. TAMPILKAN CHAT HISTORY
# ================================
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{chat['msg']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{chat['msg']}</div>", unsafe_allow_html=True)


# ================================
# 8. INPUT USER (BUBBLE)
# ================================
user_input = st.chat_input("Ketik pesan Anda...")

if user_input:
    # Simpan pesan user
    st.session_state.chat_history.append({"role": "user", "msg": user_input})

    # Balasan bot
    reply = ask_gemini(user_input)
    st.session_state.chat_history.append({"role": "bot", "msg": reply})

    st.rerun()


st.markdown("</div>", unsafe_allow_html=True)
