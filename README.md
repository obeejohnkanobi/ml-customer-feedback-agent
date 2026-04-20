# Customer Feedback Analysis Agent

Dette projekt analyserer kundefeedback med en AutoGen-agent og fire mini-tools:

- `feedback_reader`
- `sentiment_analysis`
- `keyword_extraction`
- `categorization`

Projektet er lavet som en skolevenlig MVP, der er nem at forstå, køre og forklare.

## 1) Arkitektur (kort overblik)

Pipeline-flowet er:

1. `feedback_reader` henter feedback-data.
2. `sentiment_analysis` klassificerer hver tekst som `positive`, `negative` eller `neutral`.
3. `keyword_extraction` udtrækker nøgleord fra teksten.
4. `categorization` mapper nøgleord til forretningskategorier.
5. Agenten samler resultatet og gemmer en rapport i `reports/`.

Primær entrypoint:

- `feedback_agent/agent/feedback_analysis_agent.py`

Tool-filer:

- `feedback_agent/tools/feedback_reader_tool.py`
- `feedback_agent/tools/sentiment_analysis_tool.py`
- `feedback_agent/tools/keyword_extraction_tool.py`
- `feedback_agent/tools/categorization_tool.py`

## 2) Krav

- Python 3.10+
- Mistral API key
- Internetadgang (til LLM-kald)

## 3) Opsætning

### Trin A: Opret og aktivér virtuelt miljø

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Trin B: Installér dependencies

```powershell
pip install -r requirements.txt
```

### Trin C: Installér spaCy-model

```powershell
python -m spacy download en_core_web_sm
```

### Trin D: Tilføj API key

Opret en `.env`-fil i projektets root med:

```dotenv
MISTRAL_API_KEY="your_api_key_here"
```

## 4) Kør projektet

Kør den fulde feedback-analyse:

```powershell
python -m feedback_agent.agent.feedback_analysis_agent
```

Kør den lille calculator-demo:

```powershell
python -m feedback_agent.agent.calculator_agent
```

## 5) Formel validering (tests)

Projektet indeholder `pytest`-tests for tools og datakontrakter.

Kør alle tests:

```powershell
pytest -q
```

Seneste lokale resultat i dette projekt:

- `11 passed`

## 6) Robusthed i denne løsning

Der er tilføjet safeguards, så projektet fejler mindre under demo/aflevering:

- tom inputtekst håndteres med sikre defaults
- sentiment-tool har retry ved midlertidige API-fejl
- manglende spaCy-model giver tydelig installationsbesked
- kategorisering understøtter delvise keyword-match

## 7) Fejlsøgning

### `MISTRAL_API_KEY is missing`

- Tjek at `.env` findes i projektets root.
- Tjek at variabelnavnet er præcis `MISTRAL_API_KEY`.
- Tjek at `.env` er gemt i UTF-8 uden skjult BOM.

### `spaCy model 'en_core_web_sm' is not installed`

Kør:

```powershell
python -m spacy download en_core_web_sm
```

### Mistral `503` eller midlertidig API-fejl

Det er typisk en midlertidig backend-fejl. Prøv igen efter kort tid.

## 8) Næste iteration (efter MVP)

- Tilføj end-to-end integrationstests for hele agent-flowet.
- Tilføj bedre evalueringsmålinger for sentiment/kategorier.
- Erstat in-memory feedback med CSV eller database.
