# Histórico de Mudanças (Changelog)

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2026-10-27

### Adicionado
- Frontend interativo em Streamlit com ícones SVG modernos e responsivos.
- Módulo de visão computacional comparativo para detecção de pás deformadas e objetos tortos via `cv2.matchShapes`.
- Inspeção térmica no espaço de cor HSV para delimitação de hotspots críticos.
- Microsserviço RESTful em FastAPI com schemas Pydantic e endpoints assíncronos.
- Conteinerização completa com Dockerfile e docker-compose para Edge Computing.
- Documentação regulatória (LGPD, EU AI Act) e plano de MLOps em PDF consolidado.

### Alterado
- Estrutura de diretórios reorganizada para o padrão profissional Git em kebab-case (`src/`, `assets/`, `docs/`, `scripts/`, `tests/`).
- Atualizados caminhos de carregamento de artefatos treinados e imagens térmicas.

### Corrigido
- Tratamento de outliers e ruídos eletromagnéticos nas séries temporais (-99 mm/s e 999.9 °C).
- Liberação automática de portas locais de rede no script de inicialização.
