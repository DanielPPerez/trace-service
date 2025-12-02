# Guía Específica para Thunder Client - POST /practices

## ⚠️ PROBLEMA COMÚN: Error 422 - Campo 'imagen' faltante

Si recibes este error:
```json
{
  "detail": [{
    "type": "missing",
    "loc": ["body", "imagen"],
    "msg": "Field required"
  }]
}
```

**Es porque el archivo no se está enviando correctamente.** Sigue estos pasos exactamente:

---

## 📋 Configuración Paso a Paso

### Paso 1: Configurar la Petición Básica

1. **Método**: Selecciona `POST`
2. **URL**: `http://localhost:8002/practices`
3. **Headers Tab**: Agrega solo esto:
   ```
   Authorization: Bearer {tu_token_aqui}
   ```
   ⚠️ **NO agregues** `Content-Type` manualmente. Thunder Client lo agregará automáticamente.

### Paso 2: Configurar el Body (⚠️ MUY IMPORTANTE)

1. Ve a la pestaña **Body**
2. Selecciona la opción **Form** (NO JSON, NO Text, NO Form-encode)
3. Debes ver dos secciones:
   - **Form Fields** (campos de texto)
   - **Files** (archivos)

### Paso 3: Agregar el Campo 'letra'

En la sección **Form Fields**:

1. Haz clic en el campo vacío o en el botón **+ Add** si está disponible
2. **Field name**: Escribe exactamente `letra` (minúsculas, sin espacios)
3. **Value**: Escribe un solo carácter, por ejemplo: `A`
4. Asegúrate de que el checkbox esté **MARCADO** ✅

### Paso 4: Agregar el Campo 'imagen' (⚠️ CRÍTICO)

En la sección **Files**:

1. Haz clic en el campo vacío o en el botón **+ Add** si está disponible
2. **Field name**: Escribe exactamente `imagen` (minúsculas, sin espacios)
3. Haz clic en **Choose File** o **Select File**
4. Selecciona tu archivo de imagen (PNG, JPG, etc.)
5. ⚠️ **MUY IMPORTANTE**: Asegúrate de que el checkbox esté **MARCADO** ✅

**El campo debe verse así cuando esté correcto:**
```
☑ imagen    [A_template.png]  [Choose File]
```

**NO debe verse así:**
```
☐ imagen    [A_template.png]  [Choose File]  ❌ (checkbox desmarcado)
```

### Paso 5: Verificar Antes de Enviar

Antes de hacer clic en **Send**, verifica:

- ✅ El método es `POST`
- ✅ La URL es correcta
- ✅ Tienes el header `Authorization` con tu token
- ✅ Estás en la pestaña **Body → Form**
- ✅ El campo `letra` está en **Form Fields** con checkbox marcado
- ✅ El campo `imagen` está en **Files** con checkbox marcado y archivo seleccionado
- ✅ NO hay header `Content-Type` manual (debe ser automático)

### Paso 6: Enviar la Petición

Haz clic en **Send** y revisa la respuesta.

---

## 🔍 Solución de Problemas

### Problema: El archivo no se envía

**Solución 1: Verificar que el checkbox esté marcado**
- En la sección **Files**, asegúrate de que el checkbox al lado de `imagen` esté marcado ✅
- Si el checkbox está desmarcado, el archivo NO se enviará

**Solución 2: Eliminar y volver a agregar el campo**
1. Elimina el campo `imagen`
2. Agrega un nuevo campo en **Files**
3. Escribe `imagen` como field name
4. Selecciona el archivo
5. Marca el checkbox ✅

**Solución 3: Verificar el nombre del campo**
- Debe ser exactamente `imagen` (sin mayúsculas, sin espacios)
- No `image`, no `Image`, no `IMAGEN`

### Problema: Sigue apareciendo error 422

**Solución: Verificar la estructura completa**

Tu petición debe verse así en Thunder Client:

```
POST http://localhost:8002/practices

Headers:
  Authorization: Bearer eyJhbGciOi...

Body → Form:

  Form Fields:
    ☑ letra          A

  Files:
    ☑ imagen        [A_template.png]  [Choose File]
```

### Problema: Error "Field required" para 'letra'

- Verifica que esté en la sección **Form Fields** (no en Files)
- Verifica que el checkbox esté marcado ✅
- Verifica que el valor sea un solo carácter válido

---

## ✅ Ejemplo de Configuración Correcta

### Visualización en Thunder Client:

```
┌─────────────────────────────────────────────┐
│ POST  http://localhost:8002/practices      │
│                                             │
│ Tabs: [Query] [Headers 1] [Body 1]        │
│                                             │
│ Body Tab → Form Selected                    │
│                                             │
│ Form Fields:                                │
│   ☑ letra              A                    │
│   ☐ [field name]      [value]              │
│                                             │
│ Files:                                      │
│   ☑ imagen            [A_template.png]      │
│                       [Choose File]         │
│   ☐ [field name]      [Select file]        │
└─────────────────────────────────────────────┘
```

---

## 📝 Checklist Final

Antes de enviar, verifica que:

- [ ] Método: POST
- [ ] URL correcta: `http://localhost:8002/practices`
- [ ] Header `Authorization` con token Bearer
- [ ] Body → **Form** seleccionado (NO JSON)
- [ ] Campo `letra` en Form Fields con checkbox ✅
- [ ] Valor de `letra` es un solo carácter (A, a, B, etc.)
- [ ] Campo `imagen` en Files con checkbox ✅
- [ ] Archivo seleccionado en `imagen`
- [ ] NO hay Content-Type manual en headers

---

## 🎯 Valores Válidos para 'letra'

- **Minúsculas**: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
- **Mayúsculas**: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
- **Números**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

---

## 💡 Tips Adicionales

1. **Si nada funciona**: Intenta reiniciar Thunder Client
2. **Verifica el tamaño del archivo**: Archivos muy grandes pueden causar problemas
3. **Formato de imagen**: Asegúrate de que sea un formato válido (PNG, JPG, JPEG)
4. **Logs del servidor**: Revisa los logs del trace-service para ver más detalles del error

---

## 🆘 Si Aún No Funciona

Si después de seguir todos estos pasos sigues teniendo problemas:

1. **Captura una imagen** de tu configuración en Thunder Client
2. **Revisa los logs** del servidor para ver el error exacto
3. **Verifica** que `python-multipart` esté instalado en el servidor:
   ```bash
   pip list | grep multipart
   ```
   Debe mostrar: `python-multipart 0.0.20` (o similar)

Si `python-multipart` no está instalado, instálalo:
```bash
pip install python-multipart
```

Y reinicia el servidor.

