# Python virtual environment for this workspace

This project uses a local virtual environment created at `.venv`.

Activate (bash / zsh / macOS):

    # bash or zsh
    source .venv/bin/activate

Verify Python and pip inside the venv:

    python -V
    pip --version

Add dependencies to `requirements.txt` and install inside the venv:

    pip install -r requirements.txt

To deactivate:

    deactivate

Notes:
- The `.gitignore` excludes `.venv` and common artifacts.
- If you prefer a different env tool (poetry, pipx, conda), tell me and I can scaffold that instead.
# chatCthulhu
