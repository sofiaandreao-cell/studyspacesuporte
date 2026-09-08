"""
Módulo de Controle e Gestão de Faltas por Matéria do StudySpace.
Calcula taxas de presença, limites de reprovação (regra USP 70%), alertas e botões rápidos.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
import uuid


def render_attendance_view(dm):
    st.markdown("## ⚠️ Controle de Faltas por Matéria")
    st.markdown("Monitore a frequência de cada disciplina para nunca correr risco de reprovação por faltas (RF).")

    subjects = dm.get_subjects()

    if not subjects:
        st.info("Nenhuma disciplina cadastrada. Cadastre uma disciplina abaixo para começar.")

    # Estatísticas Globais
    total_absences = sum(s.get("absences", 0) for s in subjects)
    critical_count = 0
    warning_count = 0
    safe_count = 0

    for s in subjects:
        stats = dm.get_attendance_stats(s)
        if stats["status"] in ["danger", "failed"]:
            critical_count += 1
        elif stats["status"] == "warning":
            warning_count += 1
        else:
            safe_count += 1

    # KPIs no Topo
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total de Faltas</div>
            <div class="kpi-value">{total_absences}</div>
            <div class="kpi-subtext">em todas as matérias</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Frequência Segura</div>
            <div class="kpi-value" style="color: #34D399;">{safe_count}</div>
            <div class="kpi-subtext">disciplinas com folga</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Em Atenção</div>
            <div class="kpi-value" style="color: #FBBF24;">{warning_count}</div>
            <div class="kpi-subtext">acima de 50% do limite</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Risco Crítico</div>
            <div class="kpi-value" style="color: #F87171;">{critical_count}</div>
            <div class="kpi-subtext">próximo de reprovar</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Botão de Adicionar Disciplina
    # Controles Superiores: Adicionar Matéria e Modelos
    col_add, col_presets = st.columns([1, 1])

    with col_add:
        with st.expander("➕ Cadastrar Nova Matéria Personalizada", expanded=(len(subjects) == 0)):
            with st.form("form_add_subject", clear_on_submit=True):
                st.markdown("##### 📝 Escolha o Nome e Detalhes da Matéria")
                col1, col2 = st.columns(2)
                with col1:
                    sub_name = st.text_input("Nome da Matéria *", placeholder="Ex: Anatomia Humana, Direito Penal, Biologia, Cálculo...")
                    sub_code = st.text_input("Código ou Sigla da Disciplina", placeholder="Ex: BIO101, DP201, MAT01...")
                    sub_prof = st.text_input("Nome do(a) Professor(a)", placeholder="Ex: Profa. Maria")
                with col2:
                    total_cls = st.number_input("Total de Aulas Previstas *", min_value=10, max_value=200, value=60, step=2)
                    max_abs_pct = st.number_input("Limite Máximo de Faltas (%)", min_value=5.0, max_value=50.0, value=25.0, step=5.0,
                                                  help="Padrão mais comum no Brasil (MEC): 25% de faltas (75% presença). USP: 30%.")
                    pass_grd = st.number_input("Média Mínima para Aprovação", min_value=4.0, max_value=10.0, value=6.0, step=0.5,
                                               help="Ex: 5.0 (USP/Federais), 6.0 ou 7.0 (outras faculdades/escolas).")
                    color_pick = st.color_picker("Cor de Identificação", value="#3B82F6")

                submitted_sub = st.form_submit_button("💾 Salvar Matéria Personalizada", use_container_width=True)
                if submitted_sub:
                    if not sub_name.strip():
                        st.error("Por favor, digite o nome da matéria.")
                    else:
                        new_sub = {
                            "id": f"sub_{uuid.uuid4().hex[:8]}",
                            "name": sub_name.strip(),
                            "code": sub_code.strip() or "GERAL",
                            "professor": sub_prof.strip() or "Não informado",
                            "total_classes": int(total_cls),
                            "absences": 0,
                            "max_absence_pct": float(max_abs_pct),
                            "passing_grade": float(pass_grd),
                            "color": color_pick,
                            "evaluations": [
                                {"name": "Avaliação 1", "grade": None, "weight": 1.0, "done": False},
                                {"name": "Avaliação 2", "grade": None, "weight": 1.0, "done": False}
                            ]
                        }
                        dm.add_subject(new_sub)
                        st.success(f"Matéria '{sub_name}' cadastrada com sucesso!")
                        st.rerun()

    with col_presets:
        with st.expander("🗂️ Modelos Prontos ou Começar do Zero", expanded=False):
            st.caption("Você pode carregar modelos de matérias ou limpar todas para cadastrar apenas as suas:")
            cp_col1, cp_col2, cp_col3 = st.columns(3)
            with cp_col1:
                if st.button("🗑️ Limpar Tudo (Zero)", use_container_width=True, help="Remove todas as matérias para você cadastrar as suas"):
                    dm.clear_all_subjects()
                    st.toast("Matérias limpas! Agora você pode cadastrar as suas.")
                    st.rerun()
            with cp_col2:
                if st.button("📚 Modelo Geral", use_container_width=True, help="Matemática, Comunicação e Pesquisa"):
                    dm.load_preset("geral")
                    st.toast("Modelo geral carregado!")
                    st.rerun()
            with cp_col3:
                if st.button("⚙️ Modelo Engenharia", use_container_width=True, help="Cálculo, Física, Álgebra e Computação"):
                    dm.load_preset("engenharia")
                    st.toast("Modelo de engenharia carregado!")
                    st.rerun()

    if not subjects:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); border: 2px dashed rgba(96, 165, 250, 0.4); border-radius: 14px; padding: 30px; text-align: center; margin: 20px 0;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">📚</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #F8FAFC;">Nenhuma matéria cadastrada ainda!</div>
            <div style="color: #94A3B8; font-size: 0.9rem; margin-top: 6px;">
                Clique no botão <strong>➕ Cadastrar Nova Matéria Personalizada</strong> acima para adicionar suas próprias disciplinas (seja de Medicina, Direito, Engenharia, Ensino Médio ou qualquer curso).
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Cards de Cada Matéria com Controle Rápido
    st.markdown("#### 📚 Suas Disciplinas e Situação de Presença")

    for subj in subjects:
        stats = dm.get_attendance_stats(subj)
        subj_id = subj["id"]

        with st.container():
            col_info, col_controls = st.columns([4, 2])

            with col_info:
                # Barra de progresso customizada
                bar_pct = min(100.0, stats["usage_pct"])
                fill_color = stats["status_color"]

                alert_box = ""
                if stats["status"] == "failed":
                    alert_box = f"""
                    <div style="background: rgba(220, 38, 38, 0.2); border: 1px solid #DC2626; color: #FCA5A5; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; margin-top: 8px;">
                        🚨 <strong>Atenção Máxima:</strong> Limite de faltas ultrapassado em {stats['excess_absences']} aula(s)! Risco iminente de reprovação por frequência.
                    </div>
                    """
                elif stats["status"] == "danger":
                    alert_box = f"""
                    <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; color: #FCA5A5; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; margin-top: 8px;">
                        ⚠️ <strong>Perigo de Reprovação:</strong> Você só pode faltar mais <strong>{stats['remaining_allowed']} aula(s)</strong> no semestre!
                    </div>
                    """
                elif stats["status"] == "warning":
                    alert_box = f"""
                    <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; color: #FCD34D; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; margin-top: 8px;">
                        ⚠️ <strong>Fique Alerta:</strong> Mais da metade das faltas permitidas já foram utilizadas. Restam <strong>{stats['remaining_allowed']} faltas</strong>.
                    </div>
                    """
                else:
                    alert_box = f"""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 6px 12px; border-radius: 8px; font-size: 0.8rem; margin-top: 8px;">
                        ✅ <strong>Frequência Confortável:</strong> Você ainda tem direito a <strong>{stats['remaining_allowed']} falta(s)</strong> restantes.
                    </div>
                    """

                card_html = f"""
                <div style="background: rgba(30, 41, 59, 0.6); border-left: 5px solid {subj.get('color', '#3B82F6')}; 
                            border-radius: 12px; padding: 16px; margin-bottom: 12px; border-top: 1px solid rgba(255,255,255,0.06);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; font-size: 1.15rem; color: #F8FAFC;">
                            {subj['name']} <span style="font-size: 0.8rem; color: #94A3B8; font-weight: normal;">({subj.get('code', '---')})</span>
                        </span>
                        <span style="background: {stats['status_color']}22; color: {stats['status_color']}; border: 1px solid {stats['status_color']}55; 
                                     padding: 3px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">
                            {stats['status_text']}
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin: 4px 0 10px 0;">
                        Docente: {subj.get('professor', 'Não informado')} · Total de Aulas: {stats['total_classes']} · Média Mínima: {subj.get('passing_grade', 6.0)}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #CBD5E1; font-weight: 600;">
                        <span>Faltas: <strong>{stats['absences']}</strong> de {stats['max_allowed_absences']} permitidas ({stats['usage_pct']}% do limite)</span>
                        <span>Presença Atual: <strong>{stats['attendance_rate']}%</strong> (Exigência: {100 - subj.get('max_absence_pct', 25)}%)</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {bar_pct}%; background: {fill_color};"></div>
                    </div>
                    {alert_box}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

            with col_controls:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.write("**Ações Rápidas:**")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("➕ 1 Falta", key=f"add_abs_{subj_id}", use_container_width=True):
                        dm.modify_absences(subj_id, +1)
                        st.rerun()
                with btn_col2:
                    if st.button("➖ 1 Falta", key=f"sub_abs_{subj_id}", use_container_width=True):
                        dm.modify_absences(subj_id, -1)
                        st.rerun()

                with st.popover("⚙️ Personalizar / Editar Matéria"):
                    st.markdown(f"##### ✏️ Editar Detalhes de: **{subj['name']}**")
                    
                    edit_name = st.text_input("Nome da Matéria:", value=subj["name"], key=f"ed_name_{subj_id}")
                    edit_code = st.text_input("Código / Sigla:", value=subj.get("code", ""), key=f"ed_code_{subj_id}")
                    edit_prof = st.text_input("Professor(a):", value=subj.get("professor", ""), key=f"ed_prof_{subj_id}")
                    
                    col_ep1, col_ep2 = st.columns(2)
                    with col_ep1:
                        edit_total_cls = st.number_input("Total de Aulas:", min_value=10, max_value=250, value=subj.get("total_classes", 60), key=f"ed_cls_{subj_id}")
                        edit_pass = st.number_input("Média para Passar:", min_value=1.0, max_value=10.0, value=float(subj.get("passing_grade", 6.0)), step=0.5, key=f"ed_pass_{subj_id}")
                    with col_ep2:
                        edit_max_abs = st.number_input("Limite de Faltas (%):", min_value=5.0, max_value=50.0, value=float(subj.get("max_absence_pct", 25.0)), step=5.0, key=f"ed_maxabs_{subj_id}")
                        edit_color = st.color_picker("Cor da Matéria:", value=subj.get("color", "#3B82F6"), key=f"ed_col_{subj_id}")

                    edit_abs_val = st.number_input(
                        "Alterar contador exato de faltas:",
                        min_value=0,
                        max_value=int(edit_total_cls),
                        value=subj["absences"],
                        key=f"inp_abs_{subj_id}"
                    )
                    
                    if st.button("💾 Salvar Alterações", key=f"save_ed_{subj_id}", use_container_width=True):
                        dm.update_subject(subj_id, {
                            "name": edit_name.strip() or subj["name"],
                            "code": edit_code.strip() or "---",
                            "professor": edit_prof.strip() or "Não informado",
                            "total_classes": int(edit_total_cls),
                            "absences": int(edit_abs_val),
                            "passing_grade": float(edit_pass),
                            "max_absence_pct": float(edit_max_abs),
                            "color": edit_color
                        })
                        st.success("Matéria personalizada com sucesso!")
                        st.rerun()

                    st.markdown("---")
                    if st.button("🗑️ Excluir esta Matéria", key=f"del_subj_{subj_id}", type="secondary", use_container_width=True):
                        dm.delete_subject(subj_id)
                        st.warning("Matéria removida.")
                        st.rerun()

    # Gráfico Visual Comparativo de Presença com Plotly
    if subjects:
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 📊 Gráfico de Frequência vs Limite de Aprovação (70%)")

        names = [s["name"] for s in subjects]
        presences = [dm.get_attendance_stats(s)["attendance_rate"] for s in subjects]
        colors = [dm.get_attendance_stats(s)["status_color"] for s in subjects]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=names,
            y=presences,
            marker_color=colors,
            text=[f"{p:.1f}%" for p in presences],
            textposition="auto",
            name="Presença Real"
        ))

        # Linha de corte de 70% (Mínimo para aprovação na USP)
        fig.add_hline(
            y=70.0,
            line_dash="dash",
            line_color="#EF4444",
            annotation_text="Mínimo USP: 70%",
            annotation_position="top right"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(30, 41, 59, 0.4)",
            margin=dict(l=20, r=20, t=30, b=40),
            yaxis=dict(range=[0, 105], title="Presença (%)"),
            xaxis=dict(tickangle=-15),
            height=320
        )
        st.plotly_chart(fig, use_container_width=True)
