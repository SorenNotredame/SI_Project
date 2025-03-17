
function updateKwartiervermogen(value) {
    // Update de waarde op de pagina
    document.getElementById('kwartiervermogen-waarde').innerText = value;

    // Update de CSS variabele voor de kleur van de slider
    document.documentElement.style.setProperty('--slider-value', (value - 2500) / (10000 - 2500) * 100 + '%');
}

    let deviceStatuses = {
        a: true,  // Type A is actief
        b: false, // Type B is niet actief
        c: true   // Type C is actief
    };

    // Functie om de statuslabels aan te passen
    function updateDeviceStatus() {
        for (let type in deviceStatuses) {
            let statusLabel = document.getElementById(`status-label-${type}`);

            if (deviceStatuses[type]) {
                statusLabel.innerText = "Actief";
                statusLabel.classList.add("active");
            } else {
                statusLabel.innerText = "Niet Actief";
                statusLabel.classList.remove("active");
            }
        }
    }

    // Functie om de schakelaar en lampje te updaten
    function toggleDevice(type) {
        let switchElement = document.getElementById(`switch-${type}`);
        let statusLight = document.getElementById(`status-${type}`);
        let statusText = document.getElementById(`text-${type}`);

        if (switchElement.checked) {
            statusLight.style.backgroundColor = "green"; // AAN
            statusText.innerText = "Aan";
        } else {
            statusLight.style.backgroundColor = "red"; // UIT
            statusText.innerText = "Uit";
        }
    }

function logout() {
    localStorage.removeItem("loggedIn"); // Verwijder login status
    window.location.href = "login.html"; // Redirect naar login
}


    // Bij het laden van de pagina de statussen ophalen
    document.addEventListener("DOMContentLoaded", updateDeviceStatus);



