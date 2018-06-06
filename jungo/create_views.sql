USE django_db;

CREATE OR REPLACE VIEW jungo_userinfo
AS
SELECT username, student_id, phone_no, email
FROM jungo_student
INNER JOIN auth_user
ON jungo_student.user_ptr_id = auth_user.id;

CREATE OR REPLACE VIEW jungo_wishinfo
AS
SELECT username, pid, pname, price, prodType
FROM jungo_product
INNER JOIN jungo_wishlist_buyer
ON jungo_product.pid = jungo_wishlist_buyer.wishlist_id
INNER JOIN jungo_student
ON jungo_wishlist_buyer.student_id = jungo_student.student_id
INNER JOIN auth_user
ON jungo_student.user_ptr_id = auth_user.id;

CREATE OR REPLACE VIEW jungo_sellinfo
AS
SELECT username, pid, pname, price, prodType
FROM jungo_product
INNER JOIN jungo_selllist_seller
ON jungo_product.pid = jungo_selllist_seller.selllist_id
INNER JOIN jungo_student
ON jungo_selllist_seller.student_id = jungo_student.student_id
INNER JOIN auth_user
ON jungo_student.user_ptr_id = auth_user.id;
    
CREATE OR REPLACE VIEW jungo_matchinfo1
AS
SELECT jungo_matchlist_buyer.student_id as buyer_id,
       jungo_matchlist_seller.student_id as seller_id,
       pid, pname, price
FROM jungo_matchlist_buyer
INNER JOIN jungo_product
ON jungo_product.pid = jungo_matchlist_buyer.matchlist_id
INNER JOIN jungo_matchlist_seller
ON jungo_product.pid = jungo_matchlist_seller.matchlist_id;

CREATE OR REPLACE VIEW jungo_matchinfo2
AS
SELECT username as buyername, seller_id, pid, pname, price
FROM jungo_userinfo
INNER JOIN jungo_matchinfo1
ON jungo_userinfo.student_id = jungo_matchinfo1.buyer_id;

CREATE OR REPLACE VIEW jungo_matchinfo
AS
SELECT username as sellername, buyername, pid, pname, price
FROM jungo_userinfo
INNER JOIN jungo_matchinfo2
ON jungo_userinfo.student_id = jungo_matchinfo2.seller_id;
