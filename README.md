# DCF UI

This repository provides a simple three-stage DCF engine usable from Python via a CLI or API.

## Backend

The backend is built with FastAPI. The main endpoint `/dcf` receives a `MultiStageDCFConfig` describing the forecast stages and returns the present value of the cash flows.

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

