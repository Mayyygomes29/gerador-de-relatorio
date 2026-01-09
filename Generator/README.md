# Data Analyzer – Análise de Dados e Geração de Relatórios em PDF

### Visão Geral

O Data Analyzer é um projeto desenvolvido em Python com Django que permite a análise automática de arquivos de dados (CSV, Excel, Json, Xml), geração de estatísticas descritivas, criação de gráficos e exportação de relatórios em PDF.

O objetivo do projeto é facilitar a extração de insights de dados brutos, sem a necessidade de ferramentas complexas como Power BI ou Excel avançado, sendo ideal para análises rápidas, estudos exploratórios e relatórios automatizados.

### Problema Resolvido

- Usuários que trabalham com dados frequentemente precisam:

- Identificar padrões rapidamente

- Gerar estatísticas e visualizações

- Criar relatórios para compartilhamento

Esse projeto automatiza todo esse processo, permitindo que o usuário faça upload do arquivo e receba análises visuais e relatórios prontos para download.

### Funcionalidades

- Upload de arquivos CSV, Excel, JSON, XML

- Detecção automática de separador de CSV

- Leitura e tratamento de dados com Pandas

- Seleção automática de colunas numéricas

- Geração de estatísticas descritivas

- Criação de gráficos (histogramas)

- Exportação de relatórios em PDF

- Integração entre backend Django e visualização de dados

### Tecnologias Utilizadas

- Python 3
- Django
- Pandas
- Matplotlib
- HTML5 / CSS3
- Render (deploy da aplicação)

### Estrutura do Projeto
```
Generator/
│── file/
│ ├── migrations/
│ ├── templates/
│ │ ├── error.html
│ │ ├── graphs.html
│ │ ├── stats.html
│ │ └── upload.html
│ │
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
│
│── Generator/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│ └── .env
│ └── Procfile
│ └── render.yaml
| 
│── runtime.txt
│── db.sqlite3
│── manage.py
│── requirements.txt
│── .gitignore
│── venv/
```

### Exemplos de Uso

- Upload de arquivo CSV ou Excel

- Visualização das estatísticas dos dados

- Geração automática de gráficos

- Download de relatório em PDF com gráficos e tabelas

### Aprendizados

- Manipulação e limpeza de dados com Pandas

- Geração de visualizações com Matplotlib

- Criação de relatórios em PDF a partir de dados analisados

- Integração entre Django e análise de dados

- Boas práticas na organização de projetos Python/Django

### Próximas Melhorias

- Dashboard interativo com filtros dinâmicos

- Exportação para outros formatos (Excel, CSV tratado)

- Deploy em ambiente cloud (Render, AWS ou Railway)

- Autenticação de usuários

- Histórico de análises realizadas

### Autora

##### Mayara Gomes Silva
##### Formada em Análise e Desenvolvimento de Sistemas
##### Pós-graduanda em Ciências de Dados e Big Data Analytics

📌 Projeto desenvolvido para fins de estudo, portfólio e aprimoramento em Análise de Dados e Desenvolvimento Python.
