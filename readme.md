# Flask SWIFT Transfer Web App

Welcome to the Flask SWIFT Transfer Web App! This web application is built using Flask, Jinja2 templates, and Bootstrap. It includes features such as user authentication, authorization, customer management, and SWIFT transactions.

## Setup

### Prerequisites

- Python 3.x
- Virtual Environment (venv)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/wende61/swift_transfer.git

2. Navigate to the folder
    
    ```bash
    cd swift_transfer

3. Create and activate a virtual environment:

    you can use the python script or the VS code package

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Mac, use "source venv/bin/activate

### Database Migration

Initialize the database and run migrations:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade 


### Features

    User Authentication: Users can register, log in, and log out.
    Authorization: Role-based access control for users and admin.
    Customer Management: CRUD operations for managing customers.
    SWIFT Transactions: Customers can initiate SWIFT transactions, and admins can approve or reject them.

### Folder Structure
    swift_tansfer/: Contains the main application code.
    templates/: Jinja2 templates for rendering HTML pages.
    static/: Static assets (CSS, JS, images).
    migrations/: Database migration scripts.

### Scripts
    venv/: Virtual environment directory.

## Screenshots

![Screenshot of Welcome Page](https://github.com/wende61/swift_transfer/blob/main/static/images/welcome.png)

![Screenshot of Users](https://github.com/wende61/swift_transfer/blob/main/static/images/users.png)

![Screenshot of Users](https://github.com/wende61/swift_transfer/blob/main/static/images/users.png)

![Screenshot of Users Update](https://github.com/wende61/swift_transfer/blob/main/static/images/update_users.png)

![Screenshot of customers](https://github.com/wende61/swift_transfer/blob/main/static/images/customers.png)

![Screenshot of Add Customer](https://github.com/wende61/swift_transfer/blob/main/static/images/add_customer.png)

![Screenshot of Update Customer](https://github.com/wende61/swift_transfer/blob/main/static/images/update_customer.png)

![Screenshot of Remove Customer](https://github.com/wende61/swift_transfer/blob/main/static/images/delete_customer.png)

![Screenshot of Transfer Approval](https://github.com/wende61/swift_transfer/blob/main/static/images/Transfer_approval.png)

![Screenshot of Admin Transfers](https://github.com/wende61/swift_transfer/blob/main/static/images/admin_transfer_list.png)

![Screenshot of Customer initiate Transfers](https://github.com/wende61/swift_transfer/blob/main/static/images/initiate_transfer_request.png)

![Screenshot of Customer Update Transfers](https://github.com/wende61/swift_transfer/blob/main/static/images/edit_my_transfer.png)


![Screenshot of Password Change](https://github.com/wende61/swift_transfer/blob/main/static/images/change_password.png)