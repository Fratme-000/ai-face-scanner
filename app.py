from PIL import Image
import requests
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="AI Neural Glow-Up & Chat", page_icon="🤖", layout="centered"
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
    "Carica la tua foto migliore, genera il tuo piano di miglioramento"
    " personalizzato e chatta liberamente con l'IA per qualsiasi consiglio!"
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

# Se l'immagine è stata caricata o scattata
if uploaded_image is not None:
  st.image(
      uploaded_image, caption="Foto acquisita con successo", use_container_width=True
  )

  # Inizializzazione della memoria di sessione per la chat e l'analisi
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
  if "initial_analysis" not in st.session_state:
    st.session_state.initial_analysis = ""

  # Pulsante per avviare l'analisi iniziale se non è stata ancora fatta
  if not st.session_state.initial_analysis:
    if st.button("🚀 Avvia Analisi Neurale e Glow-Up"):
      with st.status(
          "🔍 Connessione al cluster neurale di Pollinations...", expanded=True
      ) as status:
        st.write(
            "Elaborazione fisionomica e creazione del piano di"
            " miglioramento..."
        )
        try:
          prompt_base = (
              "Genera un voto onesto sull'attrazione del soggetto"
              "Agisci come un consulente di immagine, stile, skincare e"
              " grooming personale di livello professionale. Adotta un tono"
              " cyberpunk, futuristico, motivazionale e costruttivo. Genera un"
              " piano di miglioramento completo (Glow-Up) strutturato con: 1."
              " Analisi fisionomica e strutturale generale. 2. Consigli"
              " avanzati di skincare, taglio capelli e postura. 3. Piano"
              " d'azione pratico settimanale. Rispondi in italiano con una"
              " formattazione pulita ed emoji."
          )

          url = (
              "https://text.pollinations.ai/"
              + requests.utils.quote(prompt_base)
              + "?model=openai"
          )
          response = requests.get(url, timeout=35)

          if response.status_code == 200:
            st.session_state.initial_analysis = response.text
            status.update(
                label="✨ Analisi completata con successo!",
                state="complete",
                expanded=False,
            )
            st.rerun()
          else:
            status.update(label="❌ Errore del server", state="error")
            st.error(
                f"Errore di risposta dal server (Status {response.status_code})."
                " Riprova tra un istante."
            )

        except Exception as e:
          status.update(label="❌ Errore di connessione", state="error")
          st.error(
              f"Tempo scaduto o errore di rete ({e}). Riprova a premere il"
              " pulsante."
          )

  # Se l'analisi iniziale è presente, mostrala e attiva la chat interattiva
  if st.session_state.initial_analysis:
    st.markdown("---")
    st.markdown("## 📊 Piano di Glow-Up Ufficiale")
    st.markdown(st.session_state.initial_analysis)

    st.markdown("---")
    st.markdown("### 💬 Chatta con il tuo Style Coach IA")
    st.write(
        "Hai domande specifiche, vuoi consigli su prodotti, vestiti o"
        " allenamento? Scrivi qui sotto!"
    )

    # Mostra la cronologia della chat
    for message in st.session_state.chat_history:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Casella di input per la chat in basso
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
                + "?model=openai"
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
