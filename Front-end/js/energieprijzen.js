document.addEventListener("DOMContentLoaded", function () {
    fetch("energieprijzen.json")
        .then(response => response.json())
        .then(data => {
            updateEnergieprijzen(data);
        })
        .catch(error => console.error("Fout bij ophalen van JSON:", error));
});

function updateEnergieprijzen(data) {
    // Vandaag
    const goedkoopsteUurVandaag = formatBlok(data.vandaag.goedkoopste_uur);
    const prijsVandaag = Object.values(data.vandaag.goedkoopste_uur)[0];
    document.querySelector("#beste_uur_vandaag").textContent = `${goedkoopsteUurVandaag} (€${prijsVandaag.toFixed(2)})`;

    const goedkoopste2UurVandaag = formatBlok(data.vandaag.goedkoopste_2u_blok);
    const gemiddeldePrijs2Uur = berekenGemiddeldePrijs(Object.keys(data.vandaag.goedkoopste_2u_blok), data.vandaag.prijzen);
    document.querySelector("#beste_twee_uur_vandaag").textContent = `${goedkoopste2UurVandaag} (Gemiddeld: €${gemiddeldePrijs2Uur.toFixed(2)})`;

    const goedkoopste3UurVandaag = formatBlok(data.vandaag.goedkoopste_3u_blok);
    const gemiddeldePrijs3Uur = berekenGemiddeldePrijs(Object.keys(data.vandaag.goedkoopste_3u_blok), data.vandaag.prijzen);
    document.querySelector("#beste_drie_uur_vandaag").textContent = `${goedkoopste3UurVandaag} (Gemiddeld: €${gemiddeldePrijs3Uur.toFixed(2)})`;

// Controleer of er gegevens zijn voor morgen
    if (data.morgen && Object.keys(data.morgen.prijzen).length > 0) {
        const goedkoopsteUurMorgen = formatBlok(data.morgen.goedkoopste_uur);
        const prijsMorgen = Object.values(data.morgen.goedkoopste_uur)[0];
        document.querySelector("#beste_uur_morgen").textContent = `${goedkoopsteUurMorgen} (€${prijsMorgen.toFixed(2)})`;

        const goedkoopste2UurMorgen = formatBlok(data.morgen.goedkoopste_2u_blok);
        const gemiddeldePrijs2UurMorgen = berekenGemiddeldePrijs(Object.keys(data.morgen.goedkoopste_2u_blok), data.morgen.prijzen);
        document.querySelector("#beste_twee_uur_morgen").textContent = `${goedkoopste2UurMorgen} (Gemiddeld: €${gemiddeldePrijs2UurMorgen.toFixed(2)})`;

        const goedkoopste3UurMorgen = formatBlok(data.morgen.goedkoopste_3u_blok);
        const gemiddeldePrijs3UurMorgen = berekenGemiddeldePrijs(Object.keys(data.morgen.goedkoopste_3u_blok), data.morgen.prijzen);
        document.querySelector("#beste_drie_uur_morgen").textContent = `${goedkoopste3UurMorgen} (Gemiddeld: €${gemiddeldePrijs3UurMorgen.toFixed(2)})`;
    } else {
        document.querySelector("#beste_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
        document.querySelector("#beste_twee_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
        document.querySelector("#beste_drie_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
    }


function formatBlok(blok) {
    const uren = Object.keys(blok);
    if (uren.length > 1) {
        return `${uren[0]} tot ${getEindTijd(uren[uren.length - 1])}`;
    }
    return `${uren[0]} tot ${getEindTijd(uren[0])}`;
}

function getEindTijd(startTijd) {
    const [uur, minuut] = startTijd.split(":").map(Number);
    return `${String(uur + 1).padStart(2, "0")}:${String(minuut).padStart(2, "0")}`;
}

function berekenGemiddeldePrijs(uren, prijzen) {
    const totaal = uren.reduce((sum, uur) => sum + prijzen[uur], 0);
    return totaal / uren.length;
}
