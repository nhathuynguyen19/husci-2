@echo off

REM Tạo môi trường ảo nếu chưa có
IF NOT EXIST "venv" (
    python -m venv venv
)

REM Kích hoạt môi trường ảo
call venv\Scripts\activate

REM Cài thư viện
pip install -r requirements.txt

REM Khởi chạy server
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
