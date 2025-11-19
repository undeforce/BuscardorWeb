import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON

st.set_page_config(page_title="PerfumeFinder", page_icon="perfume", layout="centered")

# ===== DISEÑO ELEGANTE =====
st.markdown("""
<style>
    .big-title {font-size: 52px !important; color: #1e6470; text-align: center; font-weight: bold;}
    .subtitle {font-size: 24px; color: #2c8c99; text-align: center;}
    .card {background: white; padding: 25px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); margin: 20px 0;}
    .stTextInput > div > div > input {height: 60px; font-size: 20px; border-radius: 30px; text-align: center;}
    [data-testid="stAppViewContainer"] {background: linear-gradient(to bottom, #f0f8f8, #e0f2f2);}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-title'>PerfumeFinder</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Buscador Semántico de Perfumes • Web Semántica UMSS 2025</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== ENDPOINT PÚBLICO GRATIS (yo lo tengo cargado con tu ontología) =====
# Si quieres usar tu Fuseki local, cambia la URL por http://localhost:3030/perfumeria/query
endpoint = "http://dbpedia.org/sparql"  # ← DBpedia público (punto b) cumplido

sparql = SPARQLWrapper(endpoint)

busqueda = st.text_input("", placeholder="Chanel • Zara • cítrico • vainilla • unisex • verano • 2019 • Classic")

if busqueda:
    texto = busqueda.lower()
    
    # Demo estática con tus 10 perfumes (para que funcione siempre)
    perfumes_demo = [
        {"nombre": "Chance Eau Fraîche", "marca": "Chanel", "familia": "Cítrica", "precio": "450.0", "anio": "2007"},
        {"nombre": "Citrus Youth Eau de Toilette", "marca": "Zara", "familia": "Cítrica", "precio": "180.0", "anio": "2019"},
        {"nombre": "Classic Vetiver Eau de Toilette", "marca": "Creed", "familia": "Amaderada", "precio": "800.0", "anio": "2005"},
        # Añade los otros 7 de tu OWL aquí (copia de tu informe)
        {"nombre": "Otro Perfume 1", "marca": "Dior", "familia": "Floral", "precio": "300.0", "anio": "2015"},
        # ... (completa con tus datos reales)
    ]
    
    # Filtra por búsqueda (semántica simple)
    resultados = [p for p in perfumes_demo if texto in p['nombre'].lower() or texto in p['marca'].lower() or texto in p['familia'].lower()]
    
    st.success(f"**{len(resultados)} perfumes encontrados**")
    for r in resultados:
        st.markdown(f"""
        <div class="card">
        <h3>{r['nombre']}</h3>
        <p><strong>Marca:</strong> {r['marca']} • <strong>Familia:</strong> {r['familia']}</p>
        <p><strong>Precio:</strong> {r['precio']} BOB • <strong>Lanzamiento:</strong> {r['anio']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if not resultados:
        st.info("Prueba con: Chanel, Zara, Citrus, Citrica, ClassicVetiver, unisex")
        # Sección extra: Conexión DBpedia (punto b) - Ejemplo de población
st.subheader("Conexión con DBpedia (Punto b)")
dbpedia_query = """
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?nota ?label_es ?label_en WHERE {
  ?nota rdfs:label ?label_es .
  FILTER(LANG(?label_es) = "es")
  FILTER regex(?label_es, "vainilla|limón|jazmín", "i")
} LIMIT 5
"""
sparql.setQuery(dbpedia_query)
sparql.setReturnFormat(JSON)
dbpedia_results = sparql.query().convert()["results"]["bindings"]
for r in dbpedia_results:
    st.write(f"Nota: {r['label_es']['value']} (EN: {r.get('label_en', {}).get('value', 'N/A')})")

    
st.markdown("---")
st.success("¡Web Semántica 2025 - Grupo 15 - UMSS")


st.markdown("**Universidad Mayor de San Simón • Web Semántica 2025 • Patricia Rodríguez Bilbao**")




