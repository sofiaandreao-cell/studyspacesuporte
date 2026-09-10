"""
Configurações gerais e estilos visuais (CSS customizado) do StudySpace.
"""

APP_TITLE = "StudySpace"
APP_SUBTITLE = "Sua plataforma pessoal de estudos: provas, faltas, notas e foco em um só lugar."
APP_ICON = "🎓"

CUSTOM_CSS = """
<style>
    /* Fundo geral (Pantone 12-5409 TCX Fair Aqua) */
    .stApp {
        background-color: #B8E2DC;
    }

    /* Barra lateral em um tom levemente mais escuro da mesma cor */
    [data-testid="stSidebar"] {
        background-color: #A5D6CD;
    }

    /* Garante que todo texto padrão do Streamlit (títulos, labels, textos)
       fique em azul marinho, mesmo fora dos cartões customizados */
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
    .stApp .stMarkdown, .stApp .stRadio label, .stApp .stCaption {
        color: #1B2A4A;
    }

    /* Botões nativos do Streamlit (ex: +1 Falta, Salvar, Personalizar) 
       em um tom mais escuro de verde-água, ao invés da cor padrão do Streamlit */
    .stApp button {
        background-color: #3A7D6E !important;
        color: #FFFFFF !important;
        border: 1px solid #2F6459 !important;
    }
    .stApp button:hover {
        background-color: #2F6459 !important;
        border: 1px solid #244F42 !important;
        color: #FFFFFF !important;
    }
    .stApp button p {
        color: #FFFFFF !important;
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
        color: #33456B;
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
    .badge-info { background: rgba(255,255,255,0.5); color: #1D4ED8; border: 1px solid rgba(29,78,216,0.4); }
    .badge-safe { background: rgba(255,255,255,0.5); color: #047857; border: 1px solid rgba(4,120,87,0.4); }
    .badge-warning { background: rgba(255,255,255,0.5); color: #B45309; border: 1px solid rgba(180,83,9,0.4); }

    /* Cartões de KPI */
    .kpi-card {
        background: rgba(255,255,255,0.45);
        border: 1px solid rgba(27,42,74,0.15);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #33456B;
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
        color: #33456B;
    }

    /* Divisor com gradiente */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(27,42,74,0.35), transparent);
        margin: 20px 0;
        border: none;
    }

    /* Barra de progresso de faltas */
    .progress-bar-bg {
        width: 100%;
        height: 8px;
        background: rgba(27,42,74,0.15);
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
