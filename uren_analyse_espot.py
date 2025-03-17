import numpy as np
import json
import datetime

# Functie om de prijzen uit een JSON-bestand te laden
def laad_prijzen(dag="today"):
    try:
        # Open het JSON-bestand en laad de inhoud als een Python-dictionary
        with open("prices_per_hour.json", "r") as file:
            data = json.load(file)  # JSON inladen als dictionary

        # Haal de data voor de opgegeven dag ('today' of 'tomorrow')
        prijzen_data = data.get(dag, [])  # Haal de juiste dataset op (today of tomorrow)
        
        # Maak een dictionary van uren naar prijzen, waarbij de prijzen worden omgezet naar float
        prijzen_dict = {
            i: float(entry["price"].replace(",", "."))  # Omzetten van komma naar punt voor decimale waarden
            for i, entry in enumerate(reversed(prijzen_data))  # Reversed om 0:00 correct op index 0 te zetten
        }
        return prijzen_dict  # Retourneer de dictionary met prijzen per uur

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Foutafhandelingsmechanisme bij fouten in het inlezen van het bestand
        print(f"Fout bij het laden van het JSON-bestand: {e}")
        return {}  # Return een lege dictionary bij een fout

# Functie om het laagste gemiddelde verbruik te berekenen voor een opgegeven blok lengte
def laagste_verbruik_uren(prijzen_dict, n):
    if not prijzen_dict:
        print("Geen prijzen beschikbaar.")  # Als er geen prijzen zijn, geef een waarschuwing
        return None, None, None, None

    # Initialiseer variabelen voor het laagste gemiddelde en de beste starttijd
    min_gemiddelde = float('inf')  # Begin met een onrealistisch hoog getal
    beste_start = 0  # Start vanaf het begin van de lijst
    
    # Loop door alle mogelijke tijdsblokken van lengte n
    for i in range(25 - n):  # Er zijn 24 uren, dus we stoppen als er niet genoeg uren over zijn
        # Bereken het gemiddelde van de prijzen voor het huidige blok van n uren
        huidig_gemiddelde = np.mean([prijzen_dict[j] for j in range(i, i + n)])  

        # Als dit blok een lager gemiddelde heeft, sla deze op als het beste blok
        if huidig_gemiddelde < min_gemiddelde:  
            min_gemiddelde = huidig_gemiddelde  
            beste_start = i  
    
    # Bereken het einduur van het beste blok
    beste_eind = beste_start + n  # Het einduur is het startuur plus het aantal uren van het blok
    laagste_prijs = np.mean([prijzen_dict[j] for j in range(beste_start, beste_start + n)])  # Gemiddelde prijs voor het blok
    
    return beste_start, beste_eind, min_gemiddelde, laagste_prijs  # Retourneer de resultaten

# Functie voor het uitvoeren van de analyse
def verwerk_prijzen(dag="today"):
    # Laad de prijzen voor de opgegeven dag
    prijzen_dict = laad_prijzen(dag)  
    if not prijzen_dict:
        return  # Stop de functie als er geen prijzen beschikbaar zijn
    if dag == "today":
        print("\nPrijsoverzicht voor ",datetime.date.today(),":")
    else:
        print("\nPrijsoverzicht voor ", datetime.date.today() + datetime.timedelta(days=1) ,":")
    
    blok_1_resultaat = ""
    blok_2_resultaat = ""
    blok_3_resultaat = ""

    # Voor blokken van 1, 2 en 3 uur de beste uren berekenen en afdrukken
    for n in [1, 2, 3]:
        # Verkrijg de beste start en eind tijd, het laagste gemiddelde, en de laagste prijs voor het blok van n uren
        beste_start, beste_eind, laagste_gemiddelde, laagste_prijs = laagste_verbruik_uren(prijzen_dict, n)  
        
        # Als een geldig blok is gevonden, print de resultaten
        if beste_start is not None:
            eind_uur = beste_eind % 24
            tekst = f"Beste blok van {n} uur(en): {beste_start}:00 - {eind_uur}:00\n"
            tekst += f"  - Gemiddelde werkelijke prijs: {laagste_prijs:.2f} €/MWh\n"

            # Sla de tekst op in de juiste variabele afhankelijk van het blok
            if n == 1:
                blok_1_resultaat = tekst
            elif n == 2:
                blok_2_resultaat = tekst
            elif n == 3:
                blok_3_resultaat = tekst
    # Print de resultaten van de drie blokken    
    if blok_1_resultaat:
        print(blok_1_resultaat)
    
    if blok_2_resultaat:
        print(blok_2_resultaat)
    
    if blok_3_resultaat:
        print(blok_3_resultaat)

    # Bereken de gemiddelde prijs voor de dag
    gemiddelde_prijs = np.mean(list(prijzen_dict.values()))
    # Print de gemiddelde prijs per uur
    print(f"\nGemiddelde prijs per uur: {gemiddelde_prijs:.2f} €/MWh")
    print("Prijzen per uur:", prijzen_dict)  # Print de prijzen per uur

# **Voer de analyse uit voor vandaag en morgen**
verwerk_prijzen("today")  # Verwerk en toon de resultaten voor vandaag
verwerk_prijzen("tomorrow")  # Verwerk en toon de resultaten voor morgen
