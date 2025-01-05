INITIAL_SQL = [
    """
    -- Функция для обновления рейтинга
    CREATE OR REPLACE FUNCTION update_rating_generic()
    RETURNS TRIGGER AS $$
    DECLARE
        target_table TEXT;
        target_column TEXT;
        foreign_key_column TEXT;
        source_table TEXT;
        source_rating_column TEXT;
        source_key_column TEXT;
        avg_rating FLOAT;
    BEGIN
        -- Извлечение параметров из TG_ARGV
        target_table := TG_ARGV[0];
        target_column := TG_ARGV[1];
        foreign_key_column := TG_ARGV[2];
        source_table := TG_ARGV[3];
        source_rating_column := TG_ARGV[4];
        source_key_column := TG_ARGV[5];

        -- Рассчёт среднего значения рейтинга
        EXECUTE format(
            'SELECT AVG(%I) FROM %I WHERE %I = $1',
            source_rating_column, source_table, source_key_column
        )
        INTO avg_rating
        USING NEW.id;

        -- Обновление целевой таблицы
        EXECUTE format(
            'UPDATE %I SET %I = COALESCE($1, 0.0) WHERE %I = $2',
            target_table, target_column, foreign_key_column
        )
        USING avg_rating, NEW.id;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    -- триггер для обновления lesson
    CREATE TRIGGER update_lesson_trigger
    AFTER INSERT OR UPDATE ON feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'lesson',             -- Целевая таблица
        'rating',             -- Поле рейтинга в целевой таблице
        'id',                 -- Поле связи в целевой таблице
        'feedback',           -- Таблица-источник
        'mark',               -- Поле рейтинга в таблице-источнике
        'lesson_id'           -- Поле связи в таблице-источнике
    );
    """,
    """
    -- триггер для обновления study_group
    CREATE TRIGGER update_study_group_trigger
    AFTER INSERT OR UPDATE ON lesson
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'study_group',           
        'rating',          
        'id',     
        'lesson',  
        'rating',        
        'study_group_id'
    );
    """,
    """
    -- триггер для обновления teacher
    CREATE TRIGGER update_teacher_trigger
    AFTER INSERT OR UPDATE ON study_group
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'teacher',           
        'rating',          
        'id',     
        'study_group',  
        'rating',        
        'teacher_id'
    );
    """,
    """
    -- триггер для обновления subject
    CREATE TRIGGER update_subject_trigger
    AFTER INSERT OR UPDATE ON study_group
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'subject',           
        'rating',          
        'id',     
        'study_group',  
        'rating',        
        'subject_id'
    );
    """,
    """
    -- триггер для обновления module
    CREATE TRIGGER update_module_trigger
    AFTER INSERT OR UPDATE ON subject
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'module',           
        'rating',          
        'id',     
        'subject',  
        'rating',        
        'module_id'
    );
    """,
    """
    -- триггер для обновления institute
    CREATE TRIGGER update_institute_trigger
    AFTER UPDATE ON module
    FOR EACH ROW
    EXECUTE FUNCTION update_rating_generic(
        'institute',           
        'rating',          
        'id',     
        'module',  
        'rating',        
        'institute_id'
    );
    """
]