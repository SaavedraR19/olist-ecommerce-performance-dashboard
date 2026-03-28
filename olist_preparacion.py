import pandas as pd

# ============================================================
# CONFIGURACIÓN — cambiá esta ruta si tu carpeta es diferente
# ============================================================
base_path = r"C:\Users\USER\Desktop\Lucas\olist"

# ============================================================
# PASO 1 — Carga de archivos originales de Kaggle
# ============================================================
orders = pd.read_csv(fr"{base_path}\olist_orders_dataset.csv")
items = pd.read_csv(fr"{base_path}\olist_order_items_dataset.csv")
payments = pd.read_csv(fr"{base_path}\olist_order_payments_dataset.csv")
products = pd.read_csv(fr"{base_path}\olist_products_dataset.csv")
translation = pd.read_csv(fr"{base_path}\product_category_name_translation.csv")
customers = pd.read_csv(fr"{base_path}\olist_customers_dataset.csv")

# ============================================================
# PASO 2 — Limpieza de datos en el origen
# pd.to_numeric con errors="coerce" convierte valores corruptos
# en NaN (vacío) de forma controlada, en lugar de dejarlos.
# Luego filtramos rangos razonables para el negocio de Olist.
# ============================================================
items["price"] = pd.to_numeric(items["price"], errors="coerce")
items["freight_value"] = pd.to_numeric(items["freight_value"], errors="coerce")

items = items.dropna(subset=["price", "freight_value"])
items = items[items["price"] > 0]
items = items[items["price"] < 10000]
items = items[items["freight_value"] < 1000]

print(f"Items después de limpieza: {len(items)}")
print(f"Price máximo: R${items['price'].max():,.2f}")
print(f"Freight máximo: R${items['freight_value'].max():,.2f}")

# ============================================================
# PASO 3 — Convertir fechas
# ============================================================
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

# ============================================================
# PASO 4 — Traducir categorías al inglés
# ============================================================
products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

# ============================================================
# PASO 5 — Construir la tabla unificada (joins)
# ============================================================

# Unir items con productos para obtener la categoría en inglés
df = items.merge(
    products[["product_id", "product_category_name_english"]],
    on="product_id",
    how="left"
)

# Agregar información de la orden (fecha, estado, customer_id)
df = df.merge(
    orders[["order_id", "customer_id", "order_purchase_timestamp", "order_status"]],
    on="order_id",
    how="left"
)

# Agregar ciudad y estado del cliente
df = df.merge(
    customers[["customer_id", "customer_city", "customer_state"]],
    on="customer_id",
    how="left"
)


# Limpiar payment_type fuera de los valores estándar
tipos_validos = ["credit_card", "boleto", "voucher", "debit_card"]
payments["payment_type"] = payments["payment_type"].where(
    payments["payment_type"].isin(tipos_validos), other="other"
)


# ============================================================
# PASO 6 — Colapsar payments a una fila por orden
# La tabla de pagos puede tener varias filas por orden si el
# cliente usó más de un método de pago. Si hacemos el merge
# directo, cada ítem se duplica por cada método de pago,
# inflando el revenue de forma masiva. Por eso agrupamos
# primero y después hacemos el merge de forma segura.
# ============================================================
payments_agg = payments.groupby("order_id").agg(
    payment_type=("payment_type", lambda x: x.value_counts().index[0]),
    payment_installments=("payment_installments", "mean"),
    payment_value=("payment_value", "sum")
).reset_index()

df = df.merge(
    payments_agg,
    on="order_id",
    how="left"
)

# ============================================================
# PASO 7 — Crear columnas de negocio para Power BI
# ============================================================
df["year_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
df["revenue_items_only"] = df["price"]
df["revenue_plus_freight"] = df["price"] + df["freight_value"]
df["Order Date"] = df["order_purchase_timestamp"].dt.date

# ============================================================
# PASO 8 — Filtrar solo órdenes entregadas
# ============================================================
df_delivered = df[df["order_status"] == "delivered"].copy()

# Redondear columnas numéricas a 2 decimales para CSV limpio
# Usamos select_dtypes para evitar el warning con columnas de fecha
numeric_cols = df_delivered.select_dtypes(include="number").columns
df_delivered[numeric_cols] = df_delivered[numeric_cols].round(2)

# ============================================================
# PASO 9 — Verificaciones de sanidad
# Mirá estos números antes de continuar. El revenue total
# debería estar entre R$13M y R$16M, y el ticket promedio
# entre R$100 y R$200. Si algo no cuadra, el problema
# está en los pasos anteriores del script.
# ============================================================
print(f"\n--- VERIFICACIONES FINALES ---")
print(f"Filas totales:       {len(df_delivered):,}")
print(f"Revenue total:       R${df_delivered['revenue_plus_freight'].sum():,.2f}")
print(f"Ticket promedio:     R${df_delivered['revenue_plus_freight'].mean():,.2f}")
print(f"Revenue máximo:      R${df_delivered['revenue_plus_freight'].max():,.2f}")
print(f"Órdenes únicas:      {df_delivered['order_id'].nunique():,}")

# ============================================================
# PASO 10 — Exportar el CSV limpio
# El parámetro decimal="," es la clave para que Power BI
# en sistemas con configuración regional en español (Argentina,
# España, etc.) lea correctamente los números decimales.
# Sin esto, Power BI interpreta el punto como separador de
# miles y multiplica todos los valores por 100, lo que
# dispara el revenue a valores absurdos como "1 mil M".
# ============================================================
df_delivered.to_csv(
    fr"{base_path}\olist_dashboard_base.csv",
    index=False,
    decimal=","  # <-- punto decimal → coma, para configuración regional en español
)

print(f"\nArchivo guardado en: {base_path}\\olist_dashboard_base.csv")
print("Listo — ahora importá el CSV nuevamente en Power BI.")

