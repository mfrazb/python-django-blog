#!/bin/bash

# Django Development Helper Script
# Usage: ./dev.sh [command]

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if virtual environment is activated
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment not detected. Activate it first:"
        echo "source myvenv/bin/activate"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Django Development Helper Script"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  install     - Install/update dependencies"
    echo "  migrate     - Run database migrations"
    echo "  makemigrations - Create new migrations"
    echo "  runserver   - Start development server"
    echo "  shell       - Open Django shell"
    echo "  test        - Run tests"
    echo "  collectstatic - Collect static files"
    echo "  superuser   - Create superuser"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./dev.sh install"
    echo "  ./dev.sh runserver"
}

# Main script logic
case "$1" in
    "install")
        print_status "Installing/updating dependencies..."
        check_venv
        pip install -r requirements.txt
        print_success "Dependencies installed successfully!"
        ;;

    "migrate")
        print_status "Running database migrations..."
        check_venv
        python manage.py migrate
        print_success "Migrations completed!"
        ;;

    "makemigrations")
        print_status "Creating new migrations..."
        check_venv
        python manage.py makemigrations
        print_success "Migrations created!"
        ;;

    "runserver")
        print_status "Starting Django development server..."
        check_venv
        print_status "Server will be available at: http://127.0.0.1:8000/"
        print_status "Press Ctrl+C to stop the server"
        python manage.py runserver
        ;;

    "shell")
        print_status "Opening Django shell..."
        check_venv
        python manage.py shell
        ;;

    "test")
        print_status "Running tests..."
        check_venv
        python manage.py test
        print_success "Tests completed!"
        ;;

    "collectstatic")
        print_status "Collecting static files..."
        check_venv
        python manage.py collectstatic --noinput
        print_success "Static files collected!"
        ;;

    "superuser")
        print_status "Creating superuser..."
        check_venv
        python manage.py createsuperuser
        print_success "Superuser created!"
        ;;

    "help"|"--help"|"-h"|"")
        show_help
        ;;

    *)
        print_warning "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
