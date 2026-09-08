"""
Módulo de Cronograma Dinâmico de Estudos, Foco Pomodoro e Assistente Inteligente.
Ajuda no combate à distração com celular e organiza tarefas por prioridade acadêmica.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
import time
from datetime import datetime, date
import uuid


def render_study_assistant_view(dm):
    st.markdown("## 🧠 Assistente de Estudos & Foco Produtivo")
    st.markdown("Organize seu cronograma diário, utilize o temporizador Pomodoro anti-distração e receba recomendações inteligentes de estudo.")

    tab_tasks, tab_pomodoro, tab_ai_advisor = st.tabs([
        "📋 Cronograma & Tarefas",
        "⏱️ Foco Pomodoro (Anti-Celular)",
        "🤖 Diagnóstico Inteligente de Estudos"
    ])

    subjects = dm.get_subjects()
    subject_map = {s["id"]: s for s in subjects}

    # --- ABA 1: TAREFAS E CRONOGRAMA ---
    with tab_tasks:
        st.markdown("#### 🎯 Suas Tarefas de Estudo")

        with st.expander("➕ Adicionar Nova Tarefa de Estudo", expanded=False):
            with st.form("form_add_task", clear_on_submit=True):
                col_t1, col_t2 = st.columns([3, 1])
                with col_t1:
                    task_text = st.text_input("O que você precisa estudar / entregar?", placeholder="Ex: Resolver 5 exercícios da lista de Dinâmica")
                with col_t2:
                    task_subj = st.selectbox(
                        "Disciplina",
                        options=list(subject_map.keys()),
                        format_func=lambda x: subject_map[x]["name"]
                    )
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    task_prio = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"], index=0)
                with col_p2:
                    pass

                if st.form_submit_button("Salvar Tarefa", use_container_width=True):
                    if task_text.strip():
                        new_t = {
                            "id": f"t_{uuid.uuid4().hex[:8]}",
                            "subject_id": task_subj,
                            "text": task_text.strip(),
                            "done": False,
                            "priority": task_prio
                        }
                        dm.add_task(new_t)
                        st.toast("Tarefa adicionada!")
                        st.rerun()

        tasks = dm.get_tasks()
        if not tasks:
            st.info("Nenhuma tarefa pendente! Adicione uma no botão acima.")
        else:
            col_todo, col_done = st.columns(2)
            with col_todo:
                st.markdown("##### 📌 Pendentes")
                pending_tasks = [t for t in tasks if not t.get("done", False)]
                for t in pending_tasks:
                    s = subject_map.get(t.get("subject_id"), {"name": "Geral", "color": "#3B82F6"})
                    prio_colors = {"Alta": "#EF4444", "Média": "#F59E0B", "Baixa": "#10B981"}
                    p_col = prio_colors.get(t.get("priority", "Média"), "#3B82F6")

                    col_chk, col_txt, col_del = st.columns([1, 8, 1])
                    with col_chk:
                        if st.button("⬜", key=f"toggle_t_{t['id']}", help="Marcar como concluída"):
                            dm.toggle_task(t["id"])
                            st.rerun()
                    with col_txt:
                        st.markdown(f"""
                        <div style="background: rgba(30, 41, 59, 0.5); padding: 8px 12px; border-radius: 8px; border-left: 4px solid {s.get('color', '#3B82F6')}; margin-bottom: 6px;">
                            <span style="font-weight: 600; color: #F1F5F9;">{t['text']}</span>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">
                                {s.get('name')} · <span style="color: {p_col}; font-weight: 700;">{t.get('priority')}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_del:
                        if st.button("🗑️", key=f"del_t_{t['id']}", help="Excluir"):
                            dm.delete_task(t["id"])
                            st.rerun()

            with col_done:
                st.markdown("##### ✅ Concluídas")
                done_tasks = [t for t in tasks if t.get("done", False)]
                for t in done_tasks:
                    s = subject_map.get(t.get("subject_id"), {"name": "Geral", "color": "#10B981"})
                    col_chk, col_txt, col_del = st.columns([1, 8, 1])
                    with col_chk:
                        if st.button("✅", key=f"untoggle_t_{t['id']}", help="Reabrir tarefa"):
                            dm.toggle_task(t["id"])
                            st.rerun()
                    with col_txt:
                        st.markdown(f"""
                        <div style="background: rgba(15, 23, 42, 0.4); padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; text-decoration: line-through; color: #64748B;">
                            {t['text']} <span style="font-size: 0.75rem;">({s.get('name')})</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_del:
                        if st.button("🗑️", key=f"del_done_t_{t['id']}", help="Excluir"):
                            dm.delete_task(t["id"])
                            st.rerun()

    # --- ABA 2: POMODORO & FOCO ANTI-DISTRAÇÃO ---
    with tab_pomodoro:
        st.markdown("#### ⏱️ Cronômetro Pomodoro & Modo Anti-Celular")
        st.markdown("Bloqueie distrações e estude em blocos de alta concentração. Deixe o celular em outro cômodo ou no modo 'Não Perturbe' durante o ciclo.")

        cp1, cp2 = st.columns([2, 3])

        with cp1:
            session_type = st.radio("Selecione o Ciclo:", ["Foco Total (25 min)", "Pausa Curta (5 min)", "Pausa Longa (15 min)", "Sessão Rápida (10 min)"])
            
            durations = {
                "Foco Total (25 min)": 25 * 60,
                "Pausa Curta (5 min)": 5 * 60,
                "Pausa Longa (15 min)": 15 * 60,
                "Sessão Rápida (10 min)": 10 * 60
            }
            target_secs = durations[session_type]

            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 12px; margin-top: 10px;">
                📵 <strong>Regra de Ouro do Foco:</strong><br>
                1. Coloque o celular virado para baixo, no silencioso ou em outro cômodo.<br>
                2. Feche redes sociais, notificações e abas que distraem.<br>
                3. Tenha por perto apenas o material de estudo, garrafa de água e caneta.
            </div>
            """, unsafe_allow_html=True)

        with cp2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 2px solid #60A5FA; border-radius: 20px; padding: 30px; text-align: center; box-shadow: 0 0 25px rgba(96, 165, 250, 0.2);">
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8;">Ciclo Atual</div>
                <div style="font-size: 3.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #F8FAFC; margin: 10px 0;">
                    {target_secs // 60:02d}:00
                </div>
                <div style="font-size: 0.95rem; color: #34D399; font-weight: 600;">
                    🎯 Concentração Máxima
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.caption("⚠️ Depois de iniciar, mantenha esta aba aberta até o fim — o cronômetro roda em tempo real.")

            if st.button("▶️ Iniciar Timer", use_container_width=True):
                progress_bar = st.progress(0)
                countdown_placeholder = st.empty()
                status_placeholder = st.empty()

                for remaining in range(target_secs, -1, -1):
                    elapsed_pct = int(((target_secs - remaining) / target_secs) * 100) if target_secs > 0 else 100
                    mins, secs = divmod(remaining, 60)

                    progress_bar.progress(elapsed_pct)
                    countdown_placeholder.markdown(f"""
                    <div style="text-align: center; font-size: 3rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: #F8FAFC;">
                        {mins:02d}:{secs:02d}
                    </div>
                    """, unsafe_allow_html=True)
                    status_placeholder.text("⏳ Estudando focado... mantenha o celular longe!")

                    if remaining > 0:
                        time.sleep(1)

                progress_bar.progress(100)
                status_placeholder.success("🎉 Parabéns! Bloco de estudos concluído com sucesso!")
                st.balloons()

    # --- ABA 3: DIAGNÓSTICO INTELIGENTE ---
    with tab_ai_advisor:
        st.markdown("#### 🤖 Diagnóstico Inteligente da sua Situação Acadêmica")
        st.markdown("O assistente analisa suas provas mais próximas, matérias com menor média e situação de faltas para traçar sua prioridade semanal.")

        exams = dm.get_exams()
        now = datetime.now()

        # Análise de urgência
        urgent_exams = []
        for e in exams:
            try:
                dt = datetime.strptime(e["date"], "%Y-%m-%d")
                days_left = (dt - now).days
                if days_left >= 0 and days_left <= 14:
                    urgent_exams.append((e, days_left))
            except Exception:
                pass

        urgent_exams = sorted(urgent_exams, key=lambda x: x[1])

        # Matérias em risco
        high_risk_subjects = []
        for s in subjects:
            gstats = dm.calculate_grade_stats(s)
            astats = dm.get_attendance_stats(s)
            if astats["status"] in ["danger", "failed"] or gstats["is_impossible"] or (gstats["grade_needed_each"] and gstats["grade_needed_each"] > 7.0):
                high_risk_subjects.append((s, gstats, astats))

        col_diag1, col_diag2 = st.columns(2)

        with col_diag1:
            st.markdown("##### 🚨 Principais Pontos de Atenção")
            if not high_risk_subjects:
                st.success("Nenhuma matéria em risco no momento! Suas faltas estão seguras e suas médias estão em uma faixa tranquila.")

            for s, gs, as_ in high_risk_subjects:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.12); border-left: 4px solid #EF4444; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                    <strong>{s['name']}</strong><br>
                    • Faltas: {as_['absences']}/{as_['max_allowed_absences']} ({as_['status_text']})<br>
                    • Nota necessária nas próximas: <strong>{gs['grade_needed_each'] or 'Sub/Rec'}</strong>
                </div>
                """, unsafe_allow_html=True)

        with col_diag2:
            st.markdown("##### 💡 Plano de Ação Recomendado")
            plan_steps = []
            if urgent_exams:
                first_e, days = urgent_exams[0]
                s_name = subject_map.get(first_e.get("subject_id"), {}).get("name", "Geral")
                plan_steps.append(f"**Prioridade 1:** A prova de **{s_name}** é em **{days} dia(s)**. Resolva exercícios de provas antigas dessa matéria hoje.")

            if high_risk_subjects:
                worst_s = high_risk_subjects[0][0]
                plan_steps.append(f"**Prioridade 2:** Risco em **{worst_s['name']}**. Não falte em mais nenhuma aula desta matéria.")
            
            plan_steps.append("**Prioridade 3:** Complete as listas de exercícios e valide as dúvidas nos plantões com os monitores/professores.")

            for step in plan_steps:
                st.markdown(f"- {step}")

            st.markdown("""
            <div style="background: rgba(59, 130, 246, 0.1); border: 1px dashed #3B82F6; border-radius: 10px; padding: 12px; margin-top: 14px; font-size: 0.85rem; color: #93C5FD;">
                ✨ <strong>Dica de Alta Performance:</strong> O segredo do sucesso nos estudos não é virar noites antes da prova, mas sim manter a consistência de blocos diários de estudo focado e deliberado!
            </div>
            """, unsafe_allow_html=True)
