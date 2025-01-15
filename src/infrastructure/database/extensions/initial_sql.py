INITIAL_SQL = [
    """
    -- Триггер для обновления рейтинга в таблице lesson
    CREATE OR REPLACE FUNCTION update_lesson_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для lesson
        SELECT COALESCE(AVG(mark), 0.0)
        INTO avg_rating
        FROM feedback
        WHERE lesson_id = NEW.lesson_id;

        -- Обновление рейтинга в таблице lesson
        UPDATE lesson
        SET rating = avg_rating
        WHERE id = NEW.lesson_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_lesson_trigger
    AFTER INSERT OR UPDATE ON feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_lesson_rating();     
    """,
    """
    -- Триггер для обновления рейтинга в таблице study_group
    CREATE OR REPLACE FUNCTION update_study_group_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для study_group
        SELECT COALESCE(AVG(rating), 0.0)
        INTO avg_rating
        FROM lesson
        WHERE study_group_id = NEW.study_group_id AND rating <> 0.0;

        -- Обновление рейтинга в таблице study_group
        UPDATE study_group
        SET rating = avg_rating
        WHERE id = NEW.study_group_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_study_group_trigger
    AFTER INSERT OR UPDATE ON lesson
    FOR EACH ROW
    EXECUTE FUNCTION update_study_group_rating();
    """,
    """
    -- Триггер для обновления рейтинга в таблице teacher
    CREATE OR REPLACE FUNCTION update_teacher_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для teacher
        SELECT COALESCE(AVG(rating), 0.0)
        INTO avg_rating
        FROM study_group
        WHERE teacher_id = NEW.teacher_id AND rating <> 0.0;

        -- Обновление рейтинга в таблице teacher
        UPDATE teacher
        SET rating = avg_rating
        WHERE id = NEW.teacher_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_teacher_trigger
    AFTER INSERT OR UPDATE ON study_group
    FOR EACH ROW
    EXECUTE FUNCTION update_teacher_rating();
    """,
    """
    -- Триггер для обновления рейтинга в таблице subject
    CREATE OR REPLACE FUNCTION update_subject_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для subject
        SELECT COALESCE(AVG(rating), 0.0)
        INTO avg_rating
        FROM study_group
        WHERE subject_id = NEW.subject_id AND rating <> 0.0;

        -- Обновление рейтинга в таблице subject
        UPDATE subject
        SET rating = avg_rating
        WHERE id = NEW.subject_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_subject_trigger
    AFTER INSERT OR UPDATE ON study_group
    FOR EACH ROW
    EXECUTE FUNCTION update_subject_rating();
    """,
    """
    -- Триггер для обновления рейтинга в таблице module
    CREATE OR REPLACE FUNCTION update_module_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для module
        SELECT COALESCE(AVG(rating), 0.0)
        INTO avg_rating
        FROM subject
        WHERE module_id = NEW.module_id AND rating <> 0.0;

        -- Обновление рейтинга в таблице module
        UPDATE module
        SET rating = avg_rating
        WHERE id = NEW.module_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_module_trigger
    AFTER INSERT OR UPDATE ON subject
    FOR EACH ROW
    EXECUTE FUNCTION update_module_rating();
    """,
    """
    -- Триггер для обновления рейтинга в таблице institute
    CREATE OR REPLACE FUNCTION update_institute_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        avg_rating FLOAT;
    BEGIN
        -- Расчёт среднего значения рейтинга для institute
        SELECT COALESCE(AVG(rating), 0.0)
        INTO avg_rating
        FROM module
        WHERE institute_id = NEW.institute_id AND rating <> 0.0;

        -- Обновление рейтинга в таблице institute
        UPDATE institute
        SET rating = avg_rating
        WHERE id = NEW.institute_id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE TRIGGER update_institute_trigger
    AFTER INSERT OR UPDATE ON module
    FOR EACH ROW
    EXECUTE FUNCTION update_institute_rating();
    """,
    """
    """,
    """
    INSERT INTO administrator (id, first_name, second_name, third_name, email, password)
        VALUES (
        'd216bd55-4f57-40fa-a6d1-8444f43ccacf',
        'Евгений', 
        'Смирнов', 
        'Сергеевич', 
        'email', 
        'password_hashed'
    )
    """
]