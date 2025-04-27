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

### 2. Redis Insight
**URL**: `http://IP:5540` | `http://IP:3030`

```yaml
version: '3.8'
services:
  redisinsight:
    image: redis/redisinsight:latest
    container_name: redisinsight
    ports:
      - "5540:5540"
    restart: unless-stopped
x-casaos:
  icon: https://icon.casaos.io/main/all/redis.png
  port_map: "5540"
  scheme: http
  title:
    custom: Redis Insight
    en_us: redis-insight
```

### 3. Captcha Service & Redis Database
- **Captcha Service**: Port 4000
- **Redis**: Port 6379 | 3737
- **URL**: `http://IP:4000`

```yaml
version: '3'
services:
  captcha-service:
    container_name: captcha-service
    image: adamsetiaji/captcha-service:latest
    ports:
      - "4000:4000"
    restart: always
    environment:
      - PORT=4000
      - CAPTCHA_SOLVER_URL=http://IP:PORT/status
      - DEBUG=True
  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
volumes:
  redis_data:
x-casaos:
  author: self
  category: self
  hostname: ""
  index: /status
  is_uncontrolled: false
  port_map: "4000"
  scheme: http
  title:
    custom: Captcha Service
    en_us: captcha-service
```

### 4. Task Dashboard & User Management
- **Task Dashboard**: Port 6000-6010
- **User Management**: Port 5000-5010
- **URL**: `http://IP:6000-6010`

```yaml
version: '3.8'

services:
  task-dashboard-1:
    image: adamsetiaji/task-dashboard:latest
    container_name: task-dashboard-1
    restart: unless-stopped
    ports:
      - "5500:5500"
    environment:
      - BASE_URL=http://141.95.17.202:5000
      - CAPTCHA_SERVER=http://141.95.17.202:4000/status
      - PORT=5500
      - FLASK_ENV=production
    networks:
      - app-network
    depends_on:
      - user-management-1

  user-management-1:
    image: adamsetiaji/user-management:latest
    container_name: user-management-1
    ports:
      - "5000:5000"
    environment:
      - HOST=0.0.0.0
      - PORT=5000
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=
      - REDIS_DB=0
      - LOG_LEVEL=INFO
      - VERSION_SURFEBE=182
    restart: unless-stopped
    networks:
      - app-network
      - default
    external_links:
      - redis

networks:
  app-network:
    driver: bridge
  default:
    external: true
    name: bridge

x-casaos:
  port_map: "5500"
  scheme: http
  title:
    custom: Task Management System 1
    en_us: Task Management System 1
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
