GENITORE_SOLO_ASSENTE_VEDOVANZA = 'Assenza per vedovanza o mancato riconoscimento'
GENITORE_SOLO_ASSENTE_SEPARAZIONE = 'Assenza per separazione, divorzio o abbandono'

OPZIONI_GENITORE_SOLO = [
    'Due genitori presenti', GENITORE_SOLO_ASSENTE_VEDOVANZA, GENITORE_SOLO_ASSENTE_SEPARAZIONE
]

DISABILITA_NESSUNA = 'Nessuna'
DIS_GENITORE_GRAVE = 'Grave (>= 74%)'
DIS_GENITORE_MEDIA = 'Media (66% - 73%)'
DIS_FIGLIO_GRAVE = 'Grave (>= 74% o minorenne)'
DIS_FIGLIO_MEDIA = 'Media (66% - 73%)'

OPZIONI_DIS_GENITORE = [DISABILITA_NESSUNA, DIS_GENITORE_GRAVE, DIS_GENITORE_MEDIA]
OPZIONI_DIS_FIGLIO = [DISABILITA_NESSUNA, DIS_FIGLIO_GRAVE, DIS_FIGLIO_MEDIA]

LAVORO_DIPENDENTE_OLTRE_36H = 'Dipendente (> 36 ore/settimana)'
LAVORO_DIPENDENTE_30_36H = 'Dipendente (30 - 36 ore/settimana)'
LAVORO_DIPENDENTE_24_30H = 'Dipendente (24 - 30 ore/settimana)'
LAVORO_DIPENDENTE_18_24H = 'Dipendente (18 - 24 ore/settimana)'
LAVORO_DIPENDENTE_FINO_18H = 'Dipendente (fino a 18 ore/settimana)'
LAVORO_OCCASIONALE_OLTRE_4MESI = 'Occasionale/Precario (> 4 mesi)'
LAVORO_OCCASIONALE_FINO_4MESI = 'Occasionale/Precario (fino a 4 mesi)'
LAVORO_DISOCCUPATO = 'Disoccupato iscritto al Centro per l\'Impiego'
LAVORO_STUDENTE = 'Studente'
LAVORO_NESSUNA_OCCUPAZIONE = 'Nessuna occupazione / Altro'

# Chi rientra in queste categorie non ha diritto al bonus disagio lavorativo.
LAVORI_SENZA_DISAGIO = {LAVORO_DISOCCUPATO, LAVORO_NESSUNA_OCCUPAZIONE}

OPZIONI_LAVORO = [
    LAVORO_DIPENDENTE_OLTRE_36H, LAVORO_DIPENDENTE_30_36H,
    LAVORO_DIPENDENTE_24_30H, LAVORO_DIPENDENTE_18_24H,
    LAVORO_DIPENDENTE_FINO_18H, LAVORO_OCCASIONALE_OLTRE_4MESI,
    LAVORO_OCCASIONALE_FINO_4MESI, LAVORO_DISOCCUPATO,
    LAVORO_STUDENTE, LAVORO_NESSUNA_OCCUPAZIONE
]

PUNTI_GENITORE_SOLO = {
    GENITORE_SOLO_ASSENTE_VEDOVANZA: 10.0,
    GENITORE_SOLO_ASSENTE_SEPARAZIONE: 8.0,
}

PUNTI_DIS_GENITORE = {
    DIS_GENITORE_GRAVE: 8.0,
    DIS_GENITORE_MEDIA: 6.0,
}

PUNTI_DIS_FIGLIO = {
    DIS_FIGLIO_GRAVE: 6.0,
    DIS_FIGLIO_MEDIA: 4.0,
}

PUNTI_LAVORO = {
    LAVORO_DIPENDENTE_OLTRE_36H: 9.0,
    LAVORO_DIPENDENTE_30_36H: 8.5,
    LAVORO_DIPENDENTE_24_30H: 6.0,
    LAVORO_DIPENDENTE_18_24H: 5.5,
    LAVORO_DIPENDENTE_FINO_18H: 4.0,
    LAVORO_OCCASIONALE_OLTRE_4MESI: 3.5,
    LAVORO_OCCASIONALE_FINO_4MESI: 3.0,
    LAVORO_DISOCCUPATO: 2.5,
    LAVORO_STUDENTE: 4.0,
    LAVORO_NESSUNA_OCCUPAZIONE: 0.0,
}

# Fasce ICEF in ordine crescente di soglia. L'ultima fascia (0.44) usa "<"
# anziché "<=" come le altre, esattamente come nella versione originale.
FASCE_ICEF = [
    (0.07, 7.0),
    (0.12, 6.0),
    (0.17, 5.0),
    (0.22, 4.0),
    (0.27, 3.0),
    (0.32, 2.0),
    (0.38, 1.0),
    (0.44, 0.5),
]


def _punti_icef(icef):
    for soglia, punti in FASCE_ICEF[:-1]:
        if icef <= soglia:
            return punti
    ultima_soglia, ultimi_punti = FASCE_ICEF[-1]
    if icef < ultima_soglia:
        return ultimi_punti
    return 0.0


# Dati statistici estratti dalla graduatoria 2025/2026.
# Ordinate per soglia minima decrescente: si restituisce la prima fascia
# il cui punteggio minimo è raggiunto dal punteggio dell'utente.
FASCE_GRADUATORIA = [
    (40, "Top 10", "Certa (100%)",
     "Assegnazione garantita, quasi sicuramente nel nido di prima scelta.", "green"),
    (30, "Tra i primi 45", "Altissima (100%)",
     "Posto garantito al primo giro di assegnazioni.", "green"),
    (24.5, "Tra i primi 120", "Molto Alta",
     "La totalità dei richiedenti in questa fascia ha ottenuto un nido.", "green"),
    (21.5, "Tra il 120° e il 255° posto", "Alta",
     "Ottime chance. Le prime mancate assegnazioni si registrano solo in fondo a questo "
     "scaglione per i nidi più gettonati.", "green"),
    (19.5, "Tra il 256° e il 466° posto", "Incertezza (Media/Bassa)",
     "Dipende criticamente dalla scelta: nidi come Martignano o Piccolo Girasole esauriscono "
     "i posti prima, mentre strutture come Roncafort o Villazzano Gabbiolo offrono ancora "
     "speranze.", "orange"),
    (17, "Tra il 467° e il 585° posto", "Molto Bassa",
     "La stragrande maggioranza in questa fascia non ottiene l'assegnazione al primo turno.", "red"),
    (float('-inf'), "Oltre il 585° posto", "Quasi Nulla",
     "Punteggio insufficiente per l'ammissione iniziale, salvo rinunce massive o disponibilità "
     "in nidi periferici pochissimo richiesti.", "red"),
]


def calcola_punteggio(dati):
    punteggio = 0.0

    # 1) CONDIZIONI DI PRIORITA'
    if dati['priorita']:
        punteggio += 20.0

    # 2.1) PRESENZA DI UN SOLO GENITORE
    punteggio += PUNTI_GENITORE_SOLO.get(dati['tipo_genitore_solo'], 0.0)

    # 2.2) DISABILITA' NEL NUCLEO
    punteggio += PUNTI_DIS_GENITORE.get(dati['dis_genitore'], 0.0)
    punteggio += PUNTI_DIS_FIGLIO.get(dati['dis_figlio'], 0.0)

    # 2.3) PUNTEGGIO FIGLI
    totale_figli = dati['totale_figli']

    if totale_figli > 0:
        if totale_figli <= 2:
            punteggio += (dati['under_6'] * 1.5) + (dati['gemelli'] * 2.5) + (dati['over_6'] * 1.0)
        else:  # 3 o più figli
            punteggio += (dati['under_6'] * 2.0) + (dati['gemelli'] * 3.0) + (dati['over_6'] * 1.5)

    punteggio += (dati['fratelli_nido'] * 3.0)

    # 2.4) SITUAZIONE LAVORATIVA
    punteggio_g1 = PUNTI_LAVORO.get(dati['lavoro_g1'], 0.0)
    if dati['disagio_g1'] and dati['lavoro_g1'] not in LAVORI_SENZA_DISAGIO:
        punteggio_g1 += 2.0
    punteggio += punteggio_g1

    punteggio_g2 = PUNTI_LAVORO.get(dati['lavoro_g2'], 0.0)
    if dati['disagio_g2'] and dati['lavoro_g2'] not in LAVORI_SENZA_DISAGIO:
        punteggio_g2 += 2.0
    punteggio += punteggio_g2

    # 3) SITUAZIONE ECONOMICA (ICEF)
    punteggio += _punti_icef(dati['icef'])

    # 4) TEMPO DI ATTESA
    if dati['lista_attesa']:
        punteggio += 10.0

    # RADDOPPIO PER TEMPO PARZIALE
    if dati['solo_part_time']:
        punteggio *= 2

    return punteggio


def stima_graduatoria(punteggio):
    for soglia_minima, pos, prob, dettaglio, colore in FASCE_GRADUATORIA:
        if punteggio >= soglia_minima:
            return pos, prob, dettaglio, colore
