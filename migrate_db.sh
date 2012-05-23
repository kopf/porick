#!/bin/sh
# Populate porick's database with data from an existing Chirpy! installation

# Insert the MySQL password for porick here
PWD=''

cat <<EOF | mysql -u root
CREATE DATABASE IF NOT EXISTS porick;
GRANT ALL PRIVILEGES ON porick.* TO 'porick'@'localhost' IDENTIFIED BY '$PWD';
FLUSH PRIVILEGES;
EOF

cat <<EOF | mysql -u root porick
$(mysqldump -u root u_chirpy --tables chirpy_tags chirpy_quote_tag chirpy_quotes)
RENAME TABLE chirpy_tags TO tags;
RENAME TABLE chirpy_quotes TO quotes;
RENAME TABLE chirpy_quote_tag to quote_to_tag;
ALTER TABLE quotes ADD COLUMN status tinyint(1) NOT NULL DEFAULT 0;
UPDATE quotes SET status=0 WHERE approved=0;
UPDATE quotes SET status=1 WHERE approved=1;
UPDATE quotes SET status=3 WHERE flagged=1;
ALTER TABLE quotes DROP COLUMN flagged;
ALTER TABLE quotes DROP COLUMN approved;
EOF

paster setup-app production.ini
