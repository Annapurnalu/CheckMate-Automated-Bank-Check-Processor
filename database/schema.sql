CREATE DATABASE chequedb;

CREATE TABLE cheques (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payee_name VARCHAR(255),
    amount DECIMAL(10,2),
    bank VARCHAR(255),
    branch_name VARCHAR(255),
    cheque_number VARCHAR(50) UNIQUE,
    ifsc_code VARCHAR(20),
    micr_code VARCHAR(20),
    cheque_date DATE,
    account_number VARCHAR(50),
    signature_verified ENUM('Yes', 'No')
);
