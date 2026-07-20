-- =====================================================================
-- Hospital Management System — MySQL Schema
-- Run this once against your MySQL server to create the database.
--   mysql -u root -p < schema.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS hospital_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE hospital_db;

-- ---------------------------------------------------------------------
-- Doctors & Staff
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id       INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    specialization  VARCHAR(100) NOT NULL,
    department      VARCHAR(100) NOT NULL,
    phone           VARCHAR(20),
    email           VARCHAR(120),
    role            VARCHAR(30)  NOT NULL DEFAULT 'Doctor',
    status          ENUM('Active','On Leave','Inactive') NOT NULL DEFAULT 'Active',
    joined_on       DATE NOT NULL,
    consultation_fee DECIMAL(10,2) DEFAULT 0.00,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Patients
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    patient_id      INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    date_of_birth   DATE NOT NULL,
    gender          ENUM('Male','Female','Other') NOT NULL,
    blood_group     VARCHAR(5),
    phone           VARCHAR(20),
    email           VARCHAR(120),
    address         VARCHAR(255),
    emergency_contact VARCHAR(20),
    admission_status ENUM('Outpatient','Admitted','Discharged') NOT NULL DEFAULT 'Outpatient',
    ward            VARCHAR(50),
    registered_on   DATE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Appointments
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id  INT AUTO_INCREMENT PRIMARY KEY,
    patient_id      INT NOT NULL,
    doctor_id       INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason          VARCHAR(255),
    status          ENUM('Scheduled','Completed','Cancelled','No-Show') NOT NULL DEFAULT 'Scheduled',
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id)  REFERENCES doctors(doctor_id)   ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- Billing / Invoices
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bills (
    bill_id         INT AUTO_INCREMENT PRIMARY KEY,
    patient_id      INT NOT NULL,
    appointment_id  INT,
    bill_date       DATE NOT NULL,
    consultation_fee DECIMAL(10,2) DEFAULT 0.00,
    medicine_charges DECIMAL(10,2) DEFAULT 0.00,
    room_charges     DECIMAL(10,2) DEFAULT 0.00,
    other_charges    DECIMAL(10,2) DEFAULT 0.00,
    total_amount     DECIMAL(10,2) GENERATED ALWAYS AS
                     (consultation_fee + medicine_charges + room_charges + other_charges) STORED,
    payment_status   ENUM('Paid','Pending','Partially Paid') NOT NULL DEFAULT 'Pending',
    payment_method   VARCHAR(30),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
);

-- Helpful indexes for common lookups / dashboard queries
CREATE INDEX idx_appt_date ON appointments(appointment_date);
CREATE INDEX idx_bill_date ON bills(bill_date);
CREATE INDEX idx_patient_status ON patients(admission_status);

-- =====================================================================
-- Seed data
-- =====================================================================

-- Doctors
INSERT INTO doctors (first_name, last_name, specialization, department, phone, email, role, status, joined_on, consultation_fee) VALUES
('Priya', 'Sharma', 'Cardiology', 'Cardiology', '+91-9876543210', 'priya.sharma@meridian.in', 'Doctor', 'Active', '2020-03-15', 1500.00),
('Rahul', 'Verma', 'Orthopedics', 'Orthopedics', '+91-9876543211', 'rahul.verma@meridian.in', 'Doctor', 'Active', '2019-07-20', 1200.00),
('Ananya', 'Patel', 'Neurology', 'Neurology', '+91-9876543212', 'ananya.patel@meridian.in', 'Doctor', 'Active', '2021-01-10', 1800.00),
('Vikram', 'Reddy', 'General Medicine', 'General Medicine', '+91-9876543213', 'vikram.reddy@meridian.in', 'Doctor', 'Active', '2018-11-05', 800.00),
('Meera', 'Iyer', 'Pediatrics', 'Pediatrics', '+91-9876543214', 'meera.iyer@meridian.in', 'Doctor', 'On Leave', '2020-09-01', 1000.00),
('Arjun', 'Nair', 'Dermatology', 'Dermatology', '+91-9876543215', 'arjun.nair@meridian.in', 'Doctor', 'Active', '2022-02-14', 900.00),
('Sunita', 'Gupta', 'Oncology', 'Oncology', '+91-9876543216', 'sunita.gupta@meridian.in', 'Doctor', 'Active', '2017-06-30', 2000.00),
('Kavitha', 'Menon', 'ENT', 'ENT', '+91-9876543217', 'kavitha.menon@meridian.in', 'Nurse', 'Active', '2021-05-12', 0.00);

-- Patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_group, phone, email, address, emergency_contact, admission_status, ward, registered_on) VALUES
('Amit', 'Singh', '1985-04-12', 'Male', 'O+', '+91-9000000001', 'amit.singh@email.com', '12 MG Road, Mumbai', '+91-9000000011', 'Outpatient', NULL, '2025-01-10'),
('Priyanka', 'Das', '1990-08-23', 'Female', 'A+', '+91-9000000002', 'priyanka.das@email.com', '45 Park Street, Kolkata', '+91-9000000012', 'Admitted', 'Cardiac Ward', '2025-02-05'),
('Ravi', 'Kumar', '1978-11-30', 'Male', 'B-', '+91-9000000003', NULL, '78 Anna Salai, Chennai', '+91-9000000013', 'Outpatient', NULL, '2025-03-12'),
('Sneha', 'Joshi', '1995-02-14', 'Female', 'AB+', '+91-9000000004', 'sneha.j@email.com', '23 Civil Lines, Delhi', '+91-9000000014', 'Discharged', NULL, '2025-04-01'),
('Mohammed', 'Ali', '1982-07-09', 'Male', 'A-', '+91-9000000005', NULL, '56 Jubilee Hills, Hyderabad', '+91-9000000015', 'Admitted', 'Ortho Ward', '2025-05-18'),
('Lakshmi', 'Rao', '1968-03-25', 'Female', 'O-', '+91-9000000006', 'lakshmi.r@email.com', '89 MG Road, Bangalore', '+91-9000000016', 'Outpatient', NULL, '2025-06-02'),
('Deepak', 'Mishra', '1992-12-01', 'Male', 'B+', '+91-9000000007', NULL, '34 Hazratganj, Lucknow', '+91-9000000017', 'Outpatient', NULL, '2025-06-20'),
('Neha', 'Kapoor', '1988-06-18', 'Female', 'A+', '+91-9000000008', 'neha.k@email.com', '12 Connaught Place, Delhi', '+91-9000000018', 'Admitted', 'Neuro Ward', '2025-07-01'),
('Rajesh', 'Tiwari', '1975-09-05', 'Male', 'O+', '+91-9000000009', NULL, '67 Gomti Nagar, Lucknow', '+91-9000000019', 'Discharged', NULL, '2025-07-05'),
('Pooja', 'Verma', '2000-01-20', 'Female', 'AB-', '+91-9000000010', 'pooja.v@email.com', '90 Aundh Road, Pune', '+91-9000000020', 'Outpatient', NULL, '2025-07-10');

-- Appointments (using relative dates around today)
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status) VALUES
(1, 1, CURDATE(), '10:00', 'Chest pain consultation', 'Scheduled'),
(2, 1, CURDATE(), '11:30', 'Follow-up — post-surgery', 'Scheduled'),
(3, 2, CURDATE(), '14:00', 'Knee pain assessment', 'Scheduled'),
(4, 3, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '09:30', 'Migraine evaluation', 'Completed'),
(5, 2, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '10:00', 'Fracture follow-up', 'Completed'),
(6, 4, CURDATE(), '15:00', 'General health checkup', 'Scheduled'),
(7, 6, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:00', 'Skin rash consultation', 'Scheduled'),
(8, 3, CURDATE(), '11:00', 'Seizure follow-up', 'Scheduled'),
(9, 4, DATE_SUB(CURDATE(), INTERVAL 3 DAY), '13:00', 'Post-discharge review', 'Completed'),
(10, 5, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '10:30', 'Pediatric consultation', 'Scheduled'),
(1, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:00', 'ECG review', 'Scheduled'),
(3, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '11:00', 'X-ray results', 'Scheduled'),
(5, 2, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '14:30', 'Cast removal', 'Scheduled'),
(8, 3, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '10:00', 'MRI review', 'Scheduled'),
(4, 7, DATE_SUB(CURDATE(), INTERVAL 5 DAY), '16:00', 'Oncology screening', 'Cancelled');

-- Bills (spread across 6 months for meaningful revenue charts)
INSERT INTO bills (patient_id, appointment_id, bill_date, consultation_fee, medicine_charges, room_charges, other_charges, payment_status, payment_method) VALUES
(1, 1, DATE_SUB(CURDATE(), INTERVAL 5 MONTH), 1500, 350, 0, 100, 'Paid', 'Card'),
(2, 2, DATE_SUB(CURDATE(), INTERVAL 5 MONTH), 1500, 1200, 5000, 500, 'Paid', 'Insurance'),
(3, 3, DATE_SUB(CURDATE(), INTERVAL 4 MONTH), 1200, 200, 0, 0, 'Paid', 'UPI'),
(4, 4, DATE_SUB(CURDATE(), INTERVAL 4 MONTH), 1800, 800, 0, 200, 'Paid', 'Cash'),
(5, 5, DATE_SUB(CURDATE(), INTERVAL 3 MONTH), 1200, 450, 3000, 300, 'Paid', 'Card'),
(6, 6, DATE_SUB(CURDATE(), INTERVAL 3 MONTH), 800, 0, 0, 0, 'Paid', 'UPI'),
(7, 7, DATE_SUB(CURDATE(), INTERVAL 2 MONTH), 1800, 2500, 8000, 1000, 'Paid', 'Insurance'),
(8, 8, DATE_SUB(CURDATE(), INTERVAL 2 MONTH), 800, 150, 0, 0, 'Paid', 'Cash'),
(9, 9, DATE_SUB(CURDATE(), INTERVAL 1 MONTH), 1500, 3500, 12000, 2000, 'Partially Paid', 'Insurance'),
(10, 10, DATE_SUB(CURDATE(), INTERVAL 1 MONTH), 0, 120, 0, 0, 'Pending', NULL),
(1, NULL, CURDATE(), 1500, 350, 0, 100, 'Paid', 'Card'),
(2, NULL, CURDATE(), 1500, 1200, 5000, 500, 'Partially Paid', 'Insurance'),
(3, NULL, CURDATE(), 1200, 200, 0, 0, 'Pending', NULL),
(4, NULL, DATE_SUB(CURDATE(), INTERVAL 1 WEEK), 1800, 800, 0, 200, 'Paid', 'UPI'),
(5, NULL, DATE_SUB(CURDATE(), INTERVAL 2 WEEK), 1200, 450, 3000, 300, 'Paid', 'Cash');
