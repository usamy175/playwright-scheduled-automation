# Playwright Scheduled Automation

**English overview:** This repository is a safe portfolio project that demonstrates scheduled browser automation with Python and Playwright. It uses a fully local demo web application to show authentication, task execution, logging, error handling, screenshots on failure and environment-based configuration without exposing real services, credentials, cookies or private business rules.

## Por que este projeto existe

Este projeto foi criado para transformar uma experiência prática com automação web em uma demonstração pública, segura e profissional para portfólio. A proposta é mostrar domínio de Python, Playwright, organização de código, configuração por ambiente, logs e tratamento de falhas em um cenário que simula uma rotina real, mas sem depender de qualquer plataforma externa.

Em vez de automatizar um serviço real, o repositório traz uma aplicação local criada apenas para a demonstração. Isso permite explicar o raciocínio técnico por trás da automação sem publicar credenciais, cookies, tokens, seletores privados, URLs reais ou regras de negócio sensíveis.

O objetivo é servir como material de apoio em candidaturas para estágio ou posições iniciais em desenvolvimento, QA automation, automação web, RPA e inteligência artificial aplicada a fluxos operacionais.

## O problema demonstrado

Muitos processos digitais seguem um padrão parecido:

- acessar uma página protegida por login;
- executar uma ação recorrente em uma área autenticada;
- registrar quando a execução aconteceu;
- capturar evidências de sucesso ou falha;
- repetir o processo em intervalos configuráveis;
- encerrar recursos corretamente para evitar processos presos.

Este projeto demonstra esse fluxo em um ambiente controlado. A aplicação local simula um sistema com autenticação, dashboard e botão de ação. A automação acessa esse sistema, realiza login com credenciais demonstrativas, executa a ação e grava o resultado em logs.

## Tecnologias utilizadas

- **Python 3.10+**: linguagem principal do projeto.
- **Playwright**: automação de navegador para login, navegação e interação com elementos.
- **Biblioteca padrão do Python**: servidor local com `http.server`, sem necessidade de framework web.
- **pytest**: testes básicos para configuração e aplicação local.
- **Variáveis de ambiente**: configuração flexível com `.env`.
- **Git e GitHub**: versionamento e publicação do projeto.

## Como foi feito

O projeto foi desenhado com separação clara de responsabilidades:

```text
playwright-scheduled-automation/
├── src/playwright_scheduled_automation/
│   ├── automation.py       # Fluxo Playwright: login, ação, logs e erros
│   ├── cli.py              # Interface de linha de comando
│   ├── config.py           # Leitura de .env e variáveis de ambiente
│   ├── local_app.py        # Aplicação web local simulada
│   ├── logging_config.py   # Configuração dos logs
│   └── scheduler.py        # Execução recorrente por intervalo
├── tests/
│   ├── test_config.py      # Testes de configuração
│   └── test_local_app.py   # Testes do fluxo local de login e ação
├── logs/
├── screenshots/errors/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

### Aplicação local

A aplicação simulada foi construída com `ThreadingHTTPServer` e `BaseHTTPRequestHandler`, ambos da biblioteca padrão. Ela possui:

- tela de login;
- sessão demonstrativa via cookie local;
- área autenticada;
- botão de ação;
- mensagem visual de sucesso;
- endpoint `/health` para validação simples.

Essa escolha mantém o projeto leve e fácil de revisar. O foco do repositório não é construir uma aplicação web completa, e sim demonstrar automação sobre uma interface controlada.

### Automação com Playwright

O fluxo principal está em `automation.py`. Ele:

- abre um navegador Chromium via Playwright;
- acessa a aplicação local configurada;
- preenche usuário e senha demonstrativos;
- aguarda o redirecionamento para o dashboard;
- clica no botão da ação;
- aguarda a confirmação visual;
- grava logs de início, sucesso ou erro;
- salva screenshot em caso de falha;
- fecha o navegador no bloco final de execução.

Os seletores usam `data-testid`, que é uma prática comum em automação porque reduz acoplamento com CSS, layout e texto visual.

### Scheduler

O módulo `scheduler.py` executa a automação em loop respeitando `RUN_INTERVAL_SECONDS`. Isso permite testar com intervalos curtos, como 10 segundos, e documentar uma configuração realista de duas horas com `7200` segundos.

## Como executar

Clone o projeto:

```powershell
git clone https://github.com/usamy175/playwright-scheduled-automation.git
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

Instale o navegador gerenciado pelo Playwright:

```powershell
python -m playwright install chromium
```

Copie o arquivo de configuração:

```powershell
Copy-Item .env.example .env
```

Execute a demonstração completa:

```powershell
playwright-scheduled-automation demo
```

## Comandos disponíveis

Iniciar apenas a aplicação local:

```powershell
playwright-scheduled-automation serve
```

Executar o robô uma única vez:

```powershell
playwright-scheduled-automation run-once
```

Executar em modo programado:

```powershell
playwright-scheduled-automation schedule
```

Executar um número limitado de rodadas:

```powershell
playwright-scheduled-automation schedule --max-runs 2
```

## Variáveis de ambiente

O projeto usa `.env` para configuração local. O arquivo real não deve ser versionado; apenas `.env.example` fica público.

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

Para execução a cada duas horas:

```env
RUN_INTERVAL_SECONDS=7200
```

Para testes rápidos:

```env
RUN_INTERVAL_SECONDS=10
```

Se os navegadores gerenciados pelo Playwright não estiverem instalados, é possível usar um navegador local compatível:

```env
BROWSER_CHANNEL=msedge
```

ou:

```env
BROWSER_CHANNEL=chrome
```

## Logs, evidências e erros

Os logs são gravados em:

```text
logs/automation.log
```

Quando ocorre uma falha durante a automação, o projeto tenta salvar um screenshot em:

```text
screenshots/errors/
```

Esses artefatos são ignorados pelo Git para evitar publicação acidental de dados de execução.

## Testes

Execute:

```powershell
pytest
```

Os testes cobrem:

- leitura de valores booleanos e inteiros da configuração;
- validação de intervalo positivo;
- carregamento de `.env` sem sobrescrever variáveis já existentes;
- endpoint de saúde da aplicação local;
- fluxo básico de login e execução de ação.

## Segurança e privacidade

Este projeto foi preparado para publicação pública com os seguintes cuidados:

- não usa serviços externos;
- não contém chaves de API;
- não contém credenciais reais;
- não publica `.env`;
- não publica cookies, sessões, logs ou screenshots de erro;
- não contém domínio real, seletores privados ou regras de negócio sensíveis;
- usa apenas credenciais fictícias para a aplicação local;
- mantém o escopo técnico em automação web genérica.

## Métodos de publicação

O fluxo recomendado de publicação é:

1. criar um repositório público no GitHub;
2. revisar `.gitignore` antes do primeiro commit;
3. versionar apenas código, testes, documentação e `.env.example`;
4. manter `.env`, logs, screenshots e caches fora do Git;
5. publicar na branch `main`;
6. usar o README como página principal de explicação técnica do projeto.

Para atualizar o projeto depois da primeira publicação:

```powershell
git status
git add README.md
git commit -m "Improve project documentation"
git push
```

## Como apresentar no portfólio

Uma forma objetiva de apresentar este projeto:

> Desenvolvi uma automação web com Python e Playwright em ambiente local demonstrativo, simulando login, execução de ação programada, logs, screenshots em falha e configuração por variáveis de ambiente. O projeto foi estruturado para publicação segura em portfólio, sem uso de serviços reais ou dados sensíveis.

Competências demonstradas:

- automação de navegador;
- estruturação de projeto Python;
- uso de CLI;
- configuração por ambiente;
- tratamento de erros;
- testes automatizados;
- documentação técnica;
- preocupação com segurança e privacidade em projetos públicos.

## Possíveis melhorias futuras

- adicionar pipeline de CI com GitHub Actions;
- gerar relatório em JSON ou CSV a cada execução;
- criar testes end-to-end opcionais com Playwright;
- adicionar tipagem estática com `mypy`;
- adicionar lint/format com `ruff`;
- empacotar a aplicação com Docker;
- incluir um pequeno GIF ou screenshot demonstrativo no README.

## Aviso

Este projeto utiliza somente um ambiente local demonstrativo. Ele não acessa serviços reais, não interage com plataformas externas e não deve ser adaptado para violar termos de uso, políticas de plataformas ou leis aplicáveis.
