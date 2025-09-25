# Code — Toolkit & Runners for CrypFormBench (C.F.B)

<p align="center">
  <img alt="Pipeline" src="https://img.shields.io/badge/pipeline-generate→verify→aggregate→viz→render-111?label=CFB&labelColor=3b82f6&color=10b981">
  <img alt="Python"   src="https://img.shields.io/badge/python-≥3.10-3776AB?logo=python&logoColor=fff">
  <img alt="OS"       src="https://img.shields.io/badge/OS-Linux%20%7C%20macOS-lightgrey">
  <img alt="License"  src="https://img.shields.io/badge/License-Repo%20Root-lightgrey">
</p>

> generate → verify → aggregate → viz → render-leaderboards
> Works on Linux/macOS; Python ≥ 3.10 recommended.

---

## 🗂 Code Layout

```
.
├─ run/
│  ├─ generate.py           # Run a model on tasks/prompts → write artifacts to model_outputs/
│  ├─ verify.py             # Execute verifiers on artifacts → write logs to original_results/
│  └─ utils_io.py           # I/O helpers, hashing, path utils
├─ metrics/
│  ├─ aggregate.py          # Compute per-task metrics + §4.5 composite scores
│  ├─ scoring.py            # Harmonic means, weighting, normalization, error taxonomies
│  └─ schemas.py            # Verdict JSON / table schemas
├─ tools/
│  ├─ adapters/
│  │  ├─ proverif.py
│  │  ├─ tamarin.py
│  │  ├─ scyther.py
│  │  ├─ maude_npa.py
│  │  ├─ avispa.py
│  │  ├─ cryptoverif.py
│  │  └─ easycrypt.py
│  ├─ tools.yaml            # Per-backend config (binaries, flags, timeouts, env)
│  ├─ check_repo.py         # Sanity checks for paths/layout
│  └─ exec.py               # Process execution, timeouts, log capturing
├─ viz/
│  ├─ plot_all.py           # Recreate all figures from calculated_results/
│  ├─ plot_leaderboard.py   # Overall leaderboard SVG/PNG
│  ├─ plot_capability_boards.py  # Per-capability leaderboards
│  └─ render_readme_leaderboards.py # Replace README blocks <!-- LEADERBOARD_*:BEGIN/END -->
├─ scripts/
│  ├─ cfb.sh
├─ __init__.py
└─ requirements.txt
```

---

## ⚡ Quick Start

From the repo root:

```bash
# (Optional) create env
python -m venv .venv && source .venv/bin/activate

# Install runtime deps
pip install -r code/requirements.txt

# Sanity check the repo layout
python -m code.tools.check_repo
```

End-to-end (using an example model, tasks, and prompts):

```bash
# 1) Generate model artifacts
python -m code.run.generate \
  --model gpt-4o \
  --tasks datasets/tasks.yaml \
  --prompts datasets/prompts \
  --out model_outputs/gpt-4o

# 2) Verify artifacts with external tools
python -m code.run.verify \
  --inputs model_outputs/gpt-4o \
  --tool-config code/tools/tools.yaml \
  --out original_results/gpt-4o

# 3) Aggregate metrics & recompute §4.5 scores
python -m code.metrics.aggregate \
  --model-outputs model_outputs/gpt-4o \
  --original-results original_results/gpt-4o \
  --out calculated_results/gpt-4o

# 4) Make figures & leaderboards
python -m code.viz.plot_all --in calculated_results --out result_figures
python -m code.viz.plot_leaderboard --in calculated_results --out result_figures
python -m code.viz.plot_capability_boards --in calculated_results --out result_figures

# 5) (Optional) Update the main README leaderboards in-place
python -m code.viz.render_readme_leaderboards \
  --in calculated_results \
  --readme README.md \
  --blocks OVERALL INTERPRETATION GENERATION COMPLETATION TRANSFORMAION CORRECTION \
  --overwrite-blocks
```

---

## 🧰 Environment & Deployment

CrypFormBench has two layers of dependencies:

1. **Python runtime** (always required)
2. **External verifiers** (only needed if you re-run verification; aggregation/plots work with the bundled logs)

### 1) Python environment

```bash
# Create & activate (Linux/macOS)
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install Python deps
pip install -r code/requirements.txt

# (Optional) lock for CI
pip freeze > code/requirements.lock.txt
```

> Python ≥ **3.10** recommended.

---

### 2) External verifiers (optional but recommended)

| Backend                | Binary           | Docs / Notes                                        |
| ---------------------- | ---------------- | --------------------------------------------------- |
| ProVerif               | `proverif`       | Datalog engine for symbolic verification            |
| Tamarin                | `tamarin-prover` | Symbolic verification with multiset rewriting       |
| Scyther                | `scyther`        | Protocol analyzer for secrecy/authentication        |
| Maude-NPA              | `maude-npa`      | Narrowing-based analyzer modulo equational theories |
| AVISPA (OFMC/CL-AtSe…) | `avispa`         | Suite of backends for protocol analysis             |
| CryptoVerif            | `cryptoverif`    | Computational soundness; games/inequalities         |
| EasyCrypt              | `easycrypt`      | Proof assistant for cryptographic programs          |

> Paths, flags, and timeouts are configured in `code/tools/tools.yaml`. You can override via CLI or env vars (see below).

#### Ubuntu / Debian (quick install hints)

```bash
# Base build tools
sudo apt-get update && sudo apt-get install -y build-essential opam m4 pkg-config zlib1g-dev git curl

# OCaml toolchain for ProVerif/CryptoVerif/Tamarin/EasyCrypt (via opam)
opam init -y --disable-sandboxing
opam switch create 5.1.1 || opam switch create 4.14.2
eval $(opam env)

# ProVerif
opam install -y proverif
# CryptoVerif
opam install -y cryptoverif
# Tamarin (binary often easiest)
sudo apt-get install -y tamarin-prover || true
# Scyther
sudo apt-get install -y scyther || true
# Maude + NPA (may require building from source)
sudo apt-get install -y maude || true   # then install maude-npa from its repo if needed
# AVISPA (from repo/binaries)
# See project site; after install, ensure 'avispa' is on PATH
# EasyCrypt (may take a while)
opam repo add easycrypt-repo https://github.com/EasyCrypt/opam.git
opam install -y easycrypt
```

> Some distributions don’t ship the latest versions. If a package isn’t found, use the project’s official install instructions and then add the binary path to `tools.yaml`.

#### macOS (Homebrew)

```bash
# Base
xcode-select --install || true
brew update

# Install what brew provides directly
brew install opam maude gnuplot graphviz
opam init -y
opam switch create 5.1.1 || opam switch create 4.14.2
eval $(opam env)

# ProVerif / CryptoVerif / EasyCrypt via opam
opam install -y proverif cryptoverif easycrypt

# Tamarin / Scyther / AVISPA:
# Prefer official releases or build from source; then add to PATH and tools.yaml
```

---

### 3) Configure tool paths

Edit `code/tools/tools.yaml` if  binaries are not on `PATH`:

```yaml
proverif:
  bin: /usr/local/bin/proverif
  flags: ["-lib", "lib/"]
  timeout_sec: 900
tamarin:
  bin: /opt/tamarin/tamarin-prover
  flags: ["--prove"]
  timeout_sec: 1800
# ...
```

You can also override at runtime:

```bash
python -m code.run.verify \
  --inputs model_outputs/<model> \
  --tool-config code/tools/tools.yaml \
  --timeout-sec 1200
```

---

### 4) Environment variables (optional)

* `CFB_PARALLEL` — default parallel workers for `verify.py` (e.g., `CFB_PARALLEL=4`)
* `CFB_TIMEOUT` — default timeout (seconds) for all tools (overridden by CLI)
* `CFB_CACHE_DIR` — where to store temp/intermediate files
* `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` — if  model client needs a proxy

---

### 5) Docker (fully reproducible)

A minimal image that includes Python deps and leaves hooks to add verifiers:

```dockerfile
# Dockerfile
FROM python:3.11-slim

# System packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy only requirements first (for caching)
COPY code/requirements.txt code/requirements.txt
RUN pip install --no-cache-dir -r code/requirements.txt

# Copy repo
COPY . .

# Default to a sanity check
CMD ["python", "-m", "code.tools.check_repo"]
```

Build & run:

```bash
docker build -t crypformbench:latest .
docker run --rm -it -v $PWD:/app crypformbench:latest
```

> To include verifiers in the image, extend the Dockerfile with opam + tool installs and update `tools.yaml` paths.

---

### 6) Smoke test

```bash
# From repo root after installing Python deps
python -m code.tools.check_repo

# Quick dry-run generation (no external verifiers needed)
python -m code.run.generate \
  --model dummy-model \
  --tasks datasets/tasks.yaml \
  --prompts datasets/prompts \
  --max-samples 3 \
  --out model_outputs/dummy --dry-run

# If verifiers are installed, run one sample end-to-end
python -m code.run.generate --model dummy --tasks datasets/tasks.yaml --prompts datasets/prompts --max-samples 1 --out model_outputs/dummy
python -m code.run.verify --inputs model_outputs/dummy --tool-config code/tools/tools.yaml --out original_results/dummy
python -m code.metrics.aggregate --model-outputs model_outputs/dummy --original-results original_results/dummy --out calculated_results/dummy
python -m code.viz.plot_all --in calculated_results --out result_figures
```

---

### 7) CI tips

* Cache `.venv` or  pip cache between runs.
* For deterministic scoring, pin tool versions (recorded by `verify.py` in `*.verdict.json`).
* Use `code/viz/render_readme_leaderboards.py` to rewrite README tables from CSVs in `calculated_results/`.

---

### 8) Troubleshooting

* **`verifier not found`** → fix `bin` path in `tools.yaml` or add to `PATH`.
* **`unknown/error` verdicts** → increase `--timeout-sec`, inspect `*.log` and `stderr_tail` in `*.verdict.json`.
* **Score mismatch** → ensure §4.5 recomputation is enabled (see `code/metrics/scoring.py` constants or CLI flags).
* **macOS gatekeeper blocks binary** → `xattr -dr com.apple.quarantine /path/to/binary`.

---

## 🤖 CLI Reference

### `python -m code.run.generate`

Generate model outputs for each `task_id` and prompt.

**Required**

* `--model <name>`: model ID (free-form; used for output path & metadata)
* `--tasks <path>`: task index (YAML/JSON)
* `--prompts <dir>`: prompt templates root

**Optional**

* `--subset <regex>`: only run tasks whose IDs match regex
* `--max-samples <N>`: cap total generations
* `--seed <int>`: record a seed used by  client
* `--params <json>`: model params (temperature, top\_p, max\_tokens…)
* `--out <dir>`: default `model_outputs/<model>`
* `--dry-run`: print what would run

**Output layout**

```
model_outputs/<model>/<task_id>.{pv,spthy,if,maude,ocv,ec,...}
model_outputs/<model>/<task_id>.meta.json   # prompts, params, hashes, ts
```

---

### `python -m code.run.verify`

Run verifiers on generated artifacts.

**Required**

* `--inputs <dir>`: where `<task_id>.*` artifacts live
* `--tool-config code/tools/tools.yaml`

**Optional**

* `--timeout-sec <int>`: override per-task timeout
* `--parallel <N>`: number of workers
* `--out <dir>`: default `original_results/<model>`

**Output layout**

```
original_results/<model>/<task_id>.log
original_results/<model>/<task_id>.verdict.json
```

`verdict.json` schema (simplified):

```json
{
  "task_id": "…",
  "tool": "proverif",
  "analyzable": true,
  "status": "safe|attack|unknown|error",
  "time_sec": 3.14,
  "tool_version": "…",
  "stderr_tail": "…"
}
```

---

### `python -m code.metrics.aggregate`

Aggregate per-task metrics and recompute composite scores (per §4.5).

**Inputs**

* `--model-outputs <dir>`
* `--original-results <dir>`
* `--out <dir>` (creates tables under `calculated_results/`)

**What it computes**

* `a = analyzable ratio`
* `ACC_A, F1_A` on analyzable subset
* **Executable tasks (Generation/Completion/Transformation/Correction)**
  `Q = HM(ACC_A, F1_A)`
  `S_task = HM(a^γ, Q)` with `γ = 1` (configurable)
* **Interpretation (recomputed)**
  `S_interp = α*s_logic + β*s_anno + (1-α-β)*HM(a^γ, HM(ACC_A, F1_A))`
  defaults: `α=β=0.3, γ=1`
* **Overall**
  weighted sum with defaults:
  `w = {gen:0.25, comp:0.20, trans:0.25, corr:0.15, interp:0.15}`
* Normalization to `[0,100]`, rounding, and CSV exports:

  * `leaderboard_overall.csv`
  * `leaderboard_interpret.csv`, `leaderboard_generate.csv`, …
  * per-model breakdown tables (wide/long)

**Config overrides (optional)**

* `--weights '{"gen":0.25,"comp":0.2,"trans":0.25,"corr":0.15,"interp":0.15}'`
* `--alpha 0.3 --beta 0.3 --gamma 1.0`
* `--error-taxonomy on` (export error-class counts if available)

---

### `python -m code.viz.plot_all`

Create publication-ready figures from `calculated_results/`.

**Flags**

* `--in <dir>`: `calculated_results/`
* `--out <dir>`: `result_figures/`
* `--style paper|dark|default` (optional)
* Outputs: per-capability bars, per-language breakdown, analyzability vs. correctness scatter, runtimes, etc.

### `python -m code.viz.plot_leaderboard`

Render the **Overall** chart/table.

### `python -m code.viz.plot_capability_boards`

Render **Interpret/Generation/Completion/Transformation/Correction** leaderboards.

### `python -m code.viz.render_readme_leaderboards`

Replace blocks in `README.md` between:

```
<!-- LEADERBOARD_OVERALL:BEGIN --> … <!-- LEADERBOARD_OVERALL:END -->
<!-- LEADERBOARD_INTERPRET:BEGIN --> … <!-- LEADERBOARD_INTERPRET:END -->
… (GENERATE / COMPLETE / CONVERT / FIX)
```

---

## 🔌 Verifier Adapters

Each adapter wraps a backend with a common interface:

```python
run(artifact_path: str, timeout: int, flags: list[str]) -> Verdict
```

* **ProVerif** (`tools/adapters/proverif.py`)
* **Tamarin** (`tamarin.py`)
* **Scyther** (`scyther.py`)
* **Maude-NPA** (`maude_npa.py`)
* **AVISPA** (`avispa.py`)
* **CryptoVerif** (`cryptoverif.py`)
* **EasyCrypt** (`easycrypt.py`)

Binaries, flags, and default timeouts live in `code/tools/tools.yaml`.
You can override via env vars or CLI flags.

---

## ⚙️ Configuration

### `code/tools/tools.yaml`

Example (excerpt):

```yaml
proverif:
  bin: /usr/local/bin/proverif
  flags: ["-lib", "lib/"]
  timeout_sec: 900
tamarin:
  bin: /usr/local/bin/tamarin-prover
  flags: ["--prove"]
  timeout_sec: 1800
# …
```

### Environment variables (optional)

* `CFB_PARALLEL` — default parallelism for `verify.py`
* `CFB_TIMEOUT` — default timeout override (seconds)
* `CFB_CACHE_DIR` — cache directory for intermediate artifacts

---

## 🤖 Development Notes

* **Determinism:** We log prompt hashes, model params, and tool versions; aggregation only trusts normalized `verdict.json`.
* **Error taxonomy:** If adapters surface structured errors (syntax/typing/semantic/timeout), `aggregate.py` can export a breakdown.
* **Testing:** Add unit tests for adapters in `tests/` (if present). Mocks can simulate `stdout/stderr` to exercise parsers.
* **Style:** Black + isort recommended (not enforced).
* **Return codes:**

  * `0` success
  * `2` some tasks failed but logs were written
  * `3` configuration error (missing binary, invalid flags)
  * `4` schema violation (bad verdict JSON)

---

## Add a New Backend

1. Implement `tools/adapters/<name>.py` with `run(...)`.
2. Register in `tools.yaml`.
3. Add parsing rules in `metrics/schemas.py` (if new fields).
4. (Optional) Add a figure or table hook in `viz/`.

---

## Add a New Model Runner

`generate.py` is model-agnostic. For custom providers:

* Point `--model <id>` to  client and pass params via `--params`.
* If you need bespoke logic, add a thin shim in `run/` (e.g., `generate_<provider>.py`) that writes the same artifact + `.meta.json`.

---

## Reproducibility Checklist

* [ ] Commit `datasets/tasks.yaml` and prompt templates
* [ ] Commit `original_results/` (or instructions to regenerate)
* [ ] Run `metrics/aggregate.py` → commit `calculated_results/`
* [ ] Run `viz/plot_all.py` → commit `result_figures/`
* [ ] (Optional) Run `viz/render_readme_leaderboards.py` to update badges/tables

---

## Troubleshooting

* **Verifier not found** → fix path in `tools.yaml` or export PATH.
* **All “unknown/error”** → check tool flags & timeouts; try `--timeout-sec` larger; inspect `*.log` tail.
* **Scores look off** → ensure you’re using the recomputed §4.5 pipeline (see `metrics/scoring.py` constants).
* **README not updating** → confirm the `<!-- LEADERBOARD_*:BEGIN/END -->` markers exist and `--overwrite-blocks` is passed.

Awesome—here’s a drop-in **Environment & Deployment** section you can append to `code/README.md`. It includes: Python env setup, verifier installation (Ubuntu & macOS quick commands), a ready-to-build Docker image, environment variables, and a smoke test.