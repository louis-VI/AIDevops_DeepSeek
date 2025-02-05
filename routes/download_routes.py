from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import os

router = APIRouter()

# 定义下载请求体模型
class DownloadRequest(BaseModel):
    url: str
    fileName: str

# 添加下载文件的路由
@router.post("/download")
async def download_file(request: DownloadRequest):
    try:
        # 获取前端发送的 URL 和文件名
        url = request.url
        fileName = request.fileName

        # 设置保存文件的目录（与根目录同级的目录）
        SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'downloads')
        os.makedirs(SAVE_DIR, exist_ok=True)

        # 下载文件内容
        response = requests.get(url)
        response.raise_for_status()

        # 保存文件到指定目录
        filePath = os.path.join(SAVE_DIR, fileName)
        with open(filePath, 'wb') as file:
            file.write(response.content)

        # 返回成功响应
        return JSONResponse({"success": True, "filePath": filePath})
    except Exception as e:
        # 返回失败响应
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)