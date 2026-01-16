echo " Starting Crop Disease Detection Project..."

# Function to check if a process is running
check_process() {
    if pgrep -f "$1" > /dev/null; then
        echo "$2 is running"
        return 0
    else
        echo "$2 is not running"
        return 1
    fi
}

# Function to kill existing processes
cleanup() {
    echo " Cleaning up existing processes..."
    pkill -f "python.*server.py" 2>/dev/null
    pkill -f "python.*http.server" 2>/dev/null
    sleep 2
}

# Cleanup any existing processes
cleanup

# Activate virtual environment and start backend
echo "Starting Backend API Server..."
source .venv/bin/activate
cd backend

# Check if model files exist
if [ ! -f "../model/saved_models/best_model.pth" ] && [ ! -f "saved_models/best_model.pth" ]; then
    echo "Warning: Model file not found. Please ensure model files are in the correct location."
fi

# Start FastAPI server
python server.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start frontend server
echo "Starting Frontend Server..."
cd frontend
python -m http.server 8080 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for servers to start
echo "Waiting for servers to start..."
sleep 5

# Check if servers are running
echo ""
echo "Server Status:"
echo "=================="

if check_process "server.py" "Backend API Server (port 8000)"; then
    echo "Backend URL: http://localhost:8000"
    echo "Health Check: http://localhost:8000/health"
fi

if check_process "http.server.*8080" "Frontend Server (port 8080)"; then
    echo "Frontend URL: http://localhost:8080"
fi

echo ""
echo "Access the application at: http://localhost:8080"
echo ""
echo "Logs:"
echo "   Backend: backend.log"
echo "   Frontend: frontend.log"
echo ""
echo "To stop servers, run: ./stop_servers.sh"
echo ""
echo "Project is ready!"
