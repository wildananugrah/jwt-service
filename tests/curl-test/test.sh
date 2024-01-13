echo "================================================================"
echo "creating token..."

response=$(curl -X POST -H "Content-Type: application/json" -d '{ "username":"wildananugrah", "age":32 }' 'http://localhost:5000/token')

echo "response: " $response

token=$(echo $response | jq -r '.token')

echo "================================================================"
echo "validating token..."
if [ -z $token ]; then
    echo "token not found"
    exit 1
else
    response=$(curl -X POST -H "Content-Type: application/json" -d '{"token": "'$token'"}' 'http://localhost:5000/validate')
    echo "response: " $response
fi

echo "================================================================"
echo "refresing token..."
if [ -z $token ]; then
    echo "token not found"
    exit 1
else
    response=$(curl -X POST -H "Content-Type: application/json" -d '{"token": "'$token'"}' 'http://localhost:5000/refresh')
    echo "response: " $response
fi