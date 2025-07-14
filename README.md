# DCF UI

This repository provides a simple three-stage DCF engine usable from Python via a CLI or API.

## Backend

The backend is built with FastAPI. The main endpoint `/dcf` receives a list of stage definitions and returns the present value of the cash flows.
Each stage provides its own WACC and optional tax rate. Stage&nbsp;1 also carries the starting revenue and invested capital so no global block of parameters is required. Stage&nbsp;1 can take full consensus figures (revenue, EBIT/EBITDA and capex) or accept growth and margin paths. Stage&nbsp;2 only needs a WACC and length—the model fades ROIC to that cost of capital. The perpetual stage supplies its WACC and long‑run growth.

### Run the API

```bash
pip install -r requirements.txt
uvicorn backend.api:app --reload
```

### CLI usage

You can compute the enterprise value without running the web server:

```bash
python -m backend.cli sample_config.json
```

