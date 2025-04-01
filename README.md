**CheckMate-Automated-Bank-Check-Processor**

![Screenshot 2025-03-07 134906](https://github.com/user-attachments/assets/d6bc8bc1-28c2-4f1b-9666-8bb2cdd8e9e9)

CheckMate is an automated bank check processing system designed to extract and process cheque details efficiently. It is an AI-powered application that automates the processing of bank cheques using Python, Streamlit, MySQL, and Google Gemini API. It extracts cheque details, stores them in a database, and provides analytics and export options.This project was developed by our team, where I focused on backend integration, database management, and overall system architecture.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Clone the Repository](#clone-the-repository)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Set Up Environment Variables](#set-up-environment-variables)
  - [Set Up MySQL Database](#set-up-mysql-database)
  - [Run the Application](#run-the-application)
  - [Navigating the Application](#navigating-the-application)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## **Features**

- 📤 Upload Cheques: Supports cheque images (JPG, PNG) and PDFs.

- 🤖 AI-Powered Extraction: Uses Google Gemini API for data extraction.

- 🏦 Database Integration: Saves cheque details into MySQL.

- 📊 Analytics Dashboard: Provides statistics and visualizations.

- 📥 Data Export: Download cheque data as CSV, JSON, or Excel.

## Prerequisites
Before running the project, ensure you have the following installed:

- **Python 3.10 or higher**
- **MySQL (local or cloud-based)**
- **Poppler (for pdf processing)**
- **Git (for cloning the repository)**
- **Google Cloud API Key (for Gemini)**

## Setup Instructions
### Clone the Repository
Open a terminal or command prompt and run the following command:

```sh
git clone https://github.com/your-username/checkmate.git
cd checkmate
```

### Create a Virtual Environment
Create a virtual environment to isolate project dependencies:

```sh
python -m venv venv
```

Activate the virtual environment:

- On **Windows**:
  ```sh
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```sh
  source venv/bin/activate
  ```

### Install Dependencies
Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the root directory of the project and add the following environment variables:

```sh
GEMINI_API_KEY=your_google_gemini_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=chequedb
```

Replace placeholders with actual credentials.


### Set Up MySQL Database
Ensure MySQL is running and execute the SQL script to create required tables:

```sql
CREATE DATABASE chequedb;
```

```sql
CREATE TABLE cheques (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payee_name VARCHAR(255),
    amount DECIMAL(10,2),
    bank VARCHAR(255),
    branch_name VARCHAR(255),
    cheque_number VARCHAR(50),
    ifsc_code VARCHAR(20),
    micr_code VARCHAR(20),
    cheque_date DATE,
    account_number VARCHAR(50),
    signature_verified BOOLEAN
);
```

### Run the Application
Start the Streamlit application:

```sh
streamlit run main.py
```
This will launch the CheckMate UI in your browser.

Open your browser and navigate to [http://localhost:8501](http://localhost:8501) to use the application.

### **Navigating the Application**

- 🏠 Home: Overview of the application.

- 📤 Upload & Process: Upload cheque images or PDFs.

- 📄 Cheque Details: View stored cheque data.

- 📊 Analytics: Visualize cheque statistics.

- 📥 Export Data: Download cheque data in various formats.

## Project Structure
```
checkmate/
├── .config/
│   └── settings.py
├── database/
|   └── schema.sql
├── processed/
├── uploads/
├── utils/
│   ├── 1 api_client.py
│   ├── 2 db_operations.py
│   ├── 3 image_processing.py
│   └── 4 text_processing.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txtmain.py
```

## Troubleshooting

1️⃣ MySQL Connection Issues

Ensure MySQL is running and credentials in .env are correct.

Check if the chequedb database exists.

Run mysql -u root -p to access MySQL manually.

2️⃣ API Errors

Verify GEMINI_API_KEY is correct and active.

Ensure you have access to Google Gemini API in Google Cloud.

3️⃣ Missing Dependencies

Run pip install -r requirements.txt again.

Ensure you are using Python 3.10+.

## Contributing

**Contributions are welcome! Follow these steps:**

1. **Fork** the repository.
2. Create a new branch: `git checkout -b feature/YourFeatureName`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeatureName`.
5. Open a **pull request**.

Feel free to submit pull requests or open issues on GitHub to improve the application.

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Acknowledgments
- **Google Gemini API** for text extraction and entity recognition.
- **Streamlit** for the web framework.
- **Tesseract OCR** for optical character recognition.
- **MySQL** for database management.

**Happy Processing! 🚀🏦**
