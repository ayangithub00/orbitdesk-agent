from __future__ import annotations

import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_DIR / "web"


def format_terminal_response(result: dict) -> dict:
    """Give terminal graph routes a safe, presentable response."""
    classification = result.get("classification", "safe_failure")
    answer = result.get("answer", "").strip()
    defaults = {
        "requires_clarification": "Please share the affected workspace or object, the exact error code, and when the issue occurred so I can suggest the documented next step.",
        "requires_escalation": "This request needs assistance from the OrbitDesk support team. Please provide the relevant IDs, timestamps, error message, and steps already tried.",
        "out_of_scope": "I can help with documented OrbitDesk product support, but this request is outside that scope.",
    }
    if not answer:
        answer = defaults.get(classification, "I don't have enough information in the provided documents.")
    return {
        "classification": classification,
        "answer": answer,
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 0.0),
        "requires_human": result.get("requires_human", classification == "requires_escalation"),
        "reason": result.get("reason", "Response routed by the support agent."),
        "clarification_question": result.get("clarification_question"),
    }


class OrbitDeskHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_POST(self):
        if self.path != "/api/ask":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            question = str(payload.get("question", "")).strip()
            if not question:
                raise ValueError("Enter a support question before sending.")

            # Delay heavyweight model loading until the first real question.
            from graph import app
            result = app.invoke({"question": question, "retry_count": 0})
            self._json_response(HTTPStatus.OK, format_terminal_response(result))
        except ValueError as error:
            self._json_response(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception as error:
            print(f"Agent error: {error}")
            self._json_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The support agent could not complete that request. Check the terminal for details and try again."})

    def _json_response(self, status: HTTPStatus, body: dict):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        print(f"[Web] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), OrbitDeskHandler)
    print("OrbitDesk Support Console running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
