import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import components
from feedback.manager import FeedbackManager
from improvement.engine import ImprovementEngine
from metalearning.framework import MetaLearningFramework
from models.pipeline.llm_pipeline import LLMPipeline
from api.plugin_routes import router as plugin_router  # Import the plugin router

# Create FastAPI app
app = FastAPI(
    title="SuperDeepAgent API",
    description="API for SuperDeepAgent - An advanced AI agent system with feedback, improvement, and metalearning capabilities",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
feedback_manager = FeedbackManager()
improvement_engine = ImprovementEngine()
metalearning_framework = MetaLearningFramework()
llm_pipeline = LLMPipeline()

# Define routes
@app.get("/")
async def root():
    return {"message": "Welcome to SuperDeepAgent API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Feedback routes
@app.get("/api/feedback")
async def get_feedback():
    return {"feedback": feedback_manager.get_all_feedback()}

@app.post("/api/feedback")
async def submit_feedback(feedback_data: dict):
    return {"result": feedback_manager.process_feedback(feedback_data)}

# Improvement routes
@app.get("/api/improvements")
async def get_improvements():
    return {"improvements": improvement_engine.get_improvements()}

@app.post("/api/improvements/apply")
async def apply_improvement(improvement_data: dict):
    return {"result": improvement_engine.apply_improvement(improvement_data)}

# Metalearning routes
@app.get("/api/metalearning/metrics")
async def get_metalearning_metrics():
    return {"metrics": metalearning_framework.get_metrics()}

@app.post("/api/metalearning/transfer")
async def transfer_knowledge(transfer_data: dict):
    return {"result": metalearning_framework.transfer_knowledge(transfer_data)}

# Include plugin routes
app.include_router(plugin_router)

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
