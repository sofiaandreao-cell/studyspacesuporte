"""
Módulo de Calculadora e Simulador de Notas do StudySpace.
Calcula médias ponderadas/aritméticas e simula a nota necessária nas próximas provas para aprovação.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go


def render_grades_view(dm):
    st.markdown("## 🧮 Calculadora & Simulador de Média de Notas")
    st.markdown("Gerencie as notas de cada avaliação, calcule sua média ponderada e simule exatamente quanto precisa tirar nas próximas provas para passar.")

    subjects = dm.get_subjects()
    if not subjects:
        st.warning("⚠️ Nenhuma matéria cadastrada. Adicione disciplinas na aba 'Faltas e Disciplinas'.")
        return

    # Cálculos Globais
    total_subjects = len(subjects)
    approved_count = 0
    pending_count = 0
    risk_count = 0

    subject_stats_list = []
    for s in subjects:
        gstats = dm.calculate_grade_stats(s)
        subject_stats_list.append((s, gstats))
        if gstats["is_already_passed"]:
            approved_count += 1
        elif gstats["is_impossible"]:
            risk_count += 1
        else:
            pending_count += 1

    # KPIs no Topo
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Matérias Cursando</div>
            <div class="kpi-value">{total_subjects}</div>
            <div class="kpi-subtext">no semestre atual</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Já Aprovado(a)</div>
            <div class="kpi-value" style="color: #059669;">{approved_count}</div>
            <div class="kpi-subtext">média >= corte atingida</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Em Andamento</div>
            <div class="kpi-value" style="color: #2563EB;">{pending_count}</div>
            <div class="kpi-subtext">aguardando próximas provas</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Risco de Rec/Sub</div>
            <div class="kpi-value" style="color: #DC2626;">{risk_count}</div>
            <div class="kpi-subtext">precisa de nota alta/rec</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Detalhamento por Disciplina
    st.markdown("#### 🎯 Painel de Notas & Simulador por Disciplina")

    for s, gstats in subject_stats_list:
        subj_id = s["id"]
        evals = s.get("evaluations", [])

        with st.container():
            st.markdown(f"""
            <div style="background: rgba(27,42,74,0.06); border-radius: 14px; padding: 20px; 
                        margin-bottom: 20px; border: 1px solid rgba(27,42,74,0.12); border-left: 6px solid {s.get('color', '#3B82F6')};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 800; color: #1B2A4A;">{s['name']}</span>
                        <span style="color: #4B5A78; font-size: 0.85rem; margin-left: 8px;">({s.get('code', '---')})</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #33456B;">
                        Nota de Corte: <strong>{s.get('passing_grade', 5.0)}</strong> · Média Atual (Feitas): <strong style="color: #2563EB;">{gstats['current_avg']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_evals, col_sim = st.columns([3, 2])

            with col_evals:
                st.markdown("##### 📝 Avaliações Cadastradas")
                
                has_changed = False
                updated_evals = []

                for idx, ev in enumerate(evals):
                    ce1, ce2, ce3, ce4 = st.columns([3, 2, 2, 1])
                    with ce1:
                        st.markdown(f"**{ev['name']}**")
                    with ce2:
                        w_val = st.number_input(f"Peso", min_value=0.5, max_value=10.0, value=float(ev.get("weight", 1.0)), 
                                                step=0.5, key=f"w_{subj_id}_{idx}")
                    with ce3:
                        is_done = ev.get("done", False)
                        curr_g = float(ev.get("grade", 0.0)) if (ev.get("grade") is not None) else 0.0
                        g_input = st.number_input(f"Nota (0-10)", min_value=0.0, max_value=10.0, 
                                                  value=curr_g if is_done else 0.0, step=0.1, key=f"g_{subj_id}_{idx}")
                    with ce4:
                        done_check = st.checkbox("Feita", value=is_done, key=f"done_{subj_id}_{idx}")

                    updated_eval = {
                        "name": ev["name"],
                        "weight": float(w_val),
                        "grade": float(g_input) if done_check else None,
                        "done": done_check
                    }
                    if (updated_eval["grade"] != ev.get("grade") or 
                        updated_eval["weight"] != ev.get("weight") or 
                        updated_eval["done"] != ev.get("done")):
                        has_changed = True

                    updated_evals.append(updated_eval)

                if has_changed:
                    if st.button("💾 Atualizar Notas desta Matéria", key=f"btn_save_evals_{subj_id}", use_container_width=True):
                        dm.update_subject(subj_id, {"evaluations": updated_evals})
                        st.toast("Notas salvas com sucesso!")
                        st.rerun()

                # Adicionar mais uma avaliação (P3, Trabalho, etc)
                with st.popover(f"➕ Adicionar Avaliação em {s['name']}"):
                    new_ev_name = st.text_input("Nome (Ex: P3, Sub, Projeto Final)", key=f"new_ev_name_{subj_id}")
                    new_ev_weight = st.number_input("Peso", min_value=0.5, max_value=10.0, value=2.0, step=0.5, key=f"new_ev_w_{subj_id}")
                    if st.button("Salvar Nova Avaliação", key=f"btn_add_ev_{subj_id}"):
                        if new_ev_name.strip():
                            evals.append({"name": new_ev_name.strip(), "weight": float(new_ev_weight), "grade": None, "done": False})
                            dm.update_subject(subj_id, {"evaluations": evals})
                            st.success("Avaliação adicionada!")
                            st.rerun()

            with col_sim:
                st.markdown("##### 🔮 Simulador de Nota Necessária")

                if gstats["is_already_passed"]:
                    st.success(f"""
                    🎉 **Parabéns! Aprovado(a) por Nota!**  
                    Sua média ponderada já atingiu **{gstats['projected_current']}**, superando a nota de corte ({gstats['passing_grade']}).
                    """)
                elif gstats["pending_count"] == 0:
                    if gstats["projected_current"] >= gstats["passing_grade"]:
                        st.success(f"✅ Semestre concluído! Média Final: **{gstats['projected_current']}** (Aprovado)")
                    else:
                        st.error(f"❌ Média Final: **{gstats['projected_current']}** (Abaixo de {gstats['passing_grade']}). Necessário exame de Recuperação (REC).")
                else:
                    needed = gstats["grade_needed_each"]
                    if gstats["is_impossible"]:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 10px; padding: 14px; color: #B91C1C;">
                            ⚠️ <strong>Atenção Crítica:</strong> Para passar direto com média {gstats['passing_grade']}, seria necessário tirar <strong>{needed}</strong> nas provas restantes (acima de 10).
                            <br><br>
                            💡 <em>Estratégia:</em> Busque a nota máxima para atingir média mínima para direito à Prova Substitutiva (SUB) ou Recuperação (REC)!
                        </div>
                        """, unsafe_allow_html=True)
                    elif needed is not None and needed > 7.0:
                        st.markdown(f"""
                        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; border-radius: 10px; padding: 14px; color: #B45309;">
                            ⚡ <strong>Desafio Alto:</strong> Você precisa tirar em média <strong>{needed}</strong> em cada uma das {gstats['pending_count']} avaliações restantes para passar sem REC.
                            <br><br>
                            Recomendação: Dedicar blocos de estudo reforçados para esta matéria no cronograma!
                        </div>
                        """, unsafe_allow_html=True)
                    elif needed is not None and needed <= 5.0:
                        st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 10px; padding: 14px; color: #047857;">
                            ✨ <strong>Cenário Confortável:</strong> Você precisa tirar em média apenas <strong>{needed}</strong> nas {gstats['pending_count']} avaliações restantes para aprovação direta.
                            <br><br>
                            Mantenha o ritmo para garantir a nota com tranquilidade.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(59, 130, 246, 0.15); border: 1px solid #3B82F6; border-radius: 10px; padding: 14px; color: #1D4ED8;">
                            🎯 <strong>Meta de Desempenho:</strong> Tire pelo menos <strong>{needed}</strong> nas avaliações restantes para garantir aprovação direta.
                        </div>
                        """, unsafe_allow_html=True)

                # Mini Simulador Interativo "E se eu tirar X?"
                if gstats["pending_count"] > 0:
                    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                    hypothetical_grade = st.slider(
                        "Simular: 'E se eu tirar nas próximas:'",
                        min_value=0.0, max_value=10.0, value=max(0.0, min(10.0, float(gstats["grade_needed_each"] or 6.0))),
                        step=0.5, key=f"sim_slider_{subj_id}"
                    )
                    
                    # Calcular nota simulada
                    d_sum = sum((ev.get("grade", 0.0) * ev.get("weight", 1.0)) for ev in evals if ev.get("done"))
                    hypo_sum = d_sum + (hypothetical_grade * gstats["pending_weight"])
                    simulated_final = round(hypo_sum / gstats["total_weight"], 2)

                    if simulated_final >= s.get("passing_grade", 5.0):
                        st.caption(f"📈 Com nota {hypothetical_grade}, sua média final ficaria em **{simulated_final}** 🟢 **(Aprovado)**")
                    else:
                        st.caption(f"📉 Com nota {hypothetical_grade}, sua média final ficaria em **{simulated_final}** 🔴 **(Abaixo de {s.get('passing_grade', 5.0)})**")

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Gráfico Comparativo de Desempenho
    st.markdown("#### 📊 Comparativo das Médias Atuais por Disciplina")
    names = [s["name"] for s in subjects]
    averages = [dm.calculate_grade_stats(s)["current_avg"] for s in subjects]
    passing_thresholds = [s.get("passing_grade", 6.0) for s in subjects]
    avg_passing = (sum(passing_thresholds) / len(passing_thresholds)) if passing_thresholds else 6.0

    colors = [
        "#10B981" if averages[i] >= passing_thresholds[i] else "#EF4444"
        for i in range(len(subjects))
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=averages,
        marker_color=colors,
        text=[f"{a:.1f}" for a in averages],
        textposition="auto"
    ))
    fig.add_hline(
        y=avg_passing,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Média de Aprovação ({avg_passing:.1f})",
        annotation_position="top left"
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(27,42,74,0.03)",
        font=dict(color="#1B2A4A"),
        margin=dict(l=20, r=20, t=30, b=40),
        yaxis=dict(range=[0, 10.5], title="Média Atual"),
        xaxis=dict(tickangle=-15),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)