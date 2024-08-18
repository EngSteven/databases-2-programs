CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )


CREATE OR REPLACE PROCEDURE usuario_existe(IN _username TEXT, OUT _exists BOOLEAN)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT EXISTS(SELECT 1 FROM users WHERE username = _username) INTO _exists;
END;
$$;



CREATE OR REPLACE PROCEDURE usuario_existe_por_id(IN _id INTEGER, OUT _exists BOOLEAN)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT EXISTS(SELECT 1 FROM users WHERE id = _id) INTO _exists;
END;
$$; 




CREATE OR REPLACE FUNCTION public.registrar_usuario(IN _username TEXT, IN _password TEXT, IN _role TEXT)
RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
    existe BOOLEAN;
	id_generado INTEGER;
BEGIN
	-- Verifica si el usuario existe
    CALL usuario_existe(_username, existe);
	
    -- Solo actualiza si el usuario existe
    IF existe THEN
		RETURN -1; -- Username ya existe
	ELSE
    	INSERT INTO users (username, password, role)
    	VALUES (_username, _password, _role)
    	RETURNING id INTO id_generado; -- Captura el id del nuevo usuario
        RETURN id_generado; -- Retorna el id del nuevo usuario
	END IF;
END;
$$;


CREATE OR REPLACE FUNCTION public.obtener_usuarios()
	RETURNS TABLE(
        id integer,
        username text,
        role text
    )
	LANGUAGE 'plpgsql'
AS $$

BEGIN
	RETURN QUERY SELECT users.id, users.username, users.role FROM users;
END;
$$;


CREATE OR REPLACE FUNCTION public.eliminar_usuario_por_id(
    IN _id INTEGER
)

RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    existe BOOLEAN;
	
BEGIN
    -- Verifica si el usuario existe
    CALL usuario_existe_por_id(_id, existe);
    
    -- Solo elimina si el usuario existe
    IF existe THEN
        DELETE FROM users
        WHERE id = _id;
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END;
$$;




CREATE OR REPLACE PROCEDURE registrar_usuario(IN _username TEXT, IN _password TEXT, IN _role TEXT, OUT _user_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (username, password, role)
    VALUES (_username, _password, _role)
    RETURNING id INTO _user_id;
END;
$$;





CREATE OR REPLACE FUNCTION public.eliminar_usuario(
    IN _username TEXT
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    existe BOOLEAN;
	
BEGIN
    -- Verifica si el usuario existe
    CALL usuario_existe(_username, existe);
    
    -- Solo elimina si el usuario existe
    IF existe THEN
        DELETE FROM users
        WHERE username = _username;
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END;
$$;



CREATE OR REPLACE FUNCTION public.actualizar_usuario_por_id(
	IN _id INTEGER,
    IN _username TEXT, 
	IN _password TEXT, 
	IN _role TEXT
)

RETURNS integer
LANGUAGE 'plpgsql'

AS $$
DECLARE 
    existe BOOLEAN;
	
BEGIN
    -- Verifica si el usuario existe
    CALL usuario_existe_por_id(_id, existe);
	
    -- Solo actualiza si el usuario existe
    IF existe THEN    
		UPDATE users
		SET 
			username = _username,
			password = _password,
			role = _role
		WHERE
			id = _id;
		RETURN 1;	-- Usuario actualizado 
    ELSE
        RETURN 0; 	-- El id del usuario ingresado no existe
    END IF;
END;
$$;




CREATE OR REPLACE FUNCTION public.actualizar_usuario(
    IN _username TEXT, 
	IN _password TEXT, 
	IN _role TEXT
)

RETURNS integer
LANGUAGE 'plpgsql'

AS $$
DECLARE 
    existe BOOLEAN;
	
BEGIN
    -- Verifica si el usuario existe
    CALL usuario_existe(_username, existe);
	
    -- Solo elimina si el usuario existe
    IF existe THEN    
		UPDATE users
		SET 
			username = _username,
			password = _password,
			role = _role
		WHERE
			username = _username;
		RETURN 1;	-- Usuario actualizado 
    ELSE
        RETURN 0; 	-- El usuario ingresado no existe
    END IF;
END;
$$;




CREATE OR REPLACE FUNCTION public.login(IN _username TEXT, IN _password TEXT)
RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
    existe BOOLEAN;
BEGIN
	-- Verifica si el usuario existe
    CALL usuario_existe(_username, existe);
	SELECT EXISTS (SELECT 1 FROM users WHERE username = _username AND password = _password) INTO existe;
	
    IF existe THEN
		RETURN 1; 		-- Los datos del usario son correctos
	ELSE
        RETURN 0; 		-- Los datos del usuario son incorrectos
	END IF;
END;
$$;


