import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ============================================================
# 🎉 Nosso Encontro - Página pública (sem autenticação)
# ============================================================

st.set_page_config(page_title="Nosso Encontro - ECC", page_icon="🎉", layout="wide")

# ── CSS personalizado (Mantido idêntico ao seu original) ─────
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

    /* ===== BOTÃO DE DOWNLOAD DESTACADO (HTML PERSONALIZADO) ===== */
    .download-section {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
    .btn-download-custom {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff !important;
        font-size: 1.25rem;
        font-weight: 700;
        padding: 0.85rem 2.5rem;
        border: none;
        border-radius: 12px;
        box-shadow: 0 4px 18px rgba(102, 126, 234, 0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-decoration: none;
        text-align: center;
        cursor: pointer;
    }
    .btn-download-custom:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.55);
    }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ─────────────────────────────────────────────────
st.markdown('<p class="hero-title">🎉 Nosso Encontro</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Reviva os melhores momentos do nosso ECC</p>', unsafe_allow_html=True)

# ── Abas ──────────────────────────────────────────────────────
aba_livrao, aba_momentos = st.tabs(["📖 Livrão", "📸 Momentos"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNÇÃO AUXILIAR - LINKS DIRETOS DO GOOGLE DRIVE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def obter_link_direto_drive(url_compartilhada):
    """Transforma o link de visualização do Drive em link direto de renderização"""
    if "drive.google.com" in url_compartilhada:
        try:
            id_arquivo = url_compartilhada.split("/d/")[1].split("/")[0]
            # Formato de alta performance para renderizar imagens direto no navegador do cliente
            return f"https://lh3.googleusercontent.com/d/{id_arquivo}"
        except IndexError:
            pass
    return url_compartilhada

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 1 – LIVRÃO (Hospedado no Google Drive)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with aba_livrao:
    st.header("📖 Livrão do ECC")
    st.write("Confira o Livrão completo do nosso encontro. Você também pode baixá-lo para guardar de lembrança!")

    # 🚨 PASSO 1: Cole aqui o link de compartilhamento do seu PDF no Google Drive
    # IMPORTANTE: No Google Drive, mude o acesso do arquivo para "Qualquer pessoa com o link pode ler"
    LINK_COMPARTILHADO_PDF_DRIVE = "https://drive.google.com/file/d/1IH4ulCRxrb6w39TRUqVeAzGd8HqOeNyP/view?usp=sharing"
    
    if "SEU_ID_DO_PDF_AQUI" not in LINK_COMPARTILHADO_PDF_DRIVE:
        try:
            id_pdf = LINK_COMPARTILHADO_PDF_DRIVE.split("/d/")[1].split("/")[0]
            
            # Link direto para download do PDF
            url_download_pdf = f"https://drive.google.com/uc?export=download&id={id_pdf}"
            
            # Link para visualização interna em iframe (usa o leitor do próprio Drive, super leve)
            url_preview_pdf = f"https://drive.google.com/file/d/{id_pdf}/preview"

            # Botão de download estilizado com seu CSS, apontando para fora do Streamlit
            st.markdown(f"""
            <div class="download-section">
                <a class="btn-download-custom" href="{url_download_pdf}" target="_blank">
                    ⬇️   Baixar o Livrão (PDF)
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()  

            # Renderização síncrona delegada ao navegador do cliente (Substitui o pdf_viewer local)
            componente_pdf = f'<iframe src="{url_preview_pdf}" width="100%" height="800px" allow="autoplay"></iframe>'
            components.html(componente_pdf, height=815)
            
        except Exception as e:
            st.error(f"Erro ao processar o link do PDF do Google Drive: {e}")
    else:
        st.warning("⚠️ Por favor, configure o link do seu PDF do Google Drive na variável 'LINK_COMPARTILHADO_PDF_DRIVE'")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABA 2 – MOMENTOS (Galeria Estável e Ultraleve)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with aba_momentos:
    st.header("📸 Momentos do ECC")
    st.write("Uma galeria com os momentos mais especiais do nosso encontro!")

    LINKS_GOOGLE_DRIVE = [
        "https://drive.google.com/file/d/1LGoDxEIrOV2lNE0dUKhfhFMfWmhmh5cX/view?usp=sharing",
        "https://drive.google.com/file/d/1FqmVMTXB7y_cLkLJuALLLElNNRJnZQ8d/view?usp=sharing",
        "https://drive.google.com/file/d/1PXjiscfHBUpAr-2sZl1ORlIn41KLpYif/view?usp=sharing",
        "https://drive.google.com/file/d/1tGlKv5CQ6BZXYYKPbSKC9nCeJC-PXycr/view?usp=sharing",
        "https://drive.google.com/file/d/1OavfEp-UMGHKlVE_YOfuoxanyEiTrnPl/view?usp=sharing",
        "https://drive.google.com/file/d/189hBtIkutHLFzt2myDfiI8Y4Akrvv0cQ/view?usp=sharing",
        "https://drive.google.com/file/d/1STO0aUJ8efyeYv-ms_jHqiy2Mpkq9q6X/view?usp=sharing",
        "https://drive.google.com/file/d/1risdStpJFMZsl7yHRDbG43HeZyCKfLa2/view?usp=sharing",
        "https://drive.google.com/file/d/1jVRCEcyQFLDH5cBKRzhIdQeIN04QZM63/view?usp=sharing",
        "https://drive.google.com/file/d/1r-eodDNQ1h8AoQLKuat9U-ekNFSIrM3d/view?usp=sharing",
        "https://drive.google.com/file/d/1Vzkowj4wPEXSFWSDpm1emHxv_fR--z3Y/view?usp=sharing",
        "https://drive.google.com/file/d/1x3MThDz-BzrbguCHJ9LblDoo5i6nnkpg/view?usp=sharing",
        "https://drive.google.com/file/d/1K8krDHoC7B_yWkJV2Sisq2l5HeNLKNl7/view?usp=sharing",
        "https://drive.google.com/file/d/1r53xmSRrPitBMoXYgz5Ijm4hOt7E5cf5/view?usp=sharing",
        "https://drive.google.com/file/d/15AiwjPfOcbVjbRuKLkRWOKjNyXkYbOuh/view?usp=sharing",
        "https://drive.google.com/file/d/1rSP_VCeEnjnxuYM7xrxRJjk5DaJMjQMn/view?usp=sharing",
        "https://drive.google.com/file/d/1BTiOhebhCCK-UZe1tEEba1d33oRhue6q/view?usp=sharing",
        "https://drive.google.com/file/d/10RS1ctP-RmKzZqj8zIZF_fH2RTXtm-GN/view?usp=sharing",
        "https://drive.google.com/file/d/1ouy_vl2DuA27sr9pAiFjq2Sbgl-FYFDU/view?usp=sharing",
        "https://drive.google.com/file/d/1mtNM6iKi5nw-vIoorE8GsLoDdwFCf5dN/view?usp=sharing",
        "https://drive.google.com/file/d/13NxWETxjIKMjh-YbEYfact8THuKNcxWN/view?usp=sharing",
        "https://drive.google.com/file/d/118cAlVe1vTXFTETnYv12dI4DGnyDetGV/view?usp=sharing",
        "https://drive.google.com/file/d/1eIKL87Qv2zYJzSZt69fxcWZjvj_wwcHm/view?usp=sharing",
        "https://drive.google.com/file/d/1yM-TcSKnsMv481mmx2IjQ05taAraz2H9/view?usp=sharing",
        "https://drive.google.com/file/d/1_ToqbnHE2o_7v-Zomd51SJa9qZgHlLqI/view?usp=sharing",
        "https://drive.google.com/file/d/1pt5KLy7a-mg4WiDgBYOVVUpKTDxyieFK/view?usp=sharing",
        "https://drive.google.com/file/d/17BvnbtB55rXl1kYEPRzrO4ROi8rl5y7_/view?usp=sharing"
    ]

    if LINKS_GOOGLE_DRIVE:
        colunas = st.columns(3, gap="medium")
        
        for i, link_original in enumerate(LINKS_GOOGLE_DRIVE):
            with colunas[i % 3]:
                # Transforma o link em URL direta de imagem compatível com navegadores
                url_direta_imagem = obter_link_direto_drive(link_original)
                
                # 🚀 O GRANDE TRUQUE: Passar a URL direto para o st.image
                # O servidor do Streamlit não baixa nada! Quem faz o download é o celular do usuário.
                st.image(
                    url_direta_imagem, 
                    use_column_width=True
                )
                
        st.divider()
        st.caption(f"📷 {len(LINKS_GOOGLE_DRIVE)} foto(s) renderizada(s) via CDN estável do Google.")
    else:
        st.info("📂 Nenhuma foto configurada na lista do Google Drive.")