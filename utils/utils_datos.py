import re
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def load_airbnb_data(file_id: str):
    """
    Descarga un archivo CSV desde Google Drive usando el File ID.

    Este método transforma el ID público del archivo a una URL
    de descarga directa. El archivo debe estar configurado como
    visible con el enlace.

    Parámetro
    ---------
    file_id : str
        ID obtenido desde la URL compartida de Google Drive.

    Retorna
    -------
    DataFrame con la información cargada desde Drive.
    """
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    df = pd.read_csv(url, low_memory=False)
    return df


DRIVE_FILES = {
    "Barcelona": "18yTaNKXzREyh5IdnqEdEBokqU6y4sq1r",
    "Amsterdam": "1hwrvXG3gujLl4dle_-7r_wVusRVv-AaC",
    "Milan": "16Uv7HNWgdWgzs10s9RJAhQkZtOL545dc",
    "Atenas": "1XH1WPvK_VvKGCcN0BlJm830Z2KonnTQ1",
    "Madrid": "177x-ptsDj8216O4ikG_EICwmcmQE0epS",
}


def _to_float_price(val):
    """
    Limpia valores de precio y los convierte a flotante.
    Soporta:
    - comas decimales
    - rangos (ej. 120-150)
    - caracteres mixtos
    - separadores de miles
    """
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if not s:
        return np.nan

    s = s.replace("\u00A0", " ").replace("\u202F", " ")
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"[^\d,.\-\s]", "", s)

    if "-" in s and not s.startswith("-"):
        nums = re.findall(r"\d+(?:[.,]\d+)?", s)
        if len(nums) >= 2:
            try:
                return (float(nums[0].replace(",", ".")) + float(nums[1].replace(",", "."))) / 2
            except:
                pass

    s = s.replace(" ", "").replace("'", "")
    if "," in s and s.count(",") == 1 and s.split(",")[1].isdigit():
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        return float(s)
    except:
        return np.nan


def _bathrooms_from_text(txt):
    """
    Convierte cadenas con formato de baño a número.

    Ejemplos:
    '1 bath'        -> 1.0
    '1.5 baths'     -> 1.5
    'half bath'     -> 0.5
    """
    if pd.isna(txt):
        return np.nan

    s = str(txt).lower()

    if "half" in s and not re.search(r"\d+(\.\d+)?", s):
        return 0.5

    m = re.search(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else np.nan


def limpiar_estandarizar(df: pd.DataFrame, ciudad: str) -> pd.DataFrame:
    """
    Estandariza campos de Airbnb para comparaciones equivalentes.

    Agrega:
    - price normalizado
    - price_per_person
    - amenities_count
    - identificación d:id y ciudad
    """
    d = df.copy()
    d["ciudad"] = ciudad

    if "id" not in d.columns:
        d["id"] = np.arange(len(d)) + 1

    d["price"] = d.get("price", np.nan).map(_to_float_price)
    if d["price"].notna().any():
        d["price"] = d["price"] * 0.80

    if "neighbourhood_cleansed" in d.columns:
        d["barrio_std"] = d["neighbourhood_cleansed"]
    elif "neighbourhood" in d.columns:
        d["barrio_std"] = d["neighbourhood"]
    else:
        d["barrio_std"] = np.nan

    d["room_type"] = d.get("room_type", np.nan).astype(str).replace("nan", np.nan)
    d["accommodates"] = pd.to_numeric(d.get("accommodates", np.nan), errors="coerce")

    if "bathrooms_text" in d.columns:
        d["bathrooms_num"] = d["bathrooms_text"].map(_bathrooms_from_text)
    else:
        d["bathrooms_num"] = pd.to_numeric(d.get("bathrooms", np.nan), errors="coerce")

    d["latitude"] = pd.to_numeric(d.get("latitude", np.nan), errors="coerce")
    d["longitude"] = pd.to_numeric(d.get("longitude", np.nan), errors="coerce")

    if "amenities" in d.columns:
        def _count(x):
            s = str(x)
            if s in ("nan", "", "[]"):
                return 0
            return sum(1 for a in re.split(r"[,\|]", s.strip("[]")) if a.strip())
        d["amenities_count"] = d["amenities"].apply(_count)
    else:
        d["amenities_count"] = np.nan

    d["price_per_person"] = np.where(
        (d["accommodates"] > 0) & d["price"].notna(),
        d["price"] / d["accommodates"],
        np.nan
    )

    columnas_finales = [
        "id",
        "ciudad",
        "barrio_std",
        "room_type",
        "accommodates",
        "bathrooms_num",
        "price",
        "price_per_person",
        "amenities_count",
        "latitude",
        "longitude",
        "number_of_reviews_ltm",
        "review_scores_rating",
        "host_is_superhost"
    ]

    # Si alguna columna no existe, se rellena con NaN para evitar errores
    for col in columnas_finales:
        if col not in d.columns:
            d[col] = np.nan

    return d[columnas_finales]


def recortar_outliers_por_ciudad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica recorte de valores extremos en precio por ciudad,
    eliminando valores extremos que distorsionan KPIs.
    """
    limpio = []
    for city, group in df.groupby("ciudad"):
        if group["price"].notna().sum() < 50:
            limpio.append(group)
            continue

        low = group["price"].quantile(0.01)
        high = group["price"].quantile(0.99)

        limpio.append(group[(group["price"].isna()) |
                            ((group["price"] >= low) & (group["price"] <= high))])

    return pd.concat(limpio, ignore_index=True)


@st.cache_data(show_spinner=False)
def load_data():
    """
    Carga y procesa los datos de Airbnb desde Google Drive.

    Para cada ciudad:
    - Descarga CSV remoto
    - Limpia y estandariza
    - Aplica filtro de extremos

    Retorna:
    df_all: DataFrame único consolidado
    warnings: lista de errores ocurridos
    """
    partes = []
    warnings = []

    for city, file_id in DRIVE_FILES.items():
        try:
            df_raw = load_airbnb_data(file_id)
        except Exception as exc:
            warnings.append(f"Error cargando {city}: {exc}")
            continue

        partes.append(limpiar_estandarizar(df_raw, city))

    if not partes:
        warnings.append("No se pudo cargar ninguno de los archivos desde Drive")
        return pd.DataFrame(), warnings

    df_all = pd.concat(partes, ignore_index=True)

    df_all = df_all.drop_duplicates(subset=["ciudad", "id"])

    df_all = recortar_outliers_por_ciudad(df_all)

    return df_all, warnings
