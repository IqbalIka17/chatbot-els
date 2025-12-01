import streamlit as st
import google.generativeai as genai
import os

# =======================================================
# 1. API KEY dari Streamlit Secrets
# =======================================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =======================================================
# 2. Load store info dari TXT
# =======================================================
def load_store():
    with open("store_data.txt", "r", encoding="utf-8") as f:
        return f.read()

STORE_INFO = load_store()

# =======================================================
# 3. Model Gemini dengan system prompt
# =======================================================
system_prompt = f"""
Kamu adalah chatbot Customer Service untuk toko laptop ASUS Semarang.

Gunakan informasi berikut saat menjawab:
{STORE_INFO}

Aturan:
- Jawab dengan ramah & profesional.
- Hanya gunakan data produk yang ada di daftar.
- Bila ditanya stok, jawab: stok normalnya tersedia, tapi harus dicek.
- Bila ditanya harga, gunakan harga di file.
- Jangan gunakan markdown.
"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=system_prompt
)

# =======================================================
# 4. CSS Custom (iMessage Style) + Avatar
# =======================================================
st.markdown("""
<style>

.chat-container {
    max-width: 700px;
    margin: auto;
}

.user-row, .bot-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}

.user-icon, .bot-icon {
    font-size: 28px;
    margin: 6px;
}

.user-bubble {
    background-color: #007AFF;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 75%;
    margin-left: auto;
    font-size: 16px;
    line-height: 1.4;
}

.bot-bubble {
    background-color: #E5E5EA;
    color: black;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 75%;
    margin-right: auto;
    font-size: 16px;
    line-height: 1.4;
}

</style>
""", unsafe_allow_html=True)

# =======================================================
# 5. Fungsi Chat
# =======================================================
def ask_model(user_msg):
    response = model.generate_content(user_msg)
    return response.text

# =======================================================
# 6. Session State untuk history
# =======================================================
if "history" not in st.session_state:
    st.session_state.history = [{"role": "bot", "msg": "Halo! Ada yang bisa saya bantu hari ini? 😊"}]

# =======================================================
# 7. UI Header
# =======================================================
st.title("🖥️ ELSBOT - Customer Service Laptop ASUS Semarang")
st.write("Selamat datang! Silakan tanya tentang produk 😊")

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# =======================================================
# 8. Tampilkan history chat
# =======================================================
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(
            f"""
            <div class='user-row'>
                <div class='user-icon'>👤</div>
                <div class='user-bubble'>{chat['msg']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class='bot-row'>
                <div class='bot-icon'>🤖</div>
                <div class='bot-bubble'>{chat['msg']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =======================================================
# 9. Input chat
# =======================================================
user_input = st.chat_input("Ketik pesan Anda...")

if user_input:
    # Simpan pesan user
    st.session_state.history.append({"role": "user", "msg": user_input})

    # Balasan bot
    reply = ask_model(user_input)
    st.session_state.history.append({"role": "bot", "msg": reply})

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
