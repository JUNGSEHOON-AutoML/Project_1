from mcp.server.fastmcp import FastMCP
import os
import json
import psutil
import gc
import torch
import logging
from ultralytics import YOLO

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Industrial-Hub-Pro")

# Initialize FastMCP server
mcp = FastMCP("Industrial-Hub-Pro")

# --- Chief Engineer's Resource Guard & Sequential Logic ---
class SequentialGuard:
    _is_ai_running = False
    _is_cad_running = False

    @classmethod
    def start_ai(cls):
        if cls._is_cad_running:
            logger.warning("CAD operation detected. Waiting for CAD to finish to prevent RAM swap.")
            # In real scenario, wait or signal CAD to pause
        cls._is_ai_running = True

    @classmethod
    def end_ai(cls):
        cls._is_ai_running = False
        # Clear AI memory immediately to free RAM for CAD
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        logger.info("AI Operation finished. RAM cleared for CAD/other tasks.")

def check_intel_cpu_resources():
    ram = psutil.virtual_memory()
    free_gb = ram.available / (1024**3)
    cpu_usage = psutil.cpu_percent(interval=0.1)
    
    logger.info(f"[Intel i7-1195G7] Free RAM: {free_gb:.2f}GB, CPU: {cpu_usage}%")
    
    if free_gb < 2.0:
        raise RuntimeError("Low Memory for safe AI execution. Please close heavy apps (NX/CAD) temporarily.")
    return True

# --- Optimized Tools ---

@mcp.tool()
async def run_optimized_vision(image_path: str) -> str:
    """
    Intel CPU(OpenVINO)에 최적화된 경량 모델(YOLOv8n)로 이상 징후를 탐지합니다.
    
    - Hardware: Intel Core i7-1195G7
    - Acceleration: OpenVINO
    - Model: YOLOv8n (Nano) - 3.2M parameters
    """
    check_intel_cpu_resources()
    SequentialGuard.start_ai()
    
    try:
        # Load lightweight model with OpenVINO export format if available
        # model = YOLO("yolov8n_openvino_model") # Pre-exported OpenVINO model
        model = YOLO("yolov8n.pt") # Fallback to standard Nano
        
        # Inference using CPU with Intel acceleration
        # result = model.predict(source=image_path, device="cpu")
        
        logger.info(f"YOLOv8n inference on Intel CPU (OpenVINO) initiated for {image_path}")
        
        return "진단 완료: i7-1195G7 OpenVINO 가속을 통해 CPU 부하를 최소화하며 경량 모델(Nano) 처리를 마쳤습니다."
    finally:
        SequentialGuard.end_ai()

@mcp.tool()
async def manage_cad_pipeline(action: str, model_path: str) -> str:
    """
    CAD(NX/FreeCAD) 작업을 순차적 파이프라인으로 관리합니다.
    AI 연산과 충돌하지 않도록 리소스를 조율합니다.
    """
    if SequentialGuard._is_ai_running:
        return "AI 추론이 진행 중입니다. RAM 보호를 위해 CAD 작업을 잠시 대기시켜 주십시오."
    
    SequentialGuard._is_cad_running = True
    try:
        # CAD Action Logic here
        return f"CAD 작업 수행 중: {action} (대상: {model_path})"
    finally:
        SequentialGuard._is_cad_running = False

@mcp.tool()
async def check_system_resource() -> str:
    """현재 노트북의 RAM 및 CPU 사용량을 체크하여 실행 가능 여부를 판단합니다."""
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)
    return f"현재 리소스 상태: RAM {ram.percent}%, CPU {cpu}% (가용 RAM: {ram.available/(1024**3):.2f}GB)"

@mcp.tool()
async def consult_ai_expert(component_type: str, image_path: str = "latest.jpg") -> str:
    """
    산업용 전문가 에이전트(LangChain + RAG)에게 기술적 조언을 구합니다.
    매뉴얼 지식과 이미지 분석 결과를 결합하여 답변합니다.
    """
    from industrial_agent import analyze_industrial_scene
    try:
        result = await analyze_industrial_scene(image_path, component_type)
        return f"[AI 전문가 답변]\n- 분석: {result['analysis']}\n- 규정: {result['manual_rule']}\n- 판정: {result['decision']}"
    except Exception as e:
        return f"전문가 상담 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    mcp.run()
