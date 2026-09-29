#!/usr/bin/env python3
"""Convierte recursivamente PDFs en la carpeta `pdf/` a archivos .txt en `txt/`.

Uso:
    python tools/pdf_to_txt.py       # usa pdf/ y txt/ por defecto
    python tools/pdf_to_txt.py -s mis_pdfs -d salida_txt

Requiere: pdfminer.six
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import logging

from pdfminer.high_level import extract_text


def convert_pdf_to_txt(src: Path, dst: Path) -> None:
    """Extrae texto del PDF `src` y lo escribe en `dst` (utf-8).
    Si la extracción falla, lanza la excepción para ser manejada por el llamador.
    """
    text = extract_text(str(src)) or ""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        f.write(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convierte PDFs a TXT recursivamente")
    parser.add_argument("-s", "--source", default="pdf", help="Carpeta raíz de PDFs (por defecto: pdf)")
    parser.add_argument("-d", "--dest", default="txt", help="Carpeta raíz destino para txt (por defecto: txt)")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir txt existentes")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    src_root = Path(args.source)
    dst_root = Path(args.dest)

    if not src_root.exists():
        logging.error(f"Carpeta fuente no existe: {src_root}")
        raise SystemExit(1)

    pdf_count = 0
    err_count = 0

    for root, _, files in os.walk(src_root):
        for fname in files:
            if not fname.lower().endswith(".pdf"):
                continue
            pdf_count += 1
            src_file = Path(root) / fname
            rel = src_file.relative_to(src_root)
            dst_file = dst_root / rel.with_suffix(".txt")

            if dst_file.exists() and not args.overwrite:
                logging.info(f"Omitido (ya existe): {dst_file}")
                continue

            try:
                logging.info(f"Convirtiendo: {src_file} -> {dst_file}")
                convert_pdf_to_txt(src_file, dst_file)
            except Exception as e:  # pylint: disable=broad-except
                logging.error(f"Error convirtiendo {src_file}: {e}")
                err_count += 1

    logging.info(f"Procesados: {pdf_count} PDFs; errores: {err_count}")


if __name__ == "__main__":
    main()
