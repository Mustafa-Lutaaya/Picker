create:
	@python -m venv picker

act:
	@powershell -ExecutionPolicy Bypass -File ./picker/Scripts/Activate.ps1

install:
	@picker/Scripts/pip install -r requirements.txt
	@picker/Scripts/python.exe -m pip install --upgrade pip

freeze:
	@.\picker\Scripts\python.exe -m pip freeze > requirements.txt

start:
	@uvicorn app.main:app --reload --port 9010