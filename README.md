# 📄 Documentação: Gerador de PDF do Currículo

Esta ferramenta automatiza a geração de um PDF a partir de uma página web usando **Pyppeteer** e **Chromium**. Abaixo estão as instruções para instalação, configuração e automação com `crontab`.

---

## ✅ 1. Pré-requisitos

Antes de começar, certifique-se de ter:

* **Python 3.7+** instalado;
* **Chromium** instalado (`chromium` ou `chromium-browser` em sistemas Debian/Ubuntu);
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
   pip install pyppeteer
   ```

---

## 🔁 3. Agendamento com `crontab` (execução automática)

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

### Explicação:

| Elemento          | Função                                   |
| ----------------- | ---------------------------------------- |
| `*/5 * * * *`     | Executa a cada 5 minutos                 |
| `venv/bin/python` | Usa o Python com dependências instaladas |
| `generate_pdf.py` | Script que gera o PDF                    |

---

---

## 🧪 Teste Manual

Você pode rodar manualmente o script com:

```bash
/home/seu-usuario/projects/generate_pdf/venv/bin/python /home/seu-usuario/projects/generate_pdf/generate_pdf.py
```

---