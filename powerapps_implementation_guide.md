# PowerApps Implementation Guide for AI-Powered Customer Support System

## Prerequisites
- Microsoft PowerApps account with creator license
- Access to Power Platform admin center
- The Flask backend API running on localhost:5000 or deployed to a publicly accessible URL

## Step 1: Create a New Canvas App

1. Go to [make.powerapps.com](https://make.powerapps.com)
2. Sign in with your Microsoft account
3. Click on **+ Create** in the left navigation
4. Select **Canvas app from blank**
5. Enter a name for your app (e.g., "AI Customer Support")
6. Choose format: **Tablet layout** (provides more screen space for the dashboard)
7. Click **Create**

## Step 2: Set Up API Connection

### Create a Custom Connector:

1. Go to [make.powerapps.com](https://make.powerapps.com)
2. In the left navigation, click on **Dataverse** > **Custom connectors**
3. Click **+ New custom connector** in the top menu
4. Enter a name: "Flask Customer Support API"
5. In the **General information** section:
   - Upload an icon (optional)
   - Enter a description: "Connector for AI-Powered Customer Support System"
   - Click **Next**

6. In the **Servers and authentication** section:
   - For **Host**, enter: `localhost:5000` (or your deployed API URL)
   - For **Base URL**, enter: `/api`
   - For **Authentication type**, select: **No authentication** (for demo purposes)
   - Click **Next**

7. In the **Definition** section:

   a. Click **+ New action** to add the first action:
   - For **Summary**, enter: "Get all tickets"
   - For **Operation ID**, enter: `GetTickets`
   - For **Description**, enter: "Retrieves all tickets or filters by user/status"
   - For **Visibility**, select: `important`
   - Click **Next**

   b. In the **Request** section for GetTickets:
   - For **Method**, select: `GET`
   - For **URL**, enter: `/tickets`
   - Click **+ Import parameter** and add the following query parameters:
     - `user` (string, optional)
     - `status` (string, optional)
     - `role` (string, optional)
   - Click **Next**

   c. In the **Response** section:
   - Click **+ Add default response**
   - For **Status code**, enter: `200`
   - For **Body**, paste a sample response from your API
   - Click **Save action**

8. Repeat the process to add the following actions:

   a. **GetTicket**
   - **Summary**: "Get a specific ticket"
   - **Operation ID**: `GetTicket`
   - **Description**: "Retrieves details for a specific ticket"
   - **Method**: `GET`
   - **URL**: `/tickets/{ticket_id}`
   - **Path parameters**: `ticket_id` (string, required)

   b. **CreateTicket**
   - **Summary**: "Create a new ticket"
   - **Operation ID**: `CreateTicket`
   - **Description**: "Creates a new support ticket"
   - **Method**: `POST`
   - **URL**: `/tickets`
   - **Request body**:
     ```json
     {
       "title": "Cannot login",
       "description": "I forgot my password",
       "customer_email": "customer@example.com"
     }
     ```

   c. **AssignTicket**
   - **Summary**: "Assign ticket to agent"
   - **Operation ID**: `AssignTicket`
   - **Description**: "Assigns a ticket to a support agent"
   - **Method**: `POST`
   - **URL**: `/tickets/{ticket_id}/assign`
   - **Path parameters**: `ticket_id` (string, required)
   - **Request body**:
     ```json
     {
       "agent_email": "agent@example.com",
       "user": "admin@example.com"
     }
     ```

   d. **ResolveTicket**
   - **Summary**: "Resolve ticket"
   - **Operation ID**: `ResolveTicket`
   - **Description**: "Marks a ticket as resolved"
   - **Method**: `POST`
   - **URL**: `/tickets/{ticket_id}/resolve`
   - **Path parameters**: `ticket_id` (string, required)
   - **Request body**:
     ```json
     {
       "resolution": "Provided instructions to reset password",
       "user": "agent@example.com"
     }
     ```

   e. **GetStats**
   - **Summary**: "Get ticket statistics"
   - **Operation ID**: `GetStats`
   - **Description**: "Retrieves statistics for admin dashboard"
   - **Method**: `GET`
   - **URL**: `/stats`

9. After adding all actions, click **Create connector**

10. Test the connector:
    - Click on your new connector
    - Go to the **Test** tab
    - Select an operation to test
    - Enter any required parameters
    - Click **Test operation**

## Step 3: Create App Variables and Collections

1. In your PowerApps app, go to the **App** tab in the top ribbon
2. Click on **OnStart** in the property dropdown
3. Add the following formula to initialize app variables:

```
Set(
    CurrentUser,
    {
        Email: "customer@example.com",
        Role: "customer",
        Name: "John Customer"
    }
);

Set(
    AppTheme,
    {
        PrimaryColor: ColorValue("#2196F3"),
        SecondaryColor: ColorValue("#F5F5F5"),
        TextColor: ColorValue("#333333"),
        AccentColor: ColorValue("#FF9800")
    }
);

ClearCollect(
    TicketStatusOptions,
    [
        {Status: "new", Label: "New", Color: ColorValue("#FF9800")},
        {Status: "ai_responded", Label: "AI Responded", Color: ColorValue("#2196F3")},
        {Status: "assigned", Label: "Assigned", Color: ColorValue("#9C27B0")},
        {Status: "resolved", Label: "Resolved", Color: ColorValue("#4CAF50")}
    ]
);

// For demo purposes, we'll add some mock agents
ClearCollect(
    SupportAgents,
    [
        {Email: "agent1@example.com", Name: "Alex Agent"},
        {Email: "agent2@example.com", Name: "Sam Support"},
        {Email: "onur.vizja@gmail.com", Name: "Onur Oksuz"}
    ]
);
```

4. Click **File** > **Save** to save your changes

## Step 4: Create the Login Screen

1. Rename "Screen1" to "LoginScreen" using the tree view
2. Add a header:
   - Insert a **Rectangle** control
   - Set Width = `App.Width`
   - Set Height = `64`
   - Set Fill = `AppTheme.PrimaryColor`
   - Insert a **Label** control inside the rectangle
   - Set Text = `"AI-Powered Customer Support"`
   - Set Color = `White`
   - Set Font Size = `18`
   - Position it appropriately

3. Add login form:
   - Insert a **Rectangle** control
   - Set Width = `400`
   - Set Height = `350`
   - Set X = `(App.Width - Self.Width) / 2`
   - Set Y = `150`
   - Set Fill = `White`
   - Set BorderRadius = `8`

4. Add form controls:
   - Insert a **Label** control inside the rectangle
   - Set Text = `"Login"`
   - Set Font Size = `20`
   - Set X = `(Parent.Width - Self.Width) / 2`
   - Set Y = `20`

   - Insert a **Text input** control for email
   - Rename it to "txtEmail"
   - Set Default = `"customer@example.com"`
   - Set HintText = `"Enter your email"`
   - Position it appropriately

   - Insert a **Dropdown** control for role selection
   - Rename it to "drpRole"
   - Set Items = `["customer", "agent", "admin"]`
   - Set Default = `"customer"`
   - Position it appropriately

   - Insert a **Button** control
   - Set Text = `"Login"`
   - Set Fill = `AppTheme.PrimaryColor`
   - Set Color = `White`
   - Set OnSelect = 
   ```
   Set(
       CurrentUser,
       {
           Email: txtEmail.Text,
           Role: drpRole.Selected.Value,
           Name: If(
               drpRole.Selected.Value = "customer",
               "John Customer",
               If(
                   drpRole.Selected.Value = "agent",
                   "Alex Agent",
                   "Admin User"
               )
           )
       }
   );
   Navigate(HomeScreen, ScreenTransition.Fade)
   ```
   - Position it appropriately

## Step 5: Create the Home Screen

1. Add a new screen and rename it to "HomeScreen"
2. Add a header similar to the login screen
3. Add a welcome message:
   - Insert a **Label** control
   - Set Text = `"Welcome, " & CurrentUser.Name`
   - Set Font Size = `16`
   - Position it appropriately

4. Add navigation based on user role:
   - Insert a **Gallery** control
   - Set Layout = `Horizontal`
   - Set Items = 
   ```
   If(
       CurrentUser.Role = "customer",
       [
           {Icon: Icon.Add, Label: "New Ticket", Screen: NewTicketScreen},
           {Icon: Icon.List, Label: "My Tickets", Screen: CustomerTicketsScreen}
       ],
       If(
           CurrentUser.Role = "agent",
           [
               {Icon: Icon.Inbox, Label: "Assigned Tickets", Screen: AgentTicketsScreen},
               {Icon: Icon.People, Label: "Unassigned Tickets", Screen: UnassignedTicketsScreen}
           ],
           [
               {Icon: Icon.ChartColumn, Label: "Dashboard", Screen: AdminDashboardScreen},
               {Icon: Icon.List, Label: "All Tickets", Screen: AllTicketsScreen}
           ]
       )
   )
   ```
   - Add appropriate controls in the gallery template to display icons and labels
   - Set OnSelect property of the template to `Navigate(ThisItem.Screen, ScreenTransition.Fade)`

## Step 6: Create Customer Screens

### New Ticket Screen
1. Add a new screen and rename it to "NewTicketScreen"
2. Add a header and back button
3. Add form controls:
   - Insert a **Text input** control for ticket title
   - Rename it to "txtTicketTitle"
   - Set HintText = `"Enter ticket title"`

   - Insert a **Text area** control for description
   - Rename it to "txtTicketDescription"
   - Set HintText = `"Describe your issue"`

   - Insert a **Button** control
   - Set Text = `"Submit Ticket"`
   - Set OnSelect = 
   ```
   Set(
       newTicketResponse,
       'Flask Customer Support API'.CreateTicket(
           {
               title: txtTicketTitle.Text,
               description: txtTicketDescription.Text,
               customer_email: CurrentUser.Email
           }
       )
   );
   Notify("Ticket created successfully!");
   Navigate(CustomerTicketsScreen, ScreenTransition.Fade)
   ```

### Customer Tickets Screen
1. Add a new screen and rename it to "CustomerTicketsScreen"
2. Add a header and back button
3. Add refresh button:
   - Insert a **Button** control
   - Set Text = `"Refresh"`
   - Set OnSelect = 
   ```
   ClearCollect(
       CustomerTickets,
       Filter(
           'Flask Customer Support API'.GetTickets().value,
           customer_email = CurrentUser.Email
       )
   )
   ```

4. Add tickets gallery:
   - Insert a **Gallery** control
   - Set Layout = `Vertical`
   - Set Items = `CustomerTickets`
   - Customize the template to show:
     - Ticket ID
     - Title
     - Status (with color coding)
     - Creation date
   - Set OnSelect = `Navigate(TicketDetailScreen, ScreenTransition.Fade, {TicketId: ThisItem.id})`

## Step 7: Create Agent Screens

### Agent Tickets Screen
1. Add a new screen and rename it to "AgentTicketsScreen"
2. Add a header and back button
3. Add refresh button
4. Add tickets gallery:
   - Insert a **Gallery** control
   - Set Layout = `Vertical`
   - Set Items = 
   ```
   Filter(
       'Flask Customer Support API'.GetTickets().value,
       agent_email = CurrentUser.Email
   )
   ```
   - Customize the template similar to the customer tickets gallery
   - Set OnSelect = `Navigate(TicketDetailScreen, ScreenTransition.Fade, {TicketId: ThisItem.id})`

### Unassigned Tickets Screen
1. Add a new screen and rename it to "UnassignedTicketsScreen"
2. Add a header and back button
3. Add refresh button
4. Add tickets gallery:
   - Insert a **Gallery** control
   - Set Layout = `Vertical`
   - Set Items = 
   ```
   Filter(
       'Flask Customer Support API'.GetTickets().value,
       status = "new" || status = "ai_responded"
   )
   ```
   - Customize the template similar to the other ticket galleries
   - Set OnSelect = `Navigate(TicketDetailScreen, ScreenTransition.Fade, {TicketId: ThisItem.id})`

## Step 8: Create Admin Screens

### Admin Dashboard Screen
1. Add a new screen and rename it to "AdminDashboardScreen"
2. Add a header and back button
3. Add refresh button:
   - Insert a **Button** control
   - Set Text = `"Refresh Stats"`
   - Set OnSelect = 
   ```
   Set(
       AdminStats,
       'Flask Customer Support API'.GetStats()
   )
   ```

4. Add statistics cards:
   - Insert multiple **Rectangle** controls to create cards
   - Add labels inside each card to display different statistics
   - Example for one card:
     ```
     Label1.Text = "New Tickets"
     Label2.Text = AdminStats.new_count
     ```

5. Add charts (if available in your PowerApps license):
   - Insert a **Chart** control
   - Configure it to display ticket status distribution

## Step 9: Create Ticket Detail Screen

1. Add a new screen and rename it to "TicketDetailScreen"
2. Add a header and back button
3. Add refresh button:
   - Insert a **Button** control
   - Set Text = `"Refresh"`
   - Set OnSelect = 
   ```
   Set(
       CurrentTicket,
       'Flask Customer Support API'.GetTicket(TicketId).value
   )
   ```

4. Add ticket information display:
   - Insert various **Label** controls to show:
     - Ticket ID
     - Title
     - Status
     - Creation date
     - Customer email
     - Description

5. Add ticket history:
   - Insert a **Gallery** control
   - Set Items = `CurrentTicket.history`
   - Customize the template to show:
     - Date
     - Action
     - User

6. Add action buttons based on user role and ticket status:
   - For agents, add "Resolve Ticket" button:
     ```
     Button.Visible = CurrentUser.Role = "agent" && CurrentTicket.status <> "resolved"
     Button.OnSelect = 
     Set(
         resolveResponse,
         'Flask Customer Support API'.ResolveTicket(
             CurrentTicket.id,
             {
                 resolution: txtResolution.Text,
                 user: CurrentUser.Email
             }
         )
     );
     Refresh(CurrentTicket);
     Notify("Ticket resolved successfully!")
     ```

   - For admins, add "Assign Ticket" button:
     ```
     Button.Visible = CurrentUser.Role = "admin" && (CurrentTicket.status = "new" || CurrentTicket.status = "ai_responded")
     Button.OnSelect = 
     Set(
         assignResponse,
         'Flask Customer Support API'.AssignTicket(
             CurrentTicket.id,
             {
                 agent_email: drpAgents.Selected.Value,
                 user: CurrentUser.Email
             }
         )
     );
     Refresh(CurrentTicket);
     Notify("Ticket assigned successfully!")
     ```

## Step 10: Test and Publish

1. Test your app:
   - Click **Play** in the top right corner
   - Test all screens and functionality
   - Verify API connections are working

2. Publish your app:
   - Click **File** > **Save**
   - Click **Publish**
   - Click **Publish this version**

3. Share your app (optional):
   - Click **File** > **Share**
   - Enter email addresses of users you want to share with
   - Set appropriate permissions
   - Click **Share**

## Troubleshooting Common Issues

### API Connection Issues
- Ensure the Flask backend is running and accessible
- Check that the API URL is correct in the custom connector
- Verify that CORS is enabled on the Flask backend

### Data Not Refreshing
- Add a refresh button to manually refresh data
- Use the `OnVisible` property of screens to refresh data when the screen is shown

### Role-Based Access Not Working
- Check that the `CurrentUser.Role` variable is being set correctly
- Verify that conditional visibility formulas are correct

### Form Submission Errors
- Check the request format in the API connector
- Ensure all required fields are being provided
- Add error handling to display meaningful error messages

## Next Steps

1. Integrate with Power Automate flows for additional automation
2. Add error handling and validation
3. Implement proper authentication
4. Add offline capabilities
5. Enhance the UI with custom themes and branding
