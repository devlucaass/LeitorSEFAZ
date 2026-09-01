from pathlib import Path


def resource_path(relative_path: str) -> Path:
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / "assets").exists():
            return parent / relative_path

    raise FileNotFoundError(
        f"Não foi possível encontrar o arquivo: {relative_path}"
    )