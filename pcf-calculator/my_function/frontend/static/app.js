document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    const uploadButton = document.getElementById('upload-button');
    const fileNameDisplay = document.getElementById('file-name');
    const loadingIndicator = document.getElementById('loading-indicator');
    let selectedMaterial = '';
    let selectedThickness = '';
    let selectedLaser = '';
    let selectedGas = '';
    let material_name_id = {
        "Aluminium": "AlMg3", 
        "Stahl": "1.0038",
        "Kupfer": "Cu",
        "Messing": "CuZn"
    };
    let gas_name_id={
        "Stickstoff": "N2",
        "Sauerstoff": "O2"

    };
    $('#material').on('select2:select', function (event) {
        selectedMaterial = event.target.value;
        console.log("Material ausgewählt:", selectedMaterial);
    });

    $('#thickness').on('select2:select', function (event) {
        selectedThickness = event.target.value;
        console.log("Dicke ausgewählt:", selectedThickness);
    });

    $('#laser').on('select2:select', function (event) {
        selectedLaser = event.target.value;
        console.log("Laser ausgewählt:", selectedLaser);
    });

    $('#gas').on('select2:select', function (event) {
        selectedGas = event.target.value;
        console.log("Gas ausgewählt:", selectedGas);
    });

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        fileExtension = file.name.split('.').pop().toLowerCase();
        if (fileExtension !== 'lst' &&  fileExtension !== 'geo') {
            alert("Ungültige Dateiendung. Nur .lst und .geo Dateien werden unterstützt.");
            fileInput.value = "";
            return;
        }
        if (file) {
            fileNameDisplay.textContent = `Ausgewählte Datei: ${file.name}`;
        } else {
            fileNameDisplay.textContent = "";
        }
    });
    
    uploadButton.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Bitte wähle eine Datei aus.");
            return;
        }
        console.log("Zeige Ladeindikator an");
        loadingIndicator.style.display = 'block';
        try {
            await sendGeoPcfPostRequest(file);
        } catch (error) {
            console.error("Fehler beim Upload:", error);
            alert("Ein Fehler ist aufgetreten!");
        } finally {
            loadingIndicator.style.display = 'none';
        }
    });

    async function sendGeoPcfPostRequest(file) {
        const fileExtension = file.name.split('.').pop().toLowerCase();
        let route;

        if (fileExtension === 'lst') {
            route = '/lst/pcf';
        } else if (fileExtension === 'geo') {
            route = '/geo/pcf';
        } else {
            alert("Ungültige Dateiendung. Nur .lst und .geo Dateien werden unterstützt.");
            return;
        }

        const reader = new FileReader();
        reader.readAsArrayBuffer(file);

        reader.onload = async function () {
            const geoData = reader.result;
            const uint8Array = new Uint8Array(geoData);

            try {
                const response = await fetch(route, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/octet-stream',
                        'Filename': file.name,
                        'Materialid': material_name_id[selectedMaterial],
                        'Thickness': selectedThickness,
                        'Laser': selectedLaser,
                        'Gasid': gas_name_id[selectedGas]
                    },
                    body: uint8Array
                });

                if (response.ok) {
                    alert("Datei erfolgreich hochgeladen!");
                    window.location.href = response.url;
                } else {
                    const result = await response.json();
                    alert(`Fehler: ${result.error}`);
                }
            } catch (error) {
                console.error("Upload-Fehler:", error);
                alert("Ein Netzwerkfehler ist aufgetreten!");
            }
        };
    }
})