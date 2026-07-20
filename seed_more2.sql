-- =====================================================================
-- Batch 2 — even more patients & appointments
--   mysql -u root -p hospital_db < seed_more2.sql
-- =====================================================================

USE hospital_db;

-- More Patients (patient_id 31 onward)
INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_group, phone, email, address, emergency_contact, admission_status, ward, registered_on) VALUES
('Rakesh', 'Pandey', '1980-06-11', 'Male', 'O+', '+91-9000000061', 'rakesh.p@email.com', '19 Aliganj, Lucknow', '+91-9000000081', 'Outpatient', NULL, '2025-06-05'),
('Shreya', 'Mukherjee', '1993-09-02', 'Female', 'A+', '+91-9000000062', 'shreya.m@email.com', '7 Howrah, Kolkata', '+91-9000000082', 'Admitted', 'General Ward', '2025-06-12'),
('Deepak', 'Chawla', '1976-12-19', 'Male', 'B+', '+91-9000000063', NULL, '52 Karol Bagh, Delhi', '+91-9000000083', 'Outpatient', NULL, '2025-06-18'),
('Anita', 'Verma', '1988-03-28', 'Female', 'AB+', '+91-9000000064', 'anita.v@email.com', '31 Gomti Nagar, Lucknow', '+91-9000000084', 'Discharged', NULL, '2025-06-24'),
('Sachin', 'Kulkarni', '1984-07-15', 'Male', 'A-', '+91-9000000065', NULL, '66 Deccan, Pune', '+91-9000000085', 'Admitted', 'Cardiac Ward', '2025-06-30'),
('Neetu', 'Sharma', '1997-11-07', 'Female', 'O-', '+91-9000000066', 'neetu.s@email.com', '24 Vaishali, Ghaziabad', '+91-9000000086', 'Outpatient', NULL, '2025-07-03'),
('Abhishek', 'Roy', '1971-05-23', 'Male', 'B-', '+91-9000000067', NULL, '88 Park Circus, Kolkata', '+91-9000000087', 'Admitted', 'Neuro Ward', '2025-07-07'),
('Priya', 'Nambiar', '1999-08-14', 'Female', 'A+', '+91-9000000068', 'priya.n@email.com', '13 Panampilly, Kochi', '+91-9000000088', 'Outpatient', NULL, '2025-07-10'),
('Vishal', 'Thakur', '1983-02-01', 'Male', 'AB-', '+91-9000000069', NULL, '45 Mall Road, Shimla', '+91-9000000089', 'Discharged', NULL, '2025-07-11'),
('Komal', 'Jain', '1991-10-26', 'Female', 'O+', '+91-9000000070', 'komal.j@email.com', '29 C-Scheme, Jaipur', '+91-9000000090', 'Outpatient', NULL, '2025-07-12'),
('Tarun', 'Reddy', '1986-04-09', 'Male', 'B+', '+91-9000000071', NULL, '58 Gachibowli, Hyderabad', '+91-9000000091', 'Admitted', 'Ortho Ward', '2025-07-13'),
('Aarti', 'Deshpande', '1994-12-30', 'Female', 'A-', '+91-9000000072', 'aarti.d@email.com', '17 Camp, Pune', '+91-9000000092', 'Outpatient', NULL, '2025-07-14'),
('Naveen', 'Kumar', '1979-07-18', 'Male', 'O-', '+91-9000000073', NULL, '73 Jayanagar, Bangalore', '+91-9000000093', 'Outpatient', NULL, '2025-07-15'),
('Sana', 'Ansari', '2000-03-05', 'Female', 'AB+', '+91-9000000074', 'sana.a@email.com', '41 Frazer Town, Bangalore', '+91-9000000094', 'Admitted', 'General Ward', '2025-07-16'),
('Manish', 'Agarwal', '1982-09-22', 'Male', 'A+', '+91-9000000075', NULL, '62 Malviya Nagar, Jaipur', '+91-9000000095', 'Discharged', NULL, '2025-07-17'),
('Ruchi', 'Kapoor', '1995-06-13', 'Female', 'B+', '+91-9000000076', 'ruchi.k@email.com', '8 Greater Kailash, Delhi', '+91-9000000096', 'Outpatient', NULL, '2025-07-18'),
('Yash', 'Patel', '1987-11-01', 'Male', 'O+', '+91-9000000077', NULL, '35 Satellite, Ahmedabad', '+91-9000000097', 'Admitted', 'Cardiac Ward', '2025-07-18'),
('Lata', 'Krishnan', '1990-08-08', 'Female', 'A-', '+91-9000000078', 'lata.k@email.com', '21 Adyar, Chennai', '+91-9000000098', 'Outpatient', NULL, '2025-07-19'),
('Faisal', 'Khan', '1985-02-25', 'Male', 'AB-', '+91-9000000079', NULL, '94 Tolichowki, Hyderabad', '+91-9000000099', 'Outpatient', NULL, '2025-07-19'),
('Snehal', 'Patil', '1998-12-12', 'Female', 'O+', '+91-9000000080', 'snehal.p@email.com', '50 Baner, Pune', '+91-9000000100', 'Discharged', NULL, '2025-07-20'),
('Gopal', 'Iyer', '1973-04-17', 'Male', 'B+', '+91-9000000101', NULL, '11 Mylapore, Chennai', '+91-9000000121', 'Outpatient', NULL, '2025-07-01'),
('Meenakshi', 'Sundaram', '1992-07-29', 'Female', 'A+', '+91-9000000102', 'meenakshi.s@email.com', '39 Anna Nagar, Chennai', '+91-9000000122', 'Admitted', 'Neuro Ward', '2025-07-04'),
('Dinesh', 'Rawat', '1981-10-03', 'Male', 'O-', '+91-9000000103', NULL, '76 Rajpur Road, Dehradun', '+91-9000000123', 'Outpatient', NULL, '2025-07-08'),
('Bhavna', 'Shah', '1996-01-21', 'Female', 'AB+', '+91-9000000104', 'bhavna.s@email.com', '28 Navrangpura, Ahmedabad', '+91-9000000124', 'Outpatient', NULL, '2025-07-11'),
('Rohan', 'Kapoor', '1984-05-06', 'Male', 'A-', '+91-9000000105', NULL, '57 Sector 22, Chandigarh', '+91-9000000125', 'Discharged', NULL, '2025-07-14');

-- More Appointments (patient_id 31-55, doctor_id 1-24)
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status) VALUES
(31, 4, CURDATE(), '09:00', 'Diabetes review', 'Scheduled'),
(32, 10, CURDATE(), '09:45', 'Prenatal scan', 'Scheduled'),
(33, 21, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '10:30', 'Stomach pain', 'Completed'),
(34, 12, CURDATE(), '11:15', 'Cataract consultation', 'Scheduled'),
(35, 1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '13:00', 'Angina evaluation', 'Completed'),
(36, 5, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '10:00', 'Child fever', 'Scheduled'),
(37, 3, CURDATE(), '14:30', 'Epilepsy review', 'Scheduled'),
(38, 6, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:30', 'Eczema treatment', 'Scheduled'),
(39, 7, DATE_SUB(CURDATE(), INTERVAL 3 DAY), '11:00', 'Tumor screening', 'Completed'),
(40, 8, CURDATE(), '15:00', 'Sinus infection', 'Scheduled'),
(41, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '10:15', 'Back pain', 'Scheduled'),
(42, 18, CURDATE(), '12:30', 'Depression consultation', 'Scheduled'),
(43, 4, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '09:15', 'Routine checkup', 'Scheduled'),
(44, 23, DATE_SUB(CURDATE(), INTERVAL 4 DAY), '13:45', 'Kidney function test', 'Completed'),
(45, 24, CURDATE(), '10:45', 'Thyroid review', 'Scheduled'),
(46, 20, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '11:30', 'Eye strain', 'Scheduled'),
(47, 9, DATE_SUB(CURDATE(), INTERVAL 5 DAY), '14:00', 'Heart palpitations', 'Cancelled'),
(48, 3, CURDATE(), '09:00', 'Numbness evaluation', 'Scheduled'),
(49, 19, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '10:30', 'Urology consultation', 'Scheduled'),
(50, 11, DATE_SUB(CURDATE(), INTERVAL 6 DAY), '15:30', 'Joint pain', 'Completed'),
(51, 22, CURDATE(), '11:00', 'Breathing difficulty', 'Scheduled'),
(52, 3, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '09:45', 'Neuro follow-up', 'Scheduled'),
(53, 4, DATE_SUB(CURDATE(), INTERVAL 7 DAY), '13:15', 'Fever & cough', 'No-Show'),
(54, 6, CURDATE(), '14:15', 'Rash checkup', 'Scheduled'),
(55, 1, DATE_ADD(CURDATE(), INTERVAL 6 DAY), '10:00', 'Cholesterol review', 'Scheduled'),
(31, 24, DATE_ADD(CURDATE(), INTERVAL 8 DAY), '09:30', 'Insulin adjustment', 'Scheduled'),
(35, 1, DATE_ADD(CURDATE(), INTERVAL 9 DAY), '11:00', 'ECG recheck', 'Scheduled'),
(39, 7, DATE_SUB(CURDATE(), INTERVAL 8 DAY), '10:00', 'Chemo cycle 2', 'Completed'),
(44, 23, DATE_ADD(CURDATE(), INTERVAL 10 DAY), '12:00', 'Dialysis review', 'Scheduled'),
(50, 11, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '14:30', 'Physiotherapy', 'Scheduled');
