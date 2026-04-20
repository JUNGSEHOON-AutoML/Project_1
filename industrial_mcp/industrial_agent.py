import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize Gemini Multimodal Model (Cloud-based, 0% local load)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    IS_SIMULATION = False
else:
    # Fallback for demonstration if API key is not set
    llm = None
    IS_SIMULATION = True
    print("[System] Running in Simulation Mode (API Key missing).")

# 2. RAG Knowledge Base (Simple Implementation for Laptop Specs)
KNOWLEDGE_BASE = {
    "zipper": "Tolerance is 0.1mm. Over 0.1mm is FAIL. Cooling speed issues cause misalignment.",
    "bottle": "Zero tolerance for cracks. Vertical cracks > 1mm on neck must be REJECTED.",
    "bolt": "Torque: 15-20 Nm. Check for thread burrs."
}

def get_rag_context(component_name: str) -> str:
    """Retrieves relevant manual info from the RAG store."""
    return KNOWLEDGE_BASE.get(component_name.lower(), "General industrial safety standards apply.")

# 3. Multimodal LangChain
async def analyze_industrial_scene(image_path: str, component_name: str):
    """
    Analyzes an image using Gemini (Sense) and retrieves manual info (RAG).
    Orchestrated by LangChain.
    """
    # [Think] Get Context from RAG
    context = get_rag_context(component_name)
    
    # [Sense] Multimodal Analysis (Simulation of Gemini call)
    # prompt = f"Analyze this image of a {component_name}. Manual says: {context}. Is it a defect?"
    # response = await llm.ainvoke([HumanMessage(content=[{"type": "text", "text": prompt}, {"type": "image_url", "image_url": image_path}])])
    
    # Simulation of the combined result for building the UI flow
    result = {
        "analysis": f"AI detected a visible misalignment in the {component_name} teeth.",
        "manual_rule": context,
        "decision": "REJECT",
        "action_required": "Adjust machine cooling sequence."
    }
    return result

async def batch_process_images(folder_path: str):
    """Scans a folder and generates a comprehensive inspection report."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "Input folder created. Please add images."

    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
    report_content = "# Industrial Inspection Report\n\n"
    report_content += f"**Date:** 2026-04-20\n**Total Units:** {len(files)}\n\n---\n"

    print(f"\n[Batch] Processing {len(files)} images from {folder_path}...")

    for f in files:
        # Simple heuristic to guess class from filename
        comp_name = "zipper" if "zipper" in f.lower() else "bottle"
        result = await analyze_industrial_scene(os.path.join(folder_path, f), comp_name)
        
        report_content += f"## Unit: {f}\n"
        report_content += f"- **Target Class:** {comp_name}\n"
        report_content += f"- **Decision:** **{result['decision']}**\n"
        report_content += f"- **AI Insight:** {result['analysis']}\n"
        report_content += f"- **Knowledge Source:** {result['manual_rule']}\n\n"
        print(f"  > Processed {f}: {result['decision']}")

    # Save report
    report_dir = "reports"
    if not os.path.exists(report_dir): os.makedirs(report_dir)
    report_path = os.path.join(report_dir, "inspection_report.md")
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(report_content)
    
    return report_path

if __name__ == "__main__":
    import asyncio
    
    async def main():
        input_folder = "data/input_images"
        # Ensure dummy files for demo
        if not os.path.exists(input_folder): os.makedirs(input_folder)
        for name in ["unit_001_zipper.jpg", "unit_002_bottle.jpg"]:
            with open(os.path.join(input_folder, name), "w") as f: f.write("dummy")

        print("\n" + "="*40)
        print("INDUSTRIAL AI AGENT: BATCH MODE")
        print("="*40)
        
        report_file = await batch_process_images(input_folder)
        print("\n" + "="*40)
        print(f"Report Generated: {report_file}")
        print("="*40)

    asyncio.run(main())
