import os
import json
from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib

matplotlib.use('Agg')  # Zorgt ervoor dat het werkt in een headless omgeving
import matplotlib.pyplot as plt

# API-sleutel
client = EntsoePandasClient(api_key="d23a1866-678d-4c7c-a38e-ccf32827ca32")

# Huidige datum en tijdzone
start = pd.Timestamp.now(tz='Europe/Brussels').normalize()
end = start + pd.Timedelta(days=2)

country_code = 'BE'  # België

# Functie om bestanden te verwijderen
def verwijder_bestand(bestandsnaam):
    if os.path.exists(bestandsnaam):
        os.remove(bestandsnaam)

# Oude bestanden verwijderen
verwijder_bestand("energieprijzen.json")

try:
    # Day-ahead prijzen ophalen
    day_ahead_prices = client.query_day_ahead_prices(country_code, start=start, end=end)

    # Vandaag en morgen bepalen
    vandaag = start
    morgen = start + pd.Timedelta(days=1)

    # Prijzen filteren per dag
    prijzen_vandaag = day_ahead_prices[vandaag:vandaag + pd.Timedelta(days=1)]
    prijzen_morgen = day_ahead_prices[morgen:morgen + pd.Timedelta(days=1)]

    # Controleren of er data is voor vandaag
    if prijzen_vandaag.empty:
        raise ValueError("Geen data beschikbaar voor vandaag.")

    # Functie om goedkoopste tijdsblokken te bepalen
    def goedkoopste_blokken(prijzen, duur):
        min_prijs = float("inf")
        beste_blok = None

        for i in range(len(prijzen) - (duur - 1)):
            tijdsblok = prijzen.index[i: i + duur]
            som_prijs = prijzen[tijdsblok].sum()

            if som_prijs < min_prijs:
                min_prijs = som_prijs
                beste_blok = tijdsblok

        return beste_blok if beste_blok is not None else []

    # Functie om blokken om te zetten naar JSON-formaat met prijzen
    def blok_met_prijzen(blok, prijzen):
        return {t.strftime('%H:%M'): float(prijzen[t]) for t in blok} if len(blok) > 0 else {}

    # Analyseer prijzen voor vandaag
    goedkoopste_uur_vandaag = goedkoopste_blokken(prijzen_vandaag, 1)
    goedkoopste_2u_vandaag = goedkoopste_blokken(prijzen_vandaag, 2)
    goedkoopste_3u_vandaag = goedkoopste_blokken(prijzen_vandaag, 3)

    # Analyseer prijzen voor morgen (indien beschikbaar)
    if prijzen_morgen.empty:
        goedkoopste_uur_morgen = []
        goedkoopste_2u_morgen = []
        goedkoopste_3u_morgen = []
    else:
        goedkoopste_uur_morgen = goedkoopste_blokken(prijzen_morgen, 1)
        goedkoopste_2u_morgen = goedkoopste_blokken(prijzen_morgen, 2)
        goedkoopste_3u_morgen = goedkoopste_blokken(prijzen_morgen, 3)

    # JSON-bestand aanmaken
    energieprijzen_data = {
        "vandaag": {
            "prijzen": {t.strftime('%H:%M'): float(prijzen_vandaag[t]) for t in prijzen_vandaag.index},
            "goedkoopste_uur": blok_met_prijzen(goedkoopste_uur_vandaag, prijzen_vandaag),
            "goedkoopste_2u_blok": blok_met_prijzen(goedkoopste_2u_vandaag, prijzen_vandaag),
            "goedkoopste_3u_blok": blok_met_prijzen(goedkoopste_3u_vandaag, prijzen_vandaag)
        },
        "morgen": {
            "prijzen": {t.strftime('%H:%M'): float(prijzen_morgen[t]) for t in prijzen_morgen.index} if not prijzen_morgen.empty else {},
            "goedkoopste_uur": blok_met_prijzen(goedkoopste_uur_morgen, prijzen_morgen),
            "goedkoopste_2u_blok": blok_met_prijzen(goedkoopste_2u_morgen, prijzen_morgen),
            "goedkoopste_3u_blok": blok_met_prijzen(goedkoopste_3u_morgen, prijzen_morgen)
        }
    }

    # JSON opslaan
    with open("energieprijzen.json", "w", encoding="utf-8") as json_file:
        json.dump(energieprijzen_data, json_file, indent=4, ensure_ascii=False)

    print("✅ JSON-bestand 'energieprijzen.json' gegenereerd.")


    # Grafieken maken
    def plot_prijzen(prijzen, titel, bestandsnaam):
        plt.figure(figsize=(12, 6))
        plt.plot(prijzen.index, prijzen.values, marker='o', linestyle='-', color='blue')
        plt.xticks(prijzen.index, [t.strftime('%H:%M') for t in prijzen.index], rotation=45)
        plt.xlabel('Tijd')
        plt.ylabel('Energieprijs (€ per MWh)')
        plt.title(titel)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(bestandsnaam)


    # Grafiek voor vandaag
    plot_prijzen(prijzen_vandaag, "Energieprijzen Vandaag", "energieprijzen_vandaag.png")
    print("Grafiek voor vandaag opgeslagen als 'energieprijzen_vandaag.png'")

    # Grafiek voor morgen (indien beschikbaar)
    if not prijzen_morgen.empty:
        plot_prijzen(prijzen_morgen, "Energieprijzen Morgen", "energieprijzen_morgen.png")
        print("Grafiek voor morgen opgeslagen als 'energieprijzen_morgen.png'")

except Exception as e:
    print(f"⚠️ Er is een fout opgetreden: {e}")
