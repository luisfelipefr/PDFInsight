import asyncio
import hashlib
import os
import time
import urllib.request
import logging
import subprocess
from pyppeteer import launch

logging.basicConfig(
  filename='/home/luigifr/projects/generate_pdf/log.txt',
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s\n'
)

time_str = time.strftime("%Y-%m-%d_%H-%M-%S")

URL = "https://curriculo.luigifr.com"
ARQUIVO_ATUAL = "resposta_atual.txt"
HASH_ANTERIOR = "hash_antigo.txt"
PDF_NAME = f'curriculo_{time_str}.pdf'

urllib.request.urlretrieve(URL, ARQUIVO_ATUAL)

with open(ARQUIVO_ATUAL, 'rb') as f:
  hash_novo = hashlib.sha256(f.read()).hexdigest()

hash_antigo = None
if os.path.exists(HASH_ANTERIOR):
  with open(HASH_ANTERIOR, 'r') as f:
    hash_antigo = f.read().strip()

if hash_novo == hash_antigo:
  print(f"Sem alterações detectadas no site {URL}")
  logging.info(f"Sem alterações detectadas no site {URL}.")
  exit(0)
else:
  logging.info("Mudança detectada!")
  with open(HASH_ANTERIOR, 'w') as f:
    f.write(hash_novo)
  with open("last_pdf.txt", "w") as f:
    f.write(PDF_NAME)

async def main():
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
  await page.pdf({'path': PDF_NAME, 'format': 'A4'})
  await browser.close()
  print(f"PDF gerado como o nome: {PDF_NAME}")

asyncio.run(main())

subprocess.run(["python3", "chatgpt.py"])