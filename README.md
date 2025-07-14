# DCF UI

This repository provides a simple three-stage DCF engine usable from Python via a CLI or API.

## Backend

The backend is built with FastAPI. The main endpoint `/dcf` receives a `MultiStageDCFConfig` describing the forecast stages and returns the present value of the cash flows.
The first stage accepts detailed yearly inputs including revenue, EBIT or margin, NOPAT, reinvestment or capex and even a custom WACC per year. Any of these can be omitted and the engine will derive them from growth rates or other provided values.

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

