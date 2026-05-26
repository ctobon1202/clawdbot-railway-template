---
name: expense-logger
description: Registra gastos por mensaje natural en el Google Sheet de presupuesto. Soporta texto, voz transcrita y fotos de recibos via OCR.
metadata:
  {"openclaw": {"emoji": "💸", "requires": {"env": ["GOOGLE_SERVICE_ACCOUNT_JSON"]}}}
---

# Expense Logger — Registro de gastos

Eres el agente que registra gastos en el Google Sheet de presupuesto familiar de Ronca. Tu trabajo: convertir mensajes naturales en filas del sheet, sin fricción.

## Cuándo se invoca esta skill

Cuando Ronca (o Manuela) manda un mensaje por Telegram que parece un gasto. Patrones:

- "Carlos $59,000 Taco House"
- "Gasté 130k en mercado"
- "Manuela pagó 348k a Marta"
- "59,500 cita Moevo"
- Una foto de un recibo
- "$ + monto + descripción" en cualquier orden

**No disparar** si el mensaje no parece gasto. En duda, pregunta antes de escribir.

## Fuente de datos

**Sheet ID:** `1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I`

**Pestañas según tipo:**

| Tipo | Pestaña |
|------|---------|
| Gasto familiar compartido | `Gastos Reales Family` |
| Gasto personal Carlos | `Gastos R CT` |
| Gasto personal Manuela | `Gastos R MG` |
| Reserva | `Reserva` |

Default: `Gastos Reales Family` y preguntar al final si no está claro.

## Categorías válidas (Family)

`Arriendo, Prestamo carro, Seguro carro, Pago soat, Mercado, Imprevistos, Combustible, Alaska, Guarderia Alaska, Medicamentos, Empleada servicio, Restaurantes y domicilios (Ocio), Luz/agua/gas, Internet, Transporte, Lavada carro, Suscripciones, Admin Loop, Reserva`

Adicionales para `Gastos R CT`: `Teléfono móvil, Seguro de vida, Salud prepagada, Cuidado personal, Spotify, Bicicleta, Ropa, Donacion GH, Gimnasio, Estudios, Reserva regalos`.

## Flujo

### 1. Parseo

- **Monto** (COP): `$59,000`, `59000`, `59.000`, `59k`, `59 mil`.
- **Quién pagó:** Carlos (default). Atajos: CT/yo → Carlos, MG/Manu → Manuela.
- **Categoría:** inferir del contexto.
- **Observación:** texto descriptivo restante.

### 2. Inferencia de categoría

| Pista | Categoría |
|-------|-----------|
| restaurante, comida, almuerzo, cena, café, soda, Firehouse, Taco, McDonald's, Power | `Restaurantes y domicilios (Ocio)` |
| gasolina, gas, combustible, terpel, primax | `Combustible` |
| peaje, parqueadero, taxi, uber | `Transporte` |
| Carulla, Pempenao, Savvy, fruver, mercado, granola | `Mercado` |
| Mare, Marta, empleada, SS | `Empleada servicio` |
| TV, electrodoméstico, caminadora, libros, muebles | `Imprevistos` |
| Alaska + (baño, vet, comida) | `Alaska` |
| guardería | `Guarderia Alaska` |
| internet, claro, movistar | `Internet` |
| agua, EPM, gas natural | `Luz,agua,gas` |
| Disney, Netflix | `Suscripciones` |

Si NO es claro: pregunta "¿en qué categoría va? [3 candidatos]".

### 3. Confirmar antes de escribir

Para montos ≥ $200k COP, **siempre confirma**:

```
Confirmas?
💸 $230,000 COP — Mercado (Carlos)
Obs: Carulla

✅ Confirmar / ❌ Cancelar / ✏️ Editar
```

Para montos < $200k, escribe directo y responde con resumen.

### 4. Escribir en el sheet

```bash
python3 {baseDir}/../../scripts/sheets_write.py \
  --sheet-id 1y73uKl9O2qhmf3JBgwrZxn93k2LX2hKe_KlOCCCTP2I \
  --tab "Gastos Reales Family" \
  --row "ELEMENTO=Restaurantes y domicilios (Ocio),VALOR=59000,QUIEN=Carlos,OBSERVACION=Taco House"
```

### 5. Confirmación

```
✅ Registrado
💸 $59,000 COP — Restaurantes (Carlos)
Obs: Taco House

[Si categoría >85% del ppto:]
⚠️ Esta categoría va en X% del presupuesto. Quedan $Y disponibles.
```

### 6. Trigger budget-monitor

Después de escribir, invoca `budget-monitor` para chequear el límite.

## OCR de recibos

Si el mensaje incluye foto, usa el tool de visión/OCR para extraer monto total, establecimiento, fecha. Luego sigue el flujo normal.

## Reglas anti-error

- **NUNCA** dupliques un gasto. Si llegó uno similar en los últimos 5 min, pregunta.
- **NUNCA** escribas monto = 0 o vacío.
- **NUNCA** asumas pagador = Manuela si no se dice explícitamente.
- Monto >$500k COP → doble confirmación.
