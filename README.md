# 🏥 G.STEC - Gestão dos Setores de Engenharia Clínica

**G.STEC** é um sistema web para gerenciar processos de aquisição e planejamento de engenharia clínica em hospitais universitários, com foco em Atas de Registro de Preço (ARP), Monitoramento do PNCP, e módulos futuros como Custos Internos, Indicadores e Planejamento (RDC e Planeja HU).

## 🚀 Funcionalidades Atuais

- 📜 **Gestão de Atas**
  - Lista de Atas
  - Cadastro de novas Atas com múltiplos itens

- 🌐 **Monitoramento PNCP**git s
  - Consulta de Atas PNCP por número de controle
  - Monitoramento de Contratações públicas com filtros por data, modalidade e UASG

## 📊 Em Desenvolvimento

- Painel de Indicadores
- Módulo de Custos Internos
- Benchmarking entre Hospitais
- Planejamento (Planeja HU e RDCs)
- Gestão de Usuários e Hospitais

## 🛠 Tecnologias Utilizadas

- **Backend**: Python (Django)
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla), HTMX (em breve)
- **Banco de Dados**: SQLite (desenvolvimento)

## 📦 Instalação Local

```bash
git clone https://github.com/victoracioly/g.stec.git
cd g.stec
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
🌍 Acesse em Produção
https://victoracioly.pythonanywhere.com/

📄 Licença
Este projeto é de uso acadêmico/institucional. Direitos reservados.