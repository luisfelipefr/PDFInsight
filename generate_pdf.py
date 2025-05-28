import asyncio
import hashlib
import os
import urllib.request
import logging
from pyppeteer import launch

logging.basicConfig(
    filename='/home/luigifr/projects/curriculo/log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s\n'
)

URL = "https://luigifr.com"
ARQUIVO_ATUAL = "resposta_atual.txt"
HASH_ANTERIOR = "hash_antigo.txt"

urllib.request.urlretrieve(URL, ARQUIVO_ATUAL)

with open(ARQUIVO_ATUAL, 'rb') as f:
    hash_novo = hashlib.sha256(f.read()).hexdigest()

hash_antigo = None
if os.path.exists(HASH_ANTERIOR):
    with open(HASH_ANTERIOR, 'r') as f:
        hash_antigo = f.read().strip()

if hash_novo == hash_antigo:
    logging.info("Sem alterações detectadas.")
    exit(0)
else:
    logging.info("Mudança detectada!")
    with open(HASH_ANTERIOR, 'w') as f:
        f.write(hash_novo)

async def main():
    pdfName = 'curriculo.pdf'
    browser = await launch(
        headless=True,
        executablePath='/usr/bin/chromium-browser',
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ],
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
    )
    page = await browser.newPage()
    await page.goto(URL, waitUntil='networkidle0')
    await page.pdf({'path': pdfName, 'format': 'A4'})
    await browser.close()
    print(f"PDF gerado em {pdfName}")

asyncio.run(main())
