import requests
from bs4 import BeautifulSoup
import time
import os
import json

# CONFIGURE GITHUB SECRETS
URL_LOGIN = "https://webstudent.ase.ro/login1.aspx?ReturnUrl=%2f"
URL_NOTE = "https://webstudent.ase.ro/Note.aspx"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
USER = os.getenv("STUDENT_USER")
PASS = os.getenv("STUDENT_PASS")

FILE_NOTE = "note_vechi.json"

def incarca_note_vechi():
    if os.path.exists(FILE_NOTE):
        try:
            with open(FILE_NOTE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salveaza_note(note):
    with open(FILE_NOTE, "w") as f:
        json.dump(note, f, indent=4)

def get_asp_fields(soup):
    fields = {}
    for hidden_id in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        tag = soup.find('input', {'id': hidden_id})
        if tag:
            fields[hidden_id] = tag['value']
    return fields

def trimite_notificare_discord(materie, nota, este_noua=True):
    tip_update = "Nota Noua Publicata" if este_noua else "Nota Actualizata"
    text_notificare = f"@everyone Materie: {materie} | Nota: {nota}"
    
    payload = {
        "content": text_notificare,
        "embeds": [{
            "title": tip_update,
            "color": 3066993 if este_noua else 15105570,
            "fields": [
                {"name": "Materie", "value": materie, "inline": True},
                {"name": "Nota", "value": nota, "inline": True}
            ],
            "footer": {"text": f"Verificat la ora: {time.strftime('%H:%M:%S')}"}
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

def scanare_note():
    session = requests.Session()
    note_vechi = incarca_note_vechi()
    
    try:
        r_get = session.get(URL_LOGIN)
        soup_login = BeautifulSoup(r_get.text, 'html.parser')
        payload = get_asp_fields(soup_login)
        payload.update({
            'txtUtilizator': USER, 
            'txtParola': PASS, 
            'btnConectare': 'Conectare'
        })
        session.post(URL_LOGIN, data=payload)

        r_note = session.get(URL_NOTE)
        soup_note = BeautifulSoup(r_note.text, 'html.parser')
        tabel = soup_note.find('table', {'id': 'ctl00_Continut_grdNote'})
        
        if not tabel:
            print("Eroare: Tabelul nu a fost gasit. Verifica user/parola.")
            return

        note_prezente = {}
        rows = tabel.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                materie = cols[1].get_text(strip=True)
                nota = cols[4].get_text(strip=True)
                if materie:
                    note_prezente[materie] = nota

        schimbari = False
        if not note_vechi:
            print("Prima rulare. Salvez datele initiale.")
            salveaza_note(note_prezente)
        else:
            for materie, nota in note_prezente.items():
                if materie not in note_vechi:
                    trimite_notificare_discord(materie, nota, True)
                    schimbari = True
                elif note_vechi[materie] != nota:
                    trimite_notificare_discord(materie, nota, False)
                    schimbari = True
            
            if schimbari:
                salveaza_note(note_prezente)
            else:
                print("Nu sunt modificari.")

    except Exception as e:
        print(f"Eroare: {str(e)}")

if __name__ == "__main__":
    scanare_note()
