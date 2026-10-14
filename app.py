from PIL import Image
import requests
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="AI Glow-Up & Style Coach", page_icon="🤖", layout="centered"
)

# Stile CSS cyberpunk personalizzato
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

st.title("🤖 AI Neural Glow-Up & Style Coach")
st.markdown(
    "Carica la tua foto migliore (scattata con la fotocamera nativa del"
    " telefono o scelta dalla galleria) per generare il tuo piano"
    " personalizzato con **Pollinations AI**."
)

# Selezione della modalità di caricamento foto
scelta_foto = st.radio(
    "Scegli come inserire la foto:",
    [
        "📁 Carica dalla galleria / Fotocamera nativa",
        "📸 Scatta con la webcam del browser",
    ],
)

uploaded_image = None

if scelta_foto == "📁 Carica dalla galleria / Fotocamera nativa":
  file_caricato = st.file_uploader(
      "Scegli l'immagine dal tuo dispositivo", type=["jpg", "jpeg", "png"]
  )
  if file_caricato is not None:
    uploaded_image = Image.open(file_caricato)
else:
  camera_file = st.camera_input("Scatta un selfie rapido dal browser")
  if camera_file is not None:
    uploaded_image = Image.open(camera_file)

# Se l'immagine è stata caricata/scattata, mostriamo l'anteprima e il form
if uploaded_image is not None:
  st.image(
      uploaded_image,
      caption="Foto acquisita con successo",
      use_container_width=True,
  )

  with st.form("glow_up_form"):
    st.subheader("⚙️ Parametri Biometrici e di Stile")

    forma_viso = st.selectbox(
        "Forma del viso principale:",
        ["Ovale", "Quadrato", "Rotondo", "Allungato/Rettangolare", "A diamante"],
    )

    stile_capelli = st.text_input(
        "Stile/Taglio di capelli attuale:",
        placeholder="es. corti ai lati, medi mossi...",
    )

    obiettivo = st.text_input(
        "Qual è il tuo obiettivo principale?",
        placeholder="es. definire la mascella, migliorare la pelle, stile"
        " cyberpunk...",
    )

    submit_button = st.form_submit_button("🚀 Genera Piano di Glow-Up Neurale")

  if submit_button:
    if not obiettivo:
      st.warning("⚠️ Per favore, inserisci almeno il tuo obiettivo principale!")
    else:
      with st.status(
          "🔍 Analisi dei parametri nel cluster neurale...", expanded=True
      ) as status:
        st.write("Connessione al motore generativo di Pollinations...")
        import time

        time.sleep(1)
        st.write("Elaborazione fisionomica e creazione consigli mirati...")
        time.sleep(1.2)

        try:
          prompt_base = (
              f"Agisci come un consulente di immagine, stile, skincare e"
              f" grooming personale di livello professionale. Adotta un tono"
              f" cyberpunk, futuristico, motivazionale e costruttivo. L'utente"
              f" ha una forma del viso {forma_viso}, i capelli"
              f" {stile_capelli}, e il suo obiettivo principale è {obiettivo}."
              f" Restituisci un piano di miglioramento dettagliato (Glow-Up)"
              f" strutturato con: 1. Valutazione strutturale della fisionomia."
              f" 2. Consigli mirati di skincare, taglio capelli e postura. 3."
              f" Un piano d'azione pratico settimanale. Rispondi in italiano"
              f" con una formattazione pulita, sezioni ed emoji."
          )

          url = (
              "https://text.pollinations.ai/"
              + requests.utils.quote(prompt_base)
              + "?model=openai"
          )
          response = requests.get(url, timeout=25)

          if response.status_code == 200:
            status.update(
                label="✨ Piano di Glow-Up generato con successo!",
                state="complete",
                expanded=False,
            )

            st.markdown("---")
            st.markdown("## 📊 Il Tuo Piano Ufficiale")
            st.markdown(response.text)
          else:
            status.update(label="❌ Errore di comunicazione", state="error")
            st.error(
                f"Errore del server (Status {response.status_code}). Riprova"
                " tra un istante."
            )

        except Exception as e:
          status.update(label="❌ Errore di connessione", state="error")
          st.error(f"Si è verificato un errore di rete: {e}")
