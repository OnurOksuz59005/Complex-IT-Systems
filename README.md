# AI-Powered Customer Support System

A comprehensive customer support solution that combines Microsoft PowerApps, Power Automate, Flask backend API, and ChatGPT AI integration to streamline ticket management and customer service operations.

## System Architecture

This project consists of three main components:

1. **Flask Backend API**: RESTful API for ticket management with ChatGPT integration
2. **PowerApps Frontend**: User interface for customers, agents, and administrators
3. **Power Automate Flows**: Automation workflows connecting the frontend and backend

## Features

- **Ticket Management**: Create, view, assign, and resolve support tickets
- **AI-Powered Responses**: Automatic responses to common questions using ChatGPT
- **Role-Based Access**: Different interfaces for customers, support agents, and administrators
- **Email Notifications**: Automated email alerts for ticket events
- **Analytics Dashboard**: Statistics and insights for administrators

## Components

### 1. Flask Backend API

#### Features
- RESTful API for ticket management
- Real ChatGPT API integration for automated responses
- Email notification system using Flask-Mail
- Role-based access control (Customer, Support Agent, Admin)
- Ticket lifecycle management (creation, assignment, resolution)
- Basic statistics for admin dashboard

#### API Endpoints

**Tickets**
- `GET /api/tickets` - Get all tickets (with optional filtering)
- `GET /api/tickets/<ticket_id>` - Get a specific ticket
- `POST /api/tickets` - Create a new ticket
- `PUT /api/tickets/<ticket_id>` - Update a ticket
- `POST /api/tickets/<ticket_id>/assign` - Assign a ticket to an agent
- `POST /api/tickets/<ticket_id>/resolve` - Resolve a ticket

**Statistics**
- `GET /api/stats` - Get ticket statistics for admin dashboard

### 2. PowerApps Frontend

#### Features
- User-friendly interfaces for different user roles
- Ticket creation and management forms
- Dashboard views for agents and administrators
- Integration with the Flask backend API
- Responsive design for desktop and mobile use

#### Screens
- Login Screen
- Customer Dashboard
- Create Ticket Form
- Ticket Detail View
- Agent Dashboard
- Admin Dashboard

### 3. Power Automate Flows

#### Features
- Automated workflows for ticket lifecycle events
- Email notifications for ticket updates
- Daily summary reports for administrators
- Error handling and logging

#### Flows
- New Ticket Creation Flow
- Ticket Assignment Flow
- Ticket Resolution Flow
- Daily Ticket Summary Flow

## Setup and Installation

### 1. Flask Backend API Setup

1. Clone this repository to your local machine

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables for email notifications (optional):
   - `MAIL_USERNAME`: Your Gmail address
   - `MAIL_PASSWORD`: Your Google App Password (requires 2-Step Verification)
   - `MAIL_DEFAULT_SENDER`: Your Gmail address

4. Set up environment variable for OpenAI API (optional):
   - `OPENAI_API_KEY`: Your OpenAI API key

5. Run the Flask application:
   ```
   python app.py
   ```

6. The API will be available at `http://localhost:5000`

7. Test the API functionality:
   ```
   python test_api.py
   ```

### 2. PowerApps Frontend Setup

1. Go to [make.powerapps.com](https://make.powerapps.com)

2. Create a new canvas app following the instructions in `powerapps_implementation_guide.md`

3. Create a custom connector to the Flask backend API

4. Build the screens and forms as outlined in the implementation guide

5. Publish the app to your organization

### 3. Power Automate Flows Setup

1. Go to [make.powerautomate.com](https://make.powerautomate.com)

2. Create the flows as described in `power_automate_implementation_guide.md`

3. Connect the flows to your PowerApps application

4. Test the end-to-end functionality

## Documentation

This project includes comprehensive documentation for all components:

- `README.md`: Overview of the entire system
- `powerapps_design.md`: Design specifications for the PowerApps frontend
- `powerapps_implementation_guide.md`: Step-by-step guide for implementing the PowerApps frontend
- `power_automate_flows.md`: Design specifications for Power Automate flows
- `power_automate_implementation_guide.md`: Step-by-step guide for implementing Power Automate flows
- `presentation_guide.md`: Guide for presenting the system
- `flask_backend_presentation.md`: Presentation slides for the Flask backend component

## Integration Points

### PowerApps to Flask API

The PowerApps frontend connects to the Flask backend API using a custom connector:

- Base URL: `http://localhost:5000`
- Authentication: None (for demo purposes)
- Endpoints: See API Endpoints section above

### Power Automate to Flask API

Power Automate flows connect to the Flask backend API using HTTP actions:

- Base URL: `http://localhost:5000`
- Authentication: None (for demo purposes)
- Endpoints: See API Endpoints section above

### PowerApps to Power Automate

PowerApps triggers Power Automate flows using the Power Automate connector.

## Future Enhancements

- **Database Integration**: Migrate ticket storage from JSON files to a proper database (e.g., SQLite, PostgreSQL)
- **Authentication and Authorization**: Implement secure user authentication and role-based authorization for API endpoints
- **Enhanced AI Integration**: Expand the ChatGPT integration with more context and specialized prompts
- **Mobile App**: Create a dedicated mobile app for customers and agents
- **Analytics Dashboard**: Implement advanced analytics and reporting features
- **Multilingual Support**: Add support for multiple languages using AI translation
- **Knowledge Base Integration**: Connect to a knowledge base for more comprehensive AI responses
- **Ticket Categorization**: Implement automatic ticket categorization using AI
- **SLA Monitoring**: Add service level agreement monitoring and alerts
