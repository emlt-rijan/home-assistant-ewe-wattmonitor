<p align="center">
  <img src="https://raw.githubusercontent.com/emlt-rijan/home-assistant-ewe-wattmonitor/main/custom_components/ewe_wattmonitor/brand/logo.png" alt="EWE WattMonitor" width="420">
</p>

# EWE WattMonitor für Home Assistant

Diese Custom Integration liest aktuelle Energie- und Wetterwerte aus dem öffentlichen WattMonitor von EWE NETZ aus und stellt sie als Sensoren in Home Assistant bereit.

Die Integration ist HACS-kompatibel und wird über die Home-Assistant-Oberfläche eingerichtet.

## Status

Version 0.1.1 aktualisiert die geprüfte Gemeindeliste. Die Integration nutzt die öffentlich erreichbare API des WattMonitors.

## Disclaimer

Dieses Projekt ist ein privates, inoffizielles Open-Source-Projekt und steht in keiner Verbindung zu EWE NETZ, EWE AG oder verbundenen Unternehmen. Es ist kein offizielles Produkt von EWE NETZ und wird weder von EWE NETZ noch von EWE AG unterstützt, geprüft oder betrieben.

Das Projekt nutzt ausschließlich öffentlich zugängliche Datenquellen des WattMonitors und benötigt keine persönlichen EWE-Zugangsdaten. Es werden keine Logos oder sonstigen geschützten grafischen Assets von EWE NETZ oder EWE AG verwendet; Marken- und Unternehmensnamen werden nur beschreibend zur Einordnung der Datenquelle genannt.

## Unterstützte Gemeinden

Die Integration enthält eine geprüfte Liste von Gemeinden, für die die WattMonitor-API Daten liefert. Die Liste wird aus amtlichen Gemeindeschlüsseln aufgebaut und gegen die öffentlichen WattMonitor-Gemeinderouten validiert.

Aktuell unterstützte Gemeinden: 306 im EWE-NETZ-Gebiet in Niedersachsen. Die vollständige Liste liegt in [supported_municipalities.txt](supported_municipalities.txt).

Die EWE-Stromgebiete für Vertriebstarife sind breiter als der öffentliche WattMonitor. Nicht jeder Ort, an dem EWE Stromtarife anbietet, hat auch eine WattMonitor-Gemeindeseite.

Für Jork lautet der Gemeindeschlüssel `03359028`.

## Installation über HACS

1. HACS öffnen.
2. Benutzerdefiniertes Repository hinzufügen.
3. Repository-URL eintragen:

   `https://github.com/emlt-rijan/home-assistant-ewe-wattmonitor`

4. Kategorie `Integration` auswählen.
5. Integration installieren.
6. Home Assistant neu starten.
7. Unter `Einstellungen` > `Geräte & Dienste` die Integration `EWE WattMonitor` hinzufügen.

## Einrichtung

Bei der Einrichtung wird die Gemeinde direkt aus einem Dropdown der unterstützten WattMonitor-Gemeinden ausgewählt. Die Integration speichert den amtlichen Gemeindeschlüssel intern, prüft ihn gegen die mitgelieferte Liste und verwendet den Gemeindenamen automatisch als Namen des Eintrags.
Vor dem Speichern prüft die Integration, ob die WattMonitor-API für die ausgewählte Gemeinde erreichbar ist und Daten liefert.

Nach erfolgreicher Einrichtung werden Sensoren für die gewählte Gemeinde angelegt.
Die Integration stellt Diagnosedaten für den eingerichteten Eintrag bereit, damit Verbindungs- und Datenprobleme in Home Assistant nachvollziehbar bleiben.

## Sensoren

Die Integration stellt folgende Sensoren bereit:

- Verbrauch
- Erzeugung
- Saldo
- PV-Erzeugung
- Wind-Erzeugung
- Biomasse-Erzeugung
- Wasser-Erzeugung
- Sonstige Erzeugung
- Anteil erneuerbar
- Temperatur
- Windgeschwindigkeit
- Windrichtung
- Bewölkung
- Niederschlag

Der Saldo wird lokal berechnet:

`ErzeugungSumme - VerbrauchSumme`

Ein negativer Wert bedeutet, dass die Gemeinde aktuell mehr verbraucht als erzeugt.

Der Anteil erneuerbar wird als Verhältnis von aktueller Erzeugung zu aktuellem Verbrauch berechnet.

## Datenquelle

Die Daten stammen von:

`https://wattmonitor.ewe-netz.de/`

Die Integration ruft den API-Endpunkt des WattMonitors direkt ab. Es wird keine HTML-Seite gescrapt.

## Hinweise

- Die Aktualisierung erfolgt alle 15 Minuten.
- Wenn die EWE-API für eine Gemeinde keine Daten liefert, kann diese Gemeinde nicht eingerichtet werden.
- Änderungen an der EWE-API können Anpassungen an der Integration erforderlich machen.

## Entwicklung

Die Integration liegt unter:

`custom_components/ewe_wattmonitor`

Für eine lokale Prüfung kann mindestens die Python-Syntax kompiliert werden:

```bash
python3 -m compileall custom_components
```

## Lizenz

MIT
