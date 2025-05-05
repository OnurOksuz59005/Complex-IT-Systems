# API Architecture Diagram

```
+-------------------+        +---------------------+        +-------------------+
|                   |        |                     |        |                   |
|  PowerApps        |        |  Flask Backend API  |        |  ChatGPT API      |
|  (Frontend)       | <----> |  (Ticket Handler)   | <----> |  (AI Component)   |
|                   |        |                     |        |                   |
+-------------------+        +---------------------+        +-------------------+
                                      |
                                      |
                                      v
                             +-------------------+
                             |                   |
                             |  JSON Storage     |
                             |  (tickets.json)   |
                             |                   |
                             +-------------------+

```

## API Flow

1. **Ticket Creation**:
   - User submits ticket via PowerApps
   - Request sent to Flask API
   - API attempts AI resolution
   - Ticket stored in JSON file

2. **AI Processing**:
   - API sends ticket description to ChatGPT
   - If AI can resolve, ticket marked as "ai_responded"
   - If not, ticket remains "new"

3. **Agent Assignment**:
   - Admin assigns unresolved tickets to agents
   - API updates ticket status to "assigned"

4. **Ticket Resolution**:
   - Agent resolves ticket
   - API updates ticket status to "resolved"

## Data Models

### Ticket
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "customer_email": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "assigned_to": "string",
  "resolution": "string",
  "ai_response": "string",
  "history": []
}
```

### User Roles
- **Customer**: Submits tickets
- **Agent**: Handles tickets
- **Admin**: Oversees process, assigns tickets
