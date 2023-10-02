import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8881,
        # log_level=settings.LOG_LEVEL,
        # reload=settings.DEBUG,
    )
