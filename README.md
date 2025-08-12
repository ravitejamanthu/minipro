# Breakdown Buddy (Flask)

A simple Flask app for on-road vehicle breakdown assistance with user and mechanic flows.

## Run locally (Windows PowerShell)

```powershell
# create venv and install deps
python -m venv venv
./venv/Scripts/python.exe -m pip install -U pip
./venv/Scripts/python.exe -m pip install -r requirements.txt

# optional: set env vars (or load via your shell)
$env:SECRET_KEY = "dev_key"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "your_password"
$env:MYSQL_DB = "onroadservice"

# run
./venv/Scripts/python.exe app.py
```

## Environment
- Configure MySQL credentials via environment variables.
- Default values are used if not provided.

## Publish to GitHub

```powershell
git init
git add .
git commit -m "Initial commit: Flask app"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```