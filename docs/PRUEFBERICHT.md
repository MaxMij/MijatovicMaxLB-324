# Prüfung der LB 324

Prüfstand: 2. November 2026, Europe/Zurich. Grundlage sind `LB-324.docx`, das allgemeine `M324_Bewertungsraster.xlsx`, die vorhandenen Dateien und die live gelesenen GitHub-Daten. Bewertet wird durch die Lehrperson; eine maximale Punktzahl lässt sich ohne die offenen Live-Nachweise und wegen der historischen Abweichung nicht zusichern.

## Ausgangslage und Bewertung

Die konkrete Aufgabenstellung vergibt bei zehn Kriterien mit je drei Punkten und doppelter Gewichtung von Aufgabe 5 insgesamt **33 gewichtete Punkte**. Das separate Excel enthält allgemeine Kompetenzstufen mit anderen Gewichtungen; es ersetzt die konkrete LB-Aufgabenstellung nicht.

| Kriterium | Gewichtete Maximalpunkte | Befund und Nachweis | Noch erforderlich |
| --- | ---: | --- | --- |
| 0 Administration | 3 | Öffentlicher Repository-Name und Projektordner stimmen; README vorhanden | Moodle-URL und endgültiges ZIP nach Integration abgeben |
| 1-1 Labels und Vorlage | 3 | Drei geforderte Labels auf GitHub vorhanden; Vorlage mit Satzschema und Akzeptanzkriterien vorhanden | Bei neuen Issues den passenden Typ manuell etikettieren |
| 2-1 Formatierung bei Commit | 3 | Black auf `pre-commit` konfiguriert; Hook installiert; manuelle Ausführung erfolgreich | Bei jeder weiteren Arbeitskopie neu installieren |
| 2-2 Tests bei Push | 3 | pytest auf `pre-push`, `always_run: true`, keine Dateinamen als Parameter; Hook installiert und erfolgreich ausgeführt | Beim tatsächlichen Push aktivierte virtuelle Umgebung verwenden |
| 2-3 Installationsanleitung | 3 | Beide Hook-Arten, virtuelle Umgebung und Umgang mit Black-Änderungen erklärt | Bei einer frischen Arbeitskopie erneut installieren |
| 3-1 PR-Tests auf richtigem Ast | 3 | Ein Testjob, ausschliesslich PRs nach `dev`; PR #2 hatte erfolgreichen Check | Korrektur-PR nach `dev` grün prüfen |
| 4-1 Funktionierende Auslieferung | 3 | Bisherige Runs fehlgeschlagen; lokal vorbereitetes Laufzeit-ZIP mit Versionsprüfung | Azure bereitstellen, vollständig grünen Run und Live-Test nachweisen |
| 4-2 Geheimnisse korrekt übertragen | 3 | `.env` ist nicht versioniert und wird nicht paketiert; genaue App-Settings-Anleitung vorhanden | Azure-App-Settings und Repository-Secret tatsächlich einrichten |
| 4-3 Auslieferung vom richtigen Ast | 3 | Push-Trigger ausschliesslich `main`, Tests vor Deployment | Erfolgreichen Run nach Merge in `main` sichern |
| 5-1 GitHub Flow | 6 | Happiness-Ast erhalten; Issue #1, PR #2 nach `dev`, PR #3 nach `main`; Korrektur-Issue #4 vor neuen Änderungen | Historische Abweichung offenlegen; neuen Flow bis Deployment abschliessen |

## Verifizierter GitHub-Stand vor der Korrektur

- Repository `MaxMij/MijatovicMaxLB-324` öffentlich, Default-Ast `main`.
- `main`: `677a81a`; `dev`: `274b81d`; `feature/happiness-entry`: `71b30ef`.
- [PR #2](https://github.com/MaxMij/MijatovicMaxLB-324/pull/2) wurde nach `dev` gemergt; der zugehörige Testlauf [39962468120](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/39962468120) war erfolgreich.
- [PR #3](https://github.com/MaxMij/MijatovicMaxLB-324/pull/3) wurde nach `main` gemergt.
- [Deployment 39962685716](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/39962685716) scheiterte mit `No credentials found`. Die Liste der Repository-Actions-Secrets war leer.
- Die bisher in der README genannte App-Domäne war bei der Netzwerkprüfung nicht auflösbar. Ob eine App unter einer anderen Standarddomäne existiert, ist damit nicht geklärt.
- Azure CLI meldete `Please run 'az login'`. Azure-Ressourcen, App Settings und tatsächliche Standarddomäne konnten deshalb nicht eingesehen werden.
- Im lokalen `.git/hooks` lagen vor der Korrektur nur Beispiel-Hooks, keine aktiven Commit- oder Push-Hooks.
- Der klassische Branchschutz war für `dev` und `main` nicht eingerichtet (API: `Branch not protected`). Die automatische Branchlöschung war ausgeschaltet. Repository-Rulesets wurden durch diese beiden Abfragen nicht geprüft.

## Historische Abweichung

Der Happiness-Commit wurde am 23. Oktober 2026 um 15:20:27 Uhr erstellt, Issue #1 erst um 15:35:12 Uhr (Europe/Zurich). Die Aufgabenstellung verlangt ein Issue vor jeder Codeänderung. Die ursprüngliche Historie erfüllt diese Reihenfolge nicht. Spätere Dokumentation oder das Wiederöffnen des Issues kann die Reihenfolge nicht rückwirkend ändern.

[Issue #4](https://github.com/MaxMij/MijatovicMaxLB-324/issues/4) wurde vor den neuen Änderungen angelegt. Der neue Ast `feature/4-lb-quality` stammt von `dev`. Der ursprüngliche Happiness-Ast bleibt erhalten. Der neue Ablauf belegt die Korrektur; die ursprüngliche Abweichung bleibt sichtbar.

## Verbesserungen

- Server prüft vor jedem Anlegen eines Eintrags die Anmeldung.
- Fehlendes oder leeres konfiguriertes Passwort erlaubt keine Anmeldung; der vorherige feste Ersatzwert für den Sitzungsschlüssel entfällt. Azure verlangt explizit konfigurierte Zugangswerte.
- Inhalte werden getrimmt und auf 1 bis 5000 Zeichen begrenzt; nur die angebotenen Stimmungen werden angenommen.
- Abmeldung erfolgt per POST und entfernt den Sitzungszustand.
- Formulare haben zugeordnete Labels und eine mobile Viewport-Angabe; Zeilenumbrüche und lange Wörter werden lesbar dargestellt.
- Der vorgegebene Happiness-Test arbeitet mit einer angemeldeten Fixture. Regressionstests prüfen zusätzlich Login, Logout, Zugriffsschutz, Validierung, Darstellung und Paketinhalt.
- Deployment verwendet eine Positivliste der Laufzeitdateien. Commit-SHA und Prüfsumme machen das Artefakt nachvollziehbar; das Paket wird in GitHub Actions aufbewahrt.
- `/healthz` und die Prüfung nach dem Deployment vergleichen die laufende Version mit dem ausgelieferten Commit.
- README trennt belegte Ergebnisse von ausstehenden Schritten und beschreibt Azure, Fehlerdiagnose und Abgabe reproduzierbar.

## Nachweise vor Abgabe

1. Terminalausgabe der beiden Hook-Stufen und der vollständigen Testsuite sichern.
2. Screenshot oder Link des grünen Korrektur-PR-Checks nach `dev` sichern.
3. Screenshot oder Link des grünen Deployments vom endgültigen `main`-Commit sichern, einschliesslich Versionsprüfung.
4. App Settings nur mit verdeckten Werten und GitHub-Secrets nur mit ihren Namen dokumentieren. Weder Publish Profile noch Sitzungsschlüssel in Nachweise übernehmen.
5. Live-Anmeldung, Stimmungseintrag und Abmeldung durchführen. Die tatsächliche App-URL und Commit-SHA im folgenden Protokoll ergänzen.
6. Endgültiges ZIP auf Inhalt und Ordnernamen prüfen; URL und ZIP auf Moodle abgeben.

## Durchgeführte lokale Prüfungen

- Vollständige LB-Suite: **22 Tests bestanden** unter Python 3.11.
- Black: alle fünf Python-Dateien unverändert formatiert; Konfiguration von pre-commit gültig.
- Beide Git-Hooks wurden in dieser Arbeitskopie installiert. Die expliziten Stufen `pre-commit` und `pre-push` liefen erfolgreich.
- Workflow-Dateien als YAML gelesen: ausschliesslich PR nach `dev` beziehungsweise Push nach `main`; Shell-Blöcke mit `bash -n` geprüft. Der PR-Workflow enthält nur den Testjob.
- Das erzeugte ZIP wurde in einen frischen temporären Ordner entpackt und mit dem vorgesehenen Gunicorn-Einzelprozess gestartet. Über HTTP wurden Anmeldung, verweigerter unbefugter Schreibzugriff, Eintrag mit Stimmung und Abmeldung erfolgreich geprüft.
- Die Versionsprüfung akzeptierte den erwarteten Commit und lehnte einen abweichenden Commit ab.
- In simulierter Azure-Umgebung waren `Secure`, `HttpOnly` und `SameSite=Lax` an den Sitzungscookies vorhanden; ein fehlender erforderlicher Azure-Schlüssel verhinderte den App-Start.
- Separates Lernprojekt `zu-bbbearbeiten-stateless`: beide vorhandenen Tests bestanden. Dies ist ein technischer Teilnachweis, keine Bestätigung aller persönlichen Lernaufträge.
- Die erste Gunicorn-Prüfung hatte ein zu kurzes Startzeitlimit. Die Wiederholung mit ausreichender Startzeit war erfolgreich.

Die Netzwerkausführung der neuen GitHub-Actions und die echte Azure-Auslieferung sind durch diese lokalen Prüfungen nicht ersetzt. Der lokale Korrekturstand wird erst durch die noch offenen PRs in `dev` und `main` übernommen.

## Noch auszufüllendes Live-Protokoll

Diese Felder sind absichtlich offen, bis die Prüfung tatsächlich durchgeführt wurde:

- Tatsächliche App-URL:
- Endgültiger `main`-Commit:
- Link zum erfolgreichen Deployment:
- Datum und Uhrzeit der Live-Prüfung:
- Anmeldung mit dem vorgeschriebenen Passwort erfolgreich:
- Inhalt und Stimmung nach Speichern sichtbar:
- Abmeldung und unbefugter Schreibzugriff geprüft:
- `/healthz` entspricht dem endgültigen Commit:
- Moodle-URL und ZIP erfolgreich abgegeben:

## Verbleibende Grenzen

Die Anwendung ist ein Einzelprozess-Prototyp mit flüchtigem Speicher. Neustarts löschen die Einträge. Die LB fordert keine Datenbankmigration; es wurden keine dauerhafte Speicherung, Mehrbenutzerverwaltung oder Skalierung umgesetzt. Ein grüner lokaler Test beweist weder vorhandene Azure-Geheimnisse noch ein erfolgreiches Deployment. Die konkreten Bewertungspunkte für die Cloud bleiben bis zum Live-Nachweis offen.

## Inzwischen ausgeführte Azure-Einrichtung

Die vorhandene Web-App `mijatovicmaxlb-324` liegt in `mijatovicmaxlb-324_group`, Switzerland North, im bestehenden Gratisplan F1. Die tatsächliche Domäne lautet `mijatovicmaxlb-324-bvded0a9d4a0hucu.switzerlandnorth-01.azurewebsites.net`. Linux und Python 3.11 wurden geprüft. Der dokumentierte Gunicorn-Startbefehl ist gespeichert; HTTPS Only ist aktiv.

Die App Settings `PASSWORD`, `SECRET_KEY`, `SCM_DO_BUILD_DURING_DEPLOYMENT` und `WEBSITE_WEBDEPLOY_USE_SCM` wurden eingerichtet und durch Rücklesen bestätigt. Der Sitzungsschlüssel wurde zufällig erzeugt; geheime Werte werden hier nicht dokumentiert. Nach ausdrücklicher Benutzerfreigabe wurde SCM-Publish-Profile-Authentifizierung aktiviert und das Veröffentlichungsprofil direkt als `AZURE_WEBAPP_PUBLISH_PROFILE` im Repository gespeichert. Es wurde keine Profildatei im Projekt abgelegt.

Diese Einrichtung behebt die fehlenden Deployment-Zugangsdaten. Ein erfolgreicher Action-Run und der Live-Funktionstest sind zum Stand dieses Abschnitts noch ausstehend.
