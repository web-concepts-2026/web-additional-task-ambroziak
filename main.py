import socket
import json
import os

def parse_request(text: str) -> dict:
    '''Function that parses text into header'''

    header, _, body = text.partition("\r\n\r\n")
    lines = header.split("\r\n")

    if not lines:
        return None

    parts = lines[0].split()
    method = parts[0]

    if (len(parts) > 1):
        full_path = parts[1]
    else:
        full_path = "/"

    path, _, query_text = full_path.partition("?")

    query = {}
    if query_text:
        for item in query_text.split("&"):
            if "=" in item:
                k, v = item.split("=", 1)
                query[k] = v

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            name, value = line.split(":", 1)
            headers[name.strip().lower()] = value.strip()

    return {
        "method": method,
        "path": path,
        "query": query,
        "headers": headers,
        "body": body,
    }

def make_response(status: str, type: str, text: str) -> str:
    payload = text.encode("utf-8")

    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {type}\r\n"
        f"Content-Length: {len(payload)}\r\n"
        f"Connection: close\r\n\r\n"
    )

    return response.encode("utf-8") + payload

def handle_request(request: dict) -> str:
    if request["method"] == "GET" and request["path"] == "/page":
        user_id = request["query"].get("id", "none")
        html = f"<html><body><p>Page number {user_id}</p></body></html>"
        return make_response("200 OK", "text/html; charset=utf-8", html)

    if request["method"] == "GET":
        filepath = "index.html" if request["path"] == "/" else request["path"].lstrip("/")

        if os.path.isfile(filepath):
            if filepath.endswith('html'):
                content_type = "text/html; charset=utf-8"
            elif filepath.endswith('.css'):
                content_type = "text/css"
            elif filepath.endswith('.js'):
                content_type = "application/javascript"
            else:
                content_type = "text/plain"

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return make_response("200 OK", content_type, f.read())
        return make_response("404 Not Found", "text/html", "<p>File Not Found</p>")

    if request["method"] == "POST":
        if "application/json" in request["headers"].get("content-type", ""):
            try:
                data = json.loads(request["body"]) if request["body"] else {}
                reply = json.dumps({"status": "received", "data": data})
                return make_response("200 OK", "application/json", reply)
            except json.JSONDecodeError:
                return make_response("400 Bad Request", "application/json", '{"error": "Invalid JSON"}')
        return make_response("400 Bad Request", "text/plain", "Expected application/json")
    return make_response("501 Not Implemented", "text/plain", "Method not supported")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 8080))
server.listen(5)

print("Server running at http://localhost:8080")

while True:
    client, _ = server.accept()
    raw = client.recv(4096).decode("utf-8", errors="ignore")
    if raw:
        request = parse_request(raw)
        if request:
            client.sendall(handle_request(request=request))
    client.close()