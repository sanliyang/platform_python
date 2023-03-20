cd ./venv/Scripts
call .\activate.bat
cd ../../api
set PYTHONPATH=D:\\platform_python\\platform_python
uvicorn root.api_root:app --reload