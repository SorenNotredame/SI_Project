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
    const goedkoopsteUurVandaag = Object.keys(data.vandaag.goedkoopste_uur)[0];
    const prijsVandaag = data.vandaag.goedkoopste_uur[goedkoopsteUurVandaag];
    document.querySelector("#beste_uur_vandaag").textContent = `${goedkoopsteUurVandaag} (€${prijsVandaag.toFixed(2)})`;

    const goedkoopste2UurVandaag = Object.keys(data.vandaag.goedkoopste_2u_blok);
    document.querySelector("#beste_twee_uur_vandaag").textContent = goedkoopste2UurVandaag.map(uur => {
        return `${uur} (€${data.vandaag.prijzen[uur].toFixed(2)})`;
    }).join(", ");

    const goedkoopste3UurVandaag = Object.keys(data.vandaag.goedkoopste_3u_blok);
    document.querySelector("#beste_drie_uur_vandaag").textContent = goedkoopste3UurVandaag.map(uur => {
        return `${uur} (€${data.vandaag.prijzen[uur].toFixed(2)})`;
    }).join(", ");
    
    // Morgen
    if (data.morgen) {
        const goedkoopsteUurMorgen = Object.keys(data.morgen.goedkoopste_uur)[0];
        const prijsMorgen = data.morgen.goedkoopste_uur[goedkoopsteUurMorgen];
        document.querySelector("#beste_uur_morgen").textContent = `${goedkoopsteUurMorgen} (€${prijsMorgen.toFixed(2)})`;

        const goedkoopste2UurMorgen = Object.keys(data.morgen.goedkoopste_2u_blok);
        document.querySelector("#beste_twee_uur_morgen").textContent = goedkoopste2UurMorgen.map(uur => {
            return `${uur} (€${data.morgen.prijzen[uur].toFixed(2)})`;
        }).join(", ");

        const goedkoopste3UurMorgen = Object.keys(data.morgen.goedkoopste_3u_blok);
        document.querySelector("#beste_drie_uur_morgen").textContent = goedkoopste3UurMorgen.map(uur => {
            return `${uur} (€${data.morgen.prijzen[uur].toFixed(2)})`;
        }).join(", ");
    } else {
        document.querySelector("#beste_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
        document.querySelector("#beste_twee_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
        document.querySelector("#beste_drie_uur_morgen").textContent = "Gegevens nog niet beschikbaar";
    }
}
