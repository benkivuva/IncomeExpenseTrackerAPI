# Income & Expenses Tracking API

## Overview

The Income & Expenses Tracking API is a versatile tool designed to simplify budgeting and financial management tasks. Built using Django REST Framework (DRF), this API allows users to record, manage, and analyze income and expenses efficiently. Whether you're an individual looking to track personal finances or a business seeking comprehensive financial management solutions, our API provides the tools you need to stay organized and informed.

## Key Features

- **Authentication:** Secure user authentication ensures data privacy and access control.
- **Expense Management:** Record and categorize expenses, and track spending over time.
- **Income Tracking:** Monitor various income sources and analyze earnings over time.
- **User Statistics:** Detailed statistics provide insights into spending habits, income sources, and financial trends.
- **Comprehensive Documentation:** Clear and concise documentation facilitates easy integration and usage.

## Installation

### Income Expenses API

1. Ensure you have Python 3 installed on your system.
2. Clone the repository:

   ```bash
   git clone https://github.com/benkivuva/IncomeExpenseTrackerAPI
   ```

3. Change directory to the cloned repository:

   ```bash
   cd IncomeExpenseTrackerAPI
   ```

4. Create a virtual environment using `virtualenv`:

   ```bash
   virtualenv venv
   ```

5. Activate the virtual environment:

   - On Unix/Linux/macOS:

   ```bash
   source venv/bin/activate
   ```

   - On Windows:

   ```bash
   source venv\Scripts\activate
   ```

6. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Migrate existing database tables:

   ```bash
   python IncomeExpenseTrackerAPI/manage.py migrate
   ```

8. Run the Django development server:

   ```bash
   python IncomeExpenseTrackerAPI/manage.py runserver
   ```

9. Access the Swagger documentation:

   Once the server is running, you can access the Swagger documentation by navigating to:

   ```
   http://127.0.0.1:8000/swagger/
   ```

   This page provides detailed documentation for all available API endpoints, request formats, and authentication methods.

## Contributing

We welcome contributions from the community! If you have suggestions for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
