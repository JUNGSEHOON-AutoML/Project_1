from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import psutil
import os
import json
import sys

app = FastAPI(title="Industrial AI Hub Service")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/system/status")
async def get_status():
    return {
        "cpu_usage": psutil.cpu_percent(interval=0.1),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "status": "OPTIMAL"
    }

@app.get("/api/inspection/latest")
async def get_latest_inspection():
    return {
        "unit_id": "SN-2026-0420-X1",
        "timestamp": "2026-04-20T17:40:00",
        "class": "zipper",
        "result": "FAIL",
        "anomaly_score": 0.892,
        "llm_insight": "금속 지퍼 이빨의 정렬 불량 감지. 다이캐스팅 냉각 공정 확인 필요.",
        "rag_rule": "Tolerance is 0.1mm. Over 0.1mm is FAIL."
    }

@app.get("/api/inspection/expert")
async def get_expert_consultation(component: str):
    # industrial_agent 임포트 지연 실행 (오류 방지)
    try:
        from industrial_agent import analyze_industrial_scene
        result = await analyze_industrial_scene("latest.jpg", component)
        return {"status": "success", "analysis": result["analysis"], "rag_rule": result["manual_rule"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Serve the dashboard files
app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("🚀 INDUSTRIAL AI HUB BACKEND STARTING")
        print("URL: http://localhost:8000")
        print("Dashboard: Open live.html in your browser")
        print("="*50 + "\n")
        
        # 로그 레벨을 info로 설정하여 터미널에 출력이 나오도록 함
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
