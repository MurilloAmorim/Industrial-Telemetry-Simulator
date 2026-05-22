from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Simulador de Telemetria Industrial",
    description="API para monitoramento de tensão e controle de disjuntores em plantas de geração."
)

estado_planta = {
    "ultima_leitura_tensao": 0.0,
    "status_disjuntor": "LIGADO",  # Pode ser LIGADO ou DESLIGADO
    "modo_operacao": "AUTOMATICO", # Pode ser AUTOMATICO ou MANUAL
    "ultima_atualizacao": None,
    "alerta_critico": False
}

class LeituraSensor(BaseModel):
    tensao: float


# --- --- --- ROTAS DA API --- --- --- #

@app.get("/")
def rota_inicial():
    """Rota raiz para verificar se o servidor está online."""
    return {"status": "Servidor Industrial Online", "timestamp": datetime.now()}


@app.get("/status")
def obter_status_planta():
    """Retorna o estado atual completo da planta de geração (Painel do Operador)."""
    return estado_planta


@app.post("/telemetria")
def receber_telemetria(dados: LeituraSensor):
    """
    Rota que o hardware/simulador vai chamar a cada 2 segundos para injetar os dados de tensão.
    Também possui a lógica autônoma de proteção do sistema.
    """
    global estado_planta
    
    tensao_recebida = dados.tensao
    estado_planta["ultima_leitura_tensao"] = tensao_recebida
    estado_planta["ultima_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if tensao_recebida > 240.0:
        estado_planta["alerta_critico"] = True
        estado_planta["status_disjuntor"] = "DESLIGADO" # Desliga o switch preventivamente
    else:
        estado_planta["alerta_critico"] = False
        
    return {
        "status": "Processado com sucesso", 
        "disjuntor_atual": estado_planta["status_disjuntor"]
    }


@app.post("/disjuntor/alternar")
def alternar_disjuntor():
    """Rota manual para o operador ligar ou desligar o switch pela interface."""
    global estado_planta
    
    if estado_planta["status_disjuntor"] == "LIGADO":
        estado_planta["status_disjuntor"] = "DESLIGADO"
    else:
        estado_planta["status_disjuntor"] = "LIGADO"
        
    return {"mensagem": f"Disjuntor alterado manualmente para {estado_planta['status_disjuntor']}"}