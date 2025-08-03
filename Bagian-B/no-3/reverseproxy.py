from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import httpx, os

load_dotenv()

app = FastAPI(
    title="Reverse Proxy",
    description="Basic Reverse Proxy",
    version="1.0.0"
)

BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL")

client = httpx.AsyncClient(base_url=BACKEND_SERVER_URL, timeout=30.0, verify=False)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def reverse_proxy(request: Request, path: str):
    try:
        method = request.method
        headers = dict(request.headers)
        query_params = request.query_params
        request_body = await request.body()

        headers.pop("host", None)
        headers.pop("content-length", None)
        headers.pop("transfer-encoding", None)
        headers.pop("x-forwarded-for", None)
        client_ip = request.client.host if request.client else "unknown"
        headers["X-Forwarded-For"] = client_ip
        target_url = f"{BACKEND_SERVER_URL}/{path}"
        if query_params:
            target_url += f"?{query_params}"
        print(f"Proxying {method} request to: {target_url}")
        print(f"Headers: {headers}")
        print(f"Body length: {len(request_body)} bytes")
        backend_response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            params=query_params,
            content=request_body,
        )
        response_headers = dict(backend_response.headers)
        response_headers.pop("content-length", None)
        response_headers.pop("transfer-encoding", None)
        return StreamingResponse(
            content=backend_response.aiter_bytes(),
            status_code=backend_response.status_code,
            headers=response_headers,
            media_type=backend_response.headers.get("content-type")
        )
    except httpx.RequestError as exc:
        print(f"HTTPX Request Error: {exc}")
        raise HTTPException(status_code=503, detail=f"Backend server unavailable: {exc}")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail=f"Internal proxy error: {exc}")