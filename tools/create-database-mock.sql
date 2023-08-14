BEGIN TRANSACTION;
INSERT INTO "user_user" ("password","last_login","is_superuser","username","first_name","last_name","is_staff","is_active","date_joined","id","email","name","handle","account_type","profile_image") VALUES ('admin',NULL,0,'1','.','.',0,1,'2023-08-12 04:17:28','017867072f5247348f994e8d1d6ffae3','person@likelion.org','홍길동','person',1,'.');
INSERT INTO "user_user" ("password","last_login","is_superuser","username","first_name","last_name","is_staff","is_active","date_joined","id","email","name","handle","account_type","profile_image") VALUES ('admin',NULL,0,'2','.','.',0,1,'2023-08-12 04:17:28','14b60ac57bd746d792bf15559fdf8032','business@likelion.org','정부','business',2,'.');
INSERT INTO "feed_post" ("id","content","created_at","modified_at","created_by_id","tagged_user_id") VALUES ('a6feebde4b9c403f9888de2168d7906b','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','2023-08-12 04:17:28','2023-08-12 04:17:28','017867072f5247348f994e8d1d6ffae3','14b60ac57bd746d792bf15559fdf8032');
INSERT INTO "feed_post" ("id","content","created_at","modified_at","created_by_id","tagged_user_id") VALUES ('3f60735d15364885932af9c151960444','"많은 사람들이 더 쉽고 편안하게 사용할 수 있는 가치 있는 소프트웨어를 창조합니다"

동영상 편집 어플리케이션 1위 VLLO(블로)를 서비스하고 있는 비모소프트는 눈에 띄는 성장을 거듭하며 현재 전 세계 약 220개국에 진출하여 글로벌 기업으로 도약하고 있습니다

2022년 비모소프트는 두 번째 서비스 론칭을 앞두고 있습니다
사용자에게 최고의 경험을 제공하는 소프트웨어를 만들어나갈 동료를 기다립니다

http://www.vimosoft.com','2023-08-12 04:17:28','2023-08-12 04:17:28','017867072f5247348f994e8d1d6ffae3','14b60ac57bd746d792bf15559fdf8032');
INSERT INTO "feed_comment" ("id","content","created_at","created_by_id","post_id") VALUES ('0aa8d2957f55430aa3ebf817cac22d85','댓글입니다.','2023-08-12 04:17:28','14b60ac57bd746d792bf15559fdf8032','a6feebde4b9c403f9888de2168d7906b');
COMMIT;
