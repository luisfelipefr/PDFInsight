# 📄 Documentação: Gerador de PDF do Currículo

Esta ferramenta automatiza a geração de um PDF a partir de uma página web usando **Pyppeteer** e **Chromium**. Abaixo estão as instruções para instalação, configuração e automação com `crontab`.

---

## ✅ 1. Pré-requisitos

Antes de começar, certifique-se de ter:

* **Python 3.7+** instalado;
* **Chromium** instalado (`chromium` ou `chromium-browser` em sistemas Debian/Ubuntu);
* Conta **OpenAi** com chave API ativa
* Um **ambiente virtual (venv)** criado e ativado (recomendado).

---

## ⚙️ 2. Instalação

1. Clone o repositório e acesse a pasta:

   ```bash
   git clone https://github.com/seu-usuario/generate_pdf
   cd generate_pdf
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências do projeto:

   ```bash
   python3 install pyppeteer pypdf openai python-dotenv
   ```

4. Configure seu arquivo `.env` com sua chave da OpenAI:
   ```ini
   API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 🛠️ 3. Como funciona

1. O script baixa a página HTML e verifica se houve alteração (via hash SHA256).

2. Se houver mudança, gera um novo PDF da página usando Pyppeteer e Chromium.

3. O nome do PDF é salvo automaticamente em um arquivo de referência (last_pdf.txt).

4. Outro script lê o PDF, extrai todo o texto com o pypdf e salva em pdfReader.txt.

5. O texto extraído é enviado para a OpenAI (modelo GPT-4 ou GPT-3.5-turbo) junto com um prompt customizável (em prompt.txt), que instrui a IA a retornar apenas os pontos principais e relevantes.

6. O resultado é exibido no terminal ou pode ser salvo conforme sua necessidade.

### Explicação:

| Elemento          | Função                                   |
| ----------------- | ---------------------------------------- |
| `*/5 * * * *`     | Executa a cada 5 minutos                 |
| `venv/bin/python` | Usa o Python com dependências instaladas |
| `generate_pdf.py` | Script que gera o PDF                    |

---

## 🔁 4. Agendamento com `crontab` (execução automática)

Para gerar o PDF automaticamente a cada 5 minutos **apenas se houver mudança no conteúdo**, use o `crontab`.

### Passos:

1. Verifique se o ambiente virtual tem o `pyppeteer` instalado:

   ```bash
   /home/seu-usuario/projects/generate_pdf/venv/bin/python -m pip show pyppeteer
   ```

2. Edite o crontab:

   ```bash
   crontab -e
   ```

3. Adicione a seguinte linha:

   ```bash
   */5 * * * * /home/seu-usuario/projects/generate_pdf/venv/bin/python /home/seu-usuario/projects/generate_pdf/generate_pdf.py
   ```

---

## 🧪 Teste Manual

Você pode rodar manualmente o script com:

```bash
/home/seu-usuario/projects/generate_pdf/venv/bin/python /home/seu-usuario/projects/generate_pdf/generate_pdf.py
```

---

## 💡 Dicas
Personalize o prompt no prompt.txt para resultados conforme seu contexto (dashboard, currículo, etc).

Utilize o histórico de PDFs e logs para auditoria ou versionamento.

Troque o modelo para gpt-3.5-turbo se não tiver acesso ao GPT-4.

Utilize sempre o melhor modelo para oque você está precisando no momento


##### ⚠️ Atenção: O caminho /home/seu-usuario/projects/generate_pdf/ apresentado nos exemplos deve ser adaptado conforme a estrutura de pastas e o nome de usuário do seu próprio sistema.
