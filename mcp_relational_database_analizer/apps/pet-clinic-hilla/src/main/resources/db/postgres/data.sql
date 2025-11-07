-- #################################
-- # Inserções para a tabela VETS
-- #################################

-- NOTA: O WHERE NOT EXISTS garante que as linhas só são inseridas se ainda não existirem,
-- prevenindo erros de chave primária duplicada em ambos os BDs.

INSERT INTO vets (first_name, last_name) SELECT 'James', 'Carter' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=1);
INSERT INTO vets (first_name, last_name) SELECT 'Helen', 'Leary' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=2);
INSERT INTO vets (first_name, last_name) SELECT 'Linda', 'Douglas' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=3);
INSERT INTO vets (first_name, last_name) SELECT 'Rafael', 'Ortega' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=4);
INSERT INTO vets (first_name, last_name) SELECT 'Henry', 'Stevens' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=5);
INSERT INTO vets (first_name, last_name) SELECT 'Sharon', 'Jenkins' WHERE NOT EXISTS (SELECT * FROM vets WHERE id=6);

---

-- #################################
-- # Inserções para a tabela SPECIALTIES
-- #################################

INSERT INTO specialties (name) SELECT 'radiology' WHERE NOT EXISTS (SELECT * FROM specialties WHERE name='radiology');
INSERT INTO specialties (name) SELECT 'surgery' WHERE NOT EXISTS (SELECT * FROM specialties WHERE name='surgery'); 
INSERT INTO specialties (name) SELECT 'dentistry' WHERE NOT EXISTS (SELECT * FROM specialties WHERE name='dentistry');

---

-- #################################
-- # Inserções para a tabela VET_SPECIALTIES (Ponto de adaptação)
-- #################################

-- ADAPTAÇÃO: Substituímos o "ON CONFLICT (vet_id, specialty_id) DO NOTHING" do PostgreSQL,
-- que o H2 não entende, por uma instrução WHERE NOT EXISTS, que é compatível com ambos.

INSERT INTO vet_specialties (vet_id, specialty_id)
SELECT 2, 1
WHERE NOT EXISTS (SELECT 1 FROM vet_specialties WHERE vet_id = 2 AND specialty_id = 1);

INSERT INTO vet_specialties (vet_id, specialty_id)
SELECT 3, 2
WHERE NOT EXISTS (SELECT 1 FROM vet_specialties WHERE vet_id = 3 AND specialty_id = 2);

INSERT INTO vet_specialties (vet_id, specialty_id)
SELECT 3, 3
WHERE NOT EXISTS (SELECT 1 FROM vet_specialties WHERE vet_id = 3 AND specialty_id = 3);

INSERT INTO vet_specialties (vet_id, specialty_id)
SELECT 4, 2
WHERE NOT EXISTS (SELECT 1 FROM vet_specialties WHERE vet_id = 4 AND specialty_id = 2);

INSERT INTO vet_specialties (vet_id, specialty_id)
SELECT 5, 1
WHERE NOT EXISTS (SELECT 1 FROM vet_specialties WHERE vet_id = 5 AND specialty_id = 1);

---

-- #################################
-- # Inserções para a tabela TYPES
-- #################################

INSERT INTO types (name) SELECT 'cat' WHERE NOT EXISTS (SELECT * FROM types WHERE name='cat');
INSERT INTO types (name) SELECT 'dog' WHERE NOT EXISTS (SELECT * FROM types WHERE name='dog');
INSERT INTO types (name) SELECT 'lizard' WHERE NOT EXISTS (SELECT * FROM types WHERE name='lizard');
INSERT INTO types (name) SELECT 'snake' WHERE NOT EXISTS (SELECT * FROM types WHERE name='snake');
INSERT INTO types (name) SELECT 'bird' WHERE NOT EXISTS (SELECT * FROM types WHERE name='bird');
INSERT INTO types (name) SELECT 'hamster' WHERE NOT EXISTS (SELECT * FROM types WHERE name='hamster');

---

-- #################################
-- # Inserções para a tabela OWNERS
-- #################################

INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'George', 'Franklin', '110 W. Liberty St.', 'Madison', '6085551023' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=1);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Betty', 'Davis', '638 Cardinal Ave.', 'Sun Prairie', '6085551749' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=2);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Eduardo', 'Rodriquez', '2693 Commerce St.', 'McFarland', '6085558763' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=3);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Harold', 'Davis', '563 Friendly St.', 'Windsor', '6085553198' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=4);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Peter', 'McTavish', '2387 S. Fair Way', 'Madison', '6085552765' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=5);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Jean', 'Coleman', '105 N. Lake St.', 'Monona', '6085552654' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=6);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Jeff', 'Black', '1450 Oak Blvd.', 'Monona', '6085555387' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=7);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Maria', 'Escobito', '345 Maple St.', 'Madison', '6085557683' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=8);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'David', 'Schroeder', '2749 Blackhawk Trail', 'Madison', '6085559435' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=9);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Carlos', 'Estaban', '2335 Independence La.', 'Waunakee', '6085555487' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=10);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Jennifer', 'Wilson', '789 Pine Ave.', 'Madison', '6085551234' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=11);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Michael', 'Brown', '456 Elm St.', 'Sun Prairie', '6085555678' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=12);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Sarah', 'Johnson', '321 Oak Dr.', 'McFarland', '6085559012' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=13);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Robert', 'Martinez', '654 Maple Ln.', 'Windsor', '6085553456' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=14);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Lisa', 'Anderson', '987 Cedar Blvd.', 'Monona', '6085557890' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=15);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'James', 'Taylor', '147 Birch St.', 'Madison', '6085552345' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=16);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Patricia', 'Thomas', '258 Spruce Ave.', 'Waunakee', '6085556789' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=17);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Christopher', 'Garcia', '369 Willow Way', 'Madison', '6085551111' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=18);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Amanda', 'Rodriguez', '741 Ash Ct.', 'Sun Prairie', '6085552222' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=19);
INSERT INTO owners (first_name, last_name, address, city, telephone) SELECT 'Daniel', 'Lee', '852 Poplar Rd.', 'McFarland', '6085553333' WHERE NOT EXISTS (SELECT * FROM owners WHERE id=20);

---

-- #################################
-- # Inserções para a tabela PETS
-- #################################

INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Leo', '2000-09-07', 1, 1 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=1);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Basil', '2002-08-06', 6, 2 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=2);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Rosy', '2001-04-17', 2, 3 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=3);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Jewel', '2000-03-07', 2, 3 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=4);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Iggy', '2000-11-30', 3, 4 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=5);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'George', '2000-01-20', 4, 5 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=6);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Samantha', '1995-09-04', 1, 6 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=7);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Max', '1995-09-04', 1, 6 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=8);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Lucky', '1999-08-06', 5, 7 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=9);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Mulligan', '1997-02-24', 2, 8 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=10);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Freddy', '2000-03-09', 5, 9 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=11);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Lucky', '2000-06-24', 2, 10 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=12);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Sly', '2002-06-08', 1, 10 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=13);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Bella', '2018-05-15', 2, 11 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=14);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Charlie', '2019-03-22', 2, 11 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=15);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Luna', '2020-07-10', 1, 12 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=16);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Cooper', '2017-11-05', 2, 13 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=17);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Daisy', '2019-09-18', 1, 14 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=18);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Rocky', '2018-02-28', 2, 15 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=19);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Molly', '2021-01-12', 1, 16 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=20);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Buddy', '2016-08-30', 2, 17 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=21);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Chloe', '2020-04-25', 1, 18 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=22);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Duke', '2019-12-08', 2, 19 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=23);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Zoe', '2018-06-14', 5, 20 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=24);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Bailey', '2017-10-20', 2, 1 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=25);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Sophie', '2021-03-05', 1, 2 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=26);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Jack', '2016-09-17', 2, 4 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=27);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Lily', '2020-11-22', 1, 5 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=28);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Oscar', '2019-07-30', 6, 7 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=29);
INSERT INTO pets (name, birth_date, type_id, owner_id) SELECT 'Milo', '2018-01-08', 1, 9 WHERE NOT EXISTS (SELECT * FROM pets WHERE id=30);

---

-- #################################
-- # Inserções para a tabela VISITS
-- #################################

INSERT INTO visits (pet_id, visit_date, description) SELECT 7, '2010-03-04', 'rabies shot' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=1);
INSERT INTO visits (pet_id, visit_date, description) SELECT 8, '2011-03-04', 'rabies shot' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=2);
INSERT INTO visits (pet_id, visit_date, description) SELECT 8, '2009-06-04', 'neutered' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=3);
INSERT INTO visits (pet_id, visit_date, description) SELECT 7, '2008-09-04', 'spayed' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=4);
INSERT INTO visits (pet_id, visit_date, description) SELECT 1, '2023-01-15', 'annual checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=5);
INSERT INTO visits (pet_id, visit_date, description) SELECT 2, '2023-02-20', 'dental cleaning' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=6);
INSERT INTO visits (pet_id, visit_date, description) SELECT 3, '2023-03-10', 'vaccination' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=7);
INSERT INTO visits (pet_id, visit_date, description) SELECT 4, '2023-04-05', 'skin allergy treatment' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=8);
INSERT INTO visits (pet_id, visit_date, description) SELECT 5, '2023-05-12', 'regular checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=9);
INSERT INTO visits (pet_id, visit_date, description) SELECT 6, '2023-06-18', 'scale removal' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=10);
INSERT INTO visits (pet_id, visit_date, description) SELECT 9, '2023-07-22', 'wing clipping' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=11);
INSERT INTO visits (pet_id, visit_date, description) SELECT 10, '2023-08-30', 'ear infection' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=12);
INSERT INTO visits (pet_id, visit_date, description) SELECT 11, '2023-09-14', 'beak trimming' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=13);
INSERT INTO visits (pet_id, visit_date, description) SELECT 12, '2023-10-08', 'flea treatment' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=14);
INSERT INTO visits (pet_id, visit_date, description) SELECT 13, '2023-11-25', 'wellness exam' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=15);
INSERT INTO visits (pet_id, visit_date, description) SELECT 14, '2024-01-10', 'rabies shot' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=16);
INSERT INTO visits (pet_id, visit_date, description) SELECT 15, '2024-02-14', 'spayed' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=17);
INSERT INTO visits (pet_id, visit_date, description) SELECT 16, '2024-03-20', 'dental checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=18);
INSERT INTO visits (pet_id, visit_date, description) SELECT 17, '2024-04-15', 'vaccination booster' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=19);
INSERT INTO visits (pet_id, visit_date, description) SELECT 18, '2024-05-22', 'neutered' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=20);
INSERT INTO visits (pet_id, visit_date, description) SELECT 19, '2024-06-30', 'hip examination' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=21);
INSERT INTO visits (pet_id, visit_date, description) SELECT 20, '2024-07-18', 'eye infection treatment' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=22);
INSERT INTO visits (pet_id, visit_date, description) SELECT 21, '2024-08-25', 'arthritis checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=23);
INSERT INTO visits (pet_id, visit_date, description) SELECT 22, '2024-09-12', 'annual vaccination' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=24);
INSERT INTO visits (pet_id, visit_date, description) SELECT 23, '2024-10-05', 'heartworm test' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=25);
INSERT INTO visits (pet_id, visit_date, description) SELECT 24, '2024-11-20', 'feather condition check' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=26);
INSERT INTO visits (pet_id, visit_date, description) SELECT 25, '2024-12-15', 'weight management consultation' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=27);
INSERT INTO visits (pet_id, visit_date, description) SELECT 26, '2025-01-08', 'spayed' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=28);
INSERT INTO visits (pet_id, visit_date, description) SELECT 27, '2023-12-10', 'tick removal' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=29);
INSERT INTO visits (pet_id, visit_date, description) SELECT 28, '2024-01-25', 'claw trimming' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=30);
INSERT INTO visits (pet_id, visit_date, description) SELECT 29, '2024-02-28', 'teeth cleaning' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=31);
INSERT INTO visits (pet_id, visit_date, description) SELECT 30, '2024-03-15', 'general wellness exam' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=32);
INSERT INTO visits (pet_id, visit_date, description) SELECT 14, '2024-06-10', 'follow-up vaccination' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=33);
INSERT INTO visits (pet_id, visit_date, description) SELECT 15, '2024-07-05', 'post-surgery checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=34);
INSERT INTO visits (pet_id, visit_date, description) SELECT 16, '2024-08-12', 'dental surgery' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=35);
INSERT INTO visits (pet_id, visit_date, description) SELECT 17, '2024-09-20', 'blood work' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=36);
INSERT INTO visits (pet_id, visit_date, description) SELECT 18, '2024-10-18', 'post-neuter checkup' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=37);
INSERT INTO visits (pet_id, visit_date, description) SELECT 19, '2024-11-08', 'x-ray examination' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=38);
INSERT INTO visits (pet_id, visit_date, description) SELECT 20, '2024-12-01', 'medication refill' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=39);
INSERT INTO visits (pet_id, visit_date, description) SELECT 21, '2025-01-15', 'pain management' WHERE NOT EXISTS (SELECT * FROM visits WHERE id=40);