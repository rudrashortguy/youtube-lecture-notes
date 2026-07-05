import uuid, json, time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ponytail: in-memory store, swap for Redis if multi-process needed
results = {}

@app.post("/process")
async def process_video(data: dict):
    url = data.get("url", "")
    task_id = str(uuid.uuid4())
    results[task_id] = {"status": "processing", "url": url}
    return {"task_id": task_id, "status": "processing"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    r = results.get(task_id, {"status": "not_found"})
    if r["status"] == "processing":
        r["status"] = "completed"
        r["data"] = {
            "title": "Sample Lecture Video",
            "structured_notes": [
                {"timestamp": "00:00", "bullet": "Introduction to the topic"},
                {"timestamp": "01:30", "bullet": "Key concept explained"},
                {"timestamp": "03:45", "bullet": "Important formula derived"},
            ],
            "definitions": [{"term": "Sample Term", "definition": "A mock definition for demo purposes."}],
            "quiz": [{"question": "Sample question?", "options": ["A", "B", "C", "D"], "correct_index": 0}],
            "flashcards": [{"front": "Sample concept", "back": "Mock definition for testing"}],
            "timeline": [{"time": "00:00", "event": "Start"}, {"time": "05:00", "event": "End"}],
            "exam_questions": ["Explain the key concept from this lecture."],
        }
        results[task_id] = r
    return results[task_id]
