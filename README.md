# Kumpulan Docker Compose

## Install CasaOs
```
curl -fsSL https://get.casaos.io | sudo bash
```

Repositori ini berisi kumpulan file Docker Compose untuk berbagai layanan.

## Daftar Layanan

### 1. Recaptcha Solver
**URL**: `http://IP:3000/status`

```yaml
version: '3'
services:
  captcha-solver:
    container_name: captcha-solver
    labels:
      icon: https://raw.githubusercontent.com/adamsetiaji/list-logo/refs/heads/main/recaptcha-solver.png
    image: adamsetiaji/captcha-solver:latest
    ports:
      - "3000:3000"
    restart: always
    environment:
      - STATUS_FILE=status.json
      - TIME_VALID_GRESPONSE=110
      - TIME_RELOAD_GRESPONSE=600
      - WEBSITE_URL=https://surfe.be
      - WEBSITE_KEY=6LfMEAwTAAAAAK5MkDsHyDg-SE7wisIDM1-5mDQs
      - CAPSOLVER_API_KEY=CAP-921B178849E6366D5D57165C2D4C9F51C620A8155696A497CBA21AB82423DB45
x-casaos:
  author: self
  category: self
  hostname: ""
  icon: https://raw.githubusercontent.com/adamsetiaji/list-logo/refs/heads/main/recaptcha-solver.png
  index: /status
  is_uncontrolled: false
  port_map: "3000"
  scheme: http
  title:
    custom: Recaptcha Solver
    en_us: captcha-solver
```

### 2. Mongo Express & MongoDB
- **Mongo Express**: Port 8081
- **MongoDB**: Port 27017
- **URL**: `http://IP:8081`

```yaml
version: '3.8'
services:
  mongo-express:
    container_name: mongo-express
    environment:
      - ME_CONFIG_BASICAUTH_USERNAME=admin
      - ME_CONFIG_BASICAUTH_PASSWORD=KeminMencret2219

      - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
      - ME_CONFIG_MONGODB_ADMINPASSWORD=KeminMencret2219
      - ME_CONFIG_MONGODB_URL=mongodb://admin:KeminMencret2219@host.docker.internal:27017/
    image: mongo-express:latest
    ports:
      - target: 8081
        published: "8081"
        protocol: tcp
    restart: unless-stopped
    network_mode: bridge
    extra_hosts:
      - "host.docker.internal:host-gateway"

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: KeminMencret2219
    volumes:
      - /DATA/AppData/mongodb_data:/data/db
      - /DATA/AppData/mongodb_config:/data/configdb
    restart: unless-stopped
    network_mode: bridge
    
x-casaos:
  index: /
  port_map: "8081"
  scheme: http
  title:
    custom: Mongo Express & MongoDB
    en_us: Mongo Express & MongoDB

```

### 3. Captcha Service
- **Captcha Service**: Port 4000
- **URL**: `http://IP:4000`

```yaml
version: '3.8'

services:
  captcha-service:
    container_name: captcha-service
    image: adamsetiaji/captcha-service:latest
    ports:
      - "4000:4000"
    restart: always
    environment:
      - PORT=4000
      - CAPTCHA_SOLVER_URL=http://host.docker.internal:3000/status
      - DEBUG=True
    network_mode: bridge
    extra_hosts:
      - "host.docker.internal:host-gateway"

x-casaos:
  hostname: ""
  index: /status
  port_map: "4000"
  scheme: http
  title:
    custom: Captcha Service
    en_us: captcha-service
```

### 4. Task Dashboard & User Management
- **Task Dashboard**: Port 5500-5510
- **User Management**: Port 5000-5010
- **URL**: `http://IP:5500-5510`

```yaml
version: '3.8'

services:
  task-dashboard-3:
    image: adamsetiaji/task-dashboard:latest
    container_name: task-dashboard-3
    restart: unless-stopped
    ports:
      - "5502:5502"
    environment:
      - BASE_URL=http://host.docker.internal:5002
      - CAPTCHA_SERVER=http://host.docker.internal:4000/status
      - PORT=5502
      - FLASK_ENV=production
    networks:
      - bridge
    depends_on:
      - user-management-3
    extra_hosts:
      - host.docker.internal:host-gateway

  user-management-3:
    image: adamsetiaji/user-management:latest
    container_name: user-management-3
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
    ports:
      - "5002:5002"
    environment:
      - HOST=0.0.0.0
      - PORT=5002
      - MONGODB_HOST=host.docker.internal
      - MONGODB_PORT=27017
      - MONGODB_USERNAME=admin
      - MONGODB_PASSWORD=KeminMencret2219
      - MONGODB_DATABASE=user-management-3
      - LOG_LEVEL=INFO
      - VERSION_SURFEBE=182
    restart: unless-stopped
    networks:
      - bridge
    extra_hosts:
      - host.docker.internal:host-gateway

networks:
  bridge:
    driver: bridge

x-casaos:
  port_map: "5502"
  scheme: http
  title:
    custom: Task Management System-3
    en_us: Task Management System-3
```

## Catatan Penggunaan

1. Ganti `{NUMBER}` dengan nomor spesifik untuk instance multiple
2. Ganti `{IP-USER-MANAGEMENT}` dan `{PORT-USER-MANAGEMENT}` dengan IP dan port yang sesuai
3. Ganti `{IP-CAPTCHA-SERVICE}` dan `{PORT-CAPTCHA-SERVICE}` dengan IP dan port yang sesuai
4. Sesuaikan environment variables sesuai kebutuhan
5. Pastikan semua dependensi antar service sudah dikonfigurasi dengan benar

## Konvensi Port

- Recaptcha Solver: 3000
- Redis Insight: 5540
- Captcha Service: 4000
- Redis Database: 6379
- User Management: 5000-5010
- Task Dashboard: 6000-6010

## Lisensi

[Tambahkan informasi lisensi di sini]
