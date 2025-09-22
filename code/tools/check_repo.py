import os, sys, json, pathlib
REQ = ['code/run/generate.py','code/run/verify.py','code/metrics/aggregate.py','code/metrics/scoring.py','code/tools/tools.yaml','code/tools/adapters','code/viz/plot_all.py']
def main():
    miss=[p for p in REQ if not pathlib.Path(p).exists()]
    print(json.dumps({"ok": not miss, "missing": miss}, indent=2))
    sys.exit(0 if not miss else 2)
if __name__=="__main__": main()
