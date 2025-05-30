import asyncio
import hashlib
import os
import sys
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


if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
  print("Uso: python generate_pdf.py [1|2]")
  print("1 - Puxar de uma URL e gerar PDF")
  print("2 - Verificar alteração apenas nos nomes dos PDFs locais")
  exit(1)

option = sys.argv[1]


URL = "https://curriculo.luigifr.com"
ARQUIVO_ATUAL = "resposta_atual.txt"
HASH_ANTERIOR = "hash_antigo.txt"
PDF_NAME = f'curriculo_{time_str}.pdf'
PDF_PATH = "curriculos"

run_chatgpt = False

# Generate a PDF for URL
if option == "1":
  urllib.request.urlretrieve(URL, ARQUIVO_ATUAL)

  with open(ARQUIVO_ATUAL, 'rb') as f:
    new_hash = hashlib.sha256(f.read()).hexdigest()

  hash_antigo = None
  if os.path.exists(HASH_ANTERIOR):
    with open(HASH_ANTERIOR, 'r') as f:
      hash_antigo = f.read().strip()

  if new_hash == hash_antigo:
    print(f"Sem alterações detectadas no site {URL}")
    logging.info(f"Sem alterações detectadas no site {URL}.")
    exit(0)
  else:
    logging.info("Mudança detectada!")
    
    with open(HASH_ANTERIOR, 'w') as f:
      f.write(new_hash)
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
    await page.pdf({'path': PDF_PATH+'/'+PDF_NAME, 'format': 'A4'})
    await browser.close()
    
    pdf_files = [f for f in os.listdir(PDF_PATH) if f.lower().endswith(".pdf")]
    with open("pdf_list.txt", "w") as f:
      for pdf in pdf_files:
        f.write(PDF_PATH+"/"+ pdf + "\n")
        logging.info(f"PDF gerado: {PDF_NAME}")
        logging.info(f"Lista de PDFs atualizada: {pdf_files}")
    print(f"PDF gerado como o nome: {PDF_NAME}")
    print(pdf_files)
  try: 
    asyncio.run(main())
  except Exception as e:
    logging.error(f"Erro ao gerar pdf: {e}")
    print(f"Erro ao gerar PDF: {e}")
  run_chatgpt = True
    
# Local PDFs
elif option == "2":
  HASH_ANTERIOR = "hash_pdf_antigo.txt"

  def hash_names_pdfs(path):
    names = []
    for root, dirs, files in os.walk(path):
      for filename in files:
        if filename.lower().endswith(".pdf"):
          names.append(filename)
    names.sort()
    names_concat = "".join(names)
    hash_sha256 = hashlib.sha256(names_concat.encode()).hexdigest()
    return hash_sha256

  new_hash = hash_names_pdfs(PDF_PATH)
  hash_antigo = None
  if os.path.exists(HASH_ANTERIOR):
    with open(HASH_ANTERIOR, 'r') as f:
      hash_antigo = f.read().strip()
  if new_hash == hash_antigo:
    print("Sem alterações detectadas nos PDFs locais.")
    exit(0)
  else:
    print("Mudança detectada nos PDFs locais!")
    with open(HASH_ANTERIOR, 'w') as f:
      f.write(new_hash)

  # Atualize pdf_list.txt para garantir que a IA processará os arquivos corretos
  pdf_files = [f for f in os.listdir(PDF_PATH) if f.lower().endswith(".pdf")]
  with open("pdf_list.txt", "w") as f:
    for pdf in sorted(pdf_files):
      f.write(PDF_PATH + "/" + pdf + "\n")
  logging.info(f"Lista de PDFs atualizada: {pdf_files}")
  run_chatgpt = True
  
else:
  print("Opção inválida.")
  exit(1)

      
if run_chatgpt:
  subprocess.run(["python3", "chatgpt.py"])      
