
#AI71_API_KEY = "api71-api-80c0a825-4344-4ed1-be16-574f9d0a2f53"
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import openai
import uvicorn

app = FastAPI()

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = "api71-api-80c0a825-4344-4ed1-be16-574f9d0a2f53"

client = openai.OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)

@app.post("/generate")
async def generate(request: Request):
    prompt = (await request.body()).decode("utf-8")
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        messages=messages,
        model="tiiuae/falcon-180b-chat",
        stream=True,
    )
    output = ""
    for chunk in response:
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            output += delta_content
    return {"output": output.strip()}

@app.get("/")
async def index():
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
