# CrypFormBench – `html/` data pack

This folder contains **task-level evaluation traces** consumed by the website’s
“Evaluation Process” panel. Each file logs the 5-stage pipeline for multiple
*(language, model)* pairs:

1) `inputdata`  →  2) `prompt`  →  3) `modelinput`  →  4) `modeloutput`  →  5) `evalresult`

The web UI **does not assume the root key name**. It unwraps single-key layers
until it reaches the **language → model → record** layer.

---

## Files

| Task (UI label)                | JSON filename                |
|--------------------------------|------------------------------|
| generation                     | `generation.json`            |
| completion                     | `completion.json`            |
| translation                    | `translation.json`           |
| interpretation_logic           | `interpretation_logic.json`  |
| interpretation_notation        | `interpretation_notation.json`|
| correction_false               | `correction_false.json`      |
| correction_error               | `correction_error.json`      |

> Place all files here (same directory as this README). The site loads them via relative paths.

---

## Schema (root-agnostic)

The **root key may be anything** (e.g., `generation`, `task`, `v1`, etc.). The
viewer unwraps single-key containers until it sees the **language layer**.

```json
{
  "<any-root-key>": {
    "<language>": {
      "<model>": {
        "filename": "string, e.g. EC-1/KEMDEM.ec",
        "inputdata": {
          // free-form: dataset content you want to show in "Dataset Content"
          // often contains: { "file": "...", "logic": "...", "results": {...} }
        },
        "prompt": [
          // string OR array of { "role": "system|user|assistant", "content": "..." }
        ],
        "modelinput": [
          // the exact payload after templating (string or chat array), shown before inference
        ],
        "modeloutput": "string or object",
        "evalresult": {
          // task-specific metrics / bookkeeping, e.g. num_generates, tp/tn/fp/fn, score, timeuse, etc.
        }
      }
    }
  }
}
````

### Minimal valid example

```json
{
  "generation": {
    "hlpsl": {
      "llama4-maverick-instruct-basic": {
        "filename": "EC-1/KEMDEM.ec",
        "inputdata": { "file": "EC-1/KEMDEM.ec", "logic": "…", "results": {} },
        "prompt": [{"role":"system","content":"You are …"}, {"role":"user","content":"…"}],
        "modelinput": [{"role":"system","content":"…"}, {"role":"user","content":"…"}],
        "modeloutput": "… full model response …",
        "evalresult": {"num_generates":1, "score": "…"}
      }
    }
  }
}
```

Both of these also work (root differences are OK):

```json
{ "ec": { "llama4-maverick-instruct-basic": { /* record */ } } }
```

```json
{ "v1": { "generation": { "ec": { "model-x": { /* record */ } } } } }
```

---

## Adding data

1. **Pick the file**: choose one of the 7 task files above.
2. **Choose a language key** (e.g., `hlpsl`, `spdl`, `ec`, `tamarin`, `proverif`, etc.).
3. **Choose a model key** (e.g., `llama4-maverick-instruct-basic`).
4. **Insert a record** with fields shown in the schema (at minimum: `filename`, `inputdata`, `prompt`, `modelinput`, `modeloutput`, `evalresult`).
5. **Keep keys stable** (case-sensitive). Prefer **UTF-8** encoding, Unix newlines `\n`.

> The website will show *Filename* from `record.filename`, and will display the **entire** `inputdata` object in “Dataset Content”.

---

## Conventions

* **Encoding**: UTF-8 (no BOM).
* **Long text**: keep as strings; objects are also allowed and will be pretty-printed.
* **Prompt / modelinput**: may be a single string or an array of chat turns.
* **Language keys**: short lowercase tokens (e.g., `hlpsl`, `spdl`, `ec`, `tamarin`).
* **Model keys**: lowercase with dashes (e.g., `llama4-maverick-instruct-basic`).
* **Root key**: arbitrary; avoid colliding with language names.

---

## Preview locally / on GitHub Pages

* **Local**:

  ```bash
  # from repo root (where index.html lives)
  python -m http.server 8000
  # open http://localhost:8000/
  ```
* **GitHub Pages**: Settings → Pages → *Deploy from a branch* (point to the folder containing `index.html`).
  The site loads these files from `html/*.json`.