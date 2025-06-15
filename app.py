from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import json
import os
from datetime import datetime
import uuid
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for integration with PowerApps

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
    """Get response from OpenAI's ChatGPT API"""
    try:
        import openai
        
        # Get OpenAI API key from environment variable
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        # For local testing, you can uncomment and use this line instead
        # But NEVER commit API keys to version control
        # if not openai_api_key:
        #     openai_api_key = "your-api-key-here"  # Replace with your key for local testing only
        
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
        
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Create a system message to set the context
        system_message = "You are a helpful customer support assistant. Provide concise, accurate answers to customer questions."
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract and return the AI's response
        ai_response = response.choices[0].message.content.strip()
        logger.info(f"AI response generated for question: {question[:50]}...")
        return ai_response
        
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "I'm sorry, I encountered an error processing your question. A support agent will assist you shortly."

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets or filter by user/status"""
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
    
    return jsonify(result)

@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID"""
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            return jsonify(ticket)
    
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'description', 'customer_email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create new ticket
    ticket_id = str(uuid.uuid4())
    new_ticket = {
        'id': ticket_id,
        'title': data['title'],
        'description': data['description'],
        'customer_email': data['customer_email'],
        'status': STATUS_NEW,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'history': [
            {
                'timestamp': datetime.now().isoformat(),
                'action': 'Ticket created',
                'user': data['customer_email']
            }
        ]
    }
    
    # Try to get an AI response
    ai_response = get_ai_response(data['description'])
    if ai_response:
        new_ticket['ai_response'] = ai_response
        new_ticket['status'] = STATUS_AI_RESPONDED
        new_ticket['history'].append({
            'timestamp': datetime.now().isoformat(),
            'action': 'AI response provided',
            'user': 'AI System'
        })
    
    tickets.append(new_ticket)
    save_tickets()
    
    # Send email notifications
    try:
        # Notify customer about ticket creation
        notify_ticket_created(new_ticket)
        
        # If AI responded, send that notification too
        if ai_response:
            notify_ai_response(new_ticket)
    except Exception as e:
        logger.error(f"Error sending email notifications: {e}")
    
    return jsonify(new_ticket), 201

@app.route('/api/tickets/<ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update an existing ticket"""
    data = request.json
    
    for i, ticket in enumerate(tickets):
        if ticket['id'] == ticket_id:
            # Update allowed fields
            allowed_fields = ['status', 'assigned_to', 'resolution']
            for field in allowed_fields:
                if field in data:
                    ticket[field] = data[field]
            
            # Add history entry
            action = data.get('action', 'Ticket updated')
            user = data.get('user', 'System')
            ticket['history'].append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'user': user
            })
            
            ticket['updated_at'] = datetime.now().isoformat()
            tickets[i] = ticket
            save_tickets()
            return jsonify(ticket)
    
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/api/tickets/<ticket_id>/assign', methods=['POST'])
def assign_ticket(ticket_id):
    """Assign a ticket to an agent"""
    data = request.json
    
    if 'agent_email' not in data:
        return jsonify({"error": "Missing required field: agent_email"}), 400
    
    for i, ticket in enumerate(tickets):
        if ticket['id'] == ticket_id:
            ticket['assigned_to'] = data['agent_email']
            ticket['status'] = STATUS_ASSIGNED
            ticket['updated_at'] = datetime.now().isoformat()
            ticket['history'].append({
                'timestamp': datetime.now().isoformat(),
                'action': f"Assigned to {data['agent_email']}",
                'user': data.get('user', 'System')
            })
            
            tickets[i] = ticket
            save_tickets()
            
            # Send email notification to the assigned agent
            try:
                notify_agent_assignment(ticket)
            except Exception as e:
                logger.error(f"Error sending assignment notification: {e}")
                
            return jsonify(ticket)
    
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/api/tickets/<ticket_id>/resolve', methods=['POST'])
def resolve_ticket(ticket_id):
    """Resolve a ticket"""
    data = request.json
    
    if 'resolution' not in data:
        return jsonify({"error": "Missing required field: resolution"}), 400
    
    for i, ticket in enumerate(tickets):
        if ticket['id'] == ticket_id:
            ticket['resolution'] = data['resolution']
            ticket['status'] = STATUS_RESOLVED
            ticket['resolved_at'] = datetime.now().isoformat()
            ticket['updated_at'] = datetime.now().isoformat()
            ticket['history'].append({
                'timestamp': datetime.now().isoformat(),
                'action': f"Ticket resolved: {data['resolution']}",
                'user': data.get('user', 'System')
            })
            
            tickets[i] = ticket
            save_tickets()
            
            # Send email notification to the customer about resolution
            try:
                notify_ticket_resolved(ticket)
            except Exception as e:
                logger.error(f"Error sending resolution notification: {e}")
                
            return jsonify(ticket)
    
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/api/tickets/<ticket_id>/ai_response', methods=['GET'])
def get_ticket_ai_response(ticket_id):
    """Get or generate AI response for a specific ticket"""
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            # If ticket already has an AI response, return it
            if 'ai_response' in ticket:
                return jsonify({"ai_response": ticket['ai_response']})
            
            # Otherwise, generate a new response
            ai_response = get_ai_response(ticket['description'])
            if ai_response:
                ticket['ai_response'] = ai_response
                ticket['status'] = STATUS_AI_RESPONDED
                ticket['history'].append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'AI response provided',
                    'user': 'AI System'
                })
                save_tickets()
                
                # Send email notification about AI response
                try:
                    notify_ai_response(ticket)
                except Exception as e:
                    logger.error(f"Error sending AI response notification: {e}")
                
                return jsonify({"ai_response": ai_response})
            else:
                return jsonify({"error": "Failed to generate AI response"}), 500
    
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get ticket statistics for admin dashboard"""
    total = len(tickets)
    new = len([t for t in tickets if t['status'] == STATUS_NEW])
    ai_responded = len([t for t in tickets if t['status'] == STATUS_AI_RESPONDED])
    assigned = len([t for t in tickets if t['status'] == STATUS_ASSIGNED])
    resolved = len([t for t in tickets if t['status'] == STATUS_RESOLVED])
    
    # Calculate AI resolution rate
    ai_resolution_rate = 0
    if total > 0:
        ai_resolution_rate = (ai_responded / total) * 100
    
    return jsonify({
        'total_tickets': total,
        'new_tickets': new,
        'ai_responded_tickets': ai_responded,
        'assigned_tickets': assigned,
        'resolved_tickets': resolved,
        'ai_resolution_rate': ai_resolution_rate
    })

# Load existing tickets on startup
load_tickets()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
