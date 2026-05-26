---
name: fx-watcher
description: Monitorea el tipo de cambio USD/COP y alerta cuando el movimiento supera ±2% vs cierre anterior. Reporta el valor actual cuando se le pide.
metadata:
  {"openclaw": {"emoji": "💱"}}
---

# FX Watcher — USD/COP

Eres el agente de finanzas de Ronca para monitoreo de divisas. Tu trabajo es estar al tanto del tipo de cambio USD/COP y avisarle cuando hay movimientos importantes.

## Cuándo se invoca esta skill

1. **Programado:** todos los días hábiles a las 7:00 AM y 4:30 PM hora Colombia (configurar en `openclaw.json` automation/cron).
2. **Bajo demanda:** cuando Ronca pregunta "¿cómo está el dólar?", "valor del dólar", "USD/COP", "FX" o similar.

## Qué hacer

### 1. Obtener el valor actual

Usa el tool `exec` para consultar una fuente confiable. Opción gratuita sin auth:

```bash
curl -s "https://open.er-api.com/v6/latest/USD" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['rates']['COP'])"
```

Si esa fuente falla, usa fallback:

```bash
curl -s "https://api.exchangerate-api.com/v4/latest/USD" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['rates']['COP'])"
```

### 2. Comparar contra el cierre anterior

El último valor conocido se guarda en `/data/workspace/data/fx_last.json`. Léelo, calcula el delta porcentual contra el valor que acabas de obtener.

```json
{"value": 4150.32, "timestamp": "2026-05-25T16:30:00-05:00"}
```

### 3. Aplicar la regla de alerta

- **Si |delta| ≥ 2%** → genera alerta y manda mensaje a Ronca por el canal activo (Telegram).
- **Si |delta| < 2%** → no notifica. Solo loguea silenciosamente.

### 4. Formato del mensaje (alerta)

```
💱 Alerta FX USD/COP

Valor actual: $4,237.50 COP
Cambio: +2.1% vs cierre anterior ($4,150.32)
Hora: 16:30 — 25 may 2026

Acción sugerida: [si subió: "buen momento si ibas a vender USD" | si bajó: "buen momento si ibas a comprar USD"]
```

### 5. Formato del mensaje (consulta bajo demanda, sin alerta)

```
💱 USD/COP: $4,178.40
Δ hoy: -0.4% vs cierre ayer
```

### 6. Guardar el valor

Sobrescribe `/data/workspace/data/fx_last.json` con el nuevo valor y timestamp.

## Notas importantes

- Ronca vive en Colombia, así que la perspectiva es siempre "yo recibo USD, gasto COP". Cuando el dólar sube, le conviene si va a vender USD; cuando baja, le conviene si va a comprar USD.
- No des consejo de "comprar/vender ahora" como recomendación financiera. Solo señala la oportunidad relativa.
- El umbral de 2% es configurable — si Ronca pide cambiarlo, edita esta skill.

## Estado de integración

- [x] Fuente de FX gratuita (sin auth requerida).
- [x] Persistencia en archivo plano en `/data/workspace/data/`.
- [ ] Pendiente: que la skill `monthly-closer` lea el log histórico para el cierre de mes.
