# 🧹 Data Cleaning & SQL Integration Dashboard

Este repositório apresenta um painel demonstrativo Full-Stack voltado para automação de processos de higienização, tratamento e modelagem de dados brutos (Data Cleaning).

## 🛠️ Tecnologias Utilizadas
* **Front-End**: HTML5 e CSS3 estruturados para o painel visual (`index.html`).
* **Back-End**: Python (Pandas e SQLite3) para inteligência e execução de pipelines de tratamento (`server.py`).
* **Banco de Dados**: Estrutura e população de tabelas simuladas via comandos estruturados em SQL (`database.sql`).

## 📊 Regras de Negócio Executadas pelo Back-End (Python)
O script `server.py` foi desenvolvido de forma enxuta e otimizada para realizar de maneira automatizada:
1. **Tratamento de Nulos**: Identificação e exclusão de registros com campos essenciais (como o nome) vazios.
2. **Deduplicação**: Identificação e eliminação de cadastros repetidos na base mantendo apenas a primeira ocorrência.
3. **Validação de Sintaxe**: Filtro rigoroso em strings para validação de e-mails (garantindo a presença do caractere `@`).
4. **Consistência de Dados**: Higienização e descarte de números de telefone inconsistentes ou com tamanho fora do padrão mínimo.

## 🚀 Como o projeto funciona
* A interface em **GitHub Pages** funciona como uma camada de visualização estática do painel do usuário.
* O motor de processamento em **Python** e as queries em **SQL** atuam na raiz do projeto manipulando o arquivo local `dados.db`, garantindo que toda a massa de dados seja limpa antes de ser persistida de forma definitiva no banco.
