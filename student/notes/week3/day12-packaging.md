# Day 12 notes: Packaging the model as an API

Assignment: `assignments/week3/day12-packaging/` · Branch: `day12-packaging` · Code goes in `app/`

## Learning objectives
By the end of this lesson you should be able to:
- Explain what an API is and why models are usually served behind one
- Bundle preprocessing and model into one object so training and serving cannot drift apart
- Write a training script that saves the final model and its threshold
- Build a FastAPI service with a validated input schema, a `/predict` endpoint and a `/health` endpoint
- Run the service locally and test it from the browser, from Python and from the command line

# Part 1: Lesson

## Why this day matters
A model in a notebook helps nobody. To be used, it must accept a transaction from another system and return a decision in milliseconds. Today you turn your model into a small service, the same shape as real production fraud scoring (just much simpler).

## The concepts

### 1. What an API is
An **API** (here, a web API) is a program that listens for requests over HTTP and sends back responses, usually as JSON. The card payment system would send:
```json
{"Time": 406.0, "V1": -2.31, "V2": 1.95, ..., "V28": -0.14, "Amount": 0.0}
```
and receive:
```json
{"fraud_score": 0.93, "is_fraud": true, "threshold": 0.37, "model_version": "rf-v1"}
```
Any system that can make an HTTP request can use your model, whatever language it is written in.

### 2. Training/serving skew, and how to avoid it
The most common production bug: the API prepares data **slightly differently** from training (forgets to scale Amount, uses different column order...). The model then silently gives wrong scores.

The fix: save **one object** that contains preprocessing + model, so the API cannot forget a step:
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler

preprocess = ColumnTransformer(
    [("scale", RobustScaler(), ["Amount", "Time"])],
    remainder="passthrough",
)
pipeline = Pipeline([("prep", preprocess), ("model", your_model)])
pipeline.fit(X_train, y_train)
```
Adapt the preprocessing to your own Day 4 decisions. Also save:
- the **threshold** you chose on Day 7,
- the **feature list in order**,
- a **version** string.

```python
joblib.dump({"pipeline": pipeline, "threshold": 0.37, "features": list(X_train.columns),
             "version": "rf-v1"}, "models/fraud_model.joblib")
```
(Use your own threshold, not 0.37.)

### 3. A training script
Since model files are not committed, anyone (including you, next week) must be able to recreate the model with **one command**. Write `app/train.py` (or `src/train.py`) that loads data, splits, builds the pipeline, fits, and saves. Then document it: `python -m app.train`.

### 4. FastAPI essentials
**FastAPI** is a Python web framework. Three ideas:
- **Routes:** a function decorated with `@app.post("/predict")` runs when a request arrives at that URL.
- **Pydantic models:** a class describing the expected input. FastAPI checks every request against it and rejects bad input with a clear error, automatically.
- **Automatic docs:** visit `/docs` for an interactive page to try your API in the browser.

A skeleton to build from:
```python
# app/main.py
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "fraud_model.joblib"
bundle = joblib.load(MODEL_PATH)          # load once at startup, not per request

app = FastAPI(title="Fraud scoring API")

class Transaction(BaseModel):
    Time: float
    V1: float
    # ... V2 to V28 ...
    Amount: float

@app.get("/health")
def health():
    return {"status": "ok", "model_version": bundle["version"]}

@app.post("/predict")
def predict(tx: Transaction):
    row = pd.DataFrame([tx.model_dump()])[bundle["features"]]
    score = float(bundle["pipeline"].predict_proba(row)[0, 1])
    return {"fraud_score": score, "is_fraud": score >= bundle["threshold"], ...}
```
Things you need to finish yourself: all 30 fields, the full response, and input checks (should a negative Amount be allowed? Pydantic's `Field(ge=0)` can enforce it).

Run it from the repo root:
```
uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs.

### 5. Testing the API
Three ways, all worth knowing:
- **Browser:** `/docs` → "Try it out".
- **Python:** `requests` is not installed, but FastAPI's `TestClient` works without running a server:
  ```python
  from fastapi.testclient import TestClient
  from app.main import app
  client = TestClient(app)
  r = client.post("/predict", json=transaction_dict)
  ```
  (`TestClient` needs the `httpx` package; install it if the import fails, and add it to `requirements.txt`.)
- **Command line:** `curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d @sample.json`

Good tests: a known fraud from the test set gets a high score; a known legit gets a low one; a request missing a field is rejected (status 422); `/health` returns ok. Also check that the API's score for a row **equals** the notebook's score for the same row. That proves there is no training/serving skew.

### 6. Production thinking (to mention, not build)
- **Latency:** fraud scoring happens during the payment, so responses need to be fast (tens of milliseconds).
- **Logging:** record every request, score and decision (without sensitive data) for audits and monitoring.
- **Versioning:** return the model version with every response, so decisions can be traced.
- **Fallback:** what happens if the API is down? Approve everything? Fall back to rules?

## Summary
- An API lets any system send a transaction and get back a score and a decision.
- Save preprocessing + model + threshold + feature order as one bundle to prevent training/serving skew.
- A training script recreates the model from scratch with one command.
- FastAPI: routes, Pydantic input validation, automatic `/docs`.
- Test with the browser, TestClient and curl, and check the API matches the notebook.

## Check your understanding
1. What is training/serving skew, and how does a Pipeline prevent it?
2. Why load the model once at startup instead of in each request?
3. What status code does FastAPI return when a required field is missing?
4. Why return the model version in each response?
5. What should the payment system do if the fraud API does not respond?

# Part 2: How to attempt each task

### Task 1. Final model choice
Decide which model to package (usually your best supervised model) and write one sentence on why. The unsupervised score can be added as a second output if you want, as long as it is labeled clearly.

### Task 2. Training script
1. Write `app/train.py` that builds the Pipeline, fits on the training split, and saves the bundle to `models/` (gitignored).
2. Run it and confirm the file exists. Confirm `git status` does not show it.

### Task 3. The API
1. `app/main.py` with `/health` and `/predict` as above.
2. Input schema with all 30 features and sensible validation.
3. Response: score, flag, threshold, model version.
4. A useful error if the model file is missing ("run `python -m app.train` first").

### Task 4. Test it
1. Save one fraud and one legit test transaction as JSON files in `app/samples/` (a single row is not the dataset; that is fine to commit).
2. Call the API with both and record the responses.
3. Send a bad request and record the error.
4. Show that the API score equals the notebook score for the same row.
5. Optional: put these checks in `tests/test_api.py` using `TestClient`.

### Task 5. Document it
Update `app/README.md`: how to train, how to run, an example request and response, and the endpoint list.

### `submission.md` (suggested structure)
- **Which model and why**
- **How to run it** (the exact commands)
- **Test results:** the sample responses and the bad-request error
- **Skew check:** notebook score vs. API score
- **What production would need** (3-5 bullets from section 6)

## Common mistakes
- Scaling in the notebook but not in the API (skew). Use the Pipeline.
- Wrong column order when building the DataFrame from the request.
- Loading the model inside the request function.
- Hard-coded absolute paths that only work on your machine.
- Committing the `.joblib` file.
- Returning numpy types that JSON cannot serialize. Convert with `float()` / `bool()`.

## Self-check before the PR
- [ ] `python -m app.train` recreates the model from scratch
- [ ] `uvicorn app.main:app` starts and `/docs` works
- [ ] Fraud and legit samples give sensible scores; bad input is rejected
- [ ] API score matches the notebook score
- [ ] `app/README.md` explains how to run it
- [ ] Branch `day12-packaging`, PR opened, no model files committed

## Going further (optional)
Add a `/predict_batch` endpoint that accepts a list of transactions, and measure how long 1,000 predictions take one by one vs. as a batch.
