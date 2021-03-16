INSERT INTO public.usuario
(id, nome, email, senha, cpf, pis)
VALUES(1, 'Beltrano de Lá', 'beltranodela@example.com', 'pbkdf2:sha256:150000$9fTobSw6$da88df5c4b126c4a1b788ebcd92775a6ca66570883dc1932206428d0ad3073c4', '000.000.000-00', '000.00000.00-0');

INSERT INTO public.endereco
(cep, rua, numero, complemento, municipio, estado, pais, usuario_id)
VALUES('00000-000', 'Rua Oriente', 2393, 'Prox. Ocidente', 'Fortaleza', 'Ceara', 'BR', 1);

ALTER SEQUENCE usuario_id_seq RESTART WITH 2;
