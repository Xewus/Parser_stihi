from app.api import app
import uvicorn

def start_web_server():
    uvicorn.run(app)

if __name__ == '__main__':
    start_web_server()
