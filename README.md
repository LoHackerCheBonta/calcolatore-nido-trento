# Trento Nursery Score Calculator

A minimal Streamlit web application to calculate the estimated admission score and ranking probability for 
municipal nursery schools (*nidi d'infanzia*) in Trento, Italy. 

## Sources

I got a [PDF](https://www.comune.trento.it/content/download/5071/111460/file/Criteri_-_nido_d'infanzia.pdf) from
[this official page](https://www.comune.trento.it/Amministrazione/Documenti-e-dati/Documenti-tecnici-di-supporto/Criteri-nido-d-infanzia), 
where the criteria are all explained.
I then fed this page to an AI, which extracted an algorithm.
I used the ranking from the year I entered my own daughter to daycare (2025/2026) as historical data, 
following with some fine tuning based on my own data.

## Requirements

* Python 3.9+
* [uv](https://docs.astral.sh/uv/)

## Usage
Start the local server seamlessly using uv run:

```Bash
uv run streamlit run app.py
```
The application will automatically open in your default web browser at http://localhost:8501.