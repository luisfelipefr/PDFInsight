import os
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

with open("pdf_list.txt", "r") as f:
  PDF_NAMES = [line.strip() for line in f if line.strip()]

all_text = ""

for pdf_file in PDF_NAMES:
  print("Processando:", pdf_file)
  try:
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    for page_num, page in enumerate(reader.pages):
      page_text = page.extract_text()
      if page_text:
        all_text += f"\n--- Content from {pdf_file} (page {page_num + 1}) ---\n"
        all_text += page_text + "\n"
  except Exception as e:
    print(f"Erro ao processar {pdf_file}: {e}")

PDF_EXTRACT = 'pdfReader.txt'
with open(PDF_EXTRACT, "w", encoding="utf-8") as f:
  f.write(all_text)

with open("prompt.txt", "r", encoding="utf-8") as f:
  instructions = f.read()

try:
  response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
      {"role": "system", "content": instructions},
      {"role": "user", "content": f"Eu tenho esse texto extraído dos PDFs:\n{all_text}\nLeia ele e me pontue os pontos principais. Criando um markdown, irei armazenar esse valor em um arquivo .md"}
    ]
  )
  print(response.choices[0].message.content)
  with open("response.md", "w", encoding="utf-8") as f:
    f.write(response.choices[0].message.content)

except Exception as e:
  print("Erro ao chamar a API da OpenAI:", e)
