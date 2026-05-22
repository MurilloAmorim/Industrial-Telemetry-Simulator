# Industrial Telemetry Simulator & Autonomous Protection System

O **Industrial Telemetry Simulator** é um ecossistema de software em Python projetado para simular o monitoramento e o controle autônomo de variáveis elétricas em plantas de geração de energia (como usinas solares ou hidrelétricas). 

O projeto simula um cenário industrial real dividido em duas camadas independentes: uma **API Backend Central (Sistema de Supervisão)** e um **Injetor de Telemetria (Simulador de Hardware Embarcado)**.

---

## Arquitetura do Sistema

O sistema é estruturado seguindo o modelo de microsserviços e comunicação cliente-servidor comum em redes industriais:

1. **Central Control Unit (Servidor API):** Desenvolvido em **FastAPI**, funciona como o cérebro da operação (similar a um sistema SCADA). Ele processa dados em tempo real, valida payloads e toma decisões de proteção autônoma baseadas em regras de negócio críticas.
2. **Field Device Simulator (Injetor de Hardware):** Script Python assíncrono que emula os sensores físicos de campo na planta, gerando leituras contínuas de tensão elétrica e transmitindo-as via requisições HTTP POST para a central.

---

## Lógica de Operação Autônoma (Proteção de Grade)

Para atender aos rigorosos requisitos de segurança de plantas de geração, o sistema possui uma **regra de atuação automatizada a nível de software**:
- **Monitoramento de Tensão:** A API analisa cada leitura enviada pelos sensores.
- **Intervenção em Tempo Real (Trip Autônomo):** Caso a tensão elétrica ultrapasse o limite crítico de **240.0 Volts**, o sistema entra em estado de `ALERTA_CRÍTICO` e altera o status do disjuntor principal para `DESLIGADO` de forma 100% autônoma, protegendo os geradores contra sobrecarga antes mesmo da intervenção de um operador humano.

---

## Tecnologias Utilizadas

- **Python 3**
- **FastAPI:** Framework de alto desempenho para a construção da API e roteamento de telemetria.
- **Pydantic:** Validação rigorosa de tipos de dados de entrada (Data Enforcement) para impedir dados corrompidos de sensores na rede.
- **Uvicorn:** Servidor ASGI de velocidade ultrarrápida para sustentação do backend.
- **Requests:** Utilizado no módulo de hardware para transmissão de pacotes binários/JSON via rede.

---

## Estrutura do Projeto

```text
industrial-telemetry-simulator/
│
├── app/
│   ├── __init__.py
│   └── main.py          # Código principal da API (FastAPI) e lógica de proteção
│
├── hardware_sim/
│   └── injector.py      # Simulador de sensores e gerador de carga elétrica
│
├── .gitignore           # Isolamento seguro de ambientes (.venv) e caches
└── requirements.txt     # Gerenciamento unificado de dependências do ecossistema
