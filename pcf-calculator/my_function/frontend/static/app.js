document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    const uploadButton = document.getElementById('upload-button');
    const fileNameDisplay = document.getElementById('file-name');
    const loadingIndicator = document.getElementById('loading-indicator');

    let selectedMaterial = '';
    let selectedThickness = '';
    let selectedLaser = '';
    let selectedGas = '';

    const material_name_id = {"Aluminium": "AlMg3", "Stahl": "1.0038", "Kupfer": "Cu", "Messing": "CuZn"};
    const gas_name_id = {"Stickstoff": "N2", "Sauerstoff": "O2", "Druckluft":"Druckluft"};

    $('#material').on('select2:select', event => selectedMaterial = event.target.value);
    $('#thickness').on('select2:select', event => selectedThickness = event.target.value);
    $('#laser').on('select2:select', event => selectedLaser = event.target.value);
    $('#gas').on('select2:select', event => selectedGas = event.target.value);

    function validateFile(file) {
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (fileExtension !== 'lst' && fileExtension !== 'geo') {
            alert("Ungültige Dateiendung. Nur .lst und .geo Dateien werden unterstützt.");
            return false;
        }
        fileNameDisplay.textContent = `Ausgewählte Datei: ${file.name}`;
        return true;
    }

    function uploadFile(file) {
        loadingIndicator.style.display = 'block';
        sendGeoPcfPostRequest(file).finally(() => loadingIndicator.style.display = 'none');
    }

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file && validateFile(file)) {
            fileNameDisplay.textContent = `Ausgewählte Datei: ${file.name}`;
        } else {
            fileInput.value = "";
            fileNameDisplay.textContent = "";
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragging');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragging');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragging');

        const file = e.dataTransfer.files[0];
        if (file && validateFile(file)) {
            fileInput.files = e.dataTransfer.files;
            uploadFile(file);
        }
    });

    uploadButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Bitte wähle eine Datei aus.");
            return;
        }
        uploadFile(file);
    });

    async function sendGeoPcfPostRequest(file) {
        const route = file.name.endsWith('.lst') ? '/lst/pcf' : '/geo/pcf';
        const reader = new FileReader();
        reader.readAsArrayBuffer(file);

        reader.onload = async () => {
            const uint8Array = new Uint8Array(reader.result);

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
});
