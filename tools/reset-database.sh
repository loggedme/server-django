find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "*/db.sqlite3" -delete
pip uninstall django -y
pip install django
python manage.py makemigrations
python manage.py migrate

sqlite3 "db.sqlite3" "
INSERT INTO user_user(id, email, password, username, name, handle, account_type, profile_image, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
VALUES
    ('$(uuidgen)', 'person@likelion.org', 'admin', '1', '홍길동', 'person', 1, '.', FALSE, '.', '.', FALSE, TRUE, DATETIME('now', 'localtime')),
    ('$(uuidgen)', 'business@likelion.org', 'admin', '2', '정부', 'business', 2, '.', FALSE, '.', '.', FALSE, TRUE, DATETIME('now', 'localtime'));
"

sqlite3 "db.sqlite3" "
INSERT INTO feed_post(id, created_at, modified_at, created_by_id, tagged_user_id, content)
VALUES
('$(uuidgen)', DATETIME('now', 'localtime'), DATETIME('now', 'localtime'), (SELECT id FROM user_user WHERE account_type = 1 LIMIT 1), (SELECT id FROM user_user WHERE account_type = 2 LIMIT 1), 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'),
('$(uuidgen)', DATETIME('now', 'localtime'), DATETIME('now', 'localtime'), (SELECT id FROM user_user WHERE account_type = 1 LIMIT 1), (SELECT id FROM user_user WHERE account_type = 2 LIMIT 1), '\"많은 사람들이 더 쉽고 편안하게 사용할 수 있는 가치 있는 소프트웨어를 창조합니다\"

동영상 편집 어플리케이션 1위 VLLO(블로)를 서비스하고 있는 비모소프트는 눈에 띄는 성장을 거듭하며 현재 전 세계 약 220개국에 진출하여 글로벌 기업으로 도약하고 있습니다

2022년 비모소프트는 두 번째 서비스 론칭을 앞두고 있습니다
사용자에게 최고의 경험을 제공하는 소프트웨어를 만들어나갈 동료를 기다립니다

http://www.vimosoft.com');
"