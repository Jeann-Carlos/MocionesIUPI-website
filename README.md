MocionesIUPI
This repository contains the server-side code for the "MocionesIUPI" application, a voting management system designed for the students of the University of Puerto Rico (UPR). Please note that the client-side code, which includes proprietary components, is not included in this repository.

Overview
"MocionesIUPI" is a robust application developed to streamline the voting process for students at the University of Puerto Rico. The platform ensures secure, efficient, and transparent handling of student votes on various motions, decisions, and referendums that impact the university community. This repository houses the core server-side functionalities necessary for vote management and processing.

Key Features
Secure User Authentication and Authorization: Ensures that only authorized students can access the voting system, safeguarding the integrity of the voting process.
Motion Proposal Management: Allows administrators to create, manage, and schedule voting periods for different motions.
Vote Tracking and Recording: Accurately tracks and records student votes, ensuring all votes are counted and stored securely.
Real-Time Updates and Notifications: Provides instant updates and notifications to users during voting periods, enhancing user engagement and participation.
Historical Data Storage: Maintains a comprehensive record of all past votes, enabling the retrieval and analysis of voting history.
Technologies Used
Python: A versatile and powerful programming language used to build the server-side logic of the application.
Flask: A lightweight and flexible web framework that provides the foundation for the application's web services.
SQLAlchemy: An ORM (Object-Relational Mapping) library used to manage the database operations, ensuring efficient and scalable data handling.
Additional Dependencies: The project relies on other essential libraries and tools, detailed in the requirements.txt file.
Installation and Setup
To set up and run the "MocionesIUPI" application locally, follow these steps:

Clone the Repository:
bash
Copy code
git clone https://github.com/your-username/mocionesIUPI.git
Install Dependencies:
Navigate to the project directory and install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Configure Environment Variables:
Set up the necessary environment variables for database connections and authentication:
bash
Copy code
export FLASK_APP=app.py
export DATABASE_URL='your-database-url'
export SECRET_KEY='your-secret-key'
Run the Application:
Start the development server:
bash
Copy code
flask run
Access the Application:
Open a web browser and navigate to http://127.0.0.1:5000 to access the application.
Note: The client-side code, which includes proprietary features, is not included in this repository. Full functionality requires access to the complete codebase.

Contributing
Contributions to "MocionesIUPI" are welcome! If you encounter any issues, have suggestions for improvements, or want to contribute new features, please feel free to submit a pull request or open an issue.

License
This project is licensed under the MIT License. You are free to modify, distribute, and use the code in accordance with the terms specified in the license.
