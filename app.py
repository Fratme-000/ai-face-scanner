import base64
from io import BytesIO
from PIL import Image
import requests
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="AI Neural Glow-Up & Chat", page_icon="🤖", layout="centered"
)

# Stile CSS cyberpunk avanzato e animazione di scansione laser
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
    
    /* Animazione del raggio laser di scansione */
    @keyframes scanline {
        0% { top: 0%; }
        50% { top: 100%; }
        100% { top: 0%; }
    }
    
    .scanner-container {
        position: relative;
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid #00E676;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.4);
    }
    
    .scanner-container img {
        width: 100%;
        display: block;
    }
    
    .laser {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: #00E676;
        box-shadow: 0 0 15px #00E676, 0 0 30px #00E676;
        animation: scanline 2s ease-in-out infinite;
    }
    
    .grid-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: linear-gradient(rgba(0, 230, 118, 0.2) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 230, 118, 0.2) 1px, transparent 1px);
        background-size: 25px 25px;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)


# Funzione per convertire l'immagine in base64 da inviare all'IA visiva
def get_image_base64(img):
  buffered = BytesIO()
  img.save(buffered, format="JPEG")
  img_str = base64.b64encode(buffered.getvalue()).decode()
  return f"data:image/jpeg;base64,{img_str}"


st.title("🤖 AI Neural Glow-Up & Style Coach")
st.markdown(
    "Carica la tua foto reale, avvia la scansione biometrica visiva e chatta"
    " con l'IA!"
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

# Inizializzazione della memoria di sessione
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []
if "initial_analysis" not in st.session_state:
  st.session_state.initial_analysis = ""

# Se l'immagine è presente
if uploaded_image is not None:
  img_b64 = get_image_base64(uploaded_image)

  # Mostriamo l'anteprima normale se l'analisi non è ancora avvenuta
  if not st.session_state.initial_analysis:
    st.markdown(
        f"""
        <div class="scanner-container">
            <img src="{img_b64}">
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("🚀 Avvia Scansione Neurale e Glow-Up"):
      st.session_state.scanning = True
      st.rerun()

  # Se l'utente ha premuto il pulsante di scansione
  if (
      "scanning" in st.session_state
      and st.session_state.scanning
      and not st.session_state.initial_analysis
  ):
    placeholder_anim = st.empty()
    placeholder_anim.markdown(
        f"""
        <div style="text-align: center; color: #00E676; font-weight: bold; margin-bottom: 10px;">
            ⚡ Analisi visiva e mappatura geometrica in corso...
        </div>
        <div class="scanner-container">
            <div class="grid-overlay"></div>
            <div class="laser"></div>
            <img src="{img_b64}">
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
      # Invio della foto reale tramite richiesta POST multimodale
      payload = {
          "model": "openai",
          "messages": [{
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": (
                          "Genera un voto onesto sulla possibbile attrazione che vada da 1 a 10"
                          "Agisci come un consulente di immagine, stile,"
                          " skincare e grooming personale di livello"
                          " professionale. Guarda attentamente la foto del viso"
                          " fornita e dai un voto reale (da 1 a 10 motivato) basato"
                          " sui lineamenti effettivi, forma del viso, pelle e"
                          " capelli visibili nell'immagine. Adotta un tono"
                          " cyberpunk, futuristico, motivazionale e"
                          " costruttivo. Genera un piano di miglioramento"
                          " completo (Glow-Up) strutturato con: 1. Voto e"
                          " analisi fisionomica reale della foto. 2. Consigli"
                          " avanzati di skincare, taglio capelli e postura. 3."
                          " Piano d'azione pratico settimanale. Rispondi in"
                          " italiano con una formattazione pulita ed emoji."
                      ),
                  },
                  {"type": "image_url", "image_url": {"url": img_b64}},
              ],
          }],
      }

      response = requests.post(
          "https://text.pollinations.ai/v1/chat/completions",
          json=payload,
          timeout=40,
      )

      if response.status_code == 200:
        data = response.json()
        st.session_state.initial_analysis = data["choices"][0]["message"][
            "content"
        ]
        st.session_state.scanning = False
        placeholder_anim.empty()
        st.rerun()
      else:
        st.error(
            f"Errore di risposta dal server (Status {response.status_code})."
        )
        st.session_state.scanning = False
    except Exception as e:
      st.error(f"Tempo scaduto o errore di rete ({e}). Riprova.")
      st.session_state.scanning = False

  # Se l'analisi è completata, mostra i risultati e la chat
  if st.session_state.initial_analysis:
    st.image(
        uploaded_image,
        caption="Foto analizzata con successo",
        use_container_width=True,
    )
    st.markdown("---")
    st.markdown("## 📊 Piano di Glow-Up Ufficiale")
    st.markdown(st.session_state.initial_analysis)

    st.markdown("---")
    st.markdown("### 💬 Chatta con il tuo Style Coach IA")
    st.write(
        "Hai domande specifiche, vuoi consigli su prodotti, vestiti o"
        " allenamento? Scrivi qui sotto!"
    )

    for message in st.session_state.chat_history:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    if prompt_utente := st.chat_input("Fai una domanda all'IA..."):
      st.session_state.chat_history.append(
          {"role": "user", "content": prompt_utente}
      )
      with st.chat_message("user"):
        st.markdown(prompt_utente)

      with st.chat_message("assistant"):
        with st.spinner("L'IA sta elaborando la risposta..."):
          try:
            chat_payload = {
                "model": "openai",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Sei un esperto consulente di stile cyberpunk. L'utente"
                            " ha ricevuto questo piano di glow-up basato sulla sua"
                            " foto reale:"
                            f" {st.session_state.initial_analysis[:400]}..."
                        ),
                    },
                    {"role": "user", "content": prompt_utente},
                ],
            }
            chat_resp = requests.post(
                "https://text.pollinations.ai/v1/chat/completions",
                json=chat_payload,
                timeout=30,
            )

            if chat_resp.status_code == 200:
              chat_data = chat_resp.json()
              risposta_ia = chat_data["choices"][0]["message"]["content"]
              st.markdown(risposta_ia)
              st.session_state.chat_history.append(
                  {"role": "assistant", "content": risposta_ia}
              )
            else:
              st.error("Errore di comunicazione con il server dell'IA.")
          except Exception as e:
            st.error(f"Errore di connessione: {e}")
