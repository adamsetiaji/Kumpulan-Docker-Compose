# Kumpulan Docker Compose

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
version: '3'
services:
  task-dashboard:
    container_name: task-dashboard-{NUMBER}
    image: adamsetiaji/task-dashboard:latest
    ports:
      - "6000:6000" # 6000-6010
    restart: always
    environment:
      - PORT=6000 # 6000-6010
      - BASE_URL=http://{IP-USER-MANAGEMENT}:{PORT-USER-MANAGEMENT} 
      - CAPTCHA_SERVER=http://{IP-CAPTCHA-SERVICE}:{PORT-CAPTCHA-SERVICE}/status
  user-management:
    container_name: user-management
    image: adamsetiaji/user-management:latest
    ports:
      - "5000:5000" # 5000-5010
    environment:
      # Server Configuration
      - HOST=0.0.0.0
      - PORT=5000 # 5000-5010
      # Redis Configuration
      - DIS_HOST=172.17.0.1  # IP Host Docker
      - DIS_PORT=6379  # Port Redis Database
      - REDIS_PASSWORD=
      - REDIS_DB=0
      # Application Settings
      - LOG_LEVEL=INFO
      # Surfebe Settings
      - VERSION_SURFEBE=182
    volumes:
      - redis_data:/data
    restart: unless-stopped
volumes:
  redis_data:
x-casaos:
  is_uncontrolled: false
  port_map: "6000" # 6000-6010
  scheme: http
  title:
    custom: Task Dashboard {NUMBER}
    en_us: task-dashboard-{NUMBER}
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
