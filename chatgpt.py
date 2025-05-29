import os
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))


with open("last_pdf.txt", "r") as f:
  PDF_NAME = f.read().strip()
  
reader = PdfReader(PDF_NAME)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

PDF_EXTRACT = 'pdfReader.txt'

all_text = ""
for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        all_text += page_text + "\n"

with open(PDF_EXTRACT, "w", encoding="utf-8") as f:
    f.write(all_text)

with open("prompt.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

try:
  response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
      {"role": "system", "content": instructions},
      {"role": "user", "content": f"Eu tenho esse texto extraído do PDF:\n{all_text}\nLeia ele e me pontue os pontos principais. Criando um markdown, irei armazenar esse valor em um arquivo .md"}
    ]
  )
  print(response.choices[0].message.content)
  with open("response.md", "w") as f:
    f.write(response.choices[0].message.content)

except Exception as e:
  print("Erro ao chamar a API da OpenAI:", e)