"""
StudySpace - Plataforma de Estudos Individual
Desenvolvida para o Processo Seletivo do Poli AI Club.
Autor: Sofia Andreão da Silva
"""

# pyrefly: ignore [missing-import]
import streamlit as st
from datetime import datetime

# Configuração da página precisa ser o primeiro comando Streamlit
st.set_page_config(
    page_title="StudySpace · Plataforma de Estudos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importações dos módulos da aplicação
from config import APP_TITLE, APP_SUBTITLE, APP_ICON, CUSTOM_CSS
from data_manager import DataManager
from modules.calendar_view import render_calendar_view
from modules.attendance_view import render_attendance_view
from modules.grades_view import render_grades_view
from modules.study_assistant_view import render_study_assistant_view

# Injetar estilos visuais modernos
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Instanciar gerenciador de dados
dm = DataManager()
if hasattr(dm, "get_settings"):
    settings = dm.get_settings()
else:
    settings = {
        "student_name": "Estudante",
        "institution_name": "Minha Faculdade / Colégio",
        "academic_period": "2026/2"
    }

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown(f"## {APP_ICON} **{APP_TITLE}**")
    st.caption(f"Plataforma de Estudos Individual")
    
    # Cartão de Perfil Personalizado do Estudante
    st.markdown(f"""
    <div style="background: rgba(27,42,74,0.05); border: 1px solid rgba(27,42,74,0.12); border-radius: 10px; padding: 10px 14px; margin: 10px 0;">
        <div style="font-size: 0.75rem; text-transform: uppercase; color: #253A5C; font-weight: 700;">Estudante</div>
        <div style="font-size: 1.05rem; font-weight: 800; color: #0F1B33;">{settings.get('student_name', 'Meu Nome')}</div>
        <div style="font-size: 0.8rem; color: #2563EB;">{settings.get('institution_name', 'Minha Instituição')}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.popover("Personalizar Meu Perfil"):
        st.markdown("##### Seus Dados")
        p_name = st.text_input("Seu Nome:", value=settings.get("student_name", "Estudante"))
        p_inst = st.text_input("Faculdade / Escola / Colégio:", value=settings.get("institution_name", "Minha Instituição"))
        p_period = st.text_input("Semestre / Ano:", value=settings.get("academic_period", "2026/2"))
        
        if st.button("💾 Salvar Perfil", key="save_profile_btn", use_container_width=True):
            dm.update_settings({
                "student_name": p_name.strip() or "Estudante",
                "institution_name": p_inst.strip() or "Minha Instituição",
                "academic_period": p_period.strip() or "2026/2"
            })
            st.success("Perfil atualizado!")
            st.rerun()

    st.markdown("---")

    menu_options = [
        "Calendário de Provas",
        "Matérias e Controle de Faltas",
        "Calculadora de Médias",
        "Foco & Cronograma",
    ]
    
    selected_page = st.radio("Navegação Principal", menu_options, index=0)

    st.markdown("---")
    
    # Resumo Rápido na Sidebar
    subjects = dm.get_subjects()
    exams = dm.get_exams()
    
    st.markdown("##### Visão Rápida")
    st.write(f"**{len(subjects)}** Disciplinas Cursando")
    st.write(f"**{len(exams)}** Avaliações Agendadas")

    # Alerta de Faltas na Sidebar
    risky_subjects = []
    for s in subjects:
        st_att = dm.get_attendance_stats(s)
        if st_att["status"] in ["danger", "failed"]:
            risky_subjects.append(s["name"])

    if risky_subjects:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid #EF4444; border-radius: 8px; padding: 10px; font-size: 0.8rem; color: #B91C1C; margin-top: 10px;">
            <strong>Alerta de Frequência!</strong><br>
            Atenção em: {', '.join(risky_subjects[:2])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("*Construído com Python, Streamlit e Antigravity IDE.*")


# --- CABEÇALHO PRINCIPAL (HERO BANNER) ---
st.markdown(f"""
<div class="header-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div class="header-title">{APP_ICON} {APP_TITLE}</div>
            <div class="header-subtitle">{APP_SUBTITLE}</div>
        </div>
        <div style="text-align: right; margin-top: 8px;">
            <span class="badge badge-info">{settings.get('student_name', 'Estudante')}</span>
            <span class="badge badge-safe">{settings.get('institution_name', 'Minha Instituição')}</span>
            <span class="badge badge-warning">{settings.get('academic_period', '2026/2')}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- ROTEAMENTO DE PÁGINAS ---
if selected_page == "Calendário de Provas":
    render_calendar_view(dm)
elif selected_page == "Matérias e Controle de Faltas":
    render_attendance_view(dm)
elif selected_page == "Calculadora de Médias":
    render_grades_view(dm)
elif selected_page == "Foco & Cronograma":
    render_study_assistant_view(dm)
