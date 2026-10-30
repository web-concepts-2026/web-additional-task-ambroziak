# web-additional-task-ambroziak
Bonus assignment: Basic HTTP server

Core Functionality:
- Listens on a port 8080 and accepts incoming connections
- Parses HTTP requests to extract: method, path, headers, query parameters, and request body

- GET requests: Serves static (e.g., HTML/CSS) files and handle query parameters (e.g., `/page?id=5`)
- POST requests: Parses request body and respond accordingly

Examples:

Getting specific page:
> curl -i "http://localhost:8080/page?id=67"

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 47
Connection: close

<html><body><p>Page number 67</p></body></html>

Getting file:
> curl -i http://localhost:8080/style.css

HTTP/1.1 200 OK
Content-Type: text/css
Content-Length: 64
Connection: close

body {
    background-color: #710971;
}

h1 {
    color: #fff;
}

Submiting data:
> curl -i -X POST http://localhost:8080/submit \        
     -H "Content-Type: application/json" \
     -d '{"username": "Niko", "power": 1031}'

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 67
Connection: close

{"status": "received", "data": {"username": "Niko", "power": 1031}}

Error handling:

> curl -i http://localhost:8080/style123.css    
     
HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: 21
Connection: close

<p>File Not Found</p>%   