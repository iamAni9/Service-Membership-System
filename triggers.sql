-- Step 1: Create trigger function
CREATE OR REPLACE FUNCTION increment_member_check_ins()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment total_check_ins for the member
    UPDATE member
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 2: Drop existing trigger if it exists
DROP TRIGGER IF EXISTS attendance_insert_trigger ON attendance;

-- Step 3: Create trigger
CREATE TRIGGER attendance_insert_trigger
    AFTER INSERT ON attendance
    FOR EACH ROW
    EXECUTE FUNCTION increment_member_check_ins();


