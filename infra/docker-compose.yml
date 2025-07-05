version: "3.9"

services:
  # ─────────────────────────────────────────── Gateway Dummy
  gateway:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./gateway-dummy:/app          # tu index.js está aquí
    command: >
      sh -c "
        test -f package.json || npm init -y &&
        npm install apollo-server graphql node-fetch@2 &&
        node index.js
      "
    environment:
      - REST_PRESENTACIONES_URL=http://host.docker.internal
    ports:
      - "4000:4000"

  # ─────────────────────────────────────────── WS-logger
  wslogger:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./ws-logger:/app
    command: >
      sh -c "
        test -f package.json || npm init -y &&
        npm install express ws &&
        node index.js
      "
    ports:
      - "9000:9000"
