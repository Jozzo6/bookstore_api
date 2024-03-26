INSERT INTO users (id, created, updated, email, first_name, last_name, type, password_hash)
VALUES 
  ('550e8400-e29b-41d4-a716-446655440000', NOW(), NOW(), 'john@example.com', 'John', 'Doe', 'admin', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi'),
  ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', NOW(), NOW(), 'jane@example.com', 'Jane', 'Smith', 'librarian', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi'),
  ('550e8400-e29b-41d4-a716-446655440001', NOW(), NOW(), 'robert@example.com', 'Robert', 'Johnson', 'user', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi'),
  ('550e8400-e29b-41d4-a716-446655440002', NOW(), NOW(), 'alice@example.com', 'Alice', 'Brown', 'user', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi'),
  ('550e8400-e29b-41d4-a716-446655440003', NOW(), NOW(), 'charlie@example.com', 'Charlie', 'Taylor', 'user', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi'),
  ('550e8400-e29b-41d4-a716-446655440004', NOW(), NOW(), 'emily@example.com', 'Emily', 'Anderson', 'user', '$2b$12$t6lklpVWbH2G4q8v.wa50OT7ddh4m5oREa3MyWEAyW6xLwmSuV9mi');

INSERT INTO books (id, isbn, created, updated, title, author, year, publisher, quantity)
VALUES 
  ('550e8400-e29b-41d4-a716-446655440012', '978-3-16-148410-0', NOW(), NOW(), 'The Great Adventure', 'John Doe', 2001, 'Starlight Publishing', 1),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432c8', '978-1-86197-271-5', NOW(), NOW(), 'Journey to the Unknown', 'Jane Smith', 2002, 'Oceanview Books', 2),
  ('550e8400-e29b-41d4-a716-446655440013', '978-0-262-13472-9', NOW(), NOW(), 'The Lost World', 'Robert Johnson', 2003, 'Mountain Peak Press', 1),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432c9', '978-1-56619-909-4', NOW(), NOW(), 'The Secret Garden', 'Alice Brown', 2004, 'Silver Leaf Publications', 4),
  ('550e8400-e29b-41d4-a716-446655440014', '978-1-84356-028-9', NOW(), NOW(), 'Mystery of the Old House', 'Charlie Taylor', 2005, 'Golden Quill Publishers', 5),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432ca', '978-1-86197-876-2', NOW(), NOW(), 'The Last Frontier', 'Emily Anderson', 2006, 'Riverstone Books', 1),
  ('550e8400-e29b-41d4-a716-446655440015', '978-0-7475-3269-2', NOW(), NOW(), 'The Hidden Treasure', 'John Doe', 2007, 'Sunrise Publications', 2),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432cb', '978-0-563-38497-7', NOW(), NOW(), 'The Silent Whisper', 'Jane Smith', 2008, 'Moonbeam Publishing', 3),
  ('550e8400-e29b-41d4-a716-446655440016', '978-1-85702-901-3', NOW(), NOW(), 'The Mysterious Island', 'Robert Johnson', 2009, 'Whispering Pines Press', 6),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432cc', '978-1-86197-610-2', NOW(), NOW(), 'The Forgotten Past', 'Alice Brown', 2010, 'Crystal Clear Publishers', 3),
  ('550e8400-e29b-41d4-a716-446655440017', '978-3-16-148411-0', NOW(), NOW(), 'The Hidden Truth', 'Charlie Taylor', 2011, 'Autumn Leaves Books', 2),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432cd', '978-1-86197-272-5', NOW(), NOW(), 'The Enchanted Forest', 'Emily Anderson', 2012, 'Spring Blossom Press', 1),
  ('550e8400-e29b-41d4-a716-446655440018', '978-0-262-13473-9', NOW(), NOW(), 'The Secret Passage', 'John Doe', 2013, 'Twilight Publishing', 1),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432ce', '978-1-56619-904-4', NOW(), NOW(), 'The Haunted House', 'Jane Smith', 2014, 'Rainbow Bridge Publications', 1),
  ('550e8400-e29b-41d4-a716-446655440019', '978-1-84356-025-9', NOW(), NOW(), 'The Lost City', 'Robert Johnson', 2015, 'Evergreen Publishers', 1),
  ('6ba7b810-9dad-11d1-80b4-00c04fd432cf', '978-1-86197-876-2', NOW(), NOW(), 'The Forbidden Castle', 'Alice Brown', 2016, 'Blue Sky Books', 1),
  ('550e8400-e29b-41d4-a716-446655440020', '978-0-7475-3267-2', NOW(), NOW(), 'The Golden Key', 'Charlie Taylor', 2017, 'Sunflower Press', 1);