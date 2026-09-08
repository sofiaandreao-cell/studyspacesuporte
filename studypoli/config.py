"""
Configurações gerais e estilos visuais (CSS customizado) do StudySpace.
"""

APP_TITLE = "StudySpace"
APP_SUBTITLE = "Sua plataforma pessoal de estudos: provas, faltas, notas e foco em um só lugar."
APP_ICON = "🎓"

CUSTOM_CSS = """
<style>
    /* Fundo geral */
    .stApp {
        background-color: #F7F4EE;
    }

    /* Cabeçalho principal (hero banner) */
    .header-container {
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(27,42,74,0.05));
        border: 1px solid rgba(27,42,74,0.12);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B2A4A;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #4B5A78;
        margin-top: 2px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-left: 6px;
    }
    .badge-info { background: rgba(96,165,250,0.15); color: #2563EB; border: 1px solid rgba(96,165,250,0.4); }
    .badge-safe { background: rgba(52,211,153,0.15); color: #059669; border: 1px solid rgba(52,211,153,0.4); }
    .badge-warning { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.4); }

    /* Cartões de KPI */
    .kpi-card {
        background: rgba(27,42,74,0.06);
        border: 1px solid rgba(27,42,74,0.12);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #4B5A78;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1B2A4A;
        margin: 4px 0;
    }
    .kpi-subtext {
        font-size: 0.75rem;
        color: #5B6B8C;
    }

    /* Divisor com gradiente */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(96,165,250,0.5), transparent);
        margin: 20px 0;
        border: none;
    }

    /* Barra de progresso de faltas */
    .progress-bar-bg {
        width: 100%;
        height: 8px;
        background: rgba(27,42,74,0.12);
        border-radius: 999px;
        margin-top: 8px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.3s ease;
    }
</style>
"""
