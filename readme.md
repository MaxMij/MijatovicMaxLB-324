# LB 324 Tagebbbuch

Max Mijatović · IM24c · Modul 324 DevOps

Repository: [MaxMij/MijatovicMaxLB-324](https://github.com/MaxMij/MijatovicMaxLB-324)

Laufende App: <https://mijatovicmaxlb-324-bvded0a9d4a0hucu.switzerlandnorth-01.azurewebsites.net>

Azure ist eingerichtet und die Auslieferung erfolgreich geprüft. Der [Referenzlauf vom 2. November 2026](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/41412558040) war einschliesslich Tests, Paketierung, Deployment und Versionsvergleich vollständig erfolgreich. Anmeldung, Stimmungseintrag, Logout und verweigerte unbefugte Schreibzugriffe wurden zusätzlich live geprüft; das [Prüfprotokoll](docs/live-check.json) enthält die Ergebnisse ohne Geheimnisse. Die aktuell laufende Revision ist unter [/healthz](https://mijatovicmaxlb-324-bvded0a9d4a0hucu.switzerlandnorth-01.azurewebsites.net/healthz) sichtbar und muss dem letzten erfolgreichen main-Deployment entsprechen.

Dieses Projekt bildet die LB mit `feature/*` → `dev` → `main` ab. Die ursprüngliche Happiness-Funktion ist implementiert. Eine nachträgliche Korrektur behebt den fehlenden serverseitigen Anmeldeschutz, erweitert die Prüfungen und liefert die Anwendung mit nachvollziehbarer Versionsprüfung nach Azure aus. [Prüfbericht und Kriterien](docs/PRUEFBERICHT.md) zeigen belegte Ergebnisse und ausstehende Nachweise.

## Lokal einrichten und starten

Im Projektordner `MijatovicMaxLB-324` ausführen, nicht im übergeordneten Modulordner:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Unter Windows stattdessen `py -3.11 -m venv .venv` und in PowerShell `.venv\Scripts\Activate.ps1` verwenden.

Falls `.env` noch nicht existiert: `.env.example` nach `.env` kopieren. Ein eigenes lokales `PASSWORD` und einen zufälligen `SECRET_KEY` eintragen. Einen Schlüssel erzeugen mit:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Die `.env` bleibt lokal und wird durch `.gitignore` ausgeschlossen. Ein vorhandenes `.env` nicht mit der Beispiel-Datei überschreiben. Bereits gesetzte Umgebungsvariablen haben Vorrang vor `.env`.

```bash
python -m flask --app app run
```

Anschliessend <http://127.0.0.1:5000> öffnen und mit dem lokalen Passwort anmelden. Eintrag und optionale Stimmung speichern; abmelden und kontrollieren, dass keine Einträge mehr angezeigt werden. `/healthz` liefert lokal `{"status":"ok","revision":"local"}`. In einem erstellten Azure-Paket zeigt `revision` den paketierten Git-Commit.

## Aufgabe 1 Anforderungen verwalten

Vorlage: [anforderung.md](.github/ISSUE_TEMPLATE/anforderung.md).

Jede Codeänderung beginnt mit einem GitHub-Issue. Aufbau der Anforderung:

**Zielsystem + Priorität + Systemaktivität + allfällige Ergänzungen + Funktionalität + Bedingungen.**

Priorität: `muss` = hoch, `soll` = mittel, `wird` = niedrig. Benutzerfunktion: «dem Benutzer die Möglichkeit bieten». Schnittstelle: «fähig sein». Zeitliche Bedingungen beginnen mit «wenn», logische mit «falls».

Die folgenden Labels sind im GitHub-Repository vorhanden und werden passend zum Issue manuell gesetzt:

- `Funktionale Anforderung`: Verhalten des Systems.
- `Qualitätsanforderung`: geforderte Qualität, etwa Sicherheit oder Zuverlässigkeit.
- `Randanforderung`: organisatorische oder technische Vorgabe.

Die Vorlage enthält Formulierungshilfe, Typauswahl und Akzeptanzkriterien. Checkboxes in einem Issue ersetzen das tatsächlich gesetzte GitHub-Label nicht.

### Vergleich der Anforderungsverwaltung

| Kriterium | GitHub Issues | Azure DevOps Boards | Jira |
| --- | --- | --- | --- |
| Einrichtung in diesem Projekt | Im bestehenden GitHub-Repository nutzbar | Zusätzliches Projekt und Berechtigungen einrichten | Zusätzliches Projekt und Berechtigungen einrichten |
| Strukturierung | Issues, Labels, Milestones, Projects | Work Items, Backlogs, Iterationen | Vorgänge, Vorgangstypen, konfigurierbare Workflows |
| Nachvollziehbarkeit | Direkte Verweise auf Commits und PRs im selben Repository | Verknüpfte Work Items und Code-Integration | Vorgangsreferenzen und Code-Integration |
| Eignung für diese LB | Erfüllt die ausdrücklich verlangte GitHub-Umsetzung | Sinnvoll bei einem bestehenden Azure-DevOps-Prozess | Sinnvoll bei einem bestehenden Jira-Prozess |

Für dieses Einzelprojekt fällt die Wahl auf GitHub Issues: Akzeptanzkriterien, Tests, Branches und PRs bleiben direkt verknüpft. Dieser Vergleich ist eine begründete Projektentscheidung; er behauptet keine praktisch durchgeführte Jira- oder Boards-Erprobung.

## Aufgabe 2 Git-Hooks installieren und nachweisen

Die aktivierte virtuelle Umgebung muss bei Commit und Push verfügbar sein. Einmal pro Arbeitskopie:

```bash
python -m pre_commit install --hook-type pre-commit --hook-type pre-push --install-hooks
```

Dank `default_install_hook_types` installiert auch `python -m pre_commit install` beide Hook-Typen. Die explizite Variante oben macht die Einrichtung nachvollziehbar.

| Git-Ereignis | Hook | Wirkung |
| --- | --- | --- |
| Jeder Commit mit Python-Dateien | `black`, Stufe `pre-commit` | Formatiert die betroffenen Python-Dateien automatisch |
| Jeder Push | `pytest-check`, Stufe `pre-push` | Führt die gesamte Testsuite aus; ein Fehler verhindert den Push |

Black kann beim ersten Commit Dateien verändern und den Commit deshalb stoppen. Die geänderten Dateien prüfen, erneut mit `git add` vormerken und nochmals committen. Tests sind in dieser LB bewusst beim **Push** eingehängt.

Manuelle Prüfung beider Stufen:

```bash
python -m pre_commit run --all-files --hook-stage pre-commit
python -m pre_commit run --all-files --hook-stage pre-push
python -m pytest -v
```

Die Tests nutzen eine eigene Konfiguration und funktionieren ohne das echte lokale Passwort. Der vorgegebene Happiness-Test bleibt erhalten; seine `client`-Fixture meldet sich vorher an. Zusätzliche Tests decken unbefugte Schreibzugriffe, fehlende Passwörter, ungültige Eingaben, Logout, HTML-Escaping und das Azure-Paket ab.

## Aufgabe 3 Tests auf Pull Requests nach dev

[test-pr-dev.yml](.github/workflows/test-pr-dev.yml) reagiert ausschliesslich auf `pull_request` mit Zielast `dev`. Der einzige Job richtet Python 3.11 ein, installiert die Abhängigkeiten und führt `pytest` aus. Er formatiert, paketiert und deployt nichts. Bei neuen Commits in einem geöffneten PR werden die Tests erneut ausgeführt.

Der Branchschutz ist eingerichtet: `dev` verlangt einen Pull Request und einen erfolgreichen `pytest`-Statuscheck bei aktuellem Basisast; `main` verlangt einen Pull Request. Es ist keine fremde Approval erforderlich. Die Regeln gelten auch für Administratoren; Force-Pushes und Branchlöschungen sind gesperrt. Die automatische Branchlöschung bleibt ausgeschaltet, damit der ursprüngliche Happiness-Ast erhalten bleibt.

## Aufgabe 4 Azure einrichten

### Web-App und Laufzeit

1. [Azure-Portal](https://portal.azure.com) öffnen und die bestehende Web-App suchen. Falls sie nicht existiert, **App Services → Erstellen → Web-App** verwenden.
2. Name `mijatovicmaxlb-324`, Veröffentlichung **Code**, Betriebssystem **Linux**, Runtime **Python 3.11**. Den in der Schulsubscription verfügbaren Gratisplan F1 wählen. Bei fehlender Verfügbarkeit zuerst Region oder Schulvorgaben prüfen; nicht ungeprüft einen kostenpflichtigen Plan anlegen.
3. Unter **Übersicht → Standarddomäne** die tatsächliche URL übernehmen. Falls der Name anders lautet, `app-name` in `deploy-main.yml` anpassen; die URL oben ebenfalls aktualisieren.
4. Unter **Einstellungen → Konfiguration / Stapeleinstellungen** diesen Startbefehl setzen und speichern:

```text
gunicorn --bind=0.0.0.0:8000 --workers 1 --threads 1 --timeout 600 app:app
```

`app:app` bezeichnet die Datei `app.py` und darin die Flask-Instanz `app`. Das Lernprojekt im anderen Modulordner verwendet dagegen `main:app`. Das Tagebbbuch speichert im Arbeitsspeicher; darum genau ein Worker und eine Instanz verwenden.

### Geheimnisse aus der lokalen Konfiguration übertragen

Unter **Einstellungen → Umgebungsvariablen → Anwendungseinstellungen** folgende Werte hinzufügen, anwenden und den Neustart abwarten:

| Name | Azure-Wert | Zweck |
| --- | --- | --- |
| `PASSWORD` | `MaxMij` | Passwort gemäss ausdrücklicher LB-Vorgabe: GitHub-Benutzername |
| `SECRET_KEY` | Ein eigener, zufälliger Schlüssel mit mindestens 32 Zufallsbytes | Signatur der Anmeldesitzung |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` | Azure installiert die Python-Abhängigkeiten beim ZIP-Deployment |
| `WEBSITE_WEBDEPLOY_USE_SCM` | `true` | Publish-Profile-Bereitstellung für Linux |

Die App liest die Werte beim Start aus der Umgebung. Die lokale `.env` wird **nicht** hochgeladen. Auf Azure verweigert die App den Start, wenn `PASSWORD` oder `SECRET_KEY` fehlen. `SECRET_KEY` bei normalen Deployments beibehalten, damit Sitzungen nicht unnötig ungültig werden. HTTPS Only aktivieren; die App verwendet auf Azure sichere Sitzungscookies.

### GitHub für die Auslieferung berechtigen

Der vorhandene Workflow nutzt ein Publish Profile:

1. In Azure unter **Konfiguration → Allgemeine Einstellungen** die **SCM Basic Auth Publishing Credentials** aktivieren. Ein Publish Profile benötigt diese Einstellung. FTP muss dafür nicht aktiviert werden.
2. Unter **Übersicht → Veröffentlichungsprofil herunterladen / Download publish profile** die XML-Datei herunterladen.
3. Im GitHub-Repository **Settings → Secrets and variables → Actions → New repository secret** öffnen.
4. Name exakt `AZURE_WEBAPP_PUBLISH_PROFILE`; als Wert den **gesamten XML-Inhalt** einfügen und speichern. Nicht nur den Dateinamen oder ein einzelnes Passwort eintragen.
5. Die heruntergeladene Datei vertraulich behandeln und nicht ins Repository oder Abgabearchiv legen. Für Nachweise nur die Secret-Namen zeigen.

Ist Basic Auth durch die Schule gesperrt, funktioniert dieser Workflow nicht unverändert. Dann OIDC mit einer zugelassenen Azure-Identität einrichten und den Workflow entsprechend anpassen; nicht nur eine beliebige `azure/login`-Zeile ergänzen. Die Microsoft-Dokumentation beschreibt beide Authentifizierungsvarianten.

Keinen zweiten, automatisch generierten Azure-Workflow im Deployment Center anlegen: Die vorhandene Datei übernimmt bereits die Auslieferung von `main`.

### Automatischer Ablauf und Artefakte

[deploy-main.yml](.github/workflows/deploy-main.yml) läuft bei jedem Push auf `main`, also auch bei einem erfolgreichen PR-Merge:

1. Python einrichten und Tests ausführen. Bei einem Fehler wird nicht ausgeliefert.
2. `scripts/package_app.py` erstellt `dist/app.zip` aus einer Positivliste: `app.py`, `requirements.txt`, HTML-Templates und `build-info.json` mit Commit-SHA. `.env`, `.git` und `.venv` gelangen nicht ins Paket.
3. Das Paket und seine SHA-256-Prüfsumme werden als GitHub-Actions-Artefakt `azure-app-<Commit-SHA>` für 30 Tage gespeichert. Damit lässt sich ein Deployment seinem Quellstand zuordnen.
4. Das Publish Profile wird auf Vorhandensein geprüft und das ZIP an Azure übertragen.
5. `scripts/check_deployment.py` ruft `/healthz` ab und prüft die tatsächlich ausgelieferte Commit-SHA. Erst danach ist die Action erfolgreich.

Deployments derselben App laufen nacheinander. Der Sourcecode ist hier das Laufzeitartefakt; Azure baut daraus die Python-Umgebung. Transitive Abhängigkeiten sind durch dieses Prototyp-Setup nicht vollständig gesperrt.

### Live-Nachweis

Nach Einrichtung von Azure und Merge nach `main`:

- GitHub **Actions → Auslieferung nach Azure**: Alle Schritte einschliesslich Versionsprüfung sind grün.
- Tatsächliche App-URL öffnen; Anmeldung mit `MaxMij` testen.
- Eintrag mit `😃` speichern, Anzeige von Text, Stimmung und Zeit prüfen.
- Abmelden; Einträge sind verborgen. Direkter POST ohne Sitzung muss nach `/login` umleiten und darf nichts speichern.
- `/healthz` zeigt `status: ok` und denselben vollständigen Commit-SHA wie `main`.
- Erst danach die oben angegebene URL als nachweislich laufend bezeichnen und im Prüfbericht den Live-Nachweis ergänzen.

### Häufige Fehler

| Meldung oder Verhalten | Prüfen |
| --- | --- |
| `No credentials found` | Repository-Secret fehlt oder hat den falschen Namen; die belegte ursprüngliche Fehlerursache, inzwischen behoben |
| Publish Profile kann nicht heruntergeladen werden oder 401 beim Deployment | SCM Basic Auth, Schulrichtlinie, vollständiges und aktuelles Profil, korrekter App-Name |
| `ModuleNotFoundError` oder Azure-Standardseite | `SCM_DO_BUILD_DURING_DEPLOYMENT=true`, ZIP enthält `app.py` und `requirements.txt` direkt im Wurzelverzeichnis |
| `Application Error` | Azure **Log stream**, App Settings `PASSWORD`/`SECRET_KEY`, Python-Stack und Startbefehl prüfen |
| Anmeldung bleibt nicht bestehen | HTTPS verwenden; stabilen `SECRET_KEY` und genau einen Worker prüfen |
| Versionsprüfung schlägt fehl | App-Startprotokoll prüfen; stimmt `/healthz` mit dem Commit des aktuellen Runs überein? |

Offizielle Grundlagen: [Python und GitHub Actions auf Azure](https://learn.microsoft.com/en-us/azure/developer/python/python-web-app-github-actions-app-service), [Azure-Authentifizierung](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions), [ZIP und Build-Automation](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python), [Git-Hook-Stufen](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages).

## Aufgabe 5 GitHub Flow und belegte Historie

`main` ist der freigegebene Produktionsast; `dev` nimmt getestete Änderungen auf. Jede neue Programmierarbeit beginnt in einem neuen `feature/*`-Ast ausgehend von `dev`.

Vorhandene Belege:

- [Issue #1](https://github.com/MaxMij/MijatovicMaxLB-324/issues/1): Happiness-Anforderung.
- `feature/happiness-entry`: ursprünglicher Ast, **weiterhin vorhanden und nicht löschen**.
- [PR #2 nach dev](https://github.com/MaxMij/MijatovicMaxLB-324/pull/2): Happiness-Implementierung und erfolgreicher `pytest`-Check.
- [PR #3 nach main](https://github.com/MaxMij/MijatovicMaxLB-324/pull/3): Integration des Entwicklungsstands; anschliessende Azure-Auslieferung fehlgeschlagen.

**Abweichung:** Laut Commit- und Issue-Zeitstempeln wurde der Happiness-Commit am 23. Oktober 2026 um 15:20 Uhr erstellt, das Issue erst um 15:35 Uhr (Europe/Zurich). Die ursprüngliche Reihenfolge «Issue vor Codeänderung» ist damit nicht belegt. Historie nicht rückdatieren oder umschreiben.

Die Korrektur wurde vor den neuen Codeänderungen als [Issue #4](https://github.com/MaxMij/MijatovicMaxLB-324/issues/4) mit dem Label `Qualitätsanforderung` erfasst. Neuer Ast: `feature/4-lb-quality`, Ausgangspunkt `dev` bei `274b81d`.

Ausgeführt: [PR #5 nach `dev`](https://github.com/MaxMij/MijatovicMaxLB-324/pull/5) mit erfolgreichem `pytest`-Check → [PR #6 nach `main`](https://github.com/MaxMij/MijatovicMaxLB-324/pull/6) → [erfolgreiche Azure-Auslieferung](https://github.com/MaxMij/MijatovicMaxLB-324/actions/runs/41412558040) → Live-Prüfung. Issue #4 wurde durch die Integration in den Default-Ast `main` geschlossen. Die abschliessenden Nachweise werden unter [Issue #7](https://github.com/MaxMij/MijatovicMaxLB-324/issues/7) auf einem neuen Feature-Ast von `dev` dokumentiert.

## Abgabe

1. Öffentliches Repository `MijatovicMaxLB-324` mit aktuellem `main` prüfen.
2. Repository-URL im Moodle-Formular abgeben.
3. Erst nach abschliessender Integration den aktuellen `main`-Stand herunterladen, den entpackten Hauptordner `MijatovicMaxLB-324` nennen und als `MijatovicMaxLB-324.zip` verpacken. Der Dateiname allein genügt nicht, wenn der innere Ordner noch `...-main` heisst.
4. Alternativ aus einem aktuellen, sauberen lokalen `main` erzeugen:

```bash
git archive --format=zip --prefix=MijatovicMaxLB-324/ --output=../MijatovicMaxLB-324.zip main
```

5. Im ZIP müssen `.github`, `.pre-commit-config.yaml`, README, Quellcode, Templates und Tests enthalten sein; `.env`, Veröffentlichungsprofil, `.venv` und `.git` dürfen nicht enthalten sein.
6. ZIP auf Moodle hochladen und erfolgreiche Abgabe kontrollieren. Der Auftrag verlangt anschliessend das Löschen der LB-Daten; diesen Schritt erst selbst nach bestätigter Abgabe ausführen.

## Grenzen des Prototyps

Die Tagebucheinträge liegen ausschliesslich in der Liste `entries` im Arbeitsspeicher. Ein Neustart oder Deployment löscht sie. Mehrere Worker oder App-Instanzen würden verschiedene Listen führen. Die LB bewertet den CI/CD-Prozess; eine persistente Datenbank ist hier nicht umgesetzt. Das nach Auftrag öffentlich bekannte Passwort ist für diese Schul-Demo vorgesehen. Keine vertraulichen Tagebucheinträge verwenden.
