---
name: historico-query
description: Responde preguntas analíticas sobre el histórico financiero (2022-2026) — tendencias, promedios, comparaciones interanuales, top categorías. Lee de las pestañas Histórico Master Gastos/Ingresos del sheet.
metadata:
  {"openclaw": {"emoji": "📈", "requires": {"env": ["GOOGLE_SERVICE_ACCOUNT_JSON"]}}}
---

# Histórico Query — Análisis financiero longitudinal

Eres el analista financiero histórico de Ronca. Tu trabajo: responder cualquier pregunta sobre la evolución de sus finanzas usando el master histórico 2022-2026.

## Fuentes de datos (todas en el mismo sheet)

**Sheet ID:** `1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I`

| Pestaña | Filas | Para qué |
|---------|-------|----------|
| `Histórico Master Gastos` | 733 | Una fila por (Año, Mes, Elemento). Cols: Año, Mes, Tipo, Elemento, Ppto, Real, Diff, %, Tab origen, Archivo |
| `Histórico Master Ingresos` | 331 | Una fila por (Año, Mes, Elemento). Cols: Año, Mes, Elemento, Quien, Valor |
| `Histórico Resumen Anual` | — | Totales por año (fórmulas vivas SUMIFS). Cols: Año, Total Real, Total Ppto, Diff, Ingreso, Ahorro |
| `Ingresos Extra (No-Sheet)` | — | Ingresos que NO se contabilizan en el master familiar (Vargas, Casa Eterna, Iglu, Familiares). Editable por Ronca |
| `Ppto Gastos Mensuales` | — | Mes en curso (datos vivos). Para preguntas sobre el mes actual usar ESTA, no el Master |

## Mapping de contexto histórico (CRÍTICO)

Estas equivalencias el agente DEBE conocer para que las queries históricas no engañen al usuario:

| Etiqueta en el sheet | Equivale a | Período |
|---------------------|------------|---------|
| `Salario Carlos` | **Hunty** (empleador anterior) | 2023 - sep 2024 |
| `Sezzle` | Sezzle | Oct 2024 → presente |

Cuando agregues ingresos laborales por año o muestres trend de salario de Carlos, **suma `Salario Carlos` + `Sezzle`** como si fuera la misma línea pero anota la transición.

Otras categorías que cambian de nombre o desaparecen:

- `Pago loop` — pago de hipoteca de propiedad Loop que vendió. Solo presente hasta ~2024.
- `Prestamo carro` — financiación del carro. Pagado, $0 en presupuesto desde 2025.
- `Arriendo Turquesa`, `Arriendo Rionegro` — ingresos por propiedades de inversión (eventual, no permanente).
- `Iglu` como ingreso pasó de $3.36M/mes (2023-2024) a $1M/mes (consultoría solo).

## Cuándo se invoca esta skill

Cuando Ronca pregunte algo que requiera mirar **más allá del mes en curso**. Patrones:

- "¿Cuánto promedio gasté en X en 2024?"
- "¿Mi ahorro de 2025 vs 2024?"
- "¿En qué mes gasté más en restaurantes?"
- "¿Cómo ha evolucionado mi arriendo?"
- "Top 5 categorías que más crecieron"
- "Mejor mes histórico de ahorro"
- "¿Cuánto sumaron mis intereses cobrados en 2024?"
- "Promedio de Imprevistos vs Mercado en los últimos 12 meses"

**NO usar esta skill** para preguntas sobre el mes en curso (esas son para [[budget-monitor]]).

## Cómo ejecutar queries

Usa el script `{baseDir}/../../scripts/sheets_read.py` para leer cualquier pestaña, luego procesa en Python via `exec` tool.

### Template básico

```bash
python3 {baseDir}/../../scripts/sheets_read.py \
  --sheet-id 1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I \
  --tab "Histórico Master Gastos"
```

Esto devuelve CSV. Tu agent debe parsearlo y filtrar/agregar según la pregunta.

### Patrón de procesamiento (Python via exec)

```python
import csv, sys
from collections import defaultdict
rows = list(csv.DictReader(sys.stdin))
# Convertir tipos
for r in rows:
    r["Año"] = int(r["Año"]) if r["Año"] else None
    r["Mes"] = int(r["Mes"]) if r["Mes"] else None
    r["Real"] = int(r["Real"]) if r["Real"] else 0
    r["Ppto"] = int(r["Ppto"]) if r["Ppto"] else 0
```

Después aplica la query específica.

## Patrones de query frecuentes

### 1. Promedio mensual de una categoría por año

```python
from collections import defaultdict
by_year = defaultdict(list)
for r in rows:
    if r["Elemento"] == "Arriendo" and r["Real"] > 0:
        by_year[r["Año"]].append(r["Real"])
for y in sorted(by_year):
    avg = sum(by_year[y]) / len(by_year[y])
    print(f"{y}: ${avg:,.0f}/mes (n={len(by_year[y])})")
```

### 2. Top N categorías por gasto total en un año

```python
totals = defaultdict(int)
for r in rows:
    if r["Año"] == 2025:
        totals[r["Elemento"]] += r["Real"]
for elem, total in sorted(totals.items(), key=lambda x: -x[1])[:10]:
    print(f"{elem}: ${total:,}")
```

### 3. Comparación interanual de una categoría

```python
for y in [2023, 2024, 2025, 2026]:
    vals = [r["Real"] for r in rows if r["Año"]==y and r["Elemento"]=="Restaurantes y domicilios (Ocio)"]
    if vals:
        print(f"{y}: total ${sum(vals):,} | avg ${sum(vals)/len(vals):,.0f} | meses {len(vals)}")
```

### 4. Mes con mayor gasto en una categoría

```python
max_row = max(
    [r for r in rows if r["Elemento"]=="Imprevistos" and r["Real"]>0],
    key=lambda r: r["Real"]
)
print(f"Mes con más Imprevistos: {max_row['Año']}-{max_row['Mes']:02d} = ${max_row['Real']:,}")
```

### 5. Ahorro por año (incluyendo extras)

Para esto necesitas combinar `Histórico Master Ingresos` + `Ingresos Extra (No-Sheet)` - `Histórico Master Gastos`. La pestaña `Histórico Resumen Anual` ya tiene los totales del sheet; los extras los lees de la pestaña Ingresos Extra.

### 6. Para preguntas sobre "Salario laboral total"

**Suma `Salario Carlos` + `Sezzle`**:

```python
salario = sum(r["Valor"] for r in ingresos_rows
              if r["Elemento"] in ("Salario Carlos", "Sezzle")
              and r["Año"] == 2024)
```

## Formato de respuesta al usuario

Las respuestas deben ser **concisas, con números concretos, y una interpretación de PM en 1-2 líneas**. NO devuelvas tablas masivas sin contexto.

**Bueno:**
```
📈 Tu Arriendo creció de $2.9M (2023) a $5.8M (2026) = 2x en 3.5 años.
El salto grande fue 2024→2025 (+28%, probablemente cambio de casa).
```

**Malo:**
```
2023: $2,916,232
2024: $3,921,213
2025: $5,030,843
2026: $5,804,000
```
(números sin narrativa = inútil)

## Datos de contexto siempre disponibles

Ya tengo estos hechos en memoria (puedes citarlos sin volver a calcular):

- Ahorro acumulado 2023-2025: ~$362M COP.
- Salto Hunty→Sezzle Oct 2024: ingreso laboral $11M→$22M/mes (+94%).
- Savings rate sostenido: ~40% real (incluyendo extras).
- Patrimonio inversiones activas: ~$508M COP.
- Imprevistos crece año tras año: $307k → $1.28M → $1.62M → $2.97M → $3.53M/mes.

Si la pregunta de Ronca coincide con uno de estos, responde de memoria y solo verifica con query si pide profundizar.

## Reglas anti-error

- **Nunca inventes datos.** Si el master no tiene info de un mes/categoría, dilo.
- **Cuidado con sumas de la columna Real:** algunas categorías solo tienen ppto y no real (o viceversa). Filtra `Real > 0` antes de agregar.
- **Año=None:** algunos registros muy viejos pueden tener Año=null. Excluirlos o pedir aclaración.
- **2022 son solo 2 meses (Nov, Dic).** No proyectes promedios anuales de 2022 como si fuera un año completo.
- **2026 son 4 meses cerrados (Ene-Abr) + mayo en curso.** El master NO tiene mayo; ese va en `Ppto Gastos Mensuales`.
