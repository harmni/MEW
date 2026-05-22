#!/bin/bash
# MEW Startup Script

cd "$(dirname "$0")"

echo ""
echo "=================================================="
echo "  MEW — MY EMPIRE WINS"
echo "=================================================="
echo ""

# Kill any existing instance on port 5001
fuser -k 5001/tcp 2>/dev/null && echo "  Cleared port 5001" || true

# Check dependencies
if ! python3 -c "import flask_socketio, anthropic, requests" 2>/dev/null; then
  echo "  Installing dependencies..."
  pip install flask flask-socketio python-dotenv anthropic requests --quiet
fi

echo "  Starting MEW Agent Server..."
echo ""
echo "  ▸ Open Chrome and go to:  http://localhost:5001"
echo ""
python3 agent_server.py
