@echo off

where openssl >nul 2>&1
if errorlevel 1 (
    echo [ERROR] OpenSSL not found.
    exit /b 1
)

if not exist "certs/jwt-private.pem" (
    openssl genrsa -out certs/jwt-private.pem 2048
    if errorlevel 1 (
        echo [ERROR] Error generating private key.
        exit /b 1
    )
)

if not exist "certs/jwt-public.pem" (
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
    if errorlevel 1 (
        echo [ERROR] Error generating public key.
        exit /b 1
    )
)