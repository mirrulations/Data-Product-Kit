echo ---SQL---
echo Querying SQL
python3 sql/Query.py "SELECT d.docket_title , c.comment, c.comment_id FROM dockets AS d JOIN comments AS c ON c.docket_id = d.docket_id;"

echo
echo ---OpenSearch---
echo Querying OpenSearch
python3 opensearch/query.py
