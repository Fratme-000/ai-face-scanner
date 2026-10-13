from PIL import Image
import google.generativeai as genai
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="AI Face Scanner & Glow-Up", page_icon="🤖", layout="centered"
)

# Stile CSS personalizzato per renderlo cyberpunk e professionale
st.markdown("""
    <style>
    .stButton>button {
        background: linear-gradient(45deg, #00E676, #00B0FF);
        color: black;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 24px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.85;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Neural Face Scanner & Glow-Up")
st.markdown(
    "Benvenuto nel sistema di scansione biometrica avanzata. Scatta una foto"
    " per avviare l'analisi neurale tramite **Google Gemini**."
)

# Configurazione chiave API integrata
with st.sidebar:
  st.subheader("⚙️ Configurazione")
  api_key = st.text_input(
      "Inserisci la tua Gemini API Key",
      value="AQ.Ab8RN6LltjHDrjBBd-vcF0ypwmAcWhxZSqWs4UuQDHEcH5A0IQ",
      type="password",
  )
  st.markdown(
      "[Ottieni una chiave gratuita su Google AI"
      " Studio](https://aistudio.google.com/)"
  )

# 1. Acquisizione foto tramite la webcam del dispositivo
camera_image = st.camera_input("📸 Scatta un selfie frontale")

if camera_image is not None:
  image = Image.open(camera_image)

  col1, col2 = st.columns([1, 1])
  with col1:
    st.image(image, caption="Foto acquisita", use_container_width=True)

  with col2:
    st.write("")
    st.write("")
    scan_button = st.button("🚀 Avvia Scansione Neurale")

  if scan_button:
    if not api_key:
      st.error(
          "⚠️ Inserisci la tua API Key di Google Gemini nella barra laterale"
          " per eseguire l'analisi dell'AI!"
      )
    else:
      # 2. Animazione di scansione professionale
      with st.status(
          "🔍 Inizializzazione scanner cibernetico...", expanded=True
      ) as status:
        st.write("Connessione sicura al cluster neurale di Gemini...")
        import time

        time.sleep(1)
        st.write("Mappatura geometrica dei punti di riferimento facciali...")
        time.sleep(1.2)
        st.write(
            "Elaborazione indice di simmetria, proporzioni e potenziale"
            " estetico..."
        )
        time.sleep(1.2)

        try:
          # Configurazione e chiamata a Google Gemini (Multimodale)
          genai.configure(api_key=api_key)
          model = genai.GenerativeModel("gemini-1.5-flash")

          prompt = (
              "Agisci come un sistema di scansione biometrica ed estetica"
              " avanzata di livello professionale. Adotta un tono leggermente"
              " cyberpunk, futuristico ma incredibilmente costruttivo,"
              " motivazionale e rispettoso. Analizza questa foto del viso e"
              " restituisci:\n1. Un punteggio di attrattiva complessivo da 1.0"
              " a 10.0 (con un decimale, es. 8.3/10).\n2. Una valutazione"
              " dettagliata della geometria e della simmetria facciale"
              " (struttura degli occhi, linea mandibolare/jawline,"
              " proporzioni).\n3. Un piano di miglioramento personalizzato"
              " (Glow-Up) con esercizi pratici e consigli mirati (es. postura,"
              " skincare, cura della barba/capelli o esercizi muscolari).\nUsa"
              " una formattazione pulita con sezioni, elenchi puntati ed"
              " emoji."
          )

          response = model.generate_content([prompt, image])

          status.update(
              label="✨ Scansione neurale completata con successo!",
              state="complete",
              expanded=False,
          )

          # 3. Output dei risultati dell'AI
          st.markdown("---")
          st.markdown("## 📊 Esito Ufficiale Scansione Biometrica")
          st.markdown(response.text)

        except Exception as e:
          status.update(
              label="❌ Errore durante la scansione", state="error"
          )
          st.error(
              f"Si è verificato un errore di comunicazione con l'AI di Google:"
              f" {e}"
          )
