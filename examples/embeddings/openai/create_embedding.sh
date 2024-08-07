curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is flask?",
    "model": "text-embedding-ada-002",
    "encoding_format": "float"
  }'
