-- =====================================================================
-- Additional seed data — more doctors, patients, appointments
--   mysql -u root -p hospital_db < seed_more.sql
-- =====================================================================

USE hospital_db;

-- ---------------------------------------------------------------------
-- More Doctors (doctor_id 9 onward)
-- ---------------------------------------------------------------------
INSERT INTO doctors (first_name, last_name, specialization, department, phone, email, role, status, joined_on, consultation_fee) VALUES
('Sanjay', 'Mehta', 'Cardiology', 'Cardiology', '+91-9876543220', 'sanjay.mehta@meridian.in', 'Doctor', 'Active', '2016-04-11', 1600.00),
('Ritu', 'Malhotra', 'Gynecology', 'Gynecology', '+91-9876543221', 'ritu.malhotra@meridian.in', 'Doctor', 'Active', '2019-02-18', 1300.00),
('Aakash', 'Chopra', 'Orthopedics', 'Orthopedics', '+91-9876543222', 'aakash.chopra@meridian.in', 'Doctor', 'Active', '2020-08-09', 1250.00),
('Divya', 'Bhatt', 'Neurology', 'Neurology', '+91-9876543223', 'divya.bhatt@meridian.in', 'Doctor', 'On Leave', '2018-12-01', 1900.00),
('Karthik', 'Subramanian', 'Pediatrics', 'Pediatrics', '+91-9876543224', 'karthik.s@meridian.in', 'Doctor', 'Active', '2021-06-22', 1050.00),
('Neelam', 'Saxena', 'Dermatology', 'Dermatology', '+91-9876543225', 'neelam.saxena@meridian.in', 'Doctor', 'Active', '2022-09-15', 950.00),
('Rohan', 'Desai', 'Oncology', 'Oncology', '+91-9876543226', 'rohan.desai@meridian.in', 'Doctor', 'Active', '2015-03-30', 2100.00),
('Shalini', 'Pillai', 'ENT', 'ENT', '+91-9876543227', 'shalini.pillai@meridian.in', 'Doctor', 'Active', '2020-11-19', 1100.00),
('Gaurav', 'Bansal', 'General Medicine', 'General Medicine', '+91-9876543228', 'gaurav.bansal@meridian.in', 'Doctor', 'Active', '2017-07-07', 850.00),
('Anjali', 'Sethi', 'Psychiatry', 'Psychiatry', '+91-9876543229', 'anjali.sethi@meridian.in', 'Doctor', 'Active', '2019-10-14', 1400.00),
('Manoj', 'Kulkarni', 'Urology', 'Urology', '+91-9876543230', 'manoj.kulkarni@meridian.in', 'Doctor', 'Active', '2018-05-25', 1500.00),
('Preeti', 'Aggarwal', 'Ophthalmology', 'Ophthalmology', '+91-9876543231', 'preeti.aggarwal@meridian.in', 'Doctor', 'Active', '2021-01-30', 1000.00),
('Vivek', 'Ranjan', 'Gastroenterology', 'Gastroenterology', '+91-9876543232', 'vivek.ranjan@meridian.in', 'Doctor', 'Active', '2016-09-12', 1700.00),
('Nisha', 'Krishnan', 'Pulmonology', 'Pulmonology', '+91-9876543233', 'nisha.krishnan@meridian.in', 'Doctor', 'On Leave', '2020-02-08', 1350.00),
('Suresh', 'Yadav', 'Nephrology', 'Nephrology', '+91-9876543234', 'suresh.yadav@meridian.in', 'Doctor', 'Active', '2017-11-03', 1600.00),
('Farhan', 'Sheikh', 'Endocrinology', 'Endocrinology', '+91-9876543235', 'farhan.sheikh@meridian.in', 'Doctor', 'Active', '2019-04-27', 1450.00);

-- ---------------------------------------------------------------------
-- More Patients (patient_id 11 onward)
-- ---------------------------------------------------------------------
INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_group, phone, email, address, emergency_contact, admission_status, ward, registered_on) VALUES
('Aditya', 'Bose', '1983-05-19', 'Male', 'O+', '+91-9000000021', 'aditya.bose@email.com', '15 Salt Lake, Kolkata', '+91-9000000031', 'Outpatient', NULL, '2025-05-11'),
('Ishita', 'Reddy', '1991-10-08', 'Female', 'B+', '+91-9000000022', 'ishita.r@email.com', '22 Banjara Hills, Hyderabad', '+91-9000000032', 'Admitted', 'General Ward', '2025-05-22'),
('Nikhil', 'Sharma', '1979-01-15', 'Male', 'A+', '+91-9000000023', NULL, '48 Sector 17, Chandigarh', '+91-9000000033', 'Outpatient', NULL, '2025-06-01'),
('Tara', 'Menon', '1996-07-27', 'Female', 'AB+', '+91-9000000024', 'tara.m@email.com', '9 Marine Drive, Mumbai', '+91-9000000034', 'Discharged', NULL, '2025-06-08'),
('Karan', 'Malhotra', '1987-03-03', 'Male', 'O-', '+91-9000000025', NULL, '61 Rajouri Garden, Delhi', '+91-9000000035', 'Admitted', 'Cardiac Ward', '2025-06-14'),
('Simran', 'Kaur', '1993-11-11', 'Female', 'B-', '+91-9000000026', 'simran.k@email.com', '33 Model Town, Ludhiana', '+91-9000000036', 'Outpatient', NULL, '2025-06-19'),
('Rohit', 'Nair', '1974-08-21', 'Male', 'A-', '+91-9000000027', NULL, '77 Fort Kochi, Kochi', '+91-9000000037', 'Admitted', 'Neuro Ward', '2025-06-25'),
('Ananya', 'Ghosh', '1998-04-30', 'Female', 'O+', '+91-9000000028', 'ananya.g@email.com', '18 New Town, Kolkata', '+91-9000000038', 'Outpatient', NULL, '2025-07-02'),
('Sameer', 'Khan', '1981-12-17', 'Male', 'AB-', '+91-9000000029', NULL, '54 Charminar, Hyderabad', '+91-9000000039', 'Discharged', NULL, '2025-07-06'),
('Divya', 'Pillai', '1990-02-06', 'Female', 'A+', '+91-9000000030', 'divya.p@email.com', '27 Indiranagar, Bangalore', '+91-9000000040', 'Outpatient', NULL, '2025-07-09'),
('Harsh', 'Vardhan', '1985-09-14', 'Male', 'B+', '+91-9000000041', NULL, '90 Vasant Kunj, Delhi', '+91-9000000051', 'Admitted', 'Ortho Ward', '2025-07-12'),
('Meghna', 'Rao', '1994-06-23', 'Female', 'O+', '+91-9000000042', 'meghna.r@email.com', '11 Koramangala, Bangalore', '+91-9000000052', 'Outpatient', NULL, '2025-07-13'),
('Aryan', 'Gupta', '2001-01-05', 'Male', 'A-', '+91-9000000043', NULL, '38 Gomti Nagar, Lucknow', '+91-9000000053', 'Outpatient', NULL, '2025-07-14'),
('Kavya', 'Iyer', '1989-10-29', 'Female', 'AB+', '+91-9000000044', 'kavya.i@email.com', '5 T Nagar, Chennai', '+91-9000000054', 'Admitted', 'General Ward', '2025-07-15'),
('Varun', 'Chauhan', '1977-04-02', 'Male', 'O-', '+91-9000000045', NULL, '63 Civil Lines, Jaipur', '+91-9000000055', 'Discharged', NULL, '2025-07-16'),
('Riya', 'Saxena', '1997-08-16', 'Female', 'B+', '+91-9000000046', 'riya.s@email.com', '20 Hazratganj, Lucknow', '+91-9000000056', 'Outpatient', NULL, '2025-07-17'),
('Ajay', 'Deshmukh', '1982-11-24', 'Male', 'A+', '+91-9000000047', NULL, '47 Shivaji Nagar, Pune', '+91-9000000057', 'Admitted', 'Cardiac Ward', '2025-07-18'),
('Sonali', 'Banerjee', '1992-03-09', 'Female', 'O+', '+91-9000000048', 'sonali.b@email.com', '14 Ballygunge, Kolkata', '+91-9000000058', 'Outpatient', NULL, '2025-07-19'),
('Imran', 'Qureshi', '1986-07-13', 'Male', 'AB-', '+91-9000000049', NULL, '82 Mehdipatnam, Hyderabad', '+91-9000000059', 'Outpatient', NULL, '2025-07-20'),
('Pallavi', 'Joshi', '1999-12-28', 'Female', 'A-', '+91-9000000050', 'pallavi.j@email.com', '36 Kothrud, Pune', '+91-9000000060', 'Discharged', NULL, '2025-07-20');

-- ---------------------------------------------------------------------
-- More Appointments (patient_id 11-30, doctor_id 1-24, dates around today)
-- ---------------------------------------------------------------------
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status) VALUES
(11, 9, CURDATE(), '09:15', 'Hypertension review', 'Scheduled'),
(12, 10, CURDATE(), '10:00', 'Prenatal checkup', 'Scheduled'),
(13, 11, CURDATE(), '10:45', 'Shoulder pain', 'Scheduled'),
(14, 12, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '11:30', 'Headache evaluation', 'Completed'),
(15, 9, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '14:00', 'Cardiac stress test', 'Completed'),
(16, 13, CURDATE(), '15:30', 'Child vaccination', 'Scheduled'),
(17, 3, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:00', 'Stroke follow-up', 'Scheduled'),
(18, 14, CURDATE(), '11:15', 'Acne treatment', 'Scheduled'),
(19, 7, DATE_SUB(CURDATE(), INTERVAL 3 DAY), '13:30', 'Chemotherapy session', 'Completed'),
(20, 16, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '10:30', 'Ear infection', 'Scheduled'),
(21, 11, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:30', 'Fracture assessment', 'Scheduled'),
(22, 17, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '12:00', 'General checkup', 'Scheduled'),
(23, 18, CURDATE(), '16:00', 'Anxiety consultation', 'Scheduled'),
(24, 19, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '10:00', 'Kidney stone review', 'Scheduled'),
(25, 20, DATE_SUB(CURDATE(), INTERVAL 4 DAY), '11:00', 'Vision test', 'Completed'),
(26, 21, CURDATE(), '13:45', 'Acid reflux', 'Scheduled'),
(27, 22, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '09:45', 'Asthma review', 'Scheduled'),
(28, 23, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '14:30', 'Dialysis consultation', 'Scheduled'),
(29, 24, CURDATE(), '10:15', 'Diabetes management', 'Scheduled'),
(30, 10, DATE_SUB(CURDATE(), INTERVAL 5 DAY), '15:00', 'Gynecology followup', 'Cancelled'),
(11, 9, DATE_ADD(CURDATE(), INTERVAL 6 DAY), '09:00', 'ECG recheck', 'Scheduled'),
(13, 11, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '11:00', 'Physiotherapy', 'Scheduled'),
(16, 13, DATE_SUB(CURDATE(), INTERVAL 6 DAY), '10:30', 'Growth checkup', 'Completed'),
(19, 7, DATE_ADD(CURDATE(), INTERVAL 8 DAY), '13:00', 'Oncology review', 'Scheduled'),
(24, 19, DATE_SUB(CURDATE(), INTERVAL 7 DAY), '12:30', 'Post-op review', 'No-Show');
