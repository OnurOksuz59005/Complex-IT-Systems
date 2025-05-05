# AI-Powered Customer Support System - Backend API

This is the Flask backend API component for the AI-Powered Customer Support System. It handles ticket management, integration with the PowerApps frontend, and provides endpoints for the AI chatbot functionality.

## Features

- RESTful API for ticket management
- Integration points for PowerApps frontend
- Mock AI response system (placeholder for ChatGPT API integration)
- Role-based access control (Customer, Support Agent, Admin)
- Ticket lifecycle management (creation, assignment, resolution)
- Basic statistics for admin dashboard

## API Endpoints

### Tickets

- `GET /api/tickets` - Get all tickets (with optional filtering)
- `GET /api/tickets/<ticket_id>` - Get a specific ticket
- `POST /api/tickets` - Create a new ticket
- `PUT /api/tickets/<ticket_id>` - Update a ticket
- `POST /api/tickets/<ticket_id>/assign` - Assign a ticket to an agent
- `POST /api/tickets/<ticket_id>/resolve` - Resolve a ticket

### Statistics

- `GET /api/stats` - Get ticket statistics for admin dashboard

## Setup and Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

3. The API will be available at `http://localhost:5000`

## Integration with PowerApps

The API is designed to be consumed by Microsoft PowerApps. Use the following connection details in your PowerApp:

- Base URL: `http://localhost:5000`
- Authentication: None (for demo purposes)

## Future Enhancements

- Implement proper database storage (SQLite, PostgreSQL, etc.)
- Add authentication and authorization
- Integrate with actual ChatGPT API
- Implement email notifications
- Add unit and integration tests
