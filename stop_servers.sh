echo "Stopping Crop Disease Detection Project Servers..."


# Kill backend FastAPI server
echo "Stopping Backend Server..."
pkill -f "python.*server.py" 2>/dev/null && echo "Backend server stopped" || echo "Backend server was not running"

# Kill frontend HTTP server  
echo "Stopping Frontend Server..."
pkill -f "python.*http.server" 2>/dev/null && echo "Frontend server stopped" || echo "Frontend server was not running"

# Kill any other related processes
echo "Cleaning up any remaining processes..."
pkill -f "crop.*disease" 2>/dev/null

echo ""
echo "All servers stopped successfully!"
echo "Logs are still available in backend.log and frontend.log"
