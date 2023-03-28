curl -X POST -H "Content-Type: application/json" \
-d '{"Aspect": ["Trustworthiness", "Human"]}' \
http://127.0.0.1:3000/extract -o truncated.owl

