import json
import os
from mitmproxy import http
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def request(flow: http.HTTPFlow) -> None:
    if (flow.request.host == "copilot-proxy.githubusercontent.com" and
            flow.request.path == "/v1/chat/completions"):
        # Modify the request JSON
        request_data = flow.request.get_text()
        json_data = json.loads(request_data)
        json_data["model"] = "gpt-4"

        # Remove the "intent" parameter
        if "intent" in json_data:
            del json_data["intent"]

        flow.request.set_text(json.dumps(json_data))

        # Modify the request URL
        flow.request.host = "api.openai.com"

        # Strip all existing headers
        flow.request.headers.clear()

        # Add new headers
        flow.request.headers["Content-Type"] = "application/json"
        flow.request.headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
    else:
        # Forward the request to the original destination
        pass

def response(flow: http.HTTPFlow) -> None:
    if (flow.request.host == "api.openai.com" and
            flow.request.path == "/v1/chat/completions"):
        # Forward the streamed response to the client
        for chunk in flow.response.stream:
            ctx.log.info(f"Forwarding chunk: {chunk}")
            ctx.master.commands.call("view.response.stream", [chunk])