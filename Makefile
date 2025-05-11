# Makefile for stock analysis application

# Backend server commands
backend-start:
	uvicorn src.api:app --reload --port 8000

backend-stop:
	@echo "Stopping backend server..."
	@-pkill -f "uvicorn src.api:app" || echo "Backend server not running"

# Frontend server commands
frontend-start:
	cd frontend && npm run dev -- --host

frontend-stop:
	@echo "Stopping frontend server..."
	@-pkill -f "vite" || echo "Frontend server not running"

# Stop all servers
stop-all: backend-stop frontend-stop
	@echo "All servers stopped"

# Status check for running servers
status:
	@echo "Backend server status:"
	@pgrep -f "uvicorn src.api:app" > /dev/null && echo "Running" || echo "Not running"
	@echo "Frontend server status:"
	@pgrep -f "vite" > /dev/null && echo "Running" || echo "Not running"

# Docker Compose commands
docker-up:
	@echo "Starting services with Docker Compose..."
	docker-compose -f docker-compose.yml up -d --build
	@echo "Services are running. Frontend at http://localhost:8080, Backend at http://localhost:8000"

docker-down:
	@echo "Stopping services with Docker Compose..."
	docker-compose -f docker-compose.yml down
	@echo "Services stopped."

docker-logs:
	@echo "Showing logs for Docker Compose services..."
	docker-compose -f docker-compose.yml logs -f

docker-status:
	@echo "Docker Compose service status:"
	docker-compose -f docker-compose.yml ps
