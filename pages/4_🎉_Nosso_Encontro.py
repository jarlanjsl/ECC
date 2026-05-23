import streamlit as st
import os
import base64
from pathlib import Path
from PIL import Image, ImageOps
from streamlit_pdf_viewer import pdf_viewer 

# ============================================================
# 🎉 Nosso Encontro - Página pública (sem autenticação)
# ============================================================

st.set_page_config(page_title="Nosso Encontro - ECC", page_icon="🎉", layout="wide")

# ── Caminhos dos assets ──────────────────────────────────────
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LIVRAO_DIR = ASSETS_DIR / "livrao"
MOMENTOS_DIR = ASSETS_DIR / "momentos"

# ── CSS personalizado ────────────────────────────────────────
st.markdown("""
<style>
    /* ===== ESCONDER MENU / SIDEBAR ===== */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    #MainMenu,
    header[data-testid="stHeader"] button[kind="header"] {
        display: none !important;
    }

    /* Header bonito */
    .hero-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }

    /* ===== ABAS MAIORES ===== */
    [data-baseweb="tab-list"] button[data-baseweb="tab"] {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
    }

    /* Grid de fotos */
    .photo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 16px;
        padding: 8px 0;
    }
    .photo-card {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: var(--background-color, #fff);
    }
    .photo-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
    }
    .photo-card img {
        width: 100%;
        height: 260px;
        object-fit: cover;
        display: block;
    }
    /* PDF container */
    .pdf-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* ===== BOTÃO DE DOWNLOAD DESTACADO ===== */
    .download-section {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
    /* Estiliza o botão de download do Streamlit */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #fff !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        padding: 0.85rem 2.5rem !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 18px rgba(102, 126, 234, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.55) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ─────────────────────────────────────────────────
st.markdown('<p class="hero-title">🎉 Nosso Encontro</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Reviva os melhores momentos do nosso ECC</p>', unsafe_allow_html=True)

# ── Abas ──────────────────────────────────────────────────────
aba_livrao, aba_momentos = st.tabs(["📖 Livrão", "📸 Momentos"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 1 – LIVRÃO (Renderização Responsiva para Celular)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with aba_livrao:
    st.header("📖 Livrão do ECC")
    st.write("Confira o Livrão completo do nosso encontro. Você também pode baixá-lo para guardar de lembrança!")

    # Buscar o primeiro arquivo PDF na pasta livrao
    pdf_files = list(LIVRAO_DIR.glob("*.pdf"))

    if pdf_files:
        pdf_path = pdf_files[0]  
        pdf_bytes = pdf_path.read_bytes()

        # Botão de download
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        col_spacer1, col_btn, col_spacer2 = st.columns([1, 2, 1])
        with col_btn:
            st.download_button(
                label="⬇️  Baixar o Livrão (PDF)",
                data=pdf_bytes,
                file_name=pdf_path.name,
                mime="application/pdf",
                width="stretch",
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()  

        # 🚀 AJUSTADO: Renderização Fluida/Responsiva
        try:
            # Ao NÃO passar o parâmetro 'width', ou deixando-o nulo, 
            # o componente força o PDF a encolher e caber na largura da tela do celular.
            pdf_viewer(
                input=str(pdf_path)
            )
        except Exception as e:
            st.error(f"Erro ao renderizar o leitor de PDF: {e}")
            
    else:
        st.info(
            "📂 Nenhum arquivo PDF encontrado.\n\n"
            f"Coloque o PDF do Livrão na pasta:\n\n`{LIVRAO_DIR}`"
        )
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 2 – MOMENTOS (Galeria Nativa com Correção de Orientação)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with aba_momentos:
    st.header("📸 Momentos do ECC")
    st.write("Uma galeria com os momentos mais especiais do nosso encontro!")

    EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    fotos = sorted([
        f for f in MOMENTOS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSOES_IMAGEM
    ]) if MOMENTOS_DIR.exists() else []

    if fotos:
        # Cria a grade de 3 colunas
        colunas = st.columns(3, gap="medium")
        
        for i, foto in enumerate(fotos):
            with colunas[i % 3]:
                try:
                    # 1. Abre a imagem usando o Pillow
                    img = Image.open(foto)
                    
                    # 2. Corrige automaticamente a rotação com base nos metadados Exif do celular
                    img_corrigida = ImageOps.exif_transpose(img)
                    
                    # 3. Exibe a imagem já na orientação correta (vertical)
                    st.image(
                        img_corrigida, 
                        width="stretch"
                    )
                except Exception as e:
                    # Se alguma imagem falhar ou estiver corrompida, exibe o erro discretamente
                    st.error(f"Erro ao processar {foto.name}: {e}")
                
        st.divider()
        st.caption(f"📷 {len(fotos)} foto(s) encontrada(s)")
    else:
        st.info(
            "📂 Nenhuma foto encontrada.\n\n"
            f"Coloque suas fotos na pasta correspondente:\n\n`{MOMENTOS_DIR}`"
        )
