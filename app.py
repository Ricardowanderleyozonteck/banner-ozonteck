import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
import os

# Configurações de layout e identidade visual do App
st.set_page_config(
    page_title="Gerador de Banner Oficial Ozonteck", 
    page_icon="🚀",
    layout="centered"
)

# Estilização CSS Customizada - Correção de Contraste e Cores de Texto
st.markdown("""
    <style>
    /* Alterar cor de fundo geral e fontes */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 50%, #060409 100%);
        color: #ffffff;
    }
    
    /* Título Principal */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #a29bfe;
        margin-bottom: 30px;
    }
    
    /* Card de Instruções */
    .step-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00f2fe;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* FORÇAR COR DO TEXTO DENTRO DOS BOTÕES DO STREAMLIT */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #060409 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.3) !important;
    }
    
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 6px 20px rgba(0, 242, 254, 0.5) !important;
        color: #000000 !important;
    }

    /* FORÇAR TEXTO DO MODELO SELECIONADO NA TARJA PARA PRETO */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: #000000 !important;
    }
    
    /* Opções de dentro do menu suspenso continuam pretas para leitura no fundo branco do menu */
    div[role="listbox"] * {
        color: #000000 !important; 
    }

    /* FORÇAR O TEXTO DA ÁREA DE UPLOAD PARA PRETO */
    div[data-testid="stFileUploader"] * {
        color: #000000 !important;
    }
    div[data-testid="stFileUploader"] svg {
        fill: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

def process_image(user_img, base_img_path, shift_x, shift_y, zoom_percent):
    base = Image.open(base_img_path).convert("RGBA")
    user = Image.open(user_img).convert("RGBA")
    
    mask_center_x = 525  
    mask_center_y = 643  
    mask_size = 343     
    
    w_orig, h_orig = user.size
    min_dim = min(w_orig, h_orig)
    
    crop_size = int(min_dim / (zoom_percent / 100.0))
    crop_size = max(50, min(crop_size, min_dim))
    
    orig_center_x = w_orig // 2
    orig_center_y = h_orig // 2
    
    max_shift_x = (w_orig - crop_size) // 2
    max_shift_y = (h_orig - crop_size) // 2
    
    pixel_shift_x = int((shift_x / 100.0) * max_shift_x) if max_shift_x > 0 else 0
    pixel_shift_y = int((shift_y / 100.0) * max_shift_y) if max_shift_y > 0 else 0
    
    final_center_x = orig_center_x + pixel_shift_x
    final_center_y = orig_center_y - pixel_shift_y
    
    left = final_center_x - (crop_size // 2)
    top = final_center_y - (crop_size // 2)
    right = left + crop_size
    bottom = top + crop_size
    
    if left < 0: left, right = 0, crop_size
    if right > w_orig: right, left = w_orig, w_orig - crop_size
    if top < 0: top, bottom = 0, crop_size
    if bottom > h_orig: bottom, top = h_orig, h_orig - crop_size
    
    user_cropped = user.crop((left, top, right, bottom))
    user_resized = user_cropped.resize((mask_size, mask_size), resample=Image.BICUBIC)
    
    mask = Image.new('L', (mask_size, mask_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask_size, mask_size), fill=255)
    
    user_circular = Image.new('RGBA', (mask_size, mask_size), (0, 0, 0, 0))
    user_circular.paste(user_resized, (0, 0), mask=mask)
    
    pos_x = mask_center_x - (mask_size // 2)
    pos_y = mask_center_y - (mask_size // 2)
    
    base.paste(user_circular, (pos_x, pos_y), user_circular)
    return base

# Mapeamento da pasta
PASTA_BANNERS = os.path.join(os.path.dirname(__file__), "banners")

# ATUALIZADO: "🏆 OZON HAIR SCIENCE" agora aponta para o seu arquivo base original
MODELOS_DISPONIVEIS = {
    "🏆 OZON HAIR SCIENCE": "banner_base.png",
    "✨ Modelo Reconhecimento Diamante": "banner_modelo2.png",
    "🔥 Modelo Convite Especial": "banner_modelo3.png"
}

# --- INTERFACE VISUAL ---
st.markdown('<p class="main-title">✨ Banner Inteligente Ozonteck</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Escolha seu estilo predileto e crie seu convite profissional em segundos! 🚀</p>', unsafe_allow_html=True)

st.markdown("### 🗺️ Passo 1: Escolha o Estilo do seu Banner")
opcao_selecionada = st.selectbox(
    "Clique abaixo para mudar o design do convite:",
    list(MODELOS_DISPONIVEIS.keys())
)

nome_arquivo_banner = MODELOS_DISPONIVEIS[opcao_selecionada]
caminho_completo_banner = os.path.join(PASTA_BANNERS, nome_arquivo_banner)

st.markdown(f"""
    <div class="step-card">
        <strong>🎨 MODELO SELECIONADO:</strong> {opcao_selecionada}<br>
        <strong>📸 PASSO 2:</strong> Carregue sua foto oficial logo abaixo.<br>
        <strong>⚙️ PASSO 3:</strong> Use o painel lateral para fazer os ajustes finais de enquadramento.
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📸 Passo 2: Envie sua Foto")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.sidebar.markdown("## 🛠️ Central de Ajustes")
    st.sidebar.markdown("Deixe o enquadramento impecável:")
    
    zoom_percent = st.sidebar.slider("🔍 Zoom da Imagem (%)", min_value=100, max_value=300, value=100, step=5)
    shift_x = st.sidebar.slider("↔️ Mover para os Lados", min_value=-100, max_value=100, value=0, step=2)
    shift_y = st.sidebar.slider("↕️ Mover para Cima / Baixo", min_value=-100, max_value=100, value=0, step=2)
    
    try:
        with st.spinner("✨ Ajustando sua foto ao modelo..."):
            result_img = process_image(uploaded_file, caminho_completo_banner, shift_x, shift_y, zoom_percent)
        
        st.success(f"🎉 Seu banner do '{opcao_selecionada}' foi gerado!")
        st.image(result_img, use_container_width=True)
        
        buf = io.BytesIO()
        result_img.convert("RGB").save(buf, format="JPEG", quality=95)
        byte_im = buf.getvalue()
        
        st.write("")
        st.download_button(
            label=f"🔥 BAIXAR MEU BANNER OFICIAL",
            data=byte_im,
            file_name="banner_personalizado_ozonteck.jpg",
            mime="image/jpeg",
            use_container_width=True
        )
    except FileNotFoundError:
        st.error(f"❌ Arquivo '{nome_arquivo_banner}' ausente na pasta 'banners'.")
    except Exception as e:
        st.error(f"💥 Erro ao processar: {e}")
else:
    try:
        if os.path.exists(caminho_completo_banner):
            img_previa = Image.open(caminho_completo_banner)
            st.image(img_previa, caption=f"Prévia Visual: {opcao_selecionada}", use_container_width=True)
        else:
            st.warning(f"⚠️ Crie a pasta 'banners' e salve nela o arquivo '{nome_arquivo_banner}'.")
    except Exception:
        pass
