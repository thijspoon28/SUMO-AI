@echo off
:: Check if certificate exists
if not exist nginx\certs\nginx.crt (
    echo Certificate not found. Generating new certificate...
    
    :: Create certs directory if it doesn't exist
    if not exist nginx\certs mkdir nginx\certs
    
    :: Run openssl command to generate certificates
    "C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout nginx\certs\nginx.key -out nginx\certs\nginx.crt -days 365 -nodes
    
    echo Certificate generated successfully.
) else (
    echo Certificate found. Building application...
)

:: Continue with the original script
cd frontend
call npm run build-only
cd ..
docker compose up --build
