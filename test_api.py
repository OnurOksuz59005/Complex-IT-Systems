import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def print_response(response):
    """Print the response in a formatted way"""
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 50)

def test_create_ticket():
    """Test creating a new ticket"""
    print("\n1. Creating a new ticket...")
    data = {
        "title": "Cannot login to my account",
        "description": "I forgot my password and can't login. How can I reset it?",
        "customer_email": "customer@example.com"
    }
    response = requests.post(f"{BASE_URL}/tickets", json=data)
    print_response(response)
    return response.json()["data"]["id"]

def test_get_tickets():
    """Test getting all tickets"""
    print("\n2. Getting all tickets...")
    response = requests.get(f"{BASE_URL}/tickets")
    print_response(response)

def test_get_ticket(ticket_id):
    """Test getting a specific ticket"""
    print(f"\n3. Getting ticket with ID: {ticket_id}")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    print_response(response)

def test_assign_ticket(ticket_id):
    """Test assigning a ticket to an agent"""
    print(f"\n4. Assigning ticket {ticket_id} to an agent...")
    data = {
        "agent_email": "agent@example.com",
        "user": "admin@example.com"
    }
    response = requests.post(f"{BASE_URL}/tickets/{ticket_id}/assign", json=data)
    print_response(response)

def test_resolve_ticket(ticket_id):
    """Test resolving a ticket"""
    print(f"\n5. Resolving ticket {ticket_id}...")
    data = {
        "resolution": "Provided instructions on how to reset password",
        "user": "agent@example.com"
    }
    response = requests.post(f"{BASE_URL}/tickets/{ticket_id}/resolve", json=data)
    print_response(response)

def test_get_stats():
    """Test getting ticket statistics"""
    print("\n6. Getting ticket statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)

def run_all_tests():
    """Run all tests in sequence"""
    print("\n===== TESTING API FUNCTIONALITY =====\n")
    
    # Create a ticket and get its ID
    ticket_id = test_create_ticket()
    
    # Get all tickets
    test_get_tickets()
    
    # Get the specific ticket
    test_get_ticket(ticket_id)
    
    # Assign the ticket to an agent
    test_assign_ticket(ticket_id)
    
    # Resolve the ticket
    test_resolve_ticket(ticket_id)
    
    # Get ticket statistics
    test_get_stats()
    
    print("\n===== ALL TESTS COMPLETED =====\n")

if __name__ == "__main__":
    run_all_tests()
