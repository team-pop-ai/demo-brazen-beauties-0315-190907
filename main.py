import os
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import anthropic
import uvicorn

app = FastAPI(title="Brazen Beauties AI Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else []

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/promote-event")
async def promote_event(
    event_name: str = Form(...),
    event_date: str = Form(...),
    event_location: str = Form(...),
    target_audience: str = Form(...)
):
    if not event_name.strip():
        raise HTTPException(status_code=400, detail="Event name is required")
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    system_prompt = """You are Nakeesha's AI assistant with 25 years of gemology expertise. You help promote jewelry business events with professional, engaging content that attracts customers to pop-up events and jewelry shows.

Create compelling event promotion content that:
- Highlights unique jewelry offerings and expertise
- Appeals to the target demographic
- Creates urgency and excitement
- Includes call-to-action for attendance
- Maintains professional jewelry business tone"""

    user_prompt = f"""Create promotional content for this jewelry event:

Event: {event_name}
Date: {event_date}  
Location: {event_location}
Target Audience: {target_audience}

Generate:
1. Social media post (Instagram/Facebook)
2. Email subject line and preview text
3. Key talking points for promotion
4. Call-to-action suggestions"""

    try:
        message = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return {"result": message.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.post("/customer-inquiry")
async def customer_inquiry(
    customer_name: str = Form(...),
    inquiry_text: str = Form(...),
    inquiry_type: str = Form(...)
):
    if not inquiry_text.strip():
        raise HTTPException(status_code=400, detail="Inquiry text is required")
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    system_prompt = """You are Nakeesha's AI assistant with 25 years of gemology expertise. You provide professional customer service for a jewelry business, answering questions about:

- Gemstone identification and properties
- Jewelry care and maintenance  
- Custom jewelry design process
- Permanent jewelry services
- Pricing and appointment scheduling
- Event information and bookings

Respond professionally, knowledgeably, and helpfully. Include relevant gemology expertise when appropriate."""

    user_prompt = f"""Customer inquiry from {customer_name}:

Type: {inquiry_type}
Question: {inquiry_text}

Provide a professional response with your gemology expertise. If this requires an appointment or in-person consultation, suggest next steps."""

    try:
        message = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return {"result": message.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.post("/generate-followup")
async def generate_followup(
    customer_name: str = Form(...),
    event_attended: str = Form(...),
    interests: str = Form(...),
    followup_type: str = Form(...)
):
    if not customer_name.strip():
        raise HTTPException(status_code=400, detail="Customer name is required")
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    system_prompt = """You are Nakeesha's AI assistant with 25 years of gemology expertise. You create personalized follow-up sequences for jewelry business customers after events.

Create warm, professional follow-ups that:
- Thank customers for attending
- Reference their specific interests
- Offer relevant services or products
- Include gemology insights when appropriate
- Encourage future engagement
- Maintain personal, caring tone"""

    user_prompt = f"""Create a follow-up sequence for:

Customer: {customer_name}
Event Attended: {event_attended}
Interests: {interests}
Follow-up Type: {followup_type}

Generate personalized follow-up content including:
1. Initial thank you message
2. Product/service recommendations based on interests
3. Next steps or call-to-action
4. Timeline for follow-up sequence"""

    try:
        message = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return {"result": message.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.get("/api/events")
async def get_events():
    events = load_json("data/events.json", [])
    return {"events": events}

@app.get("/api/customers")
async def get_customers():
    customers = load_json("data/customers.json", [])
    return {"customers": customers}

@app.get("/api/knowledge")
async def get_knowledge():
    knowledge = load_json("data/jewelry_knowledge.json", [])
    return {"knowledge": knowledge}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)