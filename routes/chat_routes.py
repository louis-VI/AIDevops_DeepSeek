from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from osconfig.config import API_KEY  # 引入 API Key
import json  # 用于解析 JSON 数据

router = APIRouter()

# 初始化 OpenAI 客户端
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# 全局变量存储对话历史
chat_history = [
    {"role": "system", "content": "you are a helpful assistant"},
]

# 初始化 Jinja2 模板
templates = Jinja2Templates(directory="templates")

# 首页路由，返回聊天页面
@router.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket 路由，处理实时对话
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 接受 WebSocket 连接
    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()

            # 解析消息
            try:
                message = json.loads(data)  # 将消息解析为 JSON 对象
            except json.JSONDecodeError:
                # 如果消息不是 JSON 格式，按普通文本处理
                message = {"type": "user_input", "content": data}

            # 处理不同类型的消息
            if message["type"] == "set_role":
                # 更新 system 角色内容
                chat_history[0] = {"role": "system", "content": message["content"]}
                await websocket.send_text(f"角色已更新为: {message['content']}")
            elif message["type"] == "user_input":
                # 将用户输入添加到对话历史中
                chat_history.append({"role": "user", "content": message["content"]})

                # 调用 OpenAI API 获取模型回复
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=chat_history,
                    stream=False
                )

                # 获取模型回复内容
                assistant_reply = response.choices[0].message.content

                # 将模型回复添加到对话历史中
                chat_history.append({"role": "assistant", "content": assistant_reply})

                # 将模型回复发送给客户端
                await websocket.send_text(assistant_reply)
    except WebSocketDisconnect:
        # 处理客户端断开连接
        print("Client disconnected")