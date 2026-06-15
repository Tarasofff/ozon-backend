# GENERATE PRIVATE KEY
openssl genrsa -out jwt-private.pem 2048

# GENERATE PUBLIC KEY
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem