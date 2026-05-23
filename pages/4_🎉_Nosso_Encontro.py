import streamlit as st
import os
import base64
from pathlib import Path

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
    /* Botão de download estilizado */
    .download-section {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ─────────────────────────────────────────────────
st.markdown('<p class="hero-title">🎉 Nosso Encontro</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Reviva os melhores momentos do nosso ECC</p>', unsafe_allow_html=True)

# ── Abas ──────────────────────────────────────────────────────
aba_livrao, aba_momentos = st.tabs(["📖 Livrão", "📸 Momentos"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 1 – LIVRÃO (Renderização e Download de PDF)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with aba_livrao:
    st.header("📖 Livrão do ECC")
    st.write("Confira o Livrão completo do nosso encontro. Você também pode baixá-lo para guardar de lembrança!")

    # Buscar o primeiro arquivo PDF na pasta livrao
    pdf_files = list(LIVRAO_DIR.glob("*.pdf"))

    if pdf_files:
        pdf_path = pdf_files[0]  # Usa o primeiro PDF encontrado
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
                use_container_width=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Renderizar PDF no navegador via iframe com base64
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
        <div class="pdf-container">
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%"
                height="800px"
                type="application/pdf"
                style="border: none;">
            </iframe>
        </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info(
            "📂 Nenhum arquivo PDF encontrado.\n\n"
            f"Coloque o PDF do Livrão na pasta:\n\n`{LIVRAO_DIR}`"
        )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 2 – MOMENTOS (Galeria de Fotos)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with aba_momentos:
    st.header("📸 Momentos do ECC")
    st.write("Uma galeria com os momentos mais especiais do nosso encontro!")

    # Extensões suportadas
    EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    # Coletar todas as imagens da pasta
    fotos = sorted([
        f for f in MOMENTOS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSOES_IMAGEM
    ]) if MOMENTOS_DIR.exists() else []

    if fotos:
        # Gerar as imagens em base64 e montar o HTML do grid
        cards_html = ""
        for foto in fotos:
            img_bytes = foto.read_bytes()
            ext = foto.suffix.lower().replace(".", "")
            if ext == "jpg":
                ext = "jpeg"
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            cards_html += f"""
            <div class="photo-card">
                <img src="data:image/{ext};base64,{b64}" alt="{foto.stem}" loading="lazy"/>
            </div>
            """

        st.markdown(f'<div class="photo-grid">{cards_html}</div>', unsafe_allow_html=True)

        st.divider()
        st.caption(f"📷 {len(fotos)} foto(s) encontrada(s)")
    else:
        st.info(
            "📂 Nenhuma foto encontrada.\n\n"
            f"Coloque suas fotos (`.jpg`, `.png`, `.webp`, `.gif`) na pasta:\n\n`{MOMENTOS_DIR}`"
        )
