# Dijidaro

Dijidaro is an open-source platform designed to make learning resources accessible to everyone. It offers a centralized repository of schools revision and lerning materials which will empower students, educators and parents nationwide.

Our mission is to bridge the gap between resources and knowledge sharing. Educators and parents can contribute by uploading valuable teaching resources, fostering an inclusive and supportive environment for education.

## Key Features

 - Access to diverse learning materials from various institions.
 - Free resources for students, educators and parents.
 - Upload function for educators and parents to share teaching materials.
 - Community-driven platform for equal learning opportunities.

## Technology Stack

 - **Backend**: Python (Flask)
 - **Database**: PostgreSQL
 - **Frontend**: React

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

 - [Python 3.8+](https://www.python.org/downloads/)
 - [PostgreSQL](https://www.postgresql.org/download/)
 - [Node.js](https://nodejs.org/) (optional, for additional React-related builds if needed)

### Local Development Setup

**1. Clone the Repository**

`git@github.com:dijidaro/dijidaro.git`
`cd dijidaro`

**2. Set Up a Virtual Environment**

`python3 -m venv venv`
`source venv/bin/activate`

**3. Install Python Dependencies**

`pip install -r requirements.txt`

**4. Set Up PostgreSQL Database**

 - Create a new PostgreSQL database:

    `CREATE DATABSE dijidaro`;

 - Set up a PostgreSQL user with appropriate privileges and note the connection details.

**5. Configure Environment Variables**

Create a `.env` file in the project root and set the database connection URL:

`DATABASE_URL=postgresql://username:password@localhost:5432/dijidaro`;

**6. Initialize the Database**

 `flask db init`
 `flask db migrate -m "Initial migration."`
 `flask db upgrade`

**7. Run the Flask Application**

 `flask run`

 Your app will be available at [http://localhost:5000](http://localhost:5000).

## Contribution Guide

We welcome contributions from the community! To contribute:

 - Fork the repository and create a new branch.
 - Make your changes, then submit a pull request with a clear description.
 - For more details, see [CONTRIBUTING.md](.github/CONTRIBUTING.md).
 
## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE.md) file for details.