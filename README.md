# AeroMotion Dynamics - Central de IA e Análise Industrial

Sistema integrado de inteligência artificial de ponta a ponta para monitoramento preditivo de turbinas industriais e inspeção de pás por visão computacional.

## Sobre

O projeto da **AeroMotion Dynamics S.A.** atende às quatro bancadas de testes de desenvolvimento (`TURB-101` a `TURB-104`). A solução antecipa modos de falha críticos em rolamentos e rotores através de telemetria IoT em tempo real, além de automatizar o controle de qualidade geométrico e térmico de pás na linha de montagem com visão computacional.

### Principais Recursos
- **Diagnóstico Preditivo Multiclasse:** Identificação precisa dos modos de operação (Normal, Desgaste de Rolamento, Desbalanceamento de Rotor e Cavitação/Superaquecimento).
- **Detecção Não Supervisionada de Anomalias:** Algoritmo *Isolation Forest* treinado com dados nominais para flagrar desvios não catalogados.
- **Visão Computacional Multimodal (OpenCV):** Comparação morfológica contra gabarito padrão com detecção de pás deformadas/tortas (`cv2.matchShapes`) e segmentação de hotspots de calor no espaço HSV.
- **Microsserviço RESTful:** API assíncrona FastAPI pronta para integração com CLP e supervisórios SCADA industriais.
- **Centro de Monitoramento Web:** Dashboard Streamlit com ícones SVG industriais e métricas interativas em tempo real.

## Requisitos

- Python 3.10 ou superior
- Docker e Docker Compose (opcional, para implantação em contêineres Edge)

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/aeromotion-dynamics.git
cd aeromotion-dynamics
python -m venv .venv
# No Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# No Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

### Execução Local Rápida (Windows)
Execute o script em lote para iniciar a API e a interface web simultaneamente:

```cmd
scripts\iniciar-sistema.bat
```

### Execução Manual
Em terminais separados:

1. **Iniciando a API FastAPI:**
```bash
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```
Acesse a documentação Swagger em: `http://127.0.0.1:8000/docs`

2. **Iniciando o Dashboard Streamlit:**
```bash
python -m streamlit run src/frontend/app.py --server.port 8501
```
Acesse o painel central em: `http://127.0.0.1:8501`

### Execução com Docker (Edge Computing)
```bash
docker-compose up --build -d
```

## Estrutura do Projeto

```text
├── .github/
│   └── workflows/              # Automações de CI/CD
├── assets/
│   ├── dados/                  # Telemetria e séries temporais originais
│   ├── imagens/                # Amostras térmicas e ópticas para visão
│   └── modelos/                # Modelos treinados (.joblib) e scalers
├── docs/                       # Especificações, cadernos de treino e relatórios
│   ├── parecer-tecnico-regulatorio-etico-mlops.pdf
│   ├── parecer-tecnico-regulatorio-etico-mlops.md
│   └── notebook-treinamento-ia.ipynb
├── scripts/                    # Scripts utilitários e de inicialização
│   ├── iniciar-sistema.bat
│   └── gerar-pdf-parecer.py
├── src/                        # Código-fonte principal da aplicação
│   ├── api/                    # Microsserviço FastAPI e schemas Pydantic
│   │   └── app.py
│   └── frontend/               # Dashboard interativo com Streamlit
│       └── app.py
├── tests/                      # Testes automatizados (pytest)
│   └── test_api.py
├── .editorconfig
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUINDO.md
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
└── requirements.txt
```

## Testes

Para executar os testes automatizados da aplicação:

```bash
python -m unittest discover -s tests -v
```


## Contribuindo

Consulte o arquivo [CONTRIBUINDO.md](CONTRIBUINDO.md) para detalhes sobre fluxo de trabalho de branches, padrões de código e mensagens de commit.

## Licença

Este projeto está licenciado sob os termos da licença [MIT](LICENSE).
