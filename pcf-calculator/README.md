# Bachelorarbeit: Entwicklung einer Softwarelösung zur Berechnung eines Product Carbon Footprints von Blechkomponenten basierend auf Betriebsdaten komplexer mechatronischer Systeme



## Techstack


Die Anwendung wurde im Backend mit dem Python-Webframework Flask entwickelt. Obwohl keine dauerhafte Persistierung erforderlich ist, wird die In-Memory-Datenbank Redis genutzt, um Daten zwischenzuspeichern. Das Frontend wurde mit nativem JavaScript, HTML und CSS umgesetzt.


## Anforderungen

Den PCF (Product Carbon Footprint) basierend auf einer .GEO-Datei vollautomatisch zu berechnen. Die Anwenund ist darauf ausgelegt ein moderates Anfragenpensum von 100 Requests pro Tag zu verarbeiten.
