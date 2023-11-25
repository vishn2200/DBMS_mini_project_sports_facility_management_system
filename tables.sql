CREATE TABLE plan(plan_type ENUM('Member', 'Non-Member') PRIMARY KEY, plan_validity year);

CREATE TABLE users(srn CHAR(13) PRIMARY KEY, user_name VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, phone_number BIGINT(10) NOT NULL, dob DATE NOT NULL, sex ENUM('M', 'F') NOT NULL, plan ENUM('Member', 'Non-Member') NOT NULL);

CREATE TABLE auth(srn CHAR(13) PRIMARY KEY, passwd VARCHAR(255) NOT NULL);

CREATE TABLE sports(sport_id VARCHAR(5) PRIMARY KEY, sport_name VARCHAR(20) NOT NULL, no_of_players INT, coach_id VARCHAR(5));

CREATE TABLE facility(facility_id VARCHAR(5) PRIMARY KEY, facility_name VARCHAR(50), fac_location VARCHAR(25) NOT NULL, rate INT NOT NULL, availabile ENUM("Yes","No") NOT NULL, sport_id VARCHAR(5));

CREATE TABLE coaches(coach_id VARCHAR(5) PRIMARY KEY, coach_name VARCHAR(20) NOT NULL, phone_number BIGINT(10) NOT NULL, email VARCHAR(50) NOT NULL, sex ENUM("M","F") NOT NULL);

CREATE TABLE bookings(booking_id INT AUTO_INCREMENT PRIMARY KEY, srn VARCHAR(13), date_booked DATE NOT NULL, start_time TIME, end_time TIME, sport_name VARCHAR(20), facility_id VARCHAR(5));

CREATE TABLE cancelled_bookings(booking_id INT PRIMARY KEY, srn VARCHAR(13), date_booked DATE NOT NULL, start_time TIME, end_time TIME, sport_name VARCHAR(20), facility_id VARCHAR(5));

CREATE TABLE feedback(srn CHAR(13), facility_id VARCHAR(5), date_feedback DATE, comments TEXT NOT NULL);

CREATE TABLE admin(admin_id CHAR(7) PRIMARY KEY, admin_passwd VARCHAR(255) NOT NULL);

ALTER TABLE users ADD CONSTRAINT fk_plan FOREIGN KEY (plan) REFERENCES plan(plan_type) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE auth ADD CONSTRAINT fk_srn_auth FOREIGN KEY (srn) REFERENCES users(srn) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE sports ADD CONSTRAINT fk_coach_id FOREIGN KEY (coach_id) REFERENCES coaches(coach_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE facility ADD CONSTRAINT fk_sport_id FOREIGN KEY (sport_id) REFERENCES sports(sport_id) ON UPDATE CASCADE;

ALTER TABLE bookings ADD CONSTRAINT fk_srn_book FOREIGN KEY (srn) REFERENCES users(srn);

ALTER TABLE bookings ADD CONSTRAINT fk_fac_book FOREIGN KEY (facility_id) REFERENCES facility(facility_id) ;

ALTER TABLE feedback ADD CONSTRAINT pk_feedback PRIMARY KEY (srn,facility_id, date_feedback);

ALTER TABLE feedback ADD CONSTRAINT fk_srn_feedback FOREIGN KEY (srn) REFERENCES users(srn);

ALTER TABLE bookings ADD CONSTRAINT fk_fac_feedback FOREIGN KEY (facility_id) REFERENCES facility(facility_id);

INSERT INTO admin VALUES("admin01", "ican"), ("admin02", "minad");

INSERT INTO plan VALUES("Member", "2024"), ("Non-Member", NULL);

INSERT INTO users VALUES("PES1UG21CS705", "Veluri Siva Chinmayi", "csveluri@gmail.com", 6363491622, "2003-06-02", "F", "Non-Member"), ("PES1UG21CS718", "Vishnu Prakash","vishnuprakash156@gmail.com",7619639279,"2002-12-13","M","Non-Member"), ("PES1UG22EC206", "Shattesh Gomlur", "shattgommas@gmail.com", 8008555555, "2004-08-31", "F", "Member");

INSERT INTO coaches VALUES("BB01","Coach_BB",9902555772, "Coach_1@pes.edu","M"),("BD01","Coach_BD",9902019000,"Coach_2@pes.edu","F"),("SQ01","Coach_SQ",8657849792, "Coach_SQ@pes.edu", "M"),("KB01","Coach_KB",8224868429,"Coach_KB@pes.edu","M"),("FB01","Coach_FB",2345654329,"Coach_FB@pes.edu","M"),("CR01","Coach_CR",2345678902,"Coach_CR@pes.edu","F"),("TT01","Coach_TT",1234567890,"Coch_TT@pes.edu","M"),("VB01","Coach_VB",9999999999,"Coach_VB@pes.edu","F");

INSERT INTO sports VALUES("BB","Basketball",10,"BB01"),("BD","Badminton",4,"BD01"),("SQ","Squash",2,"SQ01"),("KB","Kabaddi",14,"KB01"),("FB","Football",14,"FB01"),("CR","Cricket",22,"CR01"),("TT","Table-Tennis",4,"TT01"),("VB","Volleyball",14,"VB01");

INSERT INTO facility VALUES ("BB01", "BB COURT BACK GATE PARKING", "Back gate parking", 100, "Yes", "BB"), ("BB02", "BB COURT-1 GJB", "GJB", 100, "Yes", "BB"), ("BB03", "BB COURT-2 GJB", "GJB", 100, "Yes", "BB"), ("BD01", "BD COURT-1 GJB", "GJB", 100, "Yes", "BD"), ("BD02", "BD COURT-2 GJB", "GJB", 100, "Yes", "BD"), ("BD03", "BD COURT-3 GJB", "GJB", 100, "Yes", "BD"), ("SQ01", "SQUASH COURT-1 GJB", "GJB", 100, "Yes", "SQ"), ("SQ02", "SQUASH COURT-2 GJB", "GJB", 100, "Yes", "SQ"), ("KB01", "KABADDI COURT GJB", "GJB", 100, "Yes", "KB"), ("FB01", "FOOTBALL GROUND NEAR BACK GATE", "Near back gate", 100, "Yes", "FB"), ("CR01", "CRICKET NET-1", "Back gate parking", 100, "Yes", "CR"), ("CR02", "CRICKET NET-2", "Back gate parking", 100, "Yes", "CR"), ("CR03", "CRICKET GROUND", "Back gate parking", 100, "Yes", "CR"), ("VB01", "VOLLEYBALL COURT", "Back gate parking", 100, "Yes", "VB");