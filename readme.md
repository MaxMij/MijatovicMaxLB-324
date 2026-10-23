# LB 324 – Tagebbbuch

Leistungsbeurteilung Modul 324 (DevOps)  
**Max Mijatović · IM24c · Repo:** [MaxMij/MijatovicMaxLB-324](https://github.com/MaxMij/MijatovicMaxLB-324)

Laufende Applikation: **https://mijatovicmaxlb-324.azurewebsites.net**

---

## Lokal starten

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Passwort und SECRET_KEY setzen
flask --app app run
```

Die App erwartet eine `.env` mit:

```
PASSWORD="deinLokalesPasswort"
SECRET_KEY="zufaelliger-wert"
```

Die `.env` gehört **nicht** ins Repository (siehe `.gitignore`).

Azure-Startbefehl:

```text
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

---

## Branch-Modell

| Ast | Zweck |
| --- | --- |
| `main` | Produktionsstand. Entspricht **immer** der ausgelieferten Version. |
| `dev` | Integrationsast. Nur getesteter, abgeschlossener Code. |
| `feature/*` | Entwicklung. Jeder Ast entsteht **von `dev`**. |

Ablauf: Issue → Feature-Ast von `dev` → Commit/Push → Pull Request nach `dev` (Tests) → Merge nach `dev` → Merge nach `main` (Auslieferung).

---

## Aufgabe 2 – pre-commit

Die Datei `.pre-commit-config.yaml` ist so aufgebaut:

- **bei jedem commit:** `black` formatiert den Python-Code automatisch
- **bei jedem push:** `pytest` führt die Tests aus; ein Push mit fehlgeschlagenen Tests wird abgelehnt

Das unterscheidet sich vom Modul-Auftrag, in dem die Tests bereits beim Commit liefen.

### Installation (einmalig pro Arbeitskopie)

```bash
pip install -r requirements.txt
pre-commit install
pre-commit install --hook-type pre-push
```

### Prüfen

```bash
pre-commit run --all-files          # Formatierung (commit-Hooks)
git push                            # Tests laufen über den push-Hook
```

Ohne die beiden `pre-commit install`-Befehle greifen die Hooks nicht.

---

## Aufgabe 4 – Geheimnisse auf Azure

Das lokale Passwort bleibt in `.env` und wird **nicht** committed.

Für die Auslieferung gilt die Vorgabe der LB: das Azure-Passwort ist der **GitHub-Benutzername**.

```
PASSWORD="MaxMij"
```

### Schritte, mit denen das Geheimnis übertragen wurde

1. Azure Portal → App Service `mijatovicmaxlb-324` öffnen.
2. Links **Einstellungen → Umgebungsvariablen** (Application settings).
3. Anwendungseinstellungen anlegen:
   - `PASSWORD` = `MaxMij` (GitHub-Benutzername, Vorgabe der LB)
   - `SECRET_KEY` = zufälliger Wert (nicht das lokale Dev-Secret)
   - `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
4. Unter **Konfiguration → Stapeleinstellungen** den Startbefehl setzen:

   ```text
   gunicorn --bind=0.0.0.0 --timeout 600 app:app
   ```

5. Speichern. App Service startet neu und liest `PASSWORD` zur Laufzeit über `os.getenv`.
6. Für die GitHub-Action **Auslieferung nach Azure**:
   - App Service → **Download publish profile**
   - GitHub → Repo → Settings → Secrets and variables → Actions
   - Secret `AZURE_WEBAPP_PUBLISH_PROFILE` mit dem Inhalt des Publish Profiles anlegen

Die `.env` liegt damit nur lokal. Azure kennt das Passwort ausschliesslich als App Setting. GitHub speichert nur das Publish Profile, nicht das App-Passwort.

---

## CI/CD

| Datei | Auslöser | Wirkung |
| --- | --- | --- |
| `.github/workflows/test-pr-dev.yml` | Pull Request **auf `dev`** | nur `pytest` |
| `.github/workflows/deploy-main.yml` | Push / Merge **auf `main`** | Tests, danach Auslieferung nach Azure |

Keine weiteren Jobs. PRs auf andere Äste lösen die Test-Action nicht aus.

---

## Anforderungsverwaltung

Issues entstehen **vor** jeder Code-Änderung. Vorlage: `.github/ISSUE_TEMPLATE/anforderung.md`

Aufbau: Zielsystem + Priorität (`muss` / `soll` / `wird`) + Systemaktivität + Ergänzungen + Funktionalität + Bedingungen (`wenn` / `falls`).

Labels (manuell):

- `Funktionale Anforderung`
- `Qualitätsanforderung`
- `Randanforderung`

### Vergleich der Werkzeuge (für die Wahl des RM-Ansatzes)

| | GitHub Issues | Azure DevOps Boards | Jira |
| --- | --- | --- | --- |
| Aufwand | gering, im selben Repo | mittel, extra Projekt | hoch |
| Verknüpfung Code | Branches, PRs, `closes #` | Work items, Repos | Tickets, Smart Commits |
| Labels / Typen | frei definierbar | Work item types | Issue types |
| Für dieses Projekt | **passend**: kleines Team, öffentliches Repo, GitHub Flow | überdimensioniert | überdimensioniert |

GitHub Issues sind hier tauglich, weil Anforderung, Ast, PR und Merge in einem Werkzeug nachvollziehbar bleiben.

---

## GitHub Flow dieser LB

Issue [#1](https://github.com/MaxMij/MijatovicMaxLB-324/issues/1) beschreibt die Happiness-Funktion.

Umsetzung auf dem Ast `feature/happiness-entry` (von `dev`, **nicht gelöscht**):

1. Issue mit Vorlage und Label `Funktionale Anforderung`
2. Ast `feature/happiness-entry` von `dev`
3. Test `test_add_entry_with_happiness` und Funktion
4. Pull Request nach `dev` → Action «Tests auf Pull Requests nach `dev`»
5. Merge nach `dev`
6. Merge `dev` → `main` → Action «Auslieferung nach Azure»
