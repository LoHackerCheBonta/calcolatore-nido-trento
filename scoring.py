OPZIONI_LAVORO = [
    'Dipendente (> 36 ore/settimana)', 'Dipendente (30 - 36 ore/settimana)',
    'Dipendente (24 - 30 ore/settimana)', 'Dipendente (18 - 24 ore/settimana)',
    'Dipendente (fino a 18 ore/settimana)', 'Occasionale/Precario (> 4 mesi)',
    'Occasionale/Precario (fino a 4 mesi)', 'Disoccupato iscritto al Centro per l\'Impiego',
    'Studente', 'Nessuna occupazione / Altro'
]


def calcola_punteggio(dati):
    punteggio = 0.0

    # 1) CONDIZIONI DI PRIORITA'
    if dati['priorita']:
        punteggio += 20.0

    # 2.1) PRESENZA DI UN SOLO GENITORE
    if dati['tipo_genitore_solo'] == 'Assenza per vedovanza o mancato riconoscimento':
        punteggio += 10.0
    elif dati['tipo_genitore_solo'] == 'Assenza per separazione, divorzio o abbandono':
        punteggio += 8.0

    # 2.2) DISABILITA' NEL NUCLEO
    if dati['dis_genitore'] == 'Grave (>= 74%)':
        punteggio += 8.0
    elif dati['dis_genitore'] == 'Media (66% - 73%)':
        punteggio += 6.0

    if dati['dis_figlio'] == 'Grave (>= 74% o minorenne)':
        punteggio += 6.0
    elif dati['dis_figlio'] == 'Media (66% - 73%)':
        punteggio += 4.0

    # 2.3) PUNTEGGIO FIGLI
    totale_figli = dati['totale_figli']

    if totale_figli > 0:
        if totale_figli <= 2:
            punteggio += (dati['under_6'] * 1.5) + (dati['gemelli'] * 2.5) + (dati['over_6'] * 1.0)
        else:  # 3 o più figli
            punteggio += (dati['under_6'] * 2.0) + (dati['gemelli'] * 3.0) + (dati['over_6'] * 1.5)

    punteggio += (dati['fratelli_nido'] * 3.0)

    # 2.4) SITUAZIONE LAVORATIVA
    punteggi_lavoro = {
        'Dipendente (> 36 ore/settimana)': 9.0,
        'Dipendente (30 - 36 ore/settimana)': 8.5,
        'Dipendente (24 - 30 ore/settimana)': 6.0,
        'Dipendente (18 - 24 ore/settimana)': 5.5,
        'Dipendente (fino a 18 ore/settimana)': 4.0,
        'Occasionale/Precario (> 4 mesi)': 3.5,
        'Occasionale/Precario (fino a 4 mesi)': 3.0,
        'Disoccupato iscritto al Centro per l\'Impiego': 2.5,
        'Studente': 4.0,
        'Nessuna occupazione / Altro': 0.0
    }

    punteggio_g1 = punteggi_lavoro.get(dati['lavoro_g1'], 0.0)
    if dati['disagio_g1'] and dati['lavoro_g1'] not in ['Disoccupato iscritto al Centro per l\'Impiego',
                                                        'Nessuna occupazione / Altro']:
        punteggio_g1 += 2.0
    punteggio += punteggio_g1

    punteggio_g2 = punteggi_lavoro.get(dati['lavoro_g2'], 0.0)
    if dati['disagio_g2'] and dati['lavoro_g2'] not in ['Disoccupato iscritto al Centro per l\'Impiego',
                                                        'Nessuna occupazione / Altro']:
        punteggio_g2 += 2.0
    punteggio += punteggio_g2

    # 3) SITUAZIONE ECONOMICA (ICEF)
    icef = dati['icef']
    if icef <= 0.07:
        punteggio += 7.0
    elif icef <= 0.12:
        punteggio += 6.0
    elif icef <= 0.17:
        punteggio += 5.0
    elif icef <= 0.22:
        punteggio += 4.0
    elif icef <= 0.27:
        punteggio += 3.0
    elif icef <= 0.32:
        punteggio += 2.0
    elif icef <= 0.38:
        punteggio += 1.0
    elif icef < 0.44:
        punteggio += 0.5

    # 4) TEMPO DI ATTESA
    if dati['lista_attesa']:
        punteggio += 10.0

    # RADDOPPIO PER TEMPO PARZIALE
    if dati['solo_part_time']:
        punteggio *= 2

    return punteggio


def stima_graduatoria(punteggio):
    # Dati statistici estratti dalla graduatoria 2025/2026
    if punteggio >= 40:
        pos = "Top 10"
        prob = "Certa (100%)"
        dettaglio = "Assegnazione garantita, quasi sicuramente nel nido di prima scelta."
        colore = "green"
    elif punteggio >= 30:
        pos = "Tra i primi 45"
        prob = "Altissima (100%)"
        dettaglio = "Posto garantito al primo giro di assegnazioni."
        colore = "green"
    elif punteggio >= 24.5:
        pos = "Tra i primi 120"
        prob = "Molto Alta"
        dettaglio = "La totalità dei richiedenti in questa fascia ha ottenuto un nido."
        colore = "green"
    elif punteggio >= 21.5:
        pos = "Tra il 120° e il 255° posto"
        prob = "Alta"
        dettaglio = "Ottime chance. Le prime mancate assegnazioni si registrano solo in fondo a questo scaglione per i nidi più gettonati."
        colore = "green"
    elif punteggio >= 19.5:
        pos = "Tra il 256° e il 466° posto"
        prob = "Incertezza (Media/Bassa)"
        dettaglio = "Dipende criticamente dalla scelta: nidi come Martignano o Piccolo Girasole esauriscono i posti prima, mentre strutture come Roncafort o Villazzano Gabbiolo offrono ancora speranze."
        colore = "orange"
    elif punteggio >= 17:
        pos = "Tra il 467° e il 585° posto"
        prob = "Molto Bassa"
        dettaglio = "La stragrande maggioranza in questa fascia non ottiene l'assegnazione al primo turno."
        colore = "red"
    else:
        pos = "Oltre il 585° posto"
        prob = "Quasi Nulla"
        dettaglio = "Punteggio insufficiente per l'ammissione iniziale, salvo rinunce massive o disponibilità in nidi periferici pochissimo richiesti."
        colore = "red"

    return pos, prob, dettaglio, colore
