content=$(cat 20211112-10188-server828491_sscms.sql)
curl -X "PUT" \
     -H "Accept: application/vnd.github+json" \
     -H "Authorization: token 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" \
               https://api.github.com/repos/blueface5/getAcc/sql.txt \
               -d '{
               "content":"${content}"}
               }'
