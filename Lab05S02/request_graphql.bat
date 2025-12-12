curl -w "\nTime: %{time_total}s | Size: %{size_download} bytes\n" -s -X POST http://localhost:4000/graphql -H "Content-Type: application/json" -d "{\"query\":\"{ users { id name email } }\"}"
pause
