# Bella-Bank

Bella-Bank es una API backend para gestión bancaria y financiera desarrollada con Node.js, Express y SQLite. El proyecto incluye autenticación con JWT, control de roles, gestión de saldo, inversiones, cheques/facturas y compras de un catálogo de productos.

## Descripción

La aplicación simula un sistema bancario con estas funcionalidades principales:

- Registro e inicio de sesión de usuarios
- Autenticación con JWT y refresh tokens
- Control de acceso por roles (`USER`, `EDITOR`, `ADMIN`)
- Consulta de saldo
- Depósitos
- Inversiones con vencimiento
- Emisión y cobro de cheques/facturas
- Compra de productos desde un catálogo
- Protección contra abuso con rate limiting
- Validación de payloads con Zod

## Stack tecnológico

- Node.js
- TypeScript
- Express
- SQLite (better-sqlite3)
- JWT
- bcrypt
- Zod
- express-rate-limit

## Estructura de la carpeta

```text
Bella-Bank/
├── src/
│   ├── config/
│   │   └── env.ts
│   ├── controllers/
│   │   ├── authController.ts
│   │   ├── bankController.ts
│   │   └── shopController.ts
│   ├── db/
│   │   └── database.ts
│   ├── middleware/
│   │   ├── authMiddleware.ts
│   │   ├── bankService.ts
│   │   ├── rateLimiter.ts
│   │   └── validate.ts
│   ├── models/
│   │   └── User.ts
│   ├── routes/
│   │   ├── authRoutes.ts
│   │   ├── bankRoutes.ts
│   │   └── shopRoutes.ts
│   ├── services/
│   │   ├── authService.ts
│   │   ├── bankService.ts
│   │   └── shopService.ts
│   └── index.ts
├── package.json
├── tsconfig.json
├── BellaBank.postman_collection.json
├── result.txt
├── demo
├── test
└── ...
```

## Requisitos

- Node.js 18 o superior
- npm

## Instalación

```bash
npm install
```

## Variables de entorno

Crea un archivo `.env` en la raíz de `Bella-Bank` con este contenido:

```env
PORT=3000
JWT_SECRET=tu_clave_super_secreta
JWT_REFRESH_SECRET=tu_clave_de_refresh
ACCESS_TOKEN_TTL=15m
REFRESH_TOKEN_TTL=7d
BCRYPT_ROUNDS=12
DB_PATH=./bella-bank.db
```

## Scripts disponibles

```bash
npm run dev
```

Inicia la API en modo desarrollo con recarga automática.

```bash
npm run build
```

Compila el proyecto TypeScript.

```bash
npm start
```

Ejecuta la versión compilada.

## Endpoints de la API

### Autenticación

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`

### Banco

- `GET /api/bank/balance`
- `POST /api/bank/deposit`
- `POST /api/bank/invest`
- `GET /api/bank/invest/check`
- `GET /api/bank/bills/mine`
- `GET /api/bank/bills/:id`
- `POST /api/bank/bills`
- `POST /api/bank/bills/redeem`

### Tienda

- `GET /api/shop/catalog`
- `POST /api/shop/purchase`
- `POST /api/shop/items`

### Salud

- `GET /health`

## Ejemplo de uso

### Registro de usuario

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"123456"}'
```

### Login

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"123456"}'
```

### Ver saldo

```bash
curl -X GET http://localhost:3000/api/bank/balance \
  -H "Authorization: Bearer <accessToken>"
```

### Depositar dinero

```bash
curl -X POST http://localhost:3000/api/bank/deposit \
  -H "Authorization: Bearer <accessToken>" \
  -H "Content-Type: application/json" \
  -d '{"amountCents":5000}'
```

## Seguridad

El proyecto incluye medidas básicas de seguridad, como:

- JWT para autenticación
- Refresh tokens almacenados con hash
- Validación de entrada con Zod
- Rate limiting para login y API general
- Control de roles (`RBAC`)
- Verificación de propiedad de recursos para evitar IDOR
- CORS restringido a orígenes locales permitidos

## Base de datos

La API usa SQLite con una base de datos local. Al arrancar se crean automáticamente las tablas necesarias:

- `users`
- `accounts`
- `investments`
- `refresh_tokens`
- `shop_items`
- `bills`

## Notas

Este módulo está pensado como una API bancaria de ejemplo con lógica de negocio enfocada en seguridad y validación. Incluye además una colección Postman (`BellaBank.postman_collection.json`) para probar rapidamente los endpoints.

## Licencia

Este proyecto se usa como material de ejemplo y de práctica en la carpeta `Bella-Bank`. Revisa la licencia general del repositorio si aplica.
