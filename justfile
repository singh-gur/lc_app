install-deps:
    # Install dependencies
    uv sync

upgrade-deps:
    # Upgrade dependencies
    uv sync --upgrade

build:
    # Build the project
    uv build

