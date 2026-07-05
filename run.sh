#!/usr/bin/env bash
set -e
kill $(lsof -t -i:8000) 2>/dev/null || true
kill $(lsof -t -i:5173) 2>/dev/null || true

cd "$(dirname "$0")/backend"
pip install -q -r requirements.txt 2>/dev/null
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd "$(dirname "$0")/frontend"
echo "Open http://localhost:5173 in your browser"
python3 -m http.server 5173 &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
