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


# Funzione per convertire l'immagine in base64 per l'animazione HTML
def get_image_base64(img):
  buffered = BytesIO()
  img.save(buffered, format="JPEG")
  img_str = base64.b64encode(buffered.getvalue()).decode()
  return f"data:image/jpeg;base64,{img_str}"


# Funzione per analizzare i parametri reali della foto (luminosità e colori)
def analizza_immagine_pil(img):
  img_small = img.resize((50, 50)).convert("RGB")
  pixels = list(img_small.getdata())

  r_tot = sum(p[0] for p in pixels)
  g_tot = sum(p[1] for p in pixels)
  b_tot = sum(p[2] for p in pixels)
  num_pixels = len(pixels)

  r_avg = r_tot / num_pixels
  g_avg = g_tot / num_pixels
  b_avg = b_tot / num_pixels

  brightness = (0.299 * r_avg + 0.587 * g_avg + 0.114 * b_avg) / 255.0
  width, height = img.size
  aspect_ratio = width / height

  return {
      "brightness": round(brightness, 2),
      "rgb_avg": (int(r_avg), int(g_avg), int(b_avg)),
      "aspect_ratio": round(aspect_ratio, 2),
  }


st.title("🤖 AI Neural Glow-Up & Style Coach")
st.markdown(
    "Carica la tua foto, avvia la scansione biometrica e chatta liberamente"
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

  if (
      "scanning" in st.session_state
      and st.session_state.scanning
      and not st.session_state.initial_analysis
  ):
    placeholder_anim = st.empty()
    placeholder_anim.markdown(
        f"""
        <div style="text-align: center; color: #00E676; font-weight: bold; margin-bottom: 10px;">
            ⚡ Analisi geometrica e calcolo biometrico in corso...
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
      # Estraiamo i parametri unici della foto per personalizzare il voto
      dati_foto = analizza_immagine_pil(uploaded_image)

      prompt_base = (
          "Agisci come un consulente di immagine, stile, skincare e grooming"
          " personale di livello professionale. Parametri biometrici e di"
          f" scatto unici rilevati dalla foto: Luminosità stimata:"
          f" {dati_foto['brightness']}, Bilanciamento cromatico medio RGB:"
          f" {dati_foto['rgb_avg']}, Proporzioni geometriche:"
          f" {dati_foto['aspect_ratio']}. Sulla base di questi dati unici,"
          " assegna un voto reale e onesto sulla possibbilità d'attrazione, rigoroso e variato da 1 a 10 (con decimali"
          " precisi) e genera un piano di miglioramento (Glow-Up) altamente"
          " personalizzato. Adotta un tono cyberpunk, futuristico,"
          " motivazionale e costruttivo. Struttura la risposta con: 1. Voto e"
          " analisi basata sui parametri unici della foto. 2. Consigli avanzati"
          " di skincare, taglio capelli e postura. 3. Piano d'azione pratico"
          " settimanale. Rispondi in italiano con una formattazione pulita ed"
          " emoji."
      )

      url = "https://text.pollinations.ai/" + requests.utils.quote(prompt_base)
      response = requests.get(url, timeout=35)

      if response.status_code == 200:
        st.session_state.initial_analysis = response.text
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

  # Risultati e chat interattiva
  if st.session_state.initial_analysis:
    st.image(
        uploaded_image,
        caption="Foto scannerizzata con successo",
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
            chat_prompt = (
                f"Contesto della consulenza precedente: L'utente ha ricevuto"
                f" questo piano di glow-up:"
                f" {st.session_state.initial_analysis[:400]}...\n\nDomanda"
                f" attuale dell'utente: {prompt_utente}\n\nRispondi in"
                " italiano come un esperto consulente di stile cyberpunk,"
                " dando risposte pratiche e dirette."
            )
            chat_url = (
                "https://text.pollinations.ai/"
                + requests.utils.quote(chat_prompt)
            )
            chat_resp = requests.get(chat_url, timeout=30)

            if chat_resp.status_code == 200:
              risposta_ia = chat_resp.text
              st.markdown(risposta_ia)
              st.session_state.chat_history.append(
                  {"role": "assistant", "content": risposta_ia}
              )
            else:
              st.error("Errore di comunicazione con il server dell'IA.")
          except Exception as e:
            st.error(f"Errore di connessione: {e}")
