# Banking Intelligence Agent

This project implements a **Banking Intelligence Agent** that leverages LangGraph to process user queries, retrieve relevant information from a mock database, and interact with policies and tools to provide actionable insights.

## Features

- **Query Processing**: Use LangChain to understand and process user queries.
- **Policy Interaction**: Retrieves and interacts with banking policies.
- **Mock Database Integration**: Simulates database interactions for query responses.
- **Modular Tools**: Includes tools for accounts, transactions, fraud alerts, and more.
- **Error Handling**: Robust error-handling mechanisms for seamless operation.

## Project Structure

```plaintext
.
├── bank.db                   # SQLite database file
├── banking-policies.md       # Banking policies documentation
├── main.py                   # Entry point for the application
├── requirements.txt          # Python dependencies
└── src                       # Source code directory
    ├── config                # Configuration module
    │   ├── __init__.py
    │   └── settings.py       # Configuration settings
    ├── db                    # Database interaction module
    │   ├── __init__.py
    │   └── functions.py      # Functions for database queries
    ├── retrievers            # Data retrieval module
    │   ├── __init__.py
    │   └── vector_store_retriever.py  # Retriever for vector store
    ├── state                 # State management and graph module
    │   ├── __init__.py
    │   ├── assistant.py      # Core assistant logic
    │   ├── error_handling.py # Error handling utilities
    │   └── state_graph.py    # State graph management
    ├── tools                 # Tools for various banking functionalities
    │   ├── __init__.py
    │   ├── accounts.py       # Account-related tools
    │   ├── fraud_alerts.py   # Fraud detection tools
    │   ├── loans.py          # Loan-related tools
    │   ├── payments.py       # Payment-related tools
    │   ├── policy.py         # Banking policy tools
    │   ├── safe.py           # Safety-related tools
    │   ├── sensitive.py      # Sensitive information tools
    │   ├── transactions.py   # Transaction tools
    │   └── user_info.py      # User information tools
    └── utils                 # Utility functions
        ├── __init__.py
        ├── event_printer.py  # Event logging utility
        ├── policy.py         # Policy-related utilities
        └── prompt_templates.py  # Prompt templates for LangChain
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nikavgeros/banking-intelligence-agent.git
   cd banking-intelligence-agent
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Usage

After following the installation steps, run the application using the following command:

```bash
python main.py
```

The Banking Intelligence Agent will start, process sample user queries, and provide responses. Below is a sample output:

### Example Output

#### 1. Initializing the Database

```plaintext
Initializing the banking database...
Database 'bank.db' and tables created successfully.
Mock data inserted successfully.
```

#### 2. Query Examples

1. **Discovering Accounts and Balances**

   **Input**:  
   `Hi there, what accounts do I have with your system?`

   **Output**:

   ```plaintext
   You have the following accounts with our system:

   1. **Checking Account**
      - Account Balance: $1,500.00 USD
      - Created At: 2024-11-24 15:16:17

   2. **Savings Account**
      - Account Balance: $5,000.00 USD
      - Created At: 2024-11-24 15:16:17
   ```

2. **Sending Money**

   **Input**:  
   `Please send $50 to user id 2`

   **Output**:  
   Tool prompt for action approval:

   ```plaintext
   Do you approve of the above actions? Type 'y' to continue; otherwise, explain your requested changes.

   y
   ```

3. **Recurring Payments**

   **Input**:  
   `What recurring payments are currently active for me?`

   **Output**:

   ```plaintext
   You currently have the following active recurring payment:

   - **Monthly Rent**
     - Amount: $1,200.00
     - Due Date: 2024-12-01
   ```

4. **Fraud Alerts**

   **Input**:  
   `I noticed there are some alerts on my account. Can you check if they're resolved?`

   **Output**:

   ```plaintext
   You have an unresolved fraud alert on your account:

   - **Alert ID**: 1
   - **Description**: Suspicious login detected
   - **Alert Date**: 2024-11-24 15:16:17
   - **Resolved**: No

   Would you like me to assist you in resolving this alert?
   ```

   **Follow-up**:  
   `Please resolve all active alerts on my account.`

   **Tool Prompt**:

   ```plaintext
   Do you approve of the above actions? Type 'y' to continue; otherwise, explain your requested changes.

   y
   ```

   **Final Check**:
   `Have the alerts on my account been resolved?`

   **Output**:

   ```plaintext
   Yes, the alerts on your account have been resolved. The previously reported alert for a suspicious login detected has been marked as resolved.
   ```

5. **Loans**

   **Input**:  
   `Can you fetch all the loan details and tell me their current status?`

   **Output**:

   ```plaintext
   You currently have the following loans and their statuses:

   1. **Personal Loan**
      - Loan Amount: $10,000.00
      - Status: Approved
      - Applied At: 2024-11-24 15:16:17

   2. **Mortgage Loan**
      - Loan Amount: $250,000.00
      - Status: Pending
      - Applied At: 2024-11-24 15:16:17
   ```

6. **Banking Policies**

   **Input**:  
   `What is the minimum credit score required to be eligible for a loan?`

   **Output**:

   ```plaintext
   The minimum credit score required to be eligible for a loan is 650.
   ```

   **Input**:  
   `Is there a fee for closing a checking account?`

   **Output**:

   ```plaintext
   There is no specific fee mentioned for closing a checking account as long as the balance is $0 and there are no outstanding overdraft fees at the time of closure.
   ```

7. **Web Retrieval**

   **Input**:  
   `What are the current interest rates for savings accounts offered by major banks?`

   **Output**:

   ```plaintext
   As of November 22, 2024, the best interest rate for high-yield savings accounts requiring a minimum deposit of $10,000 is 5.35%. Savings account interest rates are often influenced by the federal funds rate, meaning banks typically adjust their rates in line with changes to the Fed's rates. Online banks and credit unions usually offer the best yields compared to traditional banks due to their lower overhead costs and efforts to attract new customers.

   For more details, you can visit [Forbes Advisor](https://www.forbes.com/advisor/banking/savings/savings-account-rates-today-11-22-24/) for a comprehensive guide on the best high-yield savings accounts and current rates.
   ```

### Interactive Approvals

When tool actions are invoked (e.g., `send $50` or `resolve alerts`), the system prompts for user approval. Approve by typing `y` or provide alternative instructions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
