from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.CodeBlockProcessor import CodeBlockProcessor

router = APIRouter()

# 定义请求体模型
class ExtractCodeRequest(BaseModel):
    code: str

# 添加提取代码的路由
@router.post("/extract-code")
async def extract_code(request: ExtractCodeRequest):
    try:
        # 获取前端发送的代码内容
        code_content = request.code

        # 调用 CodeBlockProcessor 处理代码，指定输出目录为 scripts
        processor = CodeBlockProcessor(code_content, output_dir="scripts")
        processor.process()

        # 返回成功响应
        return JSONResponse({"success": True, "message": "代码已成功提取并保存到目录！"})
    except Exception as e:
        # 返回失败响应
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)