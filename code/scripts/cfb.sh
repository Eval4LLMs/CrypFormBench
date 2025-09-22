#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV="${ROOT}/.venv"
ensure_py(){ command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || { echo "Python not found"; exit 2; }; }
venv(){
  ensure_py
  python3 -m venv "${VENV}" >/dev/null 2>&1 || python -m venv "${VENV}"
  # shellcheck disable=SC1090
  source "${VENV}/bin/activate"
  pip install -r "${ROOT}/code/requirements.txt"
}
quickstart(){
  venv
  python -m code.tools.check_repo || true
  python -m code.metrics.aggregate --model-outputs model_outputs --original-results original_results --out calculated_results || true
  python -m code.viz.plot_all --in calculated_results --out result_figures || true
}
e2e(){
  venv
  python -m code.tools.check_repo || true
  python -m code.run.generate --model gpt-4o --tasks datasets/tasks.yaml --prompts datasets/prompts --out model_outputs/gpt-4o || true
  python -m code.run.verify --inputs model_outputs/gpt-4o --tool-config code/tools/tools.yaml --out original_results/gpt-4o || true
  python -m code.metrics.aggregate --model-outputs model_outputs/gpt-4o --original-results original_results/gpt-4o --out calculated_results/gpt-4o || true
  python -m code.viz.plot_all --in calculated_results --out result_figures || true
}
case "${1:-help}" in
  quickstart) quickstart ;;
  e2e) e2e ;;
  *) echo "Usage: scripts/cfb.sh [quickstart|e2e]" ;;
esac
