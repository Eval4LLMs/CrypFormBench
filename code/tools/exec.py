import subprocess, shlex
def run(cmd, timeout=None, cwd=None):
    if isinstance(cmd, str): cmd = shlex.split(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return p.returncode, out, err
    except subprocess.TimeoutExpired:
        p.kill(); return 124, "", f"timeout after {timeout}s"
