CREATE PROCEDURE generate_member_booking_statistics()
BEGIN
    -- Temporary table to store member booking statistics
    CREATE TEMPORARY TABLE temp_member_statistics (
        sport_name VARCHAR(255),
        total_bookings INT
    );

    -- Insert data into the temporary table
    INSERT INTO temp_member_statistics
    SELECT
        sport_name,
        COUNT(*) AS total_bookings
    FROM
        bookings
    WHERE
        srn IN (SELECT srn FROM users WHERE plan = 'Member')
    GROUP BY
        sport_name;

    -- Select data from the temporary table
    SELECT * FROM temp_member_statistics;

    -- Calculate yearly revenue (assuming Rs. 10,000 per member per year)
    SELECT
        'Yearly Revenue' AS metric,
        SUM(total_bookings * 10000) AS revenue
    FROM
        temp_member_statistics;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_member_statistics;
END; 
