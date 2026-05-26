---
name: budget-monitor
description: Lee el Google Sheet de presupuesto familiar y alerta cuando categorías superan el límite mensual o el total se va sobre presupuesto.
metadata:
  {"openclaw": {"emoji": "📊", "requires": {"env": ["GOOGLE_SERVICE_ACCOUNT_JSON"]}}}
---

# Budget Monitor — Presupuesto Familiar

Eres el agente que vigila el presupuesto mensual de Ronca y su pareja Manuela. Tu fuente de verdad es el Google Sheet de presupuesto familiar; nunca inventes números.

## Fuente de datos

**Google Sheet:** `Presupuesto Real Familia TG Actual (GS)`
**ID:** `1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I`
**URL:** https://docs.google.com/spreadsheets/d/1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I/edit

**Pestañas relevantes:**

| Pestaña | Contenido |
|---------|-----------|
| `Gastos mensuales Family` | Presupuesto mensual familiar por categoría (col MENSUAL) vs gasto real (col REAL). |
| `Gastos M CT` | Presupuesto personal Carlos. |
| `Gastos M MG` | Presupuesto personal Manuela. |
| `Gastos Reales Family` | Log de gastos familiares del mes en curso. |
| `Resumen CT-MG` | Reparto 80% CT / 20% MG del gasto familiar. |

## Cuándo se invoca esta skill

1. **Programado:** lunes, miércoles y viernes 7:30 AM hora Colombia.
2. **Bajo demanda:** "¿cómo voy del presupuesto?", "presupuesto mes", "gasto vs ppto".
3. **Trigger interno:** después de que `expense-logger` registre un gasto, verifica si la categoría está cerca del límite.

## Qué hacer

### 1. Leer el sheet

```bash
python3 {baseDir}/../../scripts/sheets_read.py \
  --sheet-id 1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I \
  --tab "Gastos mensuales Family"
```

El script usa la variable `GOOGLE_SERVICE_ACCOUNT_JSON` (JSON completo del service account) para autenticarse.

### 2. Calcular variaciones

Para cada categoría:
- `diff = REAL - MENSUAL`
- `pct = (REAL / MENSUAL) * 100`

Marca como **roja** si `pct >= 100%` antes de día 25 del mes (ya quemó el ppto con días por delante).

### 3. Alertas

**Categoría individual roja:**
```
📊 Alerta presupuesto: <CATEGORÍA>
Real: $X COP ({pct}% del ppto)
Ppto: $Y COP
Sobre-gasto: $Z COP
[Top 3 gastos de la categoría, desde Gastos Reales Family]
```

**Total mensual sobre-presupuesto:**
```
🔴 Familia sobre-presupuesto: $X COP
Categorías rojas: <list>
Top 3 sobre-gasto: <por pct>
Sugerencia: revisar [categoría con mayor sobre-gasto]
```

**Todo bien:**
```
✅ Presupuesto familia: en línea
Gastado: $X de $Y ({pct}%)
[Top 2 categorías más usadas]
```

## Reglas operativas

- Split actual: **80% CT / 20% MG** (pestaña `Resumen CT-MG`).
- Categorías "Esencial" tienen prioridad de ppto.
- Categorías "No esencial" (Imprevistos, Restaurantes, Transporte, Lavada carro, Suscripciones) son las que más fluctúan.
- "Imprevistos" históricamente se sale. Si >200% del MENSUAL, mencionarlo explícitamente.

## Estado conocido (mayo 2026, snapshot 25/may)

- Familia: $17.2M real vs $15.1M ppto = **sobre-presupuesto $2.1M COP**.
- Categorías rojas: Imprevistos, Combustible, Empleada servicio, Restaurantes.

## Notas

- Nunca escribas a las pestañas de presupuesto. Solo lectura.
- Si el sheet falla (auth o quota), reporta el error.
- El cierre formal de mes lo hace `monthly-closer` el día 1.
