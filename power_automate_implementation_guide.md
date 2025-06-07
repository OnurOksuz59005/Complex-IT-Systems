# Power Automate Implementation Guide

## Prerequisites
- Microsoft Power Automate account
- Access to Power Platform admin center
- The Flask backend API running on localhost:5000 or deployed to a publicly accessible URL
- PowerApps frontend created according to the PowerApps implementation guide

## Flow 1: New Ticket Creation

### Step-by-Step Implementation

1. **Create a new flow**:
   - Go to [make.powerautomate.com](https://make.powerautomate.com)
   - Click **+ Create** > **Automated cloud flow**
   - Name: "New Ticket Creation Flow"
   - Trigger: "When a new item is created" (PowerApps trigger)
   - Click **Create**

2. **Configure the PowerApps trigger**:
   - Select your PowerApps app from the dropdown

3. **Add an HTTP action to create a ticket**:
   - Click **+ New step** > **HTTP**
   - Method: `POST`
   - URI: `http://localhost:5000/api/tickets` (or your deployed API URL)
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "title": "@{triggerBody()['title']}",
       "description": "@{triggerBody()['description']}",
       "customer_email": "@{triggerBody()['customer_email']}"
     }
     ```

4. **Parse the JSON response**:
   - Click **+ New step** > **Data Operations** > **Parse JSON**
   - Content: `@{body('HTTP')}`
   - Schema: Use the sample payload from your API response

5. **Add a condition to check for AI response**:
   - Click **+ New step** > **Control** > **Condition**
   - Left side: `@{body('Parse_JSON')?['ai_response']}`
   - Operator: `is not equal to`
   - Right side: `null`

6. **If AI response is available (Yes branch)**:
   - Add another HTTP action to update the ticket with AI response
   - Method: `PUT`
   - URI: `http://localhost:5000/api/tickets/@{body('Parse_JSON')?['id']}`
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "status": "ai_responded",
       "ai_response": "@{body('Parse_JSON')?['ai_response']}"
     }
     ```

7. **Add a response to PowerApps**:
   - Click **+ New step** > **Respond to PowerApps**
   - Add dynamic content from previous steps

8. **Save and test the flow**

## Flow 2: Ticket Assignment

### Step-by-Step Implementation

1. **Create a new flow**:
   - Go to [make.powerautomate.com](https://make.powerautomate.com)
   - Click **+ Create** > **Automated cloud flow**
   - Name: "Ticket Assignment Flow"
   - Trigger: "When a button is clicked" (PowerApps trigger)
   - Click **Create**

2. **Configure the PowerApps trigger**:
   - Add input parameters:
     - `ticket_id` (string)
     - `agent_email` (string)
     - `user` (string)

3. **Add an HTTP action to assign the ticket**:
   - Click **+ New step** > **HTTP**
   - Method: `POST`
   - URI: `http://localhost:5000/api/tickets/@{triggerBody()['ticket_id']}/assign`
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "agent_email": "@{triggerBody()['agent_email']}",
       "user": "@{triggerBody()['user']}"
     }
     ```

4. **Parse the JSON response**:
   - Click **+ New step** > **Data Operations** > **Parse JSON**
   - Content: `@{body('HTTP')}`
   - Schema: Use the sample payload from your API response

5. **Add an Office 365 Outlook action to send email notification**:
   - Click **+ New step** > **Office 365 Outlook** > **Send an email (V2)**
   - To: `@{triggerBody()['agent_email']}`
   - Subject: `New ticket assigned: @{body('Parse_JSON')?['title']}`
   - Body: Create a formatted HTML email body with ticket details

6. **Add a response to PowerApps**:
   - Click **+ New step** > **Respond to PowerApps**
   - Add dynamic content from previous steps

7. **Save and test the flow**

## Flow 3: Ticket Resolution

### Step-by-Step Implementation

1. **Create a new flow**:
   - Go to [make.powerautomate.com](https://make.powerautomate.com)
   - Click **+ Create** > **Automated cloud flow**
   - Name: "Ticket Resolution Flow"
   - Trigger: "When a button is clicked" (PowerApps trigger)
   - Click **Create**

2. **Configure the PowerApps trigger**:
   - Add input parameters:
     - `ticket_id` (string)
     - `resolution` (string)
     - `user` (string)

3. **Add an HTTP action to resolve the ticket**:
   - Click **+ New step** > **HTTP**
   - Method: `POST`
   - URI: `http://localhost:5000/api/tickets/@{triggerBody()['ticket_id']}/resolve`
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "resolution": "@{triggerBody()['resolution']}",
       "user": "@{triggerBody()['user']}"
     }
     ```

4. **Parse the JSON response**:
   - Click **+ New step** > **Data Operations** > **Parse JSON**
   - Content: `@{body('HTTP')}`
   - Schema: Use the sample payload from your API response

5. **Add a response to PowerApps**:
   - Click **+ New step** > **Respond to PowerApps**
   - Add dynamic content from previous steps

6. **Save and test the flow**

## Flow 4: Daily Ticket Summary for Admins

### Step-by-Step Implementation

1. **Create a new flow**:
   - Go to [make.powerautomate.com](https://make.powerautomate.com)
   - Click **+ Create** > **Scheduled cloud flow**
   - Name: "Daily Ticket Summary Flow"
   - Trigger: "Recurrence"
   - Frequency: "Day"
   - Time: "5:00 PM"
   - Click **Create**

2. **Add an HTTP action to get ticket statistics**:
   - Click **+ New step** > **HTTP**
   - Method: `GET`
   - URI: `http://localhost:5000/api/stats`

3. **Parse the JSON response**:
   - Click **+ New step** > **Data Operations** > **Parse JSON**
   - Content: `@{body('HTTP')}`
   - Schema: Use the sample payload from your API response

4. **Add an Office 365 Outlook action to send email summary**:
   - Click **+ New step** > **Office 365 Outlook** > **Send an email (V2)**
   - To: `admin@example.com` (replace with actual admin email)
   - Subject: `Daily Ticket Summary - @{formatDateTime(utcNow(), 'yyyy-MM-dd')}`
   - Body: Create a formatted HTML email with statistics from the API response

5. **Save and test the flow**

## Connecting PowerApps to Power Automate

### In PowerApps:

1. **Add the Power Automate connector**:
   - Go to **Data** > **Add data**
   - Search for "Power Automate" and add it

2. **Call the flow from a button**:
   - Select a button in your app
   - In the OnSelect property, add:
     ```
     PowerAutomateFlow.Run(
         "New Ticket Creation Flow",
         {
             title: txtTicketTitle.Text,
             description: txtTicketDescription.Text,
             customer_email: CurrentUser.Email
         }
     )
     ```

3. **Handle the flow response**:
   - Add a notification or navigate to another screen based on the flow response

## Error Handling and Best Practices

1. **Add error handling to all flows**:
   - Use "Configure run after" to handle errors
   - Add "Apply to each" loops with conditions to handle array responses

2. **Use environment variables**:
   - Store the API URL as an environment variable
   - This makes it easier to switch between development and production environments

3. **Implement logging**:
   - Add steps to log flow execution to a SharePoint list or Azure Log Analytics
   - This helps with troubleshooting and auditing

4. **Set up flow alerts**:
   - Configure alerts for flow failures
   - This ensures you're notified when something goes wrong

5. **Use connection references**:
   - Create connection references for all connections
   - This makes it easier to manage connections across environments

## Testing Your Flows

1. **Test each flow individually**:
   - Use the "Test" button in the flow editor
   - Provide sample inputs and verify outputs

2. **Test the integration with PowerApps**:
   - Run your PowerApps app and trigger the flows
   - Verify that data is correctly passed between PowerApps and Power Automate

3. **Test error scenarios**:
   - Simulate errors (e.g., API unavailable)
   - Verify that error handling works as expected

## Deployment

1. **Export your solution**:
   - Go to **Solutions** in Power Platform
   - Export your solution containing all flows

2. **Import to target environment**:
   - Import the solution to your test or production environment
   - Update connection references as needed

3. **Test in the target environment**:
   - Verify that all flows work correctly in the new environment

## Monitoring and Maintenance

1. **Monitor flow runs**:
   - Regularly check flow run history
   - Look for patterns in failures

2. **Update flows as needed**:
   - When API changes occur, update your flows
   - Test thoroughly after any changes

3. **Document your flows**:
   - Create documentation for each flow
   - Include purpose, inputs, outputs, and dependencies
