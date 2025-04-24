# Backend Application with Python and Redis

Backend API untuk manajemen user dengan Python (FastAPI) dan Redis sebagai database. Aplikasi ini dioptimalkan untuk menangani banyak request sekaligus.

## Fitur

- **User Management API**:
  - Create User
  - Get User by Email
  - Get All Users
  - Update User
  - Delete User
  - Bulk Create Users

## Struktur Data User

```json
{
  "id": "202504110016",
  "uuid": "91f5efac-b6c6-4917-9de3-10626c3e6d12",
  "name": "username",
  "email": "email@example.com",
  "password": "Password123",
  "balance": 0,
  "password_surfebe": "Password123",
  "cookie_surfebe": "",
  "secret2fa_surfebe": "",
  "userid_surfebe": "",
  "balance_surfebe": 0,
  "is_register_surfebe": 0,
  "is_login_surfebe": 0,
  "payeer_account": "",
  "payeer_password": "Password123",
  "payeer_master_key": "",
  "payeer_secret_key": "",
  "payeer_balance": 0,
  "payeer_cookie": "",
  "is_register_payeer": 0,
  "is_login_payeer": 0,
  "is_running": 0,
  "message": "",
  "created_at": "2025-04-11T00:16:51.303586711Z",
  "updated_at": "2025-04-18T22:59:18.941068951Z"
}
```

## Cara Menjalankan

### Menggunakan Docker Compose (Direkomendasikan)

1. Clone repositori ini
2. Pastikan Docker dan Docker Compose sudah terinstal
3. Sesuaikan file `.env` jika diperlukan
4. Jalankan aplikasi:

```bash
docker-compose up -d
```

### Menjalankan Secara Lokal

1. Clone repositori ini
2. Instal Redis di komputer lokal
3. Instal dependensi Python:

```bash
pip install -r requirements.txt
```

4. Sesuaikan file `.env` agar sesuai dengan konfigurasi Redis lokal
5. Jalankan aplikasi:

```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Create User

- **URL**: `/api/users/create`
- **Method**: POST
- **Payload**:
```json
{
  "name": "username",
  "email": "email@example.com",
  "password": "Password123"
}
```

### 2. Get User

- **URL**: `/api/users/get`
- **Method**: POST
- **Payload**:
```json
{
  "email": "email@example.com"
}
```

### 3. Get All Users

- **URL**: `/api/users`
- **Method**: GET

### 4. Update User

- **URL**: `/api/users/update`
- **Method**: POST
- **Payload**:
```json
{
  "user_query": {
    "email": "email@example.com"
  },
  "user_update": {
   "password": "Password123",
		"balance": 0,
		"password_surfebe": "163163013",
		"cookie_surfebe": "",
		"secret2fa_surfebe": "",
		"userid_surfebe": "",
		"balance_surfebe": 0
		 // Anda dapat mengupdate field apapun
  }
}
```

### 5. Delete User

- **URL**: `/api/users/delete`
- **Method**: DELETE
- **Payload**:
```json
{
  "email": "email@example.com"
}
```

### 6. Add Multiple Users

- **URL**: `/api/users/bulk-create`
- **Method**: POST
- **Payload**:
```json
{
  "data": [
    {
      "name": "user1",
      "email": "user1@example.com",
      "password": "Password123"
    },
    {
      "name": "user2",
      "email": "user2@example.com",
      "password": "Password456"
    }
  ]
}
```

## Optimalisasi untuk Banyak Request

Aplikasi ini dioptimalkan untuk menangani banyak request menggunakan:

1. **FastAPI**: Framework asinkron untuk performa tinggi
2. **Redis**: Database in-memory untuk akses data cepat
3. **Background Tasks**: Memproses operasi bulk di background
4. **Asynchronous Processing**: Memanfaatkan asyncio untuk operasi massal
