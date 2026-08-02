# Pinned environment

The formal run used Python 3.12.12 and repository-level `uv.lock` SHA-256
`d8edc3ca704581ce829391b9b124bf54ce76e67ecd5e1228948c9c30dc75f185`.
Direct dependencies are pinned in `pyproject.toml`. The complete resolved
versions printed by the HF run were:

`anyio 4.14.2; click 8.4.2; contourpy 1.3.3; cycler 0.12.1; docutils 0.23;
fonttools 4.63.0; h11 0.16.0; idna 3.18; itsdangerous 2.2.0; jedi 0.19.2;
kiwisolver 1.5.0; loro 1.13.2; marimo 0.23.14; markdown 3.10.3;
matplotlib 3.10.3; narwhals 2.24.0; numpy 2.2.6; packaging 26.2;
msgspec 0.21.1; parso 0.8.7; pillow 12.3.0; psutil 7.2.2; pygments 2.20.0;
pymdown-extensions 10.21.3; pyparsing 3.3.2; python-dateutil 2.9.0.post0;
python-multipart 0.0.32; pyyaml 6.0.3; pyzmq 27.1.0; six 1.17.0;
starlette 1.3.1; tomlkit 0.15.1;
typing-extensions 4.16.0; uvicorn 0.52.1; websockets 17.0.1`.

Exact fixed command: `uv sync --frozen && uv run --no-sync python -m td_repro`.
Container: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.
