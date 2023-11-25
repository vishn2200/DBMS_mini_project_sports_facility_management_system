CREATE PROCEDURE generate_non_member_booking_statistics()
BEGIN
    -- Temporary table to store non-member booking statistics
    CREATE TEMPORARY TABLE temp_non_member_statistics (
        sport_name VARCHAR(255),
        total_revenue DECIMAL(10, 2),
        total_bookings INT
    );

    -- Insert data into the temporary table
    INSERT INTO temp_non_member_statistics
    SELECT
        b.sport_name,
        SUM(100) AS total_revenue, -- Assuming fixed amount for non-members
        COUNT(*) AS total_bookings
    FROM
        bookings b
    LEFT JOIN users u ON b.srn = u.srn
    WHERE
        u.plan != 'Member'
    GROUP BY
        b.sport_name;

    -- Select data from the temporary table
    SELECT * FROM temp_non_member_statistics;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_non_member_statistics;
END;