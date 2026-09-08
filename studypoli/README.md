# 🎓 StudySpace

Plataforma pessoal de estudos construída em Python + Streamlit. Reúne em um só lugar o calendário de provas, o controle de faltas por matéria, a calculadora/simulador de médias e um assistente de foco e cronograma.

Projeto desenvolvido para o processo seletivo do Poli AI Club.

## ✨ Funcionalidades

- **📅 Calendário de Provas** — cadastro de provas e entregas, com destaque para as mais próximas.
- **⚠️ Matérias e Controle de Faltas** — acompanha o percentual de faltas de cada disciplina e alerta quando o risco de reprovação por frequência aumenta.
- **🧮 Calculadora de Médias** — calcula a média ponderada atual e simula a nota necessária nas próximas avaliações para passar.
- **🧠 Foco & Cronograma** — lista de tarefas por disciplina, timer Pomodoro e um diagnóstico automático que cruza provas próximas com matérias em risco.

## 🗂️ Estrutura do projeto

```
studyspace/
├── app.py                        # Ponto de entrada e roteamento das páginas
├── config.py                     # Título, ícone e CSS customizado
├── data_manager.py                # Persistência dos dados (JSON) e regras de cálculo
├── requirements.txt
└── modules/
    ├── __init__.py
    ├── calendar_view.py           # Aba "Calendário de Provas"
    ├── attendance_view.py         # Aba "Matérias e Controle de Faltas"
    ├── grades_view.py              # Aba "Calculadora de Médias"
    └── study_assistant_view.py    # Aba "Foco & Cronograma"
```

Os dados são salvos localmente em `data/student_data.json`, criado automaticamente na primeira execução.

## 🚀 Rodando localmente

```bash
# 1. Clone o repositório
git clone <url-do-seu-repositorio>
cd studyspace

# 2. (Opcional, mas recomendado) crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`.

## ☁️ Deploy (link público)

1. Suba este repositório para o GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com o GitHub.
3. Clique em **New app**, selecione o repositório, a branch e informe `app.py` como arquivo principal.
4. Clique em **Deploy**. Em 1–2 minutos você recebe uma URL pública (`seu-app.streamlit.app`).

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io) — interface web
- [Plotly](https://plotly.com/python/) — gráficos de faltas e médias
- Persistência simples em JSON, sem necessidade de banco de dados

## 👤 Autor

Sofia Andreão da Silva — Processo Seletivo Poli AI Club
