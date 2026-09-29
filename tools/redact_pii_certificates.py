"""
==============================================================================
HERRAMIENTA DE REDACCIÓN Y GOBIERNO DE PRIVACIDAD PARA CERTIFICADOS PDF
Ubicación: /tools/redact_pii_certificates.py
Propósito:
  1. Resguardar certificados originales sin censura en 'pdf_archive_private/'.
  2. Aplicar Stream Redaction binaria (fitz) a los PDFs públicos reemplazando
     el número de cédula '1107835098' por '1107••••••'.
  3. Sanitizar archivos TXT y réplicas en 'docs/pdf/'.
==============================================================================
"""

import os
import shutil
import fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_ARCHIVE = os.path.join(BASE_DIR, "pdf_archive")
PDF_PRIVATE = os.path.join(BASE_DIR, "pdf_archive_private")
DOCS_PDF = os.path.join(BASE_DIR, "docs", "pdf")
DOCS_TXT = os.path.join(BASE_DIR, "docs", "txt")

PII_TARGET = "1107835098"
MASK_TEXT = "1107••••••"

TARGET_PDFS = [
    os.path.join("academic", "ICFES_Resultados.pdf"),
    os.path.join("academic", "OOPT.pdf"),
    os.path.join("certifications", "DevSeniorCode", "certificate-cmf75oet500p7rpm7ietvzkr0-cmf8idpeo02blrpm7266jps5b.pdf")
]

def backup_originals():
    print("[1/4] Resguardando originales en pdf_archive_private/...")
    os.makedirs(PDF_PRIVATE, exist_ok=True)
    for rel_path in TARGET_PDFS:
        src = os.path.join(PDF_ARCHIVE, rel_path)
        dest = os.path.join(PDF_PRIVATE, rel_path)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if not os.path.exists(dest):
                shutil.copy2(src, dest)
                print(f"  -> Backup creado: {dest}")
            else:
                print(f"  -> Backup ya existente: {dest}")
        else:
            print(f"  [AVISO] No se encontró original en {src}")

def redact_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"  [OMITIDO] No existe: {file_path}")
        return False

    doc = fitz.open(file_path)
    modified = False

    for page_num in range(len(doc)):
        page = doc[page_num]
        rects = page.search_for(PII_TARGET)
        if rects:
            for r in rects:
                print(f"  [REDACTANDO] {os.path.basename(file_path)} Pág {page_num}: {r}")
                # Expand rectangle slightly horizontally and vertically for clean mask alignment
                annot = page.add_redact_annot(
                    r,
                    text=MASK_TEXT,
                    fontname="helv",
                    fontsize=9.0,
                    text_color=(0.1, 0.1, 0.1),
                    fill=(0.96, 0.96, 0.96), # Light clean background
                    align=fitz.TEXT_ALIGN_CENTER
                )
            page.apply_redactions()
            modified = True

    if modified:
        # Strip metadata dictionary to prevent leaks in document properties
        meta = doc.metadata
        for k in meta:
            if meta[k] and PII_TARGET in str(meta[k]):
                meta[k] = meta[k].replace(PII_TARGET, MASK_TEXT)
        doc.set_metadata(meta)
        
        # Save atomically
        temp_path = file_path + ".tmp"
        doc.save(temp_path, deflate=True, garbage=4)
        doc.close()
        shutil.move(temp_path, file_path)
        print(f"  -> Guardado con redacción binaria: {file_path}")
        return True
    else:
        doc.close()
        print(f"  [INFO] No se encontró {PII_TARGET} en {file_path}")
        return False

def redact_all():
    backup_originals()

    print("\n[2/4] Aplicando redacción binaria a archivos en pdf_archive/...")
    for rel_path in TARGET_PDFS:
        full_path = os.path.join(PDF_ARCHIVE, rel_path)
        redact_pdf(full_path)

    print("\n[3/4] Sincronizando réplicas en docs/pdf/...")
    # Réplica ICFES
    redact_pdf(os.path.join(DOCS_PDF, "ICFES_Resultados.pdf"))
    # Réplica OOPT
    redact_pdf(os.path.join(DOCS_PDF, "OOPT.pdf"))
    # Réplica DevSeniorCode
    dsc_docs = os.path.join(DOCS_PDF, "DevSeniorCode", "certificate-cmf75oet500p7rpm7ietvzkr0-cmf8idpeo02blrpm7266jps5b.pdf")
    redact_pdf(dsc_docs)

    print("\n[4/4] Sanitizando archivos TXT en docs/txt/...")
    txt_file = os.path.join(DOCS_TXT, "DevSeniorCode", "certificate-cmf75oet500p7rpm7ietvzkr0-cmf8idpeo02blrpm7266jps5b.txt")
    if os.path.exists(txt_file):
        with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if PII_TARGET in content:
            new_content = content.replace(PII_TARGET, MASK_TEXT)
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  -> Sanitizado TXT: {txt_file}")
        else:
            print(f"  [INFO] TXT ya sanitizado: {txt_file}")

    print("\nProceso de redacción de certificados finalizado con éxito.")

if __name__ == "__main__":
    redact_all()
