@echo off
setlocal
pushd "%~dp0"
if exist ".venv\Scripts\ailuminode.exe" (
    ".venv\Scripts\ailuminode.exe" %*
) else (
    set "PYTHONPATH=%~dp0src"
    "C:\Users\Jade G\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m ailuminode %*
)
popd
endlocal
