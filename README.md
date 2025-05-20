# Gestão de Atas - Ebserh

Sistema web para apoio à gestão das Atas de Registro de Preço (ARPs) da rede Ebserh, com foco inicial em equipamentos médico-hospitalares. A ferramenta tem como objetivo organizar, padronizar e facilitar a consulta das ARPs utilizadas pelos hospitais da rede, promovendo governança, eficiência, padronizações e colaboração entre engenheiros clínicos.

---

## Objetivo Geral

Permitir que engenheiros clínicos da Ebserh tenham uma visão integrada de:
- Quais atas estão sendo utilizadas por cada hospital;
- Quais os itens disponíveis em cada ata;
- Qual o saldo de cada ata para adesão;
- Padronizar descrições técnicas por meio de colaboração entre os engenheiros da rede.

---

## Etapas do Projeto

### Etapa 1 – Módulo Local de Gestão de Atas [EM DESENVOLVIMENTO]
- Cadastro manual de atas por hospital (UASG)
- Cadastro de itens da ata (nome, marca, valor, empresa, etc.)
- Correção colaborativa de descrições técnicas
- Sugestão de código CATMAT
- Identificação por tipo: bem ou serviço (serviço desativado por ora)
- Busca por nome de equipamento

### Etapa 2 – Integração com Dados Públicos
- Consulta automática às APIs do governo federal (ComprasNet/SIASG)
- Importação de atas, itens e status (vigente/encerrada)
- Cálculo de empenhos e saldos para adesão (via Portal da Transparência)
- Atualização periódica das atas vinculadas

### Etapa 3 – Dashboards e Indicadores Estratégicos
- Hospitais com maior número de atas homologadas
- Atas com maior ou menor execução
- Equipamentos mais adquiridos em rede
- Visualização por ano e por tipo de item

### Etapa 4 – Módulo para Contratos de Serviços
- Inclusão de campos para prestação de serviços (escopo, postos, jornada)
- Gestão de contratos continuados
- Indicadores próprios de contratos de serviço

---

## Tecnologias Utilizadas
- Python + Django
- SQLite (inicial) / PostgreSQL (futuro)
- Bootstrap (para interface)
- APIs públicas de dados abertos do governo federal

---

## Contribuição Esperada
Engenheiros clínicos da Ebserh poderão:
- Cadastrar atas utilizadas em seus hospitais
- Corrigir e padronizar descrições de equipamentos
- Ajudar a criar uma base colaborativa e confiável de ARPs

---

## Licença
Projeto em desenvolvimento. Uso interno da Ebserh.
"""

# Salvar o README.md
with open(readme_path, "w", encoding="utf-8") as file:
    file.write(readme_content)

readme_content
