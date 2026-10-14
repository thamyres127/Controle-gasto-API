CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    telefone TEXT
);

INSERT INTO clientes (nome, email, telefone) VALUES 
('Thamyres Micaele', 'thamyres@email.com', '11999998888'),
('Thamyres Micaele', 'thamyres@email.com', '11999998888'),
('Ana Silva', '://silvaemail.com', '11988887777'),
('Carlos Souza', 'carlos@email.com', '119777'),
('', 'fantasma@email.com', '11966665555');
