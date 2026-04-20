# Projektrapport - MVP-forbedringer

## 1) Hvad der er implementeret

Projektet er udbygget fra en fungerende MVP til en mere afleveringsklar version med fokus på dokumentation, testbarhed og stabilitet.

Implementeret funktionalitet:

- **Mini-tools (krav opfyldt)**
  - `feedback_reader`: læser sample feedback-data.
  - `sentiment_analysis`: klassificerer sentiment (`positive`, `negative`, `neutral`) via LLM.
  - `keyword_extraction`: udtrækker nøgleord med spaCy noun chunks + entities.
  - `categorization`: mapper nøgleord til forretningskategorier.

- **Agent-integration (krav opfyldt)**
  - Agenten kører værktøjerne i en planlagt pipeline:
    1. læs feedback,
    2. analyser sentiment,
    3. udtræk nøgleord,
    4. kategoriser,
    5. generér samlet resultat/rapport.

- **Dokumentation forbedret**
  - `README.md` er opdateret med setup, kørsel, test, troubleshooting og arkitektur i beginner-venligt sprog.

- **Projektkonfiguration forbedret**
  - `config.py` loader `.env` mere robust via eksplicit sti til projektets root.

---

## 2) Hvordan det er testet

Der er indført **formelle automatiske tests** med `pytest`.

Testtyper:

- `tests/test_feedback_reader_tool.py`
  - validerer datastruktur og filtrering af ugyldige feedback records.

- `tests/test_keyword_extraction_tool.py`
  - validerer nøgleordsudtræk inkl. edge case med tom tekst.

- `tests/test_categorization_tool.py`
  - validerer kategorisering og fallback til `General`.

- `tests/test_sentiment_analysis_tool.py`
  - validerer sentiment parsing, støjende svarformat og fallback ved fejl.

- `tests/test_pipeline_contract.py`
  - validerer data-kontrakten for feedback-items (`id`, `text`, `source`).

Kørt kommando:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Resultat:

- **11 tests passed**
- 1 advarsel fra ekstern pakke (`flaml`) som ikke blokerer projektets funktionalitet.

---

## 3) Hvilke robustness-tiltag der er lavet

Fokus har været at undgå unødige crashes og give tydelige fejl.

- **Miljøvariabler og startup**
  - Robust `.env`-load i `feedback_agent/config.py`.
  - Klar fejlbesked hvis `MISTRAL_API_KEY` mangler.

- **Feedback reader**
  - Filtrerer ugyldige records (fx manglende `id`/`text` eller ugyldig `source`).

- **Keyword extraction**
  - Returnerer tom liste ved tom inputtekst.
  - Giver tydelig instruktion hvis spaCy-model mangler (`en_core_web_sm`).

- **Categorization**
  - Håndterer tomt/noisy keyword-input.
  - Understøtter delvise match (mere robust end kun eksakt match).

- **Sentiment analysis**
  - Retry-logik ved midlertidige API-fejl.
  - Mere tolerant parsing af LLM-svar.
  - Graceful fallback til `neutral` for at holde pipeline kørende.

---

## 4) Hvad næste iteration bør være

For at løfte kvaliteten yderligere anbefales disse næste skridt:

1. **Integrationstest end-to-end**
   - Test hele agent-flowet med fast dataset og forventet output-format.

2. **Bedre evalueringsmålinger**
   - Tilføj kvalitetsmålinger (fx precision/recall på sentiment og kategorier).

3. **Mere avanceret kategorisering**
   - Udvid fra regelbaseret match til embedding/ML-baseret semantisk match.

4. **Ekstern datakilde**
   - Erstat in-memory sample data med CSV eller database connector.

5. **Output-kvalitet og observability**
   - Gem strukturerede logs, kørselstid og fejltyper for lettere fejlfinding.

6. **Produktionsklar fejlhåndtering**
   - Central fejlhåndtering, bedre retry/backoff og tydelige brugerbeskeder.

---

## Konklusion

Projektet opfylder opgavekravene i MVP-form, og de gennemførte forbedringer har gjort løsningen mere dokumenteret, testet og robust. Det nuværende niveau er velegnet til skoleaflevering, med en klar roadmap for næste iteration.

