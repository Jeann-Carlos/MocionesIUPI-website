
# MocionesIUPI

This repository contains the server-side code for the "MocionesIUPI" application, a voting management system designed for the students of the University of Puerto Rico (UPR). Please note that the client-side code, which includes proprietary components, is not included in this repository.

## Overview

"MocionesIUPI" is a robust application developed to streamline the voting process for students at the University of Puerto Rico. The platform ensures secure, efficient, and transparent handling of student votes on various motions, decisions, and referendums that impact the university community. This repository houses the core server-side functionalities necessary for vote management and processing.

## Key Features

- **Secure User Authentication and Authorization:** Ensures that only authorized students can access the voting system, safeguarding the integrity of the voting process.
- **Motion Proposal Management:** Allows administrators to create, manage, and schedule voting periods for different motions.
- **Vote Tracking and Recording:** Accurately tracks and records student votes, ensuring all votes are counted and stored securely.
- **Real-Time Updates and Notifications:** Provides instant updates and notifications to users during voting periods, enhancing user engagement and participation.
- **Historical Data Storage:** Maintains a comprehensive record of all past votes, enabling the retrieval and analysis of voting history.

## Technologies Used

- **Python:** A versatile and powerful programming language used to build the server-side logic of the application.
- **Flask:** A lightweight and flexible web framework that provides the foundation for the application's web services.
- **SQLAlchemy:** An ORM (Object-Relational Mapping) library used to manage the database operations, ensuring efficient and scalable data handling.
- **Additional Dependencies:** The project relies on other essential libraries and tools, detailed in the `requirements.txt` file.

## Installation and Setup

To set up and run the "MocionesIUPI" application locally, follow these steps:

1. **Clone the Repository:** 
   ```bash
   git clone https://github.com/your-username/mocionesIUPI.git
   ```
2. **Install Dependencies:** 
   Navigate to the project directory and install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:** 
   Set up the necessary environment variables for database connections and authentication:
   ```bash
   export FLASK_APP=app.py
   export DATABASE_URL='your-database-url'
   export SECRET_KEY='your-secret-key'
   ```
4. **Run the Application:** 
   Start the development server:
   ```bash
   flask run
   ```
5. **Access the Application:** 
   Open a web browser and navigate to `http://127.0.0.1:5000` to access the application.

**Note:** The client-side code, which includes proprietary features, is not included in this repository. Full functionality requires access to the complete codebase.

## GitHub Projects

### MocionesIUPI
- **Description:** This project is the server-side implementation for an application managing student votes at the University of Puerto Rico. The application allows students to securely vote on various motions and decisions, with features for managing motion proposals, tracking votes, and providing real-time updates.
- **Technologies Used:** Python, Flask, SQLAlchemy
- **Key Contributions:**
  - Developed and maintained the server-side logic for user authentication, motion management, and vote tracking.
  - Implemented real-time notifications and updates for voting events using Flask.
  - Designed and managed the database schema using SQLAlchemy to ensure efficient data storage and retrieval.
- **Link:** [GitHub Repository](https://github.com/your-username/mocionesIUPI)

## Contributing

Contributions to "MocionesIUPI" are welcome! If you encounter any issues, have suggestions for improvements, or want to contribute new features, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](LICENSE). You are free to modify, distribute, and use the code in accordance with the terms specified in the license.
