import time, pathlib
def run(artifact_path: str, timeout: int = 600, flags=None):
    time.sleep(0.01)
    return {
        "task_id": pathlib.Path(artifact_path).stem,
        "tool": "easycrypt",
        "analyzable": True,
        "status": "unknown",
        "time_sec": 0.01,
        "tool_version": "placeholder-0.0.1",
        "stderr_tail": ""
    }
