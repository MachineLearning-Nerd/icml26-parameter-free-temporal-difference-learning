# Pinned environment

The formal run used Python 3.12.12 and repository-level `uv.lock` SHA-256
`601569afc6a023d8b3e121157364d78b96eb24234cb5fd2c1558b86736007f22`.
Direct dependencies are pinned in `pyproject.toml`. The complete resolved
versions printed by the HF run were:

`anyio 4.14.2; click 8.4.2; contourpy 1.3.3; cycler 0.12.1; docutils 0.23;
fonttools 4.63.0; h11 0.16.0; idna 3.18; itsdangerous 2.2.0; jedi 0.20.0;
kiwisolver 1.5.0; loro 1.13.2; marimo 0.14.17; markdown 3.10.3;
matplotlib 3.10.3; narwhals 2.24.0; numpy 2.2.6; packaging 26.2;
parso 0.8.7; pillow 12.3.0; psutil 7.2.2; pygments 2.20.0;
pymdown-extensions 10.21.3; pyparsing 3.3.2; python-dateutil 2.9.0.post0;
pyyaml 6.0.3; six 1.17.0; starlette 1.3.1; tomlkit 0.15.1;
typing-extensions 4.16.0; uvicorn 0.52.1; websockets 17.0.1`.

Exact fixed command: `uv sync --frozen && uv run --no-sync python -m td_repro`.
Container: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.
