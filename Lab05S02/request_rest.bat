curl -w "\nTime: %{time_total}s | Size: %{size_download} bytes\n" -s http://localhost:4000/api/users
pause
