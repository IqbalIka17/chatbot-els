import streamlit as st
import google.generativeai as genai
import os

# --------------------------
# CSS Messages
# --------------------------
def apply_chat_css():
    st.markdown("""
    <style>

    body {
        background-color: #ffffff;
    }

    .chat-container {
        max-width: 600px;
        margin: auto;
    }

    .user-bubble {
        background-color: #007AFF;
        color: white;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px;
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
        margin: 8px;
        max-width: 80%;
        text-align: left;
        margin-right: auto;
        font-size: 16px;
        line-height: 1.4;
    }

    </style>
    """, unsafe_allow_html=True)



# --------------------------
# Load Store Info
# --------------------------
def load_store_data_txt(file_path="store_data.txt"):
    if not os.path.exists(file_path):
        st.error(f"File {file_path} tidak ditemukan.")
        st.stop()
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------
# Initialize Gemini Model
# --------------------------
def initialize_gemini(store_txt="store_data.txt"):
    api_key = st.secrets["GEMINI_API_KEY"]   # <-- AMBIL DARI STREAMLIT SECRETS
    genai.configure(api_key=api_key)

    store_info = load_store_data_txt(store_txt)

    system_prompt = f"""
    Kamu adalah chatbot Customer Service untuk toko laptop.

    Gunakan informasi berikut saat menjawab pertanyaan user:

    {store_info}

    Aturan Respon:
    - Jawab dengan ramah dan profesional.
    - Berikan produk yang ada di daftar katalog saja.
    - Jika ditanya harga: berikan harga tertera.
    - Jika ditanya stok: jawab bahwa stok biasanya tersedia, tapi harus dicek.
    - Selalu tawarkan bantuan di akhir chat.
    """

    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=system_prompt
    )
    return model


# --------------------------
# Chat Function
# --------------------------
def chat_with_gemini(model, prompt):
    response = model.generate_content(prompt)
    return response.text.strip()


# --------------------------
# Streamlit UI
# --------------------------
def main():
    st.set_page_config(
        page_title="ELSBOT - Customer Service",
        page_icon="💻",
        layout="centered",
    )

    apply_chat_css()

    st.title("🖥️ ELSBOT - Customer Service Laptop ASUS Semarang")
    st.write("Selamat datang! Saya siap membantu Anda 😊")

    st.divider()

    # Load model once
    if "model" not in st.session_state:
        st.session_state.model = initialize_gemini("store_data.txt")

    # Prepare chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Ada yang bisa saya bantu hari ini? 😊"}
        ]

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])
        else:
            st.chat_message("user").write(msg["content"])

    # Input box
    user_input = st.chat_input("Ketik pesan Anda di sini...")

    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Generate reply
        reply = chat_with_gemini(st.session_state.model, user_input)

        # Add assistant reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)


if __name__ == "__main__":
    main()
