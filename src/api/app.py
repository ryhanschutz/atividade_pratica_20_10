from pathlib import Path
from typing import List, Literal, Optional
import cv2
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="AeroMotion Dynamics - Central Industrial de IA",
    description="Hub centralizado de monitoramento preditivo de turbinas (sensores IoT) e inspeção por visão computacional (óptica e térmica).",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {
        "status": "online",
        "mensagem": "AeroMotion Dynamics - API Industrial",
        "documentacao_swagger": "/docs",
        "verificacao_saude": "/health"
    }

DIRETORIO_RAIZ = Path(__file__).resolve().parents[2]
CAMINHO_MODELOS = DIRETORIO_RAIZ / "assets" / "modelos"

CLASSES_MAP = {
    0: "Normal",
    1: "Desgaste de Rolamento",
    2: "Desbalanceamento do Rotor",
    3: "Cavitação e Superaquecimento"
}

def carregar_artefato(nome_arquivo: str):
    caminho = CAMINHO_MODELOS / nome_arquivo
    if caminho.exists():
        return joblib.load(caminho)
    return None

scaler = carregar_artefato("robust_scaler_aeromotion.joblib")
modelo_multiclasse = carregar_artefato("modelo_multiclasse_aeromotion.joblib")
modelo_isolation_forest = carregar_artefato("modelo_isolation_forest.joblib")

class TelemetriaInput(BaseModel):
    id_equipamento: Literal["TURB-101", "TURB-102", "TURB-103", "TURB-104"] = Field(..., description="Bancada de teste")
    modo_operacao: Literal["Cruzeiro", "Carga_Media", "Carga_Alta"] = Field(..., description="Regime de operação")
    horas_operacao_acumuladas: float = Field(..., ge=0.0, le=20000.0)
    temperatura_mancal_c: float = Field(..., ge=20.0, le=150.0, description="Temperatura (°C)")
    vibracao_rms_mms: float = Field(..., ge=0.0, le=30.0, description="Vibração RMS (mm/s)")
    pressao_oleo_bar: float = Field(..., ge=0.1, le=10.0, description="Pressão do óleo (Bar)")
    rotacao_rpm: float = Field(..., ge=500.0, le=5000.0, description="Rotação (RPM)")
    emissao_acustica_db: float = Field(..., ge=20.0, le=130.0, description="Ruído acústico (dB)")
    corrente_eletrica_amp: float = Field(..., ge=5.0, le=100.0, description="Corrente elétrica (A)")
    vib_roll_mean_1h: Optional[float] = Field(default=None)
    vib_roll_std_1h: Optional[float] = Field(default=None)
    vib_roll_mean_6h: Optional[float] = Field(default=None)
    vib_roll_std_6h: Optional[float] = Field(default=None)
    temp_roll_mean_1h: Optional[float] = Field(default=None)
    temp_roll_std_1h: Optional[float] = Field(default=None)
    temp_roll_mean_6h: Optional[float] = Field(default=None)
    temp_roll_std_6h: Optional[float] = Field(default=None)

class BatchTelemetriaInput(BaseModel):
    leituras: List[TelemetriaInput]

class PredicaoOutput(BaseModel):
    id_equipamento: str
    modo_operacao: str
    codigo_falha: int
    diagnostico: str
    probabilidade_confianca: float
    probabilidades_classes: dict
    severidade_dinamica: float
    anomalia_isolation_forest: bool
    status_geral: str
    recomendacao_manutencao: str

def montar_vetor_features(item: TelemetriaInput) -> np.ndarray:
    sev = item.vibracao_rms_mms / item.rotacao_rpm if item.rotacao_rpm > 0 else 0.0
    eq_101 = 1.0 if item.id_equipamento == "TURB-101" else 0.0
    eq_102 = 1.0 if item.id_equipamento == "TURB-102" else 0.0
    eq_103 = 1.0 if item.id_equipamento == "TURB-103" else 0.0
    eq_104 = 1.0 if item.id_equipamento == "TURB-104" else 0.0
    mod_alta = 1.0 if item.modo_operacao == "Carga_Alta" else 0.0
    mod_media = 1.0 if item.modo_operacao == "Carga_Media" else 0.0
    mod_cruz = 1.0 if item.modo_operacao == "Cruzeiro" else 0.0

    v_m1 = item.vib_roll_mean_1h if item.vib_roll_mean_1h is not None else item.vibracao_rms_mms
    v_s1 = item.vib_roll_std_1h if item.vib_roll_std_1h is not None else 0.15
    v_m6 = item.vib_roll_mean_6h if item.vib_roll_mean_6h is not None else item.vibracao_rms_mms
    v_s6 = item.vib_roll_std_6h if item.vib_roll_std_6h is not None else 0.20

    t_m1 = item.temp_roll_mean_1h if item.temp_roll_mean_1h is not None else item.temperatura_mancal_c
    t_s1 = item.temp_roll_std_1h if item.temp_roll_std_1h is not None else 1.2
    t_m6 = item.temp_roll_mean_6h if item.temp_roll_mean_6h is not None else item.temperatura_mancal_c
    t_s6 = item.temp_roll_std_6h if item.temp_roll_std_6h is not None else 1.8

    return np.array([[
        item.horas_operacao_acumuladas, item.temperatura_mancal_c, item.vibracao_rms_mms,
        item.pressao_oleo_bar, item.rotacao_rpm, item.emissao_acustica_db, item.corrente_eletrica_amp,
        v_m1, v_s1, v_m6, v_s6, t_m1, t_s1, t_m6, t_s6,
        sev, eq_101, eq_102, eq_103, eq_104, mod_alta, mod_media, mod_cruz
    ]])

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "servico": "AeroMotion Central AI API",
        "versao": "2.0.0",
        "modelos_carregados": {
            "scaler": scaler is not None,
            "multiclasse": modelo_multiclasse is not None,
            "isolation_forest": modelo_isolation_forest is not None
        }
    }

@app.post("/predict", response_model=PredicaoOutput)
async def predict_single(payload: TelemetriaInput):
    if not (scaler and modelo_multiclasse and modelo_isolation_forest):
        raise HTTPException(status_code=503, detail="Modelos de Machine Learning não foram carregados.")

    X_raw = montar_vetor_features(payload)
    X_scaled = scaler.transform(X_raw)
    pred_cls = int(modelo_multiclasse.predict(X_scaled)[0])
    probs = modelo_multiclasse.predict_proba(X_scaled)[0]
    conf = float(np.max(probs))

    core_idx = [1, 2, 3, 4, 5, 6, 15]
    iso_flag = bool(modelo_isolation_forest.predict(X_scaled[:, core_idx])[0] == -1)

    prob_map = {CLASSES_MAP[i]: round(float(probs[i]), 4) for i in range(len(probs))}

    status = "Normal"
    if pred_cls != 0:
        status = "Crítico" if pred_cls == 3 else "Alerta"
    elif iso_flag:
        status = "Atenção (Comportamento Atípico)"

    recomendacoes = {
        0: "Operação estável dentro dos parâmetros nominais. Manter plano de inspeção preventiva.",
        1: "ALERTA: Desgaste mecânico no rolamento principal. Agendar substituição prévia antes do próximo ciclo.",
        2: "ALERTA: Desbalanceamento de rotor com vibração acentuada. Programar calibração e alinhamento dinâmico.",
        3: "CRÍTICO: Cavitação severa e colapso de pressão com superaquecimento. Desligamento imediato da bancada!"
    }

    return PredicaoOutput(
        id_equipamento=payload.id_equipamento,
        modo_operacao=payload.modo_operacao,
        codigo_falha=pred_cls,
        diagnostico=CLASSES_MAP[pred_cls],
        probabilidade_confianca=round(conf, 4),
        probabilidades_classes=prob_map,
        severidade_dinamica=round(payload.vibracao_rms_mms / payload.rotacao_rpm, 6),
        anomalia_isolation_forest=iso_flag,
        status_geral=status,
        recomendacao_manutencao=recomendacoes[pred_cls]
    )

@app.post("/predict-batch", response_model=List[PredicaoOutput])
async def predict_batch(batch: BatchTelemetriaInput):
    resultados = []
    for item in batch.leituras:
        res = await predict_single(item)
        resultados.append(res)
    return resultados
