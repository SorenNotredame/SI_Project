
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
                console.log(data)     
                //checken manueele override voor elk type        
                if (data["a_manueel"] != document.getElementById("switch-a").checked) {
                    document.getElementById("switch-a").checked = data["a_manueel"]
                    toggleDevice("a", false)
                }
                if (data["b_manueel"] != document.getElementById("switch-b").checked) {
                    document.getElementById("switch-b").checked = data["b_manueel"]
                    toggleDevice("b", false)
                }
                
                if (data["c_manueel"] != document.getElementById("switch-c").checked) {
                    document.getElementById("switch-c").checked = data["c_manueel"]
                    toggleDevice("c", false)
                }
                // kwartiervermogen gewenst aanpassen
                document.getElementById("kwartiervermogen-slider").value = data["kwartiervermorgen_gewenst"]
                updateKwartiervermogen(data["kwartiervermorgen_gewenst"])
                // hoogste kwartiervermogen aanpassen
                document.getElementById("hoogste-kwartiervermogen").textContent = data["hoogste_kwartiervermogen"]
                
                
                // Actieve status bijwerken voor A met controle van override
            if (data["a_manueel"]) {
                document.getElementById("status-label-a").classList.remove("active");
                document.getElementById("status-label-a").textContent = "Niet actief";
            } else {
                if (data["a_actief"]) {
                    document.getElementById("status-label-a").classList.remove("active");
                    document.getElementById("status-label-a").textContent = "Niet actief";
                } else {
                    document.getElementById("status-label-a").classList.add("active");
                    document.getElementById("status-label-a").textContent = "Actief";
                }
            }

            // Actieve status bijwerken voor B met controle van override
            if (data["b_manueel"]) {
                document.getElementById("status-label-b").classList.remove("active");
                document.getElementById("status-label-b").textContent = "Niet actief";
            } else {
                if (data["b_actief"]) {
                    document.getElementById("status-label-b").classList.remove("active");
                    document.getElementById("status-label-b").textContent = "Niet actief";
                } else {
                    document.getElementById("status-label-b").classList.add("active");
                    document.getElementById("status-label-b").textContent = "Actief";
                }
            }

            // Actieve status bijwerken voor C met controle van override
            if (data["c_manueel"]) {
                document.getElementById("status-label-c").classList.remove("active");
                document.getElementById("status-label-c").textContent = "Niet actief";
            } else {
                if (data["c_actief"]) {
                    document.getElementById("status-label-c").classList.remove("active");
                    document.getElementById("status-label-c").textContent = "Niet actief";
                } else {
                    document.getElementById("status-label-c").classList.add("active");
                    document.getElementById("status-label-c").textContent = "Actief";
                }
            }
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
            setTimeout(get_info,200)
        }
    }

function logout() {
    localStorage.removeItem("loggedIn"); // Verwijder login status
    window.location.href = "login.html"; // Redirect naar login
}


    // Bij het laden van de pagina de statussen ophalen
    document.addEventListener("DOMContentLoaded", updateDeviceStatus);





