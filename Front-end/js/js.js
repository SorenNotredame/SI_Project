
function updateKwartiervermogen(value) {
    // Update de waarde op de pagina
    document.getElementById('kwartiervermogen-waarde').innerText = value;

    // Update de CSS variabele voor de kleur van de slider
    document.documentElement.style.setProperty('--slider-value', (value - 2500) / (10000 - 2500) * 100 + '%');
    send_info();
}

    let deviceStatuses = {
        a: true,  // Type A is actief
        b: false, // Type B is niet actief
        c: true   // Type C is actief
    };
    

    function get_info() {
        fetch('http://94.110.252.19:5000/get_values', {method: 'GET'})
            .then(response => response.json())
            .then(data => {                
                if (data["a"] != document.getElementById("switch-a").checked) {
                    document.getElementById("switch-a").checked = data["a"]
                    toggleDevice("a", false)
                }
                if (data["b"] != document.getElementById("switch-b").checked) {
                    document.getElementById("switch-b").checked = data["b"]
                    toggleDevice("b", false)
                }
                if (data["c"] != document.getElementById("switch-c").checked) {
                    document.getElementById("switch-c").checked = data["c"]
                    toggleDevice("c", false)
                }
                document.getElementById("kwartiervermogen-slider").value = data["kwartiervermorgen_gewenst"]
                console.log(deviceStatuses)
                updateKwartiervermogen(data["kwartiervermorgen_gewenst"])
           
                document.getElementById("hoogste-kwartiervermogen").value = data["hoogste_kwartiervermogen"]
                        console.log(deviceStatuses)
		 })
            .catch(error => console.error('Error:', error));
    }

    // Functie om de statuslabels aan te passen
    function updateDeviceStatus() {
        get_info()
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

    // Functie om info door te geven aan Falsk
    function send_info() {
        data = {"kwartiervermorgen_gewenst": document.getElementById("kwartiervermogen-waarde").innerHTML,
                "a": document.getElementById("switch-a").checked,
                "b": document.getElementById("switch-b").checked,
                "c": document.getElementById("switch-c").checked}

        console.log(data)
        fetch('http://94.110.252.19:5000/data', {
            method: "POST",
            mode: "cors",
            body: JSON.stringify(data),
            cache: "no-cache",
            headers: new Headers({
            "content-type": "application/json"
            })
        })
    }

    // Functie om de schakelaar en lampje te updaten
    function toggleDevice(type, send=true) {
        let switchElement = document.getElementById(`switch-${type}`);
        let statusLight = document.getElementById(`status-${type}`);
        let statusText = document.getElementById(`text-${type}`);

        if (switchElement.checked) {
            
            statusText.innerText = "Manuele mode ON";
        } else {
            
            statusText.innerText = "Manuele mode OFF ";
        }
        if (send) {
            send_info()
        }
    }

function logout() {
    localStorage.removeItem("loggedIn"); // Verwijder login status
    window.location.href = "login.html"; // Redirect naar login
}


    // Bij het laden van de pagina de statussen ophalen
    document.addEventListener("DOMContentLoaded", updateDeviceStatus);





