import os
import uuid
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get('API_URL', 'http://127.0.0.1:8000')

def init_session():
    return str(uuid.uuid4())[:8]

def send_chat(message: str, history: list, session_id: str):
    if not message.strip():
        return "", history, {}, {}
    
    # Gửi tới API FastAPI
    try:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"session_id": session_id, "message": message},
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            reply = data.get("reply", "")
            tool_calls = data.get("tool_calls", [])
            db_changes = data.get("db_changes", {})
        else:
            reply = f"Lỗi từ server: {resp.status_code} - {resp.text}"
            tool_calls = []
            db_changes = {}
    except Exception as e:
        reply = f"Không thể kết nối đến backend ({API_URL}). Hãy đảm bảo FastAPI đang chạy: uvicorn app.api.main:app\nChi tiết lỗi: {e}"
        tool_calls = []
        db_changes = {}

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]
    return "", history, tool_calls, db_changes

def reset_chat(session_id: str):
    try:
        requests.post(f"{API_URL}/reset", timeout=5)
    except Exception:
        pass
    new_sid = init_session()
    return [], new_sid, [], {}, "Đã reset cơ sở dữ liệu và phiên làm việc."

with gr.Blocks(title="TechNest Agent - Bảng Soi Bên Trong") as demo:
    session_state = gr.State(init_session)
    
    gr.Markdown("# 🤖 TechNest Agent: Trợ Lý Chăm Sóc Khách Hàng")
    gr.Markdown("*Giao diện chat kèm bảng soi bên trong (Inspect Panel) theo dõi Tool Calling và DB State Diff.*")
    
    with gr.Row():
        # Cột trái: Chatbot
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Cuộc trò chuyện", height=500)
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Nhập yêu cầu của bạn (ví dụ: 'Tôi là số 0900000001. Đơn TN-1001 tới đâu rồi?')...",
                    show_label=False,
                    scale=4
                )
                send_btn = gr.Button("Gửi", variant="primary", scale=1)
            with gr.Row():
                reset_btn = gr.Button("🔄 Reset CSDL & Phiên", variant="secondary")
                status_txt = gr.Markdown("")

        # Cột phải: Bảng soi bên trong
        with gr.Column(scale=2):
            gr.Markdown("### 🔍 Bảng soi bên trong (Inspect Panel)")
            tools_box = gr.JSON(label="Công cụ đã gọi ở lượt này (Tool Calls)", value=[])
            db_box = gr.JSON(label="Dữ liệu CSDL thay đổi (DB Changes)", value={})

    # Sự kiện
    send_btn.click(
        send_chat,
        inputs=[msg_input, chatbot, session_state],
        outputs=[msg_input, chatbot, tools_box, db_box]
    )
    msg_input.submit(
        send_chat,
        inputs=[msg_input, chatbot, session_state],
        outputs=[msg_input, chatbot, tools_box, db_box]
    )
    reset_btn.click(
        reset_chat,
        inputs=[session_state],
        outputs=[chatbot, session_state, tools_box, db_box, status_txt]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

