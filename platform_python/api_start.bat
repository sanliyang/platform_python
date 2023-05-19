cd ./venv/Scripts
call .\activate.bat
cd ../../front_desk
set PYTHONPATH=D:\\platform_python\\platform_python
uvicorn root.api_root:app --host="127.0.0.1" --port="4800" --reload