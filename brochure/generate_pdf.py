from pathlib import Path
import shutil
import subprocess
import sys

BROCHURE_DIR = Path(__file__).resolve().parent
PDF_PATH = BROCHURE_DIR / "nicolas-martinez-brochure.pdf"
PREVIEW_PATH = BROCHURE_DIR / "nicolas-martinez-brochure-preview.png"
HTML_URL = (BROCHURE_DIR / "index.html").resolve().as_uri()
PREVIEW_URL = f"{HTML_URL}?preview=1"


def resolve_playwright() -> str:
    direct = shutil.which("playwright")
    if direct:
        return direct

    candidate = Path.home() / ".hermes" / "hermes-agent" / "node_modules" / ".bin" / "playwright"
    if candidate.exists():
        return str(candidate)

    raise FileNotFoundError("Playwright CLI not found. Install it or add it to PATH.")


def run(command: list[str]) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    playwright = resolve_playwright()

    run(
        [
            playwright,
            "screenshot",
            "--full-page",
            "--viewport-size",
            "1400,1800",
            "--wait-for-selector",
            ".brochure-sheet",
            "--wait-for-timeout",
            "1200",
            PREVIEW_URL,
            str(PREVIEW_PATH),
        ]
    )

    run(
        [
            playwright,
            "pdf",
            "--paper-format",
            "A4",
            "--viewport-size",
            "1400,1800",
            "--wait-for-selector",
            ".brochure-sheet",
            "--wait-for-timeout",
            "1200",
            HTML_URL,
            str(PDF_PATH),
        ]
    )

    print(PREVIEW_PATH)
    print(PDF_PATH)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
