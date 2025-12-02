# Guía para Hacer POST a /practices

## Configuración en Thunder Client

### 1. URL y Método
- **Método**: `POST`
- **URL**: `http://localhost:8002/practices`

### 2. Headers
Asegúrate de tener estos headers:

```
Authorization: Bearer {tu_access_token}
Accept: */*
```

**Importante**: NO agregues el header `Content-Type` manualmente. Thunder Client lo agregará automáticamente cuando uses form-data.

### 3. Body (Form-Data)

En la pestaña **Body**, selecciona la opción **Form** (no JSON, no Text, sino **Form**).

Agrega dos campos:

#### Campo 1: `letra`
- **Field Name**: `letra`
- **Type**: Text (o deja el checkbox desmarcado)
- **Value**: Un solo carácter válido, por ejemplo: `A`, `a`, `B`, `b`, `1`, `2`, etc.

**Valores permitidos para `letra`**:
- **Letras minúsculas**: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
- **Letras mayúsculas**: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
- **Números**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

#### Campo 2: `imagen`
- **Field Name**: `imagen`
- **Type**: File (marca el checkbox)
- **Value**: Selecciona un archivo de imagen (PNG, JPG, etc.)

### 4. Ejemplo Visual en Thunder Client

```
Body Tab → Seleccionar "Form"

┌─────────────────────────────────────┐
│ Form Fields                         │
├─────────────────────────────────────┤
│ ☐ letra          A                  │
│ ☑ imagen         [Choose File]      │
│                                    │
└─────────────────────────────────────┘
```

## Errores Comunes y Soluciones

### Error 422: Unprocessable Entity

**Posibles causas**:

1. **La letra no es válida**
   - ❌ `letra: "AA"` (más de un carácter)
   - ❌ `letra: "@"` (carácter no permitido)
   - ✅ `letra: "A"` (correcto)

2. **El Body no está en formato Form**
   - ❌ Body → JSON
   - ❌ Body → Text
   - ✅ Body → **Form**

3. **El nombre del campo está mal escrito**
   - ❌ `letter` en vez de `letra`
   - ❌ `image` en vez de `imagen`
   - ✅ `letra` y `imagen` exactamente así

4. **Falta el archivo de imagen**
   - Asegúrate de haber seleccionado un archivo en el campo `imagen`

### Error 401: Unauthorized

- Verifica que el token JWT sea válido
- El formato del header debe ser: `Authorization: Bearer {token}`
- Si el token expiró, vuelve a hacer login

## Ejemplo de Petición Completa

```
POST http://localhost:8002/practices

Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Body (Form):
  letra: A
  imagen: [archivo seleccionado: A_template.png]
```

## Verificación de la Respuesta

Si todo está correcto, deberías recibir:

- **Status**: `201 Created`
- **Body**: Un objeto JSON con los detalles de la práctica creada

```json
{
  "practice_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "04ec4f5d-69b4-4306-828b-e8ca952c6afb",
  "letra_plantilla": "A",
  "url_imagen": "https://s3.bucket.name/images/...",
  "fecha_carga": "2025-02-12T...",
  "estado_analisis": "pendiente",
  "analisis": null
}
```

