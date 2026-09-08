"""
Módulo de Calendário de Provas e Entregas do StudySpace.
Lista as próximas avaliações, permite cadastrar novas e destaca as mais urgentes.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
from datetime import datetime
import uuid


def render_calendar_view(dm):
    st.markdown("## 📅 Calendário de Provas & Entregas")
    st.markdown("Acompanhe suas próximas avaliações e entregas, organizadas por proximidade da data.")

    subjects = dm.get_subjects()
    subject_map = {s["id"]: s for s in subjects}
    exams = dm.get_exams()
    now = datetime.now()

    if not subjects:
        st.warning("⚠️ Cadastre pelo menos uma matéria na aba 'Matérias e Controle de Faltas' antes de adicionar provas.")

    # --- KPIs ---
    total_exams = len(exams)
    urgent_count = 0
    for e in exams:
        try:
            dt = datetime.strptime(e["date"], "%Y-%m-%d")
            if 0 <= (dt - now).days <= 7:
                urgent_count += 1
        except Exception:
            pass

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avaliações Cadastradas</div>
            <div class="kpi-value">{total_exams}</div>
            <div class="kpi-subtext">provas e entregas no total</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Nos Próximos 7 Dias</div>
            <div class="kpi-value" style="color: #DC2626;">{urgent_count}</div>
            <div class="kpi-subtext">exigem atenção imediata</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # --- Formulário para adicionar nova prova/entrega ---
    with st.expander("➕ Adicionar Nova Prova ou Entrega", expanded=(total_exams == 0 and len(subjects) > 0)):
        if not subjects:
            st.info("Cadastre uma matéria primeiro para poder vincular uma prova a ela.")
        else:
            with st.form("form_add_exam", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    ex_title = st.text_input("Título *", placeholder="Ex: P2 - Cálculo I")
                    ex_subject = st.selectbox(
                        "Disciplina",
                        options=list(subject_map.keys()),
                        format_func=lambda x: subject_map[x]["name"]
                    )
                    ex_date = st.date_input("Data")
                with col2:
                    ex_time = st.text_input("Horário", placeholder="Ex: 14:00", value="08:00")
                    ex_room = st.text_input("Local / Sala", placeholder="Ex: Biênio - Sala 12")
                    ex_importance = st.selectbox("Importância", ["Baixa", "Média", "Alta", "Crítica"], index=2)
                ex_topics = st.text_area("Conteúdo / Tópicos que Cairão", placeholder="Ex: Derivadas, Regra da Cadeia...")

                if st.form_submit_button("💾 Salvar Prova/Entrega", use_container_width=True):
                    if not ex_title.strip():
                        st.error("Por favor, digite um título para a avaliação.")
                    else:
                        new_exam = {
                            "id": f"exam_{uuid.uuid4().hex[:8]}",
                            "subject_id": ex_subject,
                            "title": ex_title.strip(),
                            "date": ex_date.strftime("%Y-%m-%d"),
                            "time": ex_time.strip() or "08:00",
                            "room": ex_room.strip() or "A definir",
                            "topics": ex_topics.strip(),
                            "weight": 1.0,
                            "importance": ex_importance
                        }
                        dm.add_exam(new_exam)
                        st.success("Avaliação cadastrada com sucesso!")
                        st.rerun()

    st.markdown("#### 🗓️ Próximas Avaliações")

    if not exams:
        st.info("Nenhuma prova ou entrega cadastrada ainda.")
        return

    importance_colors = {"Crítica": "#DC2626", "Alta": "#EF4444", "Média": "#F59E0B", "Baixa": "#10B981"}

    for e in exams:
        s = subject_map.get(e.get("subject_id"), {"name": "Geral", "color": "#3B82F6"})
        try:
            dt = datetime.strptime(e["date"], "%Y-%m-%d")
            days_left = (dt - now).days
            if days_left < 0:
                days_label = "Já passou"
                days_color = "#5B6B8C"
            elif days_left == 0:
                days_label = "É hoje!"
                days_color = "#DC2626"
            else:
                days_label = f"Faltam {days_left} dia(s)"
                days_color = "#EF4444" if days_left <= 7 else "#2563EB"
        except Exception:
            days_label = "Data inválida"
            days_color = "#5B6B8C"

        imp_color = importance_colors.get(e.get("importance", "Média"), "#3B82F6")

        col_info, col_actions = st.columns([5, 1])
        with col_info:
            st.markdown(f"""
            <div style="background: rgba(27,42,74,0.05); border-left: 5px solid {s.get('color', '#3B82F6')};
                        border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <span style="font-weight: 700; font-size: 1.05rem; color: #1B2A4A;">{e['title']}</span>
                    <span style="background: {imp_color}22; color: {imp_color}; border: 1px solid {imp_color}55;
                                 padding: 2px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">
                        {e.get('importance', 'Média')}
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #4B5A78; margin: 4px 0;">
                    {s.get('name')} · 📅 {e['date']} às {e.get('time', '--:--')} · 📍 {e.get('room', 'A definir')}
                </div>
                <div style="font-size: 0.85rem; font-weight: 700; color: {days_color};">⏳ {days_label}</div>
                {f'<div style="font-size: 0.8rem; color: #33456B; margin-top: 6px;">📖 {e["topics"]}</div>' if e.get('topics') else ''}
            </div>
            """, unsafe_allow_html=True)
        with col_actions:
            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"del_exam_{e['id']}", help="Excluir avaliação"):
                dm.delete_exam(e["id"])
                st.rerun()
