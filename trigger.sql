DELIMITER //

CREATE TRIGGER before_delete_bookings
BEFORE DELETE
ON bookings FOR EACH ROW

BEGIN
    INSERT INTO cancelled_bookings (booking_id, srn, sport_name, facility_id, date_booked, start_time, end_time)
    VALUES (OLD.booking_id, OLD.srn, OLD.sport_name, OLD.facility_id, OLD.date_booked, OLD.start_time, OLD.end_time);
    
END;

//

DELIMITER ;