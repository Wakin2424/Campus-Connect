INSERT INTO qa (user_id, course_id, question, description, answers, views, likes, subjects, created_at)
VALUES
-- 1
(1, 2, 
 'What is the difference between TCP and UDP?',
 'I am struggling to understand the reliability and speed trade-offs between these two protocols.',
 '[{"user_id": 3, "answer": "TCP is connection-oriented, reliable but slower."}, 
   {"user_id": 5, "answer": "UDP is faster but does not guarantee delivery."}]',
 45, 12, '["Networking","Protocols"]', NOW()),

-- 2
(2, 3,
 'Explain the concept of polymorphism in OOP.',
 'Looking for real-life examples and how it is applied in Java.',
 '[{"user_id": 4, "answer": "Polymorphism allows objects to take many forms, for example method overriding."},
   {"user_id": 1, "answer": "In Java, you can have multiple classes implement the same interface differently."},
   {"user_id": 6, "answer": "Think of a single remote controlling different devices – that is polymorphism conceptually."}]',
 62, 21, '["OOP","Java"]', NOW()),

-- 3
(3, 1,
 'What is normalization in databases?',
 'I need a simple explanation of the first three normal forms.',
 '[{"user_id": 2, "answer": "Normalization reduces data redundancy by organizing data into related tables."}]',
 25, 8, '["Database","Normalization"]', NOW()),

-- 4
(4, 4,
 'Difference between supervised and unsupervised learning?',
 'Trying to figure out when to use which approach in ML.',
 '[{"user_id": 5, "answer": "Supervised uses labeled data, unsupervised uses unlabeled data."},
   {"user_id": 7, "answer": "Clustering is an example of unsupervised, regression is supervised."}]',
 78, 33, '["Machine Learning","AI"]', NOW()),

-- 5
(1, 2,
 'Explain recursion with an example.',
 'I find it confusing when a function calls itself.',
 '[{"user_id": 3, "answer": "A common example is calculating factorials recursively."}]',
 40, 15, '["Programming","Algorithms"]', NOW()),

-- 6
(2, 3,
 'What is an API and how does it work?',
 'I see this term everywhere but still unclear what it exactly means.',
 '[{"user_id": 6, "answer": "An API is a set of rules that lets software programs communicate with each other."},
   {"user_id": 4, "answer": "Think of it as a waiter taking your order and bringing food from the kitchen."}]',
 101, 50, '["Software Engineering","Web Development"]', NOW()),

-- 7
(5, 1,
 'Difference between GET and POST in HTTP?',
 'Is one more secure than the other?',
 '[{"user_id": 3, "answer": "GET appends data to the URL, POST sends data in the body."}]',
 56, 22, '["Web Development","HTTP"]', NOW()),

-- 8
(6, 2,
 'What is Big O notation?',
 'Trying to understand time complexity of algorithms.',
 '[{"user_id": 1, "answer": "Big O describes how runtime grows relative to input size."},
   {"user_id": 2, "answer": "O(n) means runtime grows linearly with input."},
   {"user_id": 4, "answer": "O(1) means constant time, regardless of input size."}]',
 93, 41, '["Algorithms","Complexity Analysis"]', NOW()),

-- 9
(3, 4,
 'What is the difference between RAM and ROM?',
 'Need an easy explanation for my exam.',
 '[{"user_id": 5, "answer": "RAM is volatile, ROM is non-volatile and stores firmware."}]',
 30, 12, '["Computer Architecture","Memory"]', NOW()),

-- 10
(4, 3,
 'Explain foreign keys in SQL.',
 'How do they maintain data integrity?',
 '[{"user_id": 6, "answer": "Foreign keys ensure that a value in one table matches a primary key in another table."},
   {"user_id": 2, "answer": "They help maintain referential integrity."}]',
 70, 27, '["Database","SQL"]', NOW());
