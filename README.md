# Playwright Scheduled Automation

**English summary:** This project is a safe portfolio demo that shows how to build scheduled browser automation with Python and Playwright. It uses only a local simulated web application, demo credentials, structured logs, error screenshots and environment-based configuration.

## Objetivo do projeto

Este repositório demonstra uma automação web programada usando Python e Playwright em um ambiente totalmente local, seguro e genérico. A ideia é apresentar competências úteis para vagas de estágio em desenvolvimento, automação e inteligência artificial sem expor serviços reais, credenciais, cookies, tokens ou detalhes de contextos privados.

## Problema demonstrado

Muitas rotinas operacionais exigem acessar uma área autenticada, executar uma ação recorrente, registrar o resultado e lidar com falhas de forma rastreável. Este projeto simula esse fluxo com uma aplicação local:

- login com credenciais demonstrativas;
- acesso a uma área autenticada;
- execução de uma ação pelo robô;
- confirmação visual da ação concluída;
- logs com data, horário e resultado;
- screenshot automático quando ocorre erro;
- execução única ou execução programada por intervalo configurável.

## Tecnologias utilizadas

- Python 3.10+
- Playwright para automação do navegador
- `http.server` da biblioteca padrão para a aplicação local simulada
- `pytest` para testes básicos
- `.env` para configuração local
- Git para versionamento

## Arquitetura e funcionamento

```text
playwright-scheduled-automation/
├── src/playwright_scheduled_automation/
│   ├── automation.py       # Fluxo Playwright: login, ação e tratamento de erro
│   ├── cli.py              # Comandos de execução
│   ├── config.py           # Leitura de variáveis de ambiente e .env
│   ├── local_app.py        # Aplicação web local demonstrativa
│   ├── logging_config.py   # Configuração de logs
│   └── scheduler.py        # Execução recorrente por intervalo
├── tests/                  # Testes seguros da configuração e app local
├── logs/                   # Logs gerados em runtime
├── screenshots/errors/     # Screenshots gerados apenas em falhas
├── .env.example            # Exemplo público de configuração
├── .gitignore
└── pyproject.toml
```

O comando `demo` inicia a aplicação local em segundo plano, executa o robô e encerra o servidor ao final. Também é possível iniciar a aplicação com `serve` e rodar a automação separadamente com `run-once` ou `schedule`.

## Instalação

Clone ou baixe o projeto e entre na pasta:

```powershell
cd playwright-scheduled-automation
```

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -e ".[dev]"
```

Instale os navegadores do Playwright:

```powershell
python -m playwright install chromium
```

Se preferir usar um navegador já instalado, defina `BROWSER_CHANNEL=msedge` ou `BROWSER_CHANNEL=chrome` no `.env`.

## Configuração

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Variáveis disponíveis:

```env
APP_HOST=127.0.0.1
APP_PORT=8000
APP_BASE_URL=http://127.0.0.1:8000
APP_USERNAME=demo_user
APP_PASSWORD=demo_password
RUN_INTERVAL_SECONDS=10
HEADLESS=true
BROWSER_CHANNEL=
```

Para configurar execução a cada duas horas:

```env
RUN_INTERVAL_SECONDS=7200
```

Durante testes e demonstrações rápidas, use um intervalo curto, por exemplo:

```env
RUN_INTERVAL_SECONDS=10
```

## Execução

Rodar a demonstração completa uma vez:

```powershell
playwright-scheduled-automation demo
```

Iniciar somente a aplicação local:

```powershell
playwright-scheduled-automation serve
```

Executar o robô uma vez contra `APP_BASE_URL`:

```powershell
playwright-scheduled-automation run-once
```

Executar de forma programada:

```powershell
playwright-scheduled-automation schedule
```

Executar apenas duas rodadas para validação:

```powershell
playwright-scheduled-automation schedule --max-runs 2
```

## Logs e erros

Os logs são gravados em:

```text
logs/automation.log
```

Quando ocorre uma falha durante a automação, o projeto tenta salvar um screenshot em:

```text
screenshots/errors/
```

Esses arquivos são ignorados pelo Git para evitar exposição acidental de dados de runtime.

## Testes

Execute:

```powershell
pytest
```

Os testes cobrem a leitura segura de configuração, validação de intervalo e o fluxo básico da aplicação local.

## Medidas de segurança

- O projeto usa apenas uma aplicação local demonstrativa.
- O `.env` real é ignorado pelo Git.
- Apenas `.env.example` deve ser publicado.
- Cookies, sessões, screenshots de erro, logs e arquivos temporários são ignorados.
- Não há chaves de API, tokens, cookies reais ou credenciais reais.
- Não há referência a domínios, seletores, regras de negócio ou serviços externos usados em projetos pessoais anteriores.
- As credenciais incluídas são apenas dados de demonstração para o ambiente local.

## Aprendizados demonstrados

- Organização de projeto Python com `pyproject.toml`.
- Automação browser-based com Playwright.
- Separação entre configuração, app local, automação, scheduler e CLI.
- Tratamento de erros com logs claros e screenshots.
- Uso de variáveis de ambiente para parametrizar execução.
- Escrita de testes para partes seguras e determinísticas.
- Cuidados para publicar uma demo técnica sem expor dados sensíveis.

## Aviso

Este projeto utiliza somente um ambiente local demonstrativo. Ele não acessa serviços reais, não interage com plataformas externas e não deve ser adaptado para violar termos de uso, políticas de plataformas ou leis aplicáveis.
