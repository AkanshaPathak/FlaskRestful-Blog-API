
-- Sample data for Testing

-- Create Users 

INSERT INTO raxoweb.users (public_id,username,password,email,admin,is_active) VALUES 
('72684b24-b5d4-4d19-a6ce-b1e1ef4b65da','bipul','sha256$LgpZCoGu$ffad7d0ee97b95c069d45d6a3a8e580ed7451a632ec8e4e46fc76c3a4b1481dd','kumarbipulsingh@gmail.com',0,1)
,('d51d0ddf-5f57-46d6-bef2-0450eee58eef','bipul','sha256$ibnR61kn$3abc900e8180c29529a64e17dc214829bb7a1cf28ba8be6d6c31c5a98cebd72a','bipulsinghkashyap@gmail.com',0,1)
,('18747cdf-4f3b-4bea-8eb0-91de6606b076','bipul','sha256$a61EyK2I$e24fc21900349562d3d628ed36692644b3f182b6d07f5723b821691e0805b896','bksingh@gmail.com',0,1)
;

-- contact information

INSERT INTO raxoweb.ContactUs (firstname,lastname,email,mobile_no,message) VALUES 
('bipul','singh','kumarbipulsingh@gmail.com',0000000000,'testing message')
;

-- Reset Hash to change password

INSERT INTO raxoweb.ResetHash (email,hash) VALUES 
('kumarbipulsingh@gmail.com','c2h56a7n3d25a1n95b4d9702c71b3ef27aab5252b60e2699c94h6a78i42n91a73n58i')
;


-- OTP

INSERT INTO raxoweb.validate_code (email,code,expiretime) VALUES 
('bipulsinghkashyap@gmail.com',2435,'2020-08-26 03:02:53')
;