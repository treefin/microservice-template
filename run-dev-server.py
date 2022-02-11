#!/usr/bin/env python3
import uvicorn

if __name__ == "__main__":
    uvicorn.run("xxx_service:xxx_service_app", port=2329, workers=1)
