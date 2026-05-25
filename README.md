<p align="center">
  <img src="https://raw.githubusercontent.com/emlt-rijan/home-assistant-ewe-wattmonitor/main/custom_components/ewe_wattmonitor/brand/logo.png" alt="EWE WattMonitor" width="420">
</p>

# EWE WattMonitor für Home Assistant

Diese Custom Integration liest aktuelle Energie- und Wetterwerte aus dem öffentlichen WattMonitor von EWE NETZ aus und stellt sie als Sensoren in Home Assistant bereit.

Die Integration ist HACS-kompatibel und wird über die Home-Assistant-Oberfläche eingerichtet.

## Status

Version 0.1.4 ist eine erste veröffentlichbare Version. Die Integration nutzt die öffentlich erreichbare API des WattMonitors. Sie ist kein offizielles Produkt von EWE NETZ.

## Unterstützte Gemeinden

Die Integration enthält eine geprüfte Liste von Gemeinden, für die die WattMonitor-API Daten liefert. Die Liste wird aus amtlichen Gemeindeschlüsseln aufgebaut und gegen die öffentlichen WattMonitor-Gemeinderouten validiert.

Aktuell unterstützte Gemeinden: 304 im EWE-NETZ-Gebiet in Niedersachsen. Die vollständige Liste liegt in [supported_municipalities.txt](supported_municipalities.txt).

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

Bei der Einrichtung kann nach Gemeinde, Landkreis oder Gemeindeschlüssel gesucht werden. Anschließend wird die passende Gemeinde aus einem gefilterten Dropdown ausgewählt. Die Integration speichert den amtlichen Gemeindeschlüssel intern und prüft ihn gegen die mitgelieferte Liste.

Nach erfolgreicher Einrichtung werden Sensoren für die gewählte Gemeinde angelegt.

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
