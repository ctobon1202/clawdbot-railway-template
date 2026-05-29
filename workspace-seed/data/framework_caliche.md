# Framework Caliche — Evaluación de Acciones

Fuente: Excel "Ejemplo framewrok caliche.xlsx" entregado por Ronca 2026-05-27.
Compatible con principios de [[user-frente-finanzas]] (Buffett value investing + Tony Robbins "Domina el Dinero").

## Estructura del framework

El framework evalúa una acción con **22 indicadores** en 3 categorías, contra thresholds **específicos por sector**. Una acción es buena para **comprar** cuando cumple la mayoría de los thresholds de su sector; es buena para **vender** cuando los incumple sistemáticamente.

## Indicadores con thresholds por sector

### Value indicators (10)

| Indicador | Tecnología | Finanzas | Energía | Consumo | Salud | Industrial |
|-----------|-----------|----------|---------|---------|-------|-----------|
| **P/E Ratio** (precio/ganancia) | < 30 | < 15 | < 10 | < 20 | < 25 | < 18 |
| **P/B Ratio** (precio/libros) | < 5 | < 2 | < 2 | < 3 | < 4 | < 2.5 |
| **ROE** (rentabilidad patrimonio) | > 15% | > 12% | > 10% | > 15% | > 12% | > 10% |
| **PEG Ratio** (P/E ajust. crecimiento) | < 1.5 | < 1.5 | < 1.5 | < 1.5 | < 1.5 | < 1.5 |
| **ROA** (rentabilidad activos) | > 5% | > 1% | > 3% | > 5% | > 4% | > 3% |
| **FCF Yield** (flujo libre / precio) | > 5% | > 6% | > 8% | > 5% | > 6% | > 7% |
| **Deuda/EBITDA** | < 3 | < 3 | < 3 | < 3 | < 3 | < 3 |
| **Debt/Equity** | < 1.0 | < 5.0 | < 1.5 | < 1.0 | < 1.0 | < 1.5 |
| **Dividend Yield** | < 1% | > 3% | > 4% | > 2% | > 1% | > 2% |
| **EV/EBITDA** | < 15 | < 10 | < 8 | < 12 | < 14 | < 10 |

### Growth indicators (8)

| Indicador | Tecnología | Finanzas | Energía | Consumo | Salud | Industrial |
|-----------|-----------|----------|---------|---------|-------|-----------|
| **Gross Margins** | > 50% | > 40% | > 40% | > 45% | > 50% | > 35% |
| **Operating Margins** | > 20% | > 15% | > 20% | > 18% | > 25% | > 15% |
| **Net Margin** | > 10% | > 5% | > 10% | > 10% | > 12% | > 8% |
| **Crecimiento Ingresos** | > 10% | > 10% | > 10% | > 10% | > 10% | > 10% |
| **Crecimiento Beneficio Neto** | > 10% | > 10% | > 10% | > 10% | > 10% | > 10% |
| **Cap.Mercado/FCF** | < 20 | < 20 | < 20 | < 20 | < 20 | < 20 |
| **CAGR** (tasa crec. anual compuesta) | > 10% | > 10% | > 10% | > 10% | > 10% | > 10% |
| **EPS Growth** | > 10% | > 8% | > 5% | > 7% | > 9% | > 6% |

### Técnico indicators (6)

| Indicador | Tecnología | Finanzas | Energía | Consumo | Salud | Industrial |
|-----------|-----------|----------|---------|---------|-------|-----------|
| **Volatilidad Implícita** | < 40% | < 40% | < 40% | < 40% | < 40% | < 40% |
| **PSR** (precio/ventas) | < 5 | < 2 | < 2 | < 2 | < 2 | < 2 |
| **RSI** | < 40 | < 40 | < 40 | < 40 | < 40 | < 40 |
| **Bollinger Bands** | Fuera banda baja = infravalorada |
| **Golden Cross** | MA50 cruza MA200 al alza = bullish |
| **Cambio Interés Corto** | Disminución del interés corto = positivo |

## Reglas de interpretación

### Comprar (Buy)
La acción cumple **≥70% de los indicadores Value y Growth aplicables** de su sector, y al menos uno de los técnicos es favorable (RSI < 40, Bollinger fuera de banda baja, o Golden Cross reciente).

Casos especiales:
- Si tiene P/E muy bajo PERO los growth indicators están todos rojos → probable **value trap**, no comprar.
- Si tiene P/E alto PERO PEG < 1.5 y crecimiento sostenido > 15% → puede ser **growth compañía** justificada (típico Tech).

### Mantener (Hold)
Cumple **40-70% de los indicadores** o tiene métricas mixtas (algunas muy buenas, otras malas). Esperar más data.

### Vender (Sell)
Cumple **< 40% de los indicadores Value y Growth** Y:
- RSI > 70 (sobrecomprada) **O**
- P/E ratio en el percentil 80+ de su sector histórico, **O**
- Deterioro fundamentales (Net Margin cayó vs 3 trimestres anteriores) **O**
- Deuda/EBITDA > 4 (sobre-endeudada)

## Flujo de aplicación de Ronca (de su Excel)

> "Quiero una lista con de mayor market cap a menor market cap de todas las empresas de la industria XXXXX, y que saquemos los indicadores en valores numéricos o respuesta binaria (sí/no) para criterios técnicos. Debería añadir también headquarters e info general para filtrar por economías."

Es decir: el framework también sirve para **descubrir** acciones nuevas (no solo evaluar las que ya tiene), filtrando por industria + headquarters + indicadores.

## Cómo conectar con principios validados de Ronca

Este framework es consistente con:

**Warren Buffett** (de [[frente-lectura]]):
- Margen de seguridad → P/E < threshold del sector + P/B < threshold.
- Círculo de competencia → preferir sectores donde el inversor entiende el negocio.
- Hold long-term → si los fundamentales se mantienen verdes año tras año, no vender por movimientos de precio.

**Tony Robbins "Domina el Dinero"** (de [[frente-lectura]]):
- Asset allocation diversificada → no concentrar en un sector.
- Fees bajos → preferir acciones directas + ETFs de bajo costo (en línea con allocation 30% S&P/20% ETFs/etc.).
- Dollar-cost averaging → comprar en tandas, no all-in.

## Fuentes de datos recomendadas

- **yfinance** (Python): gratis, sin auth, da P/E, P/B, ROE, márgenes, deuda, dividend yield, sector, headquarters. Cobertura completa para US y mayoría de internacional.
- **Manual override:** Ronca puede sobreescribir el sector en `Portfolio CT` col E si yfinance lo categoriza mal.
