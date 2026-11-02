# Prüfung der LB 324

Prüfstand: 2. November 2026, Europe/Zurich. Grundlage sind `LB-324.docx`, das allgemeine `M324_Bewertungsraster.xlsx`, die Projektdateien sowie live gelesene GitHub- und Azure-Daten. Die technische Einrichtung und der Live-Nachweis sind durchgeführt. Die Bewertung bleibt der Lehrperson vorbehalten; insbesondere bleibt die historische Abweichung bei Issue #1 sichtbar.

## Kriterien und aktueller Nachweis

Die konkrete Aufgabenstellung vergibt bei zehn Kriterien mit je drei Punkten und doppelter Gewichtung von Aufgabe 5 insgesamt **33 gewichtete Punkte**. Das separate Excel enthält allgemeine Kompetenzstufen mit anderen Gewichtungen und ersetzt die konkrete LB-Aufgabenstellung nicht.

| Kriterium | Gewichtete Maximalpunkte | Befund und Nachweis | Noch erforderlich |
| --- | ---: | --- | --- |
| 0 Administration | 3 | Öffentliches Repository und Projektordner korrekt benannt; README vorhanden | Repository-URL und endgültiges ZIP auf Moodle abgeben |
| 1-1 Labels und Vorlage | 3 | Drei geforderte Labels auf GitHub; Vorlage mit Satzschema und Akzeptanzkriterien | Bei neuen Issues den passenden Typ manuell setzen |
| 2-1 Formatierung bei Commit | 3 | Black auf pre-commit; Hook installiert und erfolgreich ausgeführt | Bei neuen Arbeitskopien erneut installieren |
| 2-2 Tests bei Push | 3 | pytest auf pre-push, always_run, keine Dateinamen; auch beim tatsächlichen Push erfolgreich | Virtuelle Umgebung bei Commit und Push aktivieren |
| 2-3 Installationsanleitung | 3 | Beide Hook-Arten, virtuelle Umgebung und Umgang mit Black-Änderungen beschrieben | Keine weitere Einrichtung in dieser Arbeitskopie |
| 3-1 PR-Tests auf richtigem Ast | 3 | Ein Testjob ausschliesslich für PRs nach dev; PR #5 erfolgreich | Branchschutz und grünen Status beibehalten |
| 4-1 Funktionierende Auslieferung | 3 | Referenzlauf 41412558040 vollständig erfolgreich; Browser- und HTTP-Live-Test bestanden | App für die Bewertung erreichbar lassen |
| 4-2 Geheimnisse korrekt übertragen | 3 | Azure App Settings eingerichtet; Publish Profile als Repository-Secret; .env weder versioniert noch paketiert | Geheimnisse aus Nachweisen und Abgabe ausschliessen |
| 4-3 Auslieferung vom richtigen Ast | 3 | Push auf main durch PR #6 löste erfolgreiche Auslieferung samt Versionsprüfung aus | Weitere Freigaben über denselben Ablauf |
| 5-1 GitHub Flow | 6 | Issue #4 vor Änderung; Feature von dev; PR #5 nach dev; PR #6 nach main; Happiness-Ast erhalten | Historische Abweichung von Issue #1 offenlegen |

## Ausgangslage vor der Korrektur

- Öffentliches Repository, Default-Ast main. Ursprüngliche Stände: main `677a81a`, dev `274b81d`, Happiness-Feature `71b30ef`.
- [PR #2](https://github.com/MaxMij/MijatovicMaxLB-324/pull/2) integrierte Happiness nach dev mit erfolgreichem Testcheck; [PR #3](https://github.com/MaxMij/MijatovicMaxLB-324/pull/3) übernahm den Stand nach main.
- [Deployment 39962685716](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/39962685716) scheiterte mit `No credentials found`; die Repository-Actions-Secrets waren leer.
- Die zuvor eingetragene kurze App-Domäne war nicht auflösbar. Im Portal wurde später die tatsächliche Domäne mit zusätzlichem Namensbestandteil festgestellt.
- Es lagen nur Beispiel-Hooks im lokalen Git-Hooks-Verzeichnis. Klassischer Branchschutz war nicht eingerichtet; automatische Branchlöschung war bereits ausgeschaltet.
- Der Server erlaubte POST-Schreibzugriffe ohne Anmeldung. Die beiden vorhandenen Tests deckten diese Lücke nicht ab.

## Historische Abweichung und Korrektur

Der Happiness-Commit wurde am 23. Oktober 2026 um 15:20:27 Uhr erstellt, Issue #1 erst um 15:35:12 Uhr (Europe/Zurich). Das widerspricht der geforderten Reihenfolge «Issue vor Codeänderung». Diese Historie wurde nicht rückdatiert oder umgeschrieben.

[Issue #4](https://github.com/MaxMij/MijatovicMaxLB-324/issues/4) entstand vor den neuen Änderungen. Der Ast `feature/4-lb-quality` wurde von dev erstellt. [PR #5](https://github.com/MaxMij/MijatovicMaxLB-324/pull/5) bestand den GitHub-Testcheck und wurde nach dev gemergt; [PR #6](https://github.com/MaxMij/MijatovicMaxLB-324/pull/6) integrierte den Stand nach main und schloss Issue #4. Der ursprüngliche Ast `feature/happiness-entry` bleibt erhalten.

Für die abschliessende Dokumentation wurde vor der Änderung [Issue #7](https://github.com/MaxMij/MijatovicMaxLB-324/issues/7) erstellt und ein neuer Feature-Ast von dev angelegt.

## Verbesserte Umsetzung

Der Server prüft die Anmeldung vor jedem Eintrag. Fehlende oder leere Passwortkonfiguration erlaubt keine Anmeldung. Inhalte werden getrimmt und auf 1 bis 5000 Zeichen begrenzt; nur die angebotenen Stimmungen werden angenommen. Logout entfernt die Sitzung per POST. Die Formulare haben zugeordnete Labels, mobile Viewport-Angaben und eine lesbare Darstellung langer Inhalte.

Der vorgegebene Happiness-Test arbeitet mit einer angemeldeten Fixture. Die Tests prüfen zusätzlich Login, Logout, Zugriffsschutz, Validierung, Darstellung und Paketinhalt. Auf Azure sind explizite Zugangswerte erforderlich; Sitzungscookies sind dort Secure, HttpOnly und SameSite Lax.

Die main-Action erstellt nach erfolgreichen Tests ein ZIP aus einer Positivliste der Laufzeitdateien, ergänzt den Git-Commit und berechnet eine SHA-256-Prüfsumme. Paket und Prüfsumme werden 30 Tage als GitHub-Actions-Artefakt aufbewahrt. Nach dem Deployment vergleicht die Action die tatsächlich laufende Revision unter `/healthz` mit dem freigegebenen Commit.

## Eingerichtete Azure und GitHub Umgebung

- Web-App: `mijatovicmaxlb-324`, Ressourcengruppe `mijatovicmaxlb-324_group`, Switzerland North.
- Bestehender Gratisplan F1; keine neue kostenpflichtige Ressource angelegt.
- Linux und Python 3.11; ein Gunicorn-Worker und ein Thread, Startbefehl gemäss README; HTTPS Only aktiv.
- App Settings `PASSWORD`, `SECRET_KEY`, `SCM_DO_BUILD_DURING_DEPLOYMENT` und `WEBSITE_WEBDEPLOY_USE_SCM` gesetzt und durch Rücklesen geprüft. Sitzungsschlüssel zufällig erzeugt; geheime Werte nicht dokumentiert.
- Nach ausdrücklicher Freigabe SCM-Publish-Profile-Authentifizierung aktiviert und Profil direkt als `AZURE_WEBAPP_PUBLISH_PROFILE` im zugehörigen GitHub-Repository gespeichert. Keine Profildatei im Projekt abgelegt.
- Branchschutz auf dev: Pull Request und erfolgreicher pytest-Check mit aktuellem Basisast erforderlich. Auf main: Pull Request erforderlich. Keine fremde Approval in dieser Einzelarbeit; Regeln auch für Administratoren aktiv, Force-Pushes und Branchlöschungen gesperrt.

## Durchgeführte lokale Prüfungen

- Vollständige LB-Suite: **22 Tests bestanden** unter Python 3.11.
- Black: alle fünf Python-Dateien unverändert formatiert; pre-commit-Konfiguration gültig.
- Beide lokalen Hook-Stufen erfolgreich; pre-push auch beim tatsächlichen GitHub-Push ausgeführt.
- YAML und Shell-Syntax geprüft: PR-Workflow testet ausschliesslich nach dev; Deployment-Trigger ausschliesslich main.
- Laufzeit-ZIP frisch entpackt und mit Gunicorn getestet: Anmeldung, Schreibschutz, Stimmung und Logout erfolgreich. Versionsvergleich akzeptierte die richtige und lehnte eine falsche Revision ab.
- Simulierter Azure-Start ohne erforderlichen Schlüssel verweigert; Cookie-Eigenschaften geprüft.
- Vollständiges Abgabearchiv auf Integrität, Ordnernamen, versteckte Konfigurationsdateien und Ausschluss lokaler Geheimnisse geprüft; 22 Tests im entpackten Archiv bestanden.
- Separates Lernprojekt: zwei vorhandene Tests bestanden; kein pauschaler Nachweis aller persönlichen Lernaufträge.

## Belegter Live Referenzlauf

- App-URL: <https://mijatovicmaxlb-324-bvded0a9d4a0hucu.switzerlandnorth-01.azurewebsites.net>
- Referenz-Commit: `43b1c4c5cb40a3d5a2d784dde436683a2b1259f4`.
- Vollständig erfolgreicher [Deployment-Run 41412558040](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/41412558040).
- Zusätzliche HTTP-Live-Prüfung: **2. November 2026, 09:27 Uhr, Europe/Zurich**. Maschinenlesbares Ergebnis: [live-check.json](live-check.json).
- Browserprüfung: Anmeldung mit dem vorgeschriebenen Passwort, Eintrag mit 😃, Anzeige von Text und Zeitstempel sowie Abmeldung erfolgreich.
- HTTP-Prüfung: falsches Passwort abgelehnt, direkte Schreibzugriffe ohne Sitzung und nach Logout umgeleitet; Kontrollanmeldung bestätigte, dass unbefugte Inhalte nicht gespeichert wurden.
- Health-Endpunkt HTTP 200; Revision entspricht dem Referenz-Commit. Die aktuelle Revision steht unter [/healthz](https://mijatovicmaxlb-324-bvded0a9d4a0hucu.switzerlandnorth-01.azurewebsites.net/healthz). Nach weiteren Dokumentations-Merges zeigt sie den neueren freigegebenen Commit; dieser Referenznachweis bleibt als zeitlich eingeordnete Prüfung erhalten.

## Noch durch den Lernenden abzugeben

Repository-URL und das aus dem endgültigen main-Stand erzeugte `MijatovicMaxLB-324.zip` auf Moodle abgeben und den erfolgreichen Upload kontrollieren. Das Archiv muss den Hauptordner `MijatovicMaxLB-324` enthalten, einschliesslich `.github` und Hook-Konfiguration, ohne `.env`, `.git`, virtuelle Umgebung oder Publish Profile. Die Aufgabenstellung verlangt das anschliessende Löschen der LB-Daten; erst nach bestätigter Abgabe selbst ausführen.

## Grenzen des Prototyps

Einträge liegen im Arbeitsspeicher eines Einzelprozesses. Neustarts und Deployments löschen sie; mehrere Worker oder Instanzen hätten getrennte Listen. Dauerhafte Speicherung und Mehrbenutzerverwaltung sind nicht umgesetzt. Die LB bewertet den CI/CD-Prozess. Das gemäss Auftrag öffentlich bekannte Passwort ist für die Schul-Demo vorgesehen.
