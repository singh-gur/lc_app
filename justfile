install-deps:
    # Install dependencies
    uv sync
    .venv/bin/playwright install

upgrade-deps:
    # Upgrade dependencies
    uv sync --upgrade

build:
    # Build the project
    uv build

