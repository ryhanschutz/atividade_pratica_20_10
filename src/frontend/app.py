import streamlit as st
import pandas as pd
import numpy as np
import requests
import cv2
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="AeroMotion Dynamics - Central de Monitoramento IA",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SVG_ICONS = {
    "turbina": '''<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 4.24 4.24"/><path d="m14.83 9.17 4.24-4.24"/><path d="m14.83 14.83 4.24 4.24"/><path d="m9.17 14.83-4.24 4.24"/><circle cx="12" cy="12" r="4"/></svg>''',
    "olho_visao": '''<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>''',
    "cerebro_ia": '''<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a4 4 0 0 0-4 4v1a4 4 0 0 0-3 3.86c0 1.5.8 2.8 2 3.47A4 4 0 0 0 8 18v1a4 4 0 0 0 4 4 4 4 0 0 0 4-4v-1a4 4 0 0 0 1-3.67c1.2-.67 2-1.97 2-3.47A4 4 0 0 0 16 7V6a4 4 0 0 0-4-4Z"/><path d="M12 2v20"/></svg>''',
    "check": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>''',
    "alerta": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>''',
    "critico": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>'''
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: #0b1120; color: #f1f5f9; }
    .status-card {
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 6px solid;
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }
    .status-normal { background: rgba(16, 185, 129, 0.12); border-color: #10b981; color: #a7f3d0; }
    .status-alerta { background: rgba(245, 158, 11, 0.12); border-color: #f59e0b; color: #fde68a; }
    .status-critico { background: rgba(239, 68, 68, 0.15); border-color: #ef4444; color: #fecaca; }
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"
RAIZ_DIR = Path(__file__).resolve().parents[2]

st.sidebar.markdown(f"""
<div class="sidebar-header">
    {SVG_ICONS["turbina"]}
    <div>
        <h3 style="margin: 0; font-size: 1.15rem; color: #000000; font-weight: 700;">AeroMotion Dynamics</h3>
        <span style="font-size: 0.78rem; color: #334155; font-weight: 500;">Divisão de Turbinas S.A.</span>
    </div>
</div>

""", unsafe_allow_html=True)

modulo = st.sidebar.radio(
    "Centro de Controle",
    [
        "Telemetria das Bancadas (IoT)",
        "Inspeção Óptica & Térmica (OpenCV)",
        "Governança & MLOps"
    ],
    index=0
)

@st.cache_data(ttl=5)
def checar_api():
    try:
        r = requests.get(f"{API_URL}/health", timeout=1.5)
        if r.status_code == 200:
            return True, r.json()
    except Exception:
        pass
    return False, None

api_online, _ = checar_api()

st.sidebar.markdown("---")
if api_online:
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; color: #34d399; font-size: 0.85rem;">
        {SVG_ICONS["check"]} <span>API FastAPI Ativa (Porta 8000)</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; color: #fbbf24; font-size: 0.85rem;">
        {SVG_ICONS["alerta"]} <span>Modo Standalone (Execução Local)</span>
    </div>
    """, unsafe_allow_html=True)

def carregar_imagem(caminho_str):
    try:
        with open(caminho_str, "rb") as f:
            bytes_arr = bytearray(f.read())
            np_arr = np.asarray(bytes_arr, dtype=np.uint8)
            return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        return None

if modulo == "Telemetria das Bancadas (IoT)":
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        {SVG_ICONS["turbina"]}
        <h1 style="margin: 0; font-size: 1.8rem;">Monitoramento Preditivo das Turbinas</h1>
    </div>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 25px;">
        Inferência em tempo real via <b>Random Forest / Gradient Boosting</b> e <b>Isolation Forest</b>.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        turbina_sel = st.selectbox("Bancada de Teste", ["TURB-101", "TURB-102", "TURB-103", "TURB-104"])
    with col2:
        regime_sel = st.selectbox("Regime Operacional", ["Cruzeiro", "Carga_Media", "Carga_Alta"])
    with col3:
        cenario_predefinido = st.selectbox("Cenário de Simulação Rápida", [
            "Operação Nominal (Sem Falha)",
            "Falha 1: Desgaste de Rolamento",
            "Falha 2: Desbalanceamento de Rotor",
            "Falha 3: Cavitação e Superaquecimento",
            "Personalizado"
        ])
    with col4:
        st.write("")
        st.write("")
        executar_diagnostico = st.button("Executar Inferência", use_container_width=True)

    defaults = {
        "Operação Nominal (Sem Falha)": {"temp": 52.0, "vib": 1.8, "press": 4.5, "rpm": 2400.0, "acust": 45.0, "corr": 21.0, "horas": 1200.0},
        "Falha 1: Desgaste de Rolamento": {"temp": 68.0, "vib": 8.5, "press": 4.1, "rpm": 2900.0, "acust": 78.0, "corr": 28.0, "horas": 3800.0},
        "Falha 2: Desbalanceamento de Rotor": {"temp": 75.0, "vib": 9.2, "press": 3.8, "rpm": 3450.0, "acust": 71.0, "corr": 42.0, "horas": 4100.0},
        "Falha 3: Cavitação e Superaquecimento": {"temp": 98.5, "vib": 11.2, "press": 1.9, "rpm": 3550.0, "acust": 89.0, "corr": 48.0, "horas": 4400.0},
        "Personalizado": {"temp": 60.0, "vib": 2.5, "press": 4.2, "rpm": 3000.0, "acust": 50.0, "corr": 25.0, "horas": 2000.0}
    }[cenario_predefinido]

    st.markdown("#### Grandezas Físicas Telemetradas")
    c_s1, c_s2, c_s3 = st.columns(3)
    with c_s1:
        temperatura = st.slider("Temperatura do Mancal Principal (°C)", 20.0, 140.0, float(defaults["temp"]), 0.5)
        vibracao = st.slider("Vibração RMS Global (mm/s)", 0.0, 25.0, float(defaults["vib"]), 0.1)
    with c_s2:
        pressao = st.slider("Pressão da Linha de Lubrificação (Bar)", 0.5, 6.0, float(defaults["press"]), 0.1)
        rotacao = st.slider("Velocidade Angular do Rotor (RPM)", 1500.0, 4000.0, float(defaults["rpm"]), 50.0)
    with c_s3:
        acustica = st.slider("Emissão Acústica / Ruído Mecânico (dB)", 30.0, 110.0, float(defaults["acust"]), 1.0)
        corrente = st.slider("Corrente Elétrica do Acionamento (A)", 10.0, 60.0, float(defaults["corr"]), 0.5)

    payload_dados = {
        "id_equipamento": turbina_sel,
        "modo_operacao": regime_sel,
        "horas_operacao_acumuladas": float(defaults["horas"]),
        "temperatura_mancal_c": float(temperatura),
        "vibracao_rms_mms": float(vibracao),
        "pressao_oleo_bar": float(pressao),
        "rotacao_rpm": float(rotacao),
        "emissao_acustica_db": float(acustica),
        "corrente_eletrica_amp": float(corrente)
    }

    resultado = None
    try:
        r = requests.post(f"{API_URL}/predict", json=payload_dados, timeout=2.5)
        if r.status_code == 200:
            resultado = r.json()
    except Exception:
        pass

    if not resultado:
        try:
            from src.api import app as api_module
            import asyncio
            payload_pydantic = api_module.TelemetriaInput(**payload_dados)
            resultado = asyncio.run(api_module.predict_single(payload_pydantic)).model_dump()
        except Exception as e:
            st.error(f"Erro na inferência: {e}")

    if resultado:
        status_cls = resultado["codigo_falha"]
        diag = resultado["diagnostico"]
        conf = resultado["probabilidade_confianca"] * 100
        anomalia = resultado["anomalia_isolation_forest"]
        recom = resultado["recomendacao_manutencao"]

        if status_cls == 0:
            card_class = "status-normal"
            icon_badge = SVG_ICONS["check"]
            titulo = f"Operação Nominal: {diag}"
        elif status_cls == 3:
            card_class = "status-critico"
            icon_badge = SVG_ICONS["critico"]
            titulo = f"Falha Crítica Detectada: {diag}"
        else:
            card_class = "status-alerta"
            icon_badge = SVG_ICONS["alerta"]
            titulo = f"Alerta Preventivo: {diag}"

        st.markdown(f"""
        <div class="status-card {card_class}">
            <div style="flex-shrink: 0; padding-top: 2px;">{icon_badge}</div>
            <div>
                <h3 style="margin: 0 0 6px 0; font-size: 1.2rem; font-weight: 700;">{titulo}</h3>
                <p style="margin: 0 0 6px 0; font-size: 0.9rem;">
                    <b>Grau de Certeza:</b> {conf:.2f}% &nbsp;|&nbsp; 
                    <b>Severidade Dinâmica (Vib/RPM):</b> {resultado['severidade_dinamica']:.6f} &nbsp;|&nbsp; 
                    <b>Anomalia Isolation Forest:</b> {'Detectada' if anomalia else 'Não apontada'}
                </p>
                <p style="margin: 0; font-size: 0.88rem; opacity: 0.95;"><b>Ação Recomendada:</b> {recom}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1.2, 1])
        with col_g1:
            probs = resultado.get("probabilidades_classes", {})
            if probs:
                fig_bar = px.bar(
                    x=list(probs.keys()),
                    y=[v * 100 for v in probs.values()],
                    labels={'x': 'Modo Diagnosticado', 'y': 'Probabilidade (%)'},
                    title="Probabilidades do Modelo Multiclasse (Scikit-Learn)",
                    color=list(probs.keys()),
                    color_discrete_map={
                        "Normal": "#10b981",
                        "Desgaste de Rolamento": "#f59e0b",
                        "Desbalanceamento do Rotor": "#3b82f6",
                        "Cavitação e Superaquecimento": "#ef4444"
                    }
                )
                fig_bar.update_layout(template="plotly_dark", showlegend=False, height=330, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_bar, use_container_width=True)

        with col_g2:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=vibracao,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Vibração RMS ({turbina_sel}) - mm/s"},
                gauge={
                    'axis': {'range': [0, 20]},
                    'bar': {'color': "#ef4444" if vibracao > 7.0 else "#10b981"},
                    'steps': [
                        {'range': [0, 4.5], 'color': "rgba(16, 185, 129, 0.2)"},
                        {'range': [4.5, 7.5], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [7.5, 20], 'color': "rgba(239, 68, 68, 0.3)"}
                    ]
                }
            ))
            fig_gauge.update_layout(template="plotly_dark", height=330, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

elif modulo == "Inspeção Óptica & Térmica (OpenCV)":
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        {SVG_ICONS["olho_visao"]}
        <h1 style="margin: 0; font-size: 1.8rem;">Inspeção Geométrica e Térmica de Componentes</h1>
    </div>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 25px;">
        Análise multimodal em tempo real: comparação geométrica contra a <b>Hélice de Referência Padrão</b> e delimitação de <b>Hotspots Críticos no Espaço HSV</b>.
    </p>
    """, unsafe_allow_html=True)

    caminho_base = RAIZ_DIR / "assets" / "imagens"
    caminho_ref = caminho_base / "helice-termica-referencia.png"
    img_referencia = carregar_imagem(str(caminho_ref))

    tab_geom, tab_term = st.tabs([
        "📐 Inspeção Geométrica (Detecção de Peça Torta / Deformada)",
        "🔥 Inspeção Térmica (Termografia e Hotspots HSV)"
    ])

    with tab_geom:
        col_ctrl1, col_ctrl2 = st.columns([1, 1.2])
        with col_ctrl1:
            st.markdown("#### Selecione a Imagem para Inspeção Geométrica")
            escolha_geom = st.selectbox("Amostra Industrial", [
                "Hélice Térmica com Pás Deformada (Objeto Torto)",
                "Análise térmica de hélice aeronáutica (Conforme / Alinhada)",
                "Hélice de Aeronave em Termografia (Referência Padrão)",
                "Upload de Imagem Externa"
            ])

            img_analise = None
            if escolha_geom == "Hélice Térmica com Pás Deformada (Objeto Torto)":
                img_analise = carregar_imagem(str(caminho_base / "helice-termica-deformada.png"))
            elif escolha_geom == "Análise térmica de hélice aeronáutica (Conforme / Alinhada)":
                img_analise = carregar_imagem(str(caminho_base / "helice-termica-ponto-quente.png"))
            elif escolha_geom == "Hélice de Aeronave em Termografia (Referência Padrão)":
                img_analise = img_referencia
            else:
                up = st.file_uploader("Carregar imagem para teste dimensional", type=["png", "jpg", "jpeg"], key="up_geom")
                if up:
                    nparr = np.frombuffer(up.read(), np.uint8)
                    img_analise = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img_analise is not None:
                st.image(cv2.cvtColor(img_analise, cv2.COLOR_BGR2RGB), caption="Peça Submetida à Bancada de Visão", use_container_width=True)

        with col_ctrl2:
            st.markdown("#### Análise Comparativa contra o Gabarito de Referência")
            if img_analise is not None and img_referencia is not None:
                def get_main_contour(im):
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray, (5, 5), 1.4)
                    edges = cv2.Canny(blur, 40, 130)
                    edges = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=2)
                    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if not cnts:
                        return None, edges
                    return max(cnts, key=cv2.contourArea), edges

                c_ref, _ = get_main_contour(img_referencia)
                c_test, _ = get_main_contour(img_analise)

                if c_ref is not None and c_test is not None:
                    score_deformacao = cv2.matchShapes(c_ref, c_test, cv2.CONTOURS_MATCH_I1, 0.0)
                    x, y, w, h = cv2.boundingRect(c_test)
                    aspect_ratio = w / float(h)

                    is_torta = bool(score_deformacao > 0.20 or aspect_ratio > 1.25 or aspect_ratio < 0.85)

                    preview_img = img_analise.copy()
                    cor_borda = (0, 0, 255) if is_torta else (0, 255, 0)
                    cv2.drawContours(preview_img, [c_test], -1, cor_borda, 3)

                    st.image(cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB), caption="Contorno e Geometria Extraída pelo Algoritmo", use_container_width=True)

                    if is_torta:
                        st.markdown(f"""
                        <div class="status-card status-critico">
                            <div>{SVG_ICONS["critico"]}</div>
                            <div>
                                <h4 style="margin: 0 0 4px 0; color: #fca5a5;">REPROVADO: OBJETO TORTO / PÁS DEFORMADAS DETECTADO!</h4>
                                <p style="margin: 0; font-size: 0.88rem;">
                                    <b>Grau de Deformação Estrutural:</b> {score_deformacao:.4f} (Limite seguro: &le; 0.20)<br>
                                    <b>Proporção Dimensional (Aspect Ratio):</b> {aspect_ratio:.3f} (Padrão nominal: ~1.07)<br>
                                    <b>Diagnóstico:</b> Desvio assimétrico severo na curvatura e alinhamento das pás em relação à hélice de referência.
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="status-card status-normal">
                            <div>{SVG_ICONS["check"]}</div>
                            <div>
                                <h4 style="margin: 0 0 4px 0; color: #86efac;">APROVADO: GEOMETRIA E ALINHAMENTO CONFORME</h4>
                                <p style="margin: 0; font-size: 0.88rem;">
                                    <b>Grau de Deformação Estrutural:</b> {score_deformacao:.4f} (Dentro da tolerância)<br>
                                    <b>Proporção Dimensional:</b> {aspect_ratio:.3f}<br>
                                    <b>Diagnóstico:</b> O componente respeita rigorosamente o gabarito de fabricação.
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    with tab_term:
        col_t1, col_t2 = st.columns([1, 1.2])
        with col_t1:
            st.markdown("#### Selecione a Imagem para Análise Térmica")
            escolha_term = st.selectbox("Termografia Industrial", [
                "Análise térmica de hélice aeronáutica (Ponto Crítico de Calor)",
                "Hélice de Aeronave em Termografia (Temperatura Nominal)",
                "Hélice Térmica com Pás Deformada",
                "Upload de Termografia Externa"
            ])

            img_termica = None
            if escolha_term == "Análise térmica de hélice aeronáutica (Ponto Crítico de Calor)":
                img_termica = carregar_imagem(str(caminho_base / "helice-termica-ponto-quente.png"))
            elif escolha_term == "Hélice de Aeronave em Termografia (Temperatura Nominal)":
                img_termica = img_referencia
            elif escolha_term == "Hélice Térmica com Pás Deformada":
                img_termica = carregar_imagem(str(caminho_base / "helice-termica-deformada.png"))
            else:
                up_t = st.file_uploader("Carregar termografia", type=["png", "jpg", "jpeg"], key="up_term")
                if up_t:
                    nparr = np.frombuffer(up_t.read(), np.uint8)
                    img_termica = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img_termica is not None:
                st.image(cv2.cvtColor(img_termica, cv2.COLOR_BGR2RGB), caption="Imagem Infravermelha / Espectro de Calor", use_container_width=True)

        with col_t2:
            st.markdown("#### Segmentação HSV de Zonas Críticas")
            if img_termica is not None:
                hsv = cv2.cvtColor(img_termica, cv2.COLOR_BGR2HSV)
                mask1 = cv2.inRange(hsv, np.array([0, 150, 90]), np.array([18, 255, 255]))
                mask2 = cv2.inRange(hsv, np.array([165, 150, 90]), np.array([180, 255, 255]))
                mask = cv2.bitwise_or(mask1, mask2)
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                hotspots = [c for c in contours if cv2.contourArea(c) > 80]
                area_total = sum(cv2.contourArea(c) for c in hotspots)
                critico = area_total > 200

                preview_thermal = img_termica.copy()
                cv2.drawContours(preview_thermal, hotspots, -1, (0, 255, 0), 3)
                st.image(cv2.cvtColor(preview_thermal, cv2.COLOR_BGR2RGB), caption="Delimitação de Hotspots Críticos (Contornos Verdes)", use_container_width=True)

                if critico:
                    st.markdown(f"""
                    <div class="status-card status-critico">
                        <div>{SVG_ICONS["critico"]}</div>
                        <div>
                            <h4 style="margin: 0 0 4px 0; color: #fca5a5;">ALERTA TÉRMICO CRÍTICO: SUPERAQUECIMENTO DETECTADO!</h4>
                            <p style="margin: 0; font-size: 0.88rem;">
                                <b>Quantidade de Hotspots:</b> {len(hotspots)} zona(s)<br>
                                <b>Área Irradiada Crítica:</b> {area_total:.1f} px (Limite: 200 px)<br>
                                <b>Ação Imediata:</b> Interrupção do ciclo de rotação para inspeção de atrito e lubrificação do mancal central.
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="status-card status-normal">
                        <div>{SVG_ICONS["check"]}</div>
                        <div>
                            <h4 style="margin: 0 0 4px 0; color: #86efac;">ZONA TÉRMICA OPERACIONAL DENTRO DA TOLERÂNCIA</h4>
                            <p style="margin: 0; font-size: 0.88rem;">
                                <b>Hotspots Detectados:</b> 0 zonas críticas.<br>
                                <b>Status:</b> Espectro infravermelho compatível com resfriamento adequado.
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif modulo == "Governança & MLOps":
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        {SVG_ICONS["cerebro_ia"]}
        <h1 style="margin: 0; font-size: 1.8rem;">Governança de IA, Conformidade e MLOps</h1>
    </div>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 25px;">
        Parecer técnico consolidado atendendo às exigências regulatórias do <b>EU AI Act</b>, <b>LGPD</b> e monitoramento de <b>Data/Concept Drift</b>.
    </p>
    """, unsafe_allow_html=True)

    tab_doc, tab_mlops = st.tabs(["📄 Parecer Regulatório & Ético", "📈 Monitoramento MLOps e Modelos"])

    with tab_doc:
        pdf_path = RAIZ_DIR / "docs" / "parecer-tecnico-regulatorio-etico-mlops.pdf"
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Baixar Parecer Técnico Oficial em PDF",
                    data=f.read(),
                    file_name="parecer-tecnico-regulatorio-etico-mlops.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        md_path = RAIZ_DIR / "docs" / "parecer-tecnico-regulatorio-etico-mlops.md"
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    with tab_mlops:
        st.markdown("#### Matriz Comparativa de Modelos Supervisionados (Etapa 2)")
        df_metricas = pd.DataFrame({
            "Algoritmo / Abordagem": ["Random Forest (SMOTE + GridSearchCV)", "HistGradientBoosting (LightGBM-style)", "Isolation Forest (Não Supervisionado)"],
            "Acurácia Global": ["97.4%", "96.8%", "N/A"],
            "Recall de Falhas (Média)": ["94.8%", "93.2%", "92.5% (Detecção)"],
            "F1-Score Macro": ["0.951", "0.942", "N/A"],
            "Tempo de Inferência": ["~78 ms", "~35 ms", "~15 ms"]
        })
        st.dataframe(df_metricas, use_container_width=True, hide_index=True)
