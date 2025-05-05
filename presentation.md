# Flask Backend API for AI-Powered Customer Support System

## Overview

- Custom coded component using Flask
- RESTful API for ticket management
- Integration with PowerApps frontend
- Connection point for ChatGPT AI responses
- Role-based access for customers, agents, and admins

## Architecture

- Lightweight Flask application
- RESTful API endpoints
- JSON-based data storage (for demo)
- CORS enabled for PowerApps integration
- Mock AI response system (ready for ChatGPT integration)

## API Endpoints

- **GET /api/tickets** - List all tickets with filtering options
- **POST /api/tickets** - Create new support tickets
- **GET /api/tickets/{id}** - View specific ticket details
- **PUT /api/tickets/{id}** - Update ticket information
- **POST /api/tickets/{id}/assign** - Assign ticket to agent
- **POST /api/tickets/{id}/resolve** - Mark ticket as resolved
- **GET /api/stats** - Get ticket statistics for admin dashboard

## Ticket Lifecycle

1. Customer creates ticket via PowerApps
2. API receives ticket and attempts AI resolution
3. If AI can't resolve, ticket awaits agent assignment
4. Admin assigns ticket to appropriate agent
5. Agent resolves ticket and adds resolution notes
6. System maintains complete ticket history

## Integration Points

- **PowerApps**: Sends/receives ticket data via REST API
- **ChatGPT API**: Processes ticket descriptions for automated responses
- **Power Automate**: Can trigger workflows based on API events

## Demo

- Running the Flask server
- Creating a new ticket
- Viewing AI response
- Assigning to agent
- Resolving ticket
- Viewing statistics

## Next Steps

- Database integration (replacing JSON storage)
- Authentication and authorization
- Full ChatGPT API integration
- Email notifications
- Performance optimizations
