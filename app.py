from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import json
import os
from datetime import datetime
import uuid
import logging

app = Flask(__name__)
# Enable CORS with specific settings for PowerApps integration
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": "*"}})

# Add response headers for PowerApps compatibility
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Helper function to create standardized API responses for PowerApps
def api_response(data=None, message="Success", success=True, status_code=200):
    """Create a standardized API response format for PowerApps"""
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'onur.vizja@gmail.com'
app.config['MAIL_PASSWORD'] = 'ytrk favy lskp vmao'
app.config['MAIL_DEFAULT_SENDER'] = 'onur.vizja@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Display API documentation"""
    return '''
    <html>
        <head>
            <title>AI-Powered Customer Support System API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                h2 { color: #444; margin-top: 30px; }
                code { background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
                .endpoint { margin-bottom: 20px; border-left: 3px solid #2196F3; padding-left: 15px; }
                .method { font-weight: bold; color: #2196F3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AI-Powered Customer Support System API</h1>
                <p>This is the backend API for the AI-Powered Customer Support System. Below are the available endpoints:</p>
                
                <h2>Ticket Endpoints</h2>
                
                <div class="endpoint">
                    <p><span class="method">GET</span> /api/tickets</p>
                    <p>Get all tickets or filter by user/status</p>
                    <p>Query parameters: user, status, role</p>
                </div>
                
                <div class="endpoint">
                    <p><span class="method">POST</span> /api/tickets</p>
                    <p>Create a new support ticket</p>
                    <pre>{
  "title": "Cannot login",
  "description": "I forgot my password",
  "customer_email": "customer@example.com"
}</pre>
                </div>
                
                <div class="endpoint">
                    <p><span class="method">GET</span> /api/tickets/&lt;ticket_id&gt;</p>
                    <p>Get a specific ticket by ID</p>
                </div>
                
                <div class="endpoint">
                    <p><span class="method">PUT</span> /api/tickets/&lt;ticket_id&gt;</p>
                    <p>Update an existing ticket</p>
                </div>
                
                <div class="endpoint">
                    <p><span class="method">POST</span> /api/tickets/&lt;ticket_id&gt;/assign</p>
                    <p>Assign a ticket to an agent</p>
                    <pre>{
  "agent_email": "agent@example.com",
  "user": "admin@example.com"
}</pre>
                </div>
                
                <div class="endpoint">
                    <p><span class="method">POST</span> /api/tickets/&lt;ticket_id&gt;/resolve</p>
                    <p>Resolve a ticket</p>
                    <pre>{
  "resolution": "Provided instructions to reset password",
  "user": "agent@example.com"
}</pre>
                </div>
                
                <h2>Statistics Endpoint</h2>
                
                <div class="endpoint">
                    <p><span class="method">GET</span> /api/stats</p>
                    <p>Get ticket statistics for admin dashboard</p>
                </div>
                
                <h2>Test the API</h2>
                <p>You can test the API functionality by running the test script:</p>
                <pre>python test_api.py</pre>
            </div>
        </body>
    </html>
    '''

# In-memory database for demonstration purposes
# In a real application, you would use a proper database
tickets = []

# Sample ticket statuses
STATUS_NEW = "new"
STATUS_AI_RESPONDED = "ai_responded"
STATUS_ASSIGNED = "assigned"
STATUS_RESOLVED = "resolved"

# Sample user roles
ROLE_CUSTOMER = "customer"
ROLE_AGENT = "agent"
ROLE_ADMIN = "admin"

# Sample mock users (in a real app, this would be in a database with proper authentication)
users = {
    "customer@example.com": {"role": ROLE_CUSTOMER, "name": "John Customer"},
    "onur.vizja@gmail.com": {"role": ROLE_AGENT, "name": "Onur Oksuz"},
    "onur.vizja@gmail.com": {"role": ROLE_ADMIN, "name": "Admin User"}
}

# Load tickets from file if it exists (for persistence between server restarts)
def load_tickets():
    global tickets
    try:
        if os.path.exists('tickets.json'):
            with open('tickets.json', 'r') as f:
                tickets = json.load(f)
    except Exception as e:
        logger.error(f"Error loading tickets: {e}")

# Save tickets to file
def save_tickets():
    try:
        with open('tickets.json', 'w') as f:
            json.dump(tickets, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving tickets: {e}")
        
# Send email notification
def send_email_notification(recipient, subject, body, html_body):
    """Send email notification to the specified recipient"""
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body,
            html=html_body
        )
        mail.send(msg)
        logger.info(f"Email notification sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
        
# Notify customer about ticket creation
def notify_ticket_created(ticket):
    """Send notification to customer when ticket is created"""
    subject = f"Ticket Created: {ticket['title']}"
    
    # Plain text version
    body = f"""Dear Customer,

Thank you for contacting our support team. Your ticket has been created successfully.

Ticket ID: {ticket['id']}
Title: {ticket['title']}
Status: {ticket['status']}

We will get back to you as soon as possible.

Best regards,
Support Team"""
    
    # HTML version
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #2196F3;">Support Ticket Created</h2>
        <p>Dear Customer,</p>
        <p>Thank you for contacting our support team. Your ticket has been created successfully.</p>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Ticket ID:</strong> {ticket['id']}</p>
            <p><strong>Title:</strong> {ticket['title']}</p>
            <p><strong>Status:</strong> {ticket['status']}</p>
        </div>
        
        <p>We will get back to you as soon as possible.</p>
        
        <p>Best regards,<br>Support Team</p>
    </div>
    """
    
    return send_email_notification(ticket['customer_email'], subject, body, html_body)
    
# Notify customer about AI response
def notify_ai_response(ticket):
    """Send notification to customer when AI responds to their ticket"""
    subject = f"AI Response to Your Ticket: {ticket['title']}"
    
    # Plain text version
    body = f"""Dear Customer,

Our AI assistant has provided a response to your ticket.

Ticket ID: {ticket['id']}
Title: {ticket['title']}
AI Response: {ticket.get('ai_response', 'No response provided')}

If this resolves your issue, no further action is needed. If you need additional assistance, a support agent will follow up with you.

Best regards,
Support Team"""
    
    # HTML version
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #2196F3;">AI Response to Your Support Ticket</h2>
        <p>Dear Customer,</p>
        <p>Our AI assistant has provided a response to your ticket.</p>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Ticket ID:</strong> {ticket['id']}</p>
            <p><strong>Title:</strong> {ticket['title']}</p>
            <div style="background-color: white; padding: 10px; border-left: 4px solid #2196F3; margin-top: 10px;">
                <p><strong>AI Response:</strong> {ticket.get('ai_response', 'No response provided')}</p>
            </div>
        </div>
        
        <p>If this resolves your issue, no further action is needed. If you need additional assistance, a support agent will follow up with you.</p>
        
        <p>Best regards,<br>Support Team</p>
    </div>
    """
    
    return send_email_notification(ticket['customer_email'], subject, body, html_body)
    
# Notify customer about ticket resolution
def notify_ticket_resolved(ticket):
    """Send notification to customer when their ticket is resolved"""
    subject = f"Ticket Resolved: {ticket['title']}"
    
    # Plain text version
    body = f"""Dear Customer,

Your support ticket has been resolved.

Ticket ID: {ticket['id']}
Title: {ticket['title']}
Resolution: {ticket.get('resolution', 'No resolution details provided')}

If you have any further questions, please don't hesitate to contact us.

Best regards,
Support Team"""
    
    # HTML version
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #4CAF50;">Support Ticket Resolved</h2>
        <p>Dear Customer,</p>
        <p>Your support ticket has been resolved.</p>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Ticket ID:</strong> {ticket['id']}</p>
            <p><strong>Title:</strong> {ticket['title']}</p>
            <div style="background-color: white; padding: 10px; border-left: 4px solid #4CAF50; margin-top: 10px;">
                <p><strong>Resolution:</strong> {ticket.get('resolution', 'No resolution details provided')}</p>
            </div>
        </div>
        
        <p>If you have any further questions, please don't hesitate to contact us.</p>
        
        <p>Best regards,<br>Support Team</p>
    </div>
    """
    
    return send_email_notification(ticket['customer_email'], subject, body, html_body)
    
# Notify agent about ticket assignment
def notify_agent_assignment(ticket):
    """Send notification to agent when a ticket is assigned to them"""
    subject = f"Ticket Assigned: {ticket['title']}"
    
    # Plain text version
    body = f"""Hello,

A new ticket has been assigned to you.

Ticket ID: {ticket['id']}
Title: {ticket['title']}
Customer: {ticket['customer_email']}
Description: {ticket['description']}

Please review and respond to this ticket at your earliest convenience.

Best regards,
Support System"""
    
    # HTML version
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h2 style="color: #FF9800;">New Ticket Assigned</h2>
        <p>Hello,</p>
        <p>A new ticket has been assigned to you.</p>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Ticket ID:</strong> {ticket['id']}</p>
            <p><strong>Title:</strong> {ticket['title']}</p>
            <p><strong>Customer:</strong> {ticket['customer_email']}</p>
            <div style="background-color: white; padding: 10px; border-left: 4px solid #FF9800; margin-top: 10px;">
                <p><strong>Description:</strong> {ticket['description']}</p>
            </div>
        </div>
        
        <p>Please review and respond to this ticket at your earliest convenience.</p>
        
        <p>Best regards,<br>Support System</p>
    </div>
    """
    
    return send_email_notification(ticket['assigned_to'], subject, body, html_body)

# Mock AI response function (in a real app, this would call the ChatGPT API)
def get_ai_response(question):
    """Get response from OpenAI's ChatGPT API using direct HTTP request"""
    try:
        import requests
        import json
        
        # Get OpenAI API key from environment variable
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        # Debug logging
        if openai_api_key:
            logger.info(f"OpenAI API key found. Length: {len(openai_api_key)}, First 5 chars: {openai_api_key[:5]}")
        else:
            logger.warning("OpenAI API key not found in environment variables")
        
        # Check if API key is missing or incomplete
        if not openai_api_key or len(openai_api_key) < 20:
            logger.warning("Using mock AI response as no valid API key was provided")
            # Fall back to mock responses if no API key
            common_responses = {
                "password": "You can reset your password by clicking on 'Forgot Password' on the login screen.",
                "login": "If you're having trouble logging in, please make sure your caps lock is off and try again.",
                "account": "To create a new account, click on 'Sign Up' on our homepage.",
                "hours": "Our support hours are Monday-Friday, 9am-5pm EST."
            }
            
            for keyword, response in common_responses.items():
                if keyword in question.lower():
                    return response
            
            return "I'm sorry, I don't have an automated answer for this question. A support agent will assist you shortly."
        
        # Make a direct HTTP request to the OpenAI API
        logger.info("Making direct HTTP request to OpenAI API...")
        try:
            # API endpoint
            url = "https://api.openai.com/v1/chat/completions"
            
            # Headers
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Request body
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant. Provide concise, accurate answers to customer questions."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            # Make the request
            logger.info(f"Sending request to OpenAI API with question: {question[:50]}...")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse the response
            response_data = response.json()
            logger.info("OpenAI API call successful")
            
            # Extract the AI's response
            ai_response = response_data["choices"][0]["message"]["content"].strip()
            logger.info(f"AI response generated for question: {question[:50]}...")
            return ai_response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error("OpenAI API rate limit exceeded. You need to set up billing in your OpenAI account.")
                return "I'm sorry, the AI service is currently unavailable due to rate limiting. Please set up billing in your OpenAI account or try again later."
            else:
                logger.error(f"HTTP error during OpenAI API request: {e.response.status_code} - {str(e)}")
                return f"I'm sorry, I encountered an error processing your question. A support agent will assist you shortly. Error: {e.response.status_code}"
        except Exception as e:
            logger.error(f"Error during OpenAI API HTTP request: {str(e)}")
            return "I'm sorry, I encountered an error processing your question. A support agent will assist you shortly. Error: API request failed."
        
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "I'm sorry, I encountered an error processing your question. A support agent will assist you shortly."

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets or filter by user/status"""
    try:
        user_email = request.args.get('user')
        status = request.args.get('status')
        role = request.args.get('role')
        
        result = tickets
        
        # Filter by user if specified
        if user_email:
            if role == ROLE_CUSTOMER:
                result = [t for t in result if t['customer_email'] == user_email]
            elif role == ROLE_AGENT:
                result = [t for t in result if t.get('assigned_to') == user_email]
        
        # Filter by status if specified
        if status:
            result = [t for t in result if t['status'] == status]
        
        return api_response(data=result, message="Tickets retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving tickets: {e}")
        return api_response(data=None, message=f"Error retrieving tickets: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID"""
    try:
        for ticket in tickets:
            if ticket['id'] == ticket_id:
                return api_response(data=ticket, message="Ticket retrieved successfully")
        
        return api_response(data=None, message="Ticket not found", success=False, status_code=404)
    except Exception as e:
        logger.error(f"Error retrieving ticket {ticket_id}: {e}")
        return api_response(data=None, message=f"Error retrieving ticket: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    try:
        data = request.json
        
        # Validate required fields
        if not data or not all(k in data for k in ['title', 'description', 'customer_email']):
            return api_response(data=None, message="Missing required fields", success=False, status_code=400)
        
        # Create new ticket
        ticket = {
            'id': str(uuid.uuid4()),
            'title': data['title'],
            'description': data['description'],
            'customer_email': data['customer_email'],
            'status': STATUS_NEW,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add ticket to database
        tickets.append(ticket)
        save_tickets()
        
        # Send notification email to customer
        notify_ticket_created(ticket)
        
        # Generate AI response
        try:
            ai_response = get_ai_response(data['description'])
            
            # Update ticket with AI response
            for t in tickets:
                if t['id'] == ticket['id']:
                    t['ai_response'] = ai_response
                    t['status'] = STATUS_AI_RESPONDED
                    t['updated_at'] = datetime.now().isoformat()
                    
                    # Send notification about AI response
                    notify_ai_response(t)
                    break
                    
            save_tickets()
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
        
        return api_response(data=ticket, message="Ticket created successfully", status_code=201)
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        return api_response(data=None, message=f"Error creating ticket: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets/<ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update an existing ticket"""
    try:
        data = request.json
        
        for i, ticket in enumerate(tickets):
            if ticket['id'] == ticket_id:
                # Update allowed fields
                allowed_fields = ['status', 'assigned_to', 'resolution']
                for field in allowed_fields:
                    if field in data:
                        ticket[field] = data[field]
                
                # Add history entry if ticket has history field
                if 'history' in ticket:
                    action = data.get('action', 'Ticket updated')
                    user = data.get('user', 'System')
                    ticket['history'].append({
                        'timestamp': datetime.now().isoformat(),
                        'action': action,
                        'user': user
                    })
                else:
                    # Create history field if it doesn't exist
                    ticket['history'] = [{
                        'timestamp': datetime.now().isoformat(),
                        'action': 'Ticket updated',
                        'user': data.get('user', 'System')
                    }]
                
                ticket['updated_at'] = datetime.now().isoformat()
                tickets[i] = ticket
                save_tickets()
                return api_response(data=ticket, message="Ticket updated successfully")
        
        return api_response(data=None, message="Ticket not found", success=False, status_code=404)
    except Exception as e:
        logger.error(f"Error updating ticket {ticket_id}: {e}")
        return api_response(data=None, message=f"Error updating ticket: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets/<ticket_id>/assign', methods=['POST'])
def assign_ticket(ticket_id):
    """Assign a ticket to an agent"""
    try:
        data = request.json
        
        if 'agent_email' not in data:
            return api_response(data=None, message="Missing required field: agent_email", success=False, status_code=400)
        
        for i, ticket in enumerate(tickets):
            if ticket['id'] == ticket_id:
                ticket['assigned_to'] = data['agent_email']
                ticket['status'] = STATUS_ASSIGNED
                ticket['updated_at'] = datetime.now().isoformat()
                
                # Add history entry if ticket has history field
                if 'history' in ticket:
                    ticket['history'].append({
                        'timestamp': datetime.now().isoformat(),
                        'action': f"Assigned to {data['agent_email']}",
                        'user': data.get('user', 'System')
                    })
                else:
                    # Create history field if it doesn't exist
                    ticket['history'] = [{
                        'timestamp': datetime.now().isoformat(),
                        'action': f"Assigned to {data['agent_email']}",
                        'user': data.get('user', 'System')
                    }]
                
                tickets[i] = ticket
                save_tickets()
                
                # Send email notification to the assigned agent
                try:
                    notify_agent_assignment(ticket)
                except Exception as e:
                    logger.error(f"Error sending assignment notification: {e}")
                    
                return api_response(data=ticket, message="Ticket assigned successfully")
        
        return api_response(data=None, message="Ticket not found", success=False, status_code=404)
    except Exception as e:
        logger.error(f"Error assigning ticket {ticket_id}: {e}")
        return api_response(data=None, message=f"Error assigning ticket: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets/<ticket_id>/resolve', methods=['POST'])
def resolve_ticket(ticket_id):
    """Resolve a ticket"""
    try:
        data = request.json
        
        if 'resolution' not in data:
            return api_response(data=None, message="Missing required field: resolution", success=False, status_code=400)
        
        for i, ticket in enumerate(tickets):
            if ticket['id'] == ticket_id:
                ticket['resolution'] = data['resolution']
                ticket['status'] = STATUS_RESOLVED
                ticket['resolved_at'] = datetime.now().isoformat()
                ticket['updated_at'] = datetime.now().isoformat()
                
                # Add history entry if ticket has history field
                if 'history' in ticket:
                    ticket['history'].append({
                        'timestamp': datetime.now().isoformat(),
                        'action': f"Ticket resolved: {data['resolution']}",
                        'user': data.get('user', 'System')
                    })
                else:
                    # Create history field if it doesn't exist
                    ticket['history'] = [{
                        'timestamp': datetime.now().isoformat(),
                        'action': f"Ticket resolved: {data['resolution']}",
                        'user': data.get('user', 'System')
                    }]
                
                tickets[i] = ticket
                save_tickets()
                
                # Send email notification to the customer about resolution
                try:
                    notify_ticket_resolved(ticket)
                except Exception as e:
                    logger.error(f"Error sending resolution notification: {e}")
                    
                return api_response(data=ticket, message="Ticket resolved successfully")
        
        return api_response(data=None, message="Ticket not found", success=False, status_code=404)
    except Exception as e:
        logger.error(f"Error resolving ticket {ticket_id}: {e}")
        return api_response(data=None, message=f"Error resolving ticket: {str(e)}", success=False, status_code=500)

@app.route('/api/tickets/<ticket_id>/ai_response', methods=['GET'])
def get_ticket_ai_response(ticket_id):
    """Get or generate AI response for a specific ticket"""
    try:
        for ticket in tickets:
            if ticket['id'] == ticket_id:
                # If ticket already has an AI response, return it
                if 'ai_response' in ticket:
                    return api_response(data={"ai_response": ticket['ai_response']}, message="AI response retrieved successfully")
                
                # Otherwise, generate a new response
                ai_response = get_ai_response(ticket['description'])
                if ai_response:
                    ticket['ai_response'] = ai_response
                    ticket['status'] = STATUS_AI_RESPONDED
                    
                    # Add history entry if ticket has history field
                    if 'history' in ticket:
                        ticket['history'].append({
                            'timestamp': datetime.now().isoformat(),
                            'action': 'AI response provided',
                            'user': 'AI System'
                        })
                    else:
                        # Create history field if it doesn't exist
                        ticket['history'] = [{
                            'timestamp': datetime.now().isoformat(),
                            'action': 'AI response provided',
                            'user': 'AI System'
                        }]
                    
                    save_tickets()
                    
                    # Send email notification about AI response
                    try:
                        notify_ai_response(ticket)
                    except Exception as e:
                        logger.error(f"Error sending AI response notification: {e}")
                    
                    return api_response(data={"ai_response": ai_response}, message="AI response generated successfully")
                else:
                    return api_response(data=None, message="Failed to generate AI response", success=False, status_code=500)
        
        return api_response(data=None, message="Ticket not found", success=False, status_code=404)
    except Exception as e:
        logger.error(f"Error getting AI response for ticket {ticket_id}: {e}")
        return api_response(data=None, message=f"Error getting AI response: {str(e)}", success=False, status_code=500)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get ticket statistics for admin dashboard"""
    try:
        total = len(tickets)
        new = len([t for t in tickets if t['status'] == STATUS_NEW])
        ai_responded = len([t for t in tickets if t['status'] == STATUS_AI_RESPONDED])
        assigned = len([t for t in tickets if t['status'] == STATUS_ASSIGNED])
        resolved = len([t for t in tickets if t['status'] == STATUS_RESOLVED])
        
        # Calculate AI resolution rate
        ai_resolution_rate = 0
        if total > 0:
            ai_resolution_rate = (ai_responded / total) * 100
        
        stats_data = {
            'total_tickets': total,
            'new_tickets': new,
            'ai_responded_tickets': ai_responded,
            'assigned_tickets': assigned,
            'resolved_tickets': resolved,
            'ai_resolution_rate': ai_resolution_rate
        }
        
        return api_response(data=stats_data, message="Statistics retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        return api_response(data=None, message=f"Error retrieving statistics: {str(e)}", success=False, status_code=500)

# Load existing tickets on startup
load_tickets()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Check if ngrok should be used for public access
    use_ngrok = os.environ.get('USE_NGROK', 'False').lower() == 'true'
    
    if use_ngrok:
        # Import and initialize ngrok
        from pyngrok import ngrok
        
        # Open a ngrok tunnel to the HTTP server
        public_url = ngrok.connect(port)
        print(f" * ngrok tunnel \'{public_url}\' -> 'http://127.0.0.1:{port}'")
        print(f" * Use this URL in PowerApps: {public_url}/api")
        
        # Update any base URLs to use the ngrok URL
        app.config['BASE_URL'] = public_url
    
    app.run(host='0.0.0.0', port=port, debug=False)
