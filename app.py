import streamlit as st

from scoring import (
    OPZIONI_DIS_FIGLIO,
    OPZIONI_DIS_GENITORE,
    OPZIONI_GENITORE_SOLO,
    OPZIONI_LAVORO,
    calcola_punteggio,
    stima_graduatoria,
)

# --- INTERFACCIA STREAMLIT ---

st.set_page_config(page_title="Calcolatore Nido Trento", page_icon="🧸")
st.title("Calcolatore Graduatoria Nido")
st.markdown(
    "Scopri il tuo punteggio stimato per l'ammissione ai nidi d'infanzia comunali sulla base dei criteri ufficiali.")

st.subheader("1. Scelte generali")
st.info("Questi sono campi OPZIONALI")
solo_part_time = st.checkbox("Faccio domanda *esclusivamente* per il nido a tempo parziale (raddoppia il punteggio)")
lista_attesa = st.checkbox("Ero in lista d'attesa l'anno precedente e sto ripresentando domanda")
priorita = st.checkbox("Il minore ha una disabilità certificata o grave svantaggio sociale attestato")

st.subheader("2. Situazione Familiare")
tipo_genitore_solo = st.selectbox("Presenza di un solo genitore nel nucleo:", OPZIONI_GENITORE_SOLO)

col1, col2 = st.columns(2)
with col1:
    dis_genitore = st.selectbox("Disabilità di un genitore:", OPZIONI_DIS_GENITORE)
with col2:
    dis_figlio = st.selectbox("Disabilità di un altro figlio:", OPZIONI_DIS_FIGLIO)

st.subheader("3. Figli nel nucleo familiare (sotto gli 11 anni)")
st.info("Includi nel conteggio anche la bimba per cui stai presentando la domanda.")

totale_figli = st.number_input("Numero totale di figli (sotto gli 11 anni)", min_value=1, max_value=10, value=2)

st.markdown("Dettaglio per fasce d'età:")
c1, c2, c3 = st.columns(3)
with c1:
    under_6 = st.number_input("Bambini < 6 anni (non gemelli)", min_value=0, max_value=totale_figli, value=1)
with c2:
    gemelli = st.number_input("Bambini gemelli < 6 anni", min_value=0, max_value=totale_figli, value=0)
with c3:
    over_6 = st.number_input("Bambini tra 6 e 11 anni", min_value=0, max_value=totale_figli, value=1)

fratelli_nido = st.number_input(
    "Tra questi, quanti fratelli/sorelle frequentano già o sono iscritti allo stesso nido?",
    min_value=0,
    max_value=totale_figli,
    value=0
)

# Controllo di coerenza in tempo reale
somma_eta = under_6 + gemelli + over_6
dati_validi = True
if somma_eta != totale_figli:
    st.warning(
        f"⚠️ Attenzione: hai indicato {totale_figli} figli in totale, ma la somma delle fasce d'età fa {somma_eta}. Controlla i dati inseriti.")
    dati_validi = False

st.subheader("4. Situazione Lavorativa")
lavoro_g1 = st.selectbox("Occupazione Genitore 1:", OPZIONI_LAVORO)
disagio_g1 = st.checkbox("Disagio lavoro Genitore 1 (Lontananza > 50/110km per oltre 180gg)")

lavoro_g2 = st.selectbox("Occupazione Genitore 2 (se presente):", OPZIONI_LAVORO, index=len(OPZIONI_LAVORO) - 1)
disagio_g2 = st.checkbox("Disagio lavoro Genitore 2 (Lontananza > 50/110km per oltre 180gg)")

st.subheader("5. Situazione Economica")
icef = st.number_input("Valore ICEF (es. 0.15)", min_value=0.0, max_value=1.0, value=0.20, step=0.01)

st.markdown("---")

# Il pulsante elabora i dati solo se il controllo delle età è stato superato
if st.button("Calcola Punteggio e Stima Graduatoria", type="primary", disabled=not dati_validi):
    dati_utente = {
        'solo_part_time': solo_part_time,
        'lista_attesa': lista_attesa,
        'priorita': priorita,
        'tipo_genitore_solo': tipo_genitore_solo,
        'dis_genitore': dis_genitore,
        'dis_figlio': dis_figlio,
        'totale_figli': totale_figli,
        'under_6': under_6,
        'gemelli': gemelli,
        'over_6': over_6,
        'fratelli_nido': fratelli_nido,
        'lavoro_g1': lavoro_g1,
        'disagio_g1': disagio_g1,
        'lavoro_g2': lavoro_g2,
        'disagio_g2': disagio_g2,
        'icef': icef
    }

    totale = calcola_punteggio(dati_utente)
    posizione, probabilita, dettaglio, colore = stima_graduatoria(totale)

    st.success(f"### 🎉 Il tuo punteggio totale è: {totale} punti")

    st.markdown("#### Proiezione in Graduatoria (Basata su dati storici)")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Posizione stimata (su ~690 posti)", value=posizione)
    with col2:
        st.markdown(f"**Probabilità di ingresso:** :{colore}[{probabilita}]")

    st.info(f"💡 **Analisi per i tuoi nidi:** {dettaglio}")