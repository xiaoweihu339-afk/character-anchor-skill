#!/usr/bin/env python3
"""Build a local HTML image gallery for reviewing candidate references."""

from __future__ import annotations

import argparse
import html
from datetime import datetime, timezone
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def image_files(source_root: Path, limit: int) -> list[Path]:
    files = [
        path
        for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    files.sort(key=lambda item: item.as_posix().lower())
    return files[:limit]


def render_gallery(source_root: Path, files: list[Path], title: str) -> str:
    cards = []
    for path in files:
        try:
            label = path.relative_to(source_root).as_posix()
        except ValueError:
            label = str(path)
        cards.append(
            "\n".join(
                [
                    '<figure class="card">',
                    f'  <img src="{html.escape(path.resolve().as_uri())}" alt="{html.escape(label)}">',
                    f'  <figcaption>{html.escape(label)}</figcaption>',
                    "</figure>",
                ]
            )
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f7f5; color: #20201d; }}
    header {{ max-width: 960px; margin-bottom: 20px; }}
    .meta {{ color: #5f605c; font-size: 14px; line-height: 1.5; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 14px; }}
    .card {{ margin: 0; padding: 10px; background: #fff; border: 1px solid #deded8; border-radius: 8px; }}
    img {{ width: 100%; aspect-ratio: 1 / 1; object-fit: cover; background: #ecece8; border-radius: 6px; }}
    figcaption {{ margin-top: 8px; font-size: 12px; overflow-wrap: anywhere; color: #43433f; }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <div class="meta">Created at: {html.escape(now_iso())}</div>
    <div class="meta">Source: {html.escape(str(source_root))}</div>
    <div class="meta">Images shown: {len(files)}</div>
  </header>
  <main class="grid">
    {"".join(cards)}
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local HTML review gallery from image files.")
    parser.add_argument("source_root", help="Folder containing images to show.")
    parser.add_argument("--output", required=True, help="Output HTML file path.")
    parser.add_argument("--title", default="Character Anchor Review Gallery")
    parser.add_argument("--limit", type=int, default=300, help="Maximum number of images to include.")
    args = parser.parse_args()

    source_root = Path(args.source_root).expanduser().resolve()
    if not source_root.is_dir():
        parser.error(f"source_root is not a directory: {source_root}")

    files = image_files(source_root, args.limit)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_gallery(source_root, files, args.title), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
