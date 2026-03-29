# Clarificación de la Solución 2: Modalidad NO VERIFACTU

## ⚠️ Basado Únicamente en el Documento Proporcionado

Este documento resume **únicamente** lo que dice el PDF de verifactu.pdf sobre la modalidad NO VERIFACTU. No se añaden especulaciones ni información externa.

---

## ¿Qué dice exactamente el documento?

### Definición oficial
> **"Modalidad 'NO VERIFACTU': Permite el uso de un programa homologado que garantiza la integridad e inalterabilidad de los registros, pero no remite las facturas automáticamente. La AEAT podrá requerir acceso a estos registros en cualquier momento."**

### Puntos clave confirmados:

| Aspecto | Lo que dice el documento | Lo que NO dice |
|---------|-------------------------|----------------|
| **Envío** | No es automático | Cómo se hace si es necesario |
| **Software** | Debe estar "homologado" | Qué significa exactamente "homologado" ni el proceso de homologación |
| **Requisitos técnicos** | Garantizar integridad e inalterabilidad | Qué mecanismos técnicos específicos (hash, firma, blockchain, etc.) |
| **Acceso AEAT** | Pueden requerir acceso "en cualquier momento" | En qué formato, cómo se solicita, plazos, etc. |
| **Registros** | Se deben conservar los registros | Por cuánto tiempo, en qué formato específico |

---

## Lo que el documento NO explica (y por tanto desconocemos)

### 1. Proceso de homologación
El documento menciona que el software debe estar "homologado" pero **no explica**:
- Quién realiza la homologación
- Qué criterios se evalúan
- Si hay un registro público de software homologado
- Si es necesario solicitar la homologación o es automática al cumplir requisitos

### 2. Mecanismos técnicos de "integridad e inalterabilidad"
El documento establece el **objetivo** (integridad e inalterabilidad) pero **no especifica**:
- Si se requiere hash criptográfico (SHA-256, etc.)
- Si se requiere firma electrónica
- Si se requiere cadena de bloques (blockchain)
- Si se requiere sello de tiempo (timestamp authority)
- Si hay algún mecanismo obligatorio específico

### 3. Formato de los registros
El documento **no especifica**:
- Formato de almacenamiento (XML, JSON, base de datos, etc.)
- Estructura mínima de datos a conservar
- Si debe haber un formato específico para la exportación

### 4. Proceso de acceso por la AEAT
El documento dice que "la AEAT podrá requerir acceso" pero **no aclara**:
- Cómo se realiza la solicitud
- Plazo de respuesta
- Formato de entrega
- Medio de entrega (online, físico, etc.)

---

## Interpretaciones posibles (con su nivel de certeza)

### 🔴 Alto riesgo de estar equivocado (el documento no lo dice):
- "Hay que usar SHA-256" → **NO CONFIRMADO**
- "Hay que implementar blockchain" → **NO CONFIRMADO**  
- "Hay que firmar con certificado digital" → **NO CONFIRMADO**
- "La AEAT solicitará acceso vía web service" → **NO CONFIRMADO**

### 🟡 Inferencia razonable pero no confirmada:
- "Integridad e inalterabilidad" probablemente implica algún mecanismo criptográfico
- "Programa homologado" probablemente significa que debe cumplir estándares mínimos verificables
- "Acceso en cualquier momento" probablemente implica exportación de datos en formato legible

### 🟢 Lo que el documento sí establece claramente:
- NO hay envío automático a la AEAT
- SÍ hay obligación de conservar registros íntegros
- SÍ la AEAT puede solicitar acceso a esos registros

---

## Preguntas sin respuesta en el documento

1. **¿Un software desarrollado a medida (como Facturación Fácil) puede ser "homologado"?**
   - El documento no lo especifica.

2. **¿Qué ocurre si la AEAT solicita acceso y los registros están en SQLite local?**
   - El documento no explica el procedimiento.

3. **¿Hay que conservar los registros de forma específica (cloud, local, etc.)?**
   - El documento no lo menciona.

4. **¿Cuál es la diferencia práctica entre NO VERIFACTU y el sistema anterior?**
   - El documento no lo explica en detalle.

---

## Conclusión honesta

**La modalidad NO VERIFACTU está MUY POCO DETALLADA en el documento proporcionado.**

Para implementar correctamente esta solución, sería necesario consultar:
1. El Real Decreto 1007/2023 completo (texto legal oficial)
2. Las especificaciones técnicas publicadas por la AEAT
3. Posiblemente, contactar directamente con la AEAT para aclarar requisitos

**Lo que se puede hacer basándose SOLO en este documento:**
- Implementar medidas básicas de integridad (hash SHA-256 de facturas)
- Mantener logs de auditoría de cambios
- Asegurar que los registros son exportables
- Documentar que el sistema garantiza "inalterabilidad"

**Pero sin garantía de que cumpla los requisitos de "homologación"**, ya que estos no están definidos en el documento.

---

## Alternativa práctica mencionada en el documento

El documento menciona una opción:
> **"La segunda opción, es contratar un sistema informático que este homologado, para los que no utilizan muchos datos ni facturas, recomiendo que sea mediante nube o iCloud como puede ser SG21 Factlite"**

Esto sugiere que:
- Existen sistemas ya homologados en el mercado
- Para pequeños volúmenes, usar un sistema cloud homologado puede ser más sencillo
- La homologación es un proceso que hace el proveedor, no el usuario final

---

*Documento basado únicamente en: docs/herramientas/verifactu.pdf*
*Fecha: Marzo 2026*
