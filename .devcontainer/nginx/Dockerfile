FROM nginx:alpine

# Define build arguments for SSL certificate options
ARG SSL_DAYS=365
ARG SSL_SUBJECT="/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

# Install OpenSSL
RUN apk add --no-cache openssl

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# 1. Generate private Root CA (key and certificate)
RUN openssl req -x509 -new -nodes -days ${SSL_DAYS} \
    -keyout /etc/nginx/ssl/ca.key \
    -out /etc/nginx/ssl/ca.crt \
    -subj "/CN=My-Local-Root-CA"

# 2. Generate server private key and CSR (Certificate Signing Request)
RUN openssl req -new -nodes \
    -keyout /etc/nginx/ssl/server.key \
    -out /etc/nginx/ssl/server.csr \
    -subj ${SSL_SUBJECT}

# 3. Create SAN (Subject Alternative Name) config file to suppress browser warnings
RUN echo "authorityKeyIdentifier=keyid,issuer" > /etc/nginx/ssl/san.ext && \
    echo "basicConstraints=CA:FALSE" >> /etc/nginx/ssl/san.ext && \
    echo "keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment" >> /etc/nginx/ssl/san.ext && \
    echo "subjectAltName = @alt_names" >> /etc/nginx/ssl/san.ext && \
    echo "[alt_names]" >> /etc/nginx/ssl/san.ext && \
    echo "DNS.1 = localhost" >> /etc/nginx/ssl/san.ext && \
    echo "IP.1 = 127.0.0.1" >> /etc/nginx/ssl/san.ext

# 4. Issue server certificate signed by the private Root CA
RUN openssl x509 -req -in /etc/nginx/ssl/server.csr \
    -CA /etc/nginx/ssl/ca.crt \
    -CAkey /etc/nginx/ssl/ca.key \
    -CAcreateserial \
    -out /etc/nginx/ssl/server.crt \
    -days ${SSL_DAYS} -sha256 \
    -extfile /etc/nginx/ssl/san.ext

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
