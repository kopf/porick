mysqldump -u root -p chirpy --tables chirpy_tags chirpy_quote_tag chirpy_quotes > chirpy_dump.sql
echo "rename table chirpy_tags TO tags; rename table chirpy_quotes to quotes;rename table chirpy_quote_tag to
quote_to_tag;" >> chirpy_dump.sql
mysql -u root -p porick < chirpy_dump.sql
paster setup-app production.ini
rm -f chirpy_dump.sql

