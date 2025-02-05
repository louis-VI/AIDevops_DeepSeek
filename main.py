from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import chat_router, code_router, download_router  # 从 routes 包中引入路由

# 初始化 FastAPI 应用
app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含路由
app.include_router(chat_router)
app.include_router(code_router, prefix="/code")
app.include_router(download_router, prefix="/download")

# 启动 FastAPI 应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)