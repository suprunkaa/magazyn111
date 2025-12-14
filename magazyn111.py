import streamlit as st
import pandas as pd

# --- Inicjalizacja Magazynu (Lista w Streamlit State) ---
# Używamy st.session_state, aby lista była zachowana po interakcjach użytkownika
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["komputer", "pralka", "drabina", "młotek", "drukarka"]

# --- Funkcje Logiki Magazynu ---

def dodaj_towar(nazwa):
    """Dodaje towar do listy i czyści pole formularza."""
    if nazwa:
        st.session_state.magazyn.append(nazwa)
        st.success(f"Dodano: **{nazwa}** do magazynu.")
        # Po dodaniu czyścimy pole wprowadzania
        st.session_state.nowy_towar_input = ""
    else:
        st.error("Wprowadź nazwę towaru do dodania.")

def usun_towar(nazwa):
    """Usuwa pierwsze wystąpienie towaru z listy."""
    try:
        st.session_state.magazyn.remove(nazwa)
        st.warning(f"Usunięto pierwsze wystąpienie: **{nazwa}** z magazynu.")
    except ValueError:
        st.error(f"Błąd: Towaru **{nazwa}** nie znaleziono w magazynie.")

# --- Interfejs Użytkownika Streamlit ---

st.set_page_config(
    page_title="Prosty Magazyn (Streamlit)",
    layout="wide"
)

st.title("📦 Prosty Magazyn")
st.markdown("Aplikacja do zarządzania stanem magazynowym z użyciem listy w Pythonie.")

# Użycie kolumn do lepszego rozmieszczenia formularzy
col1, col2 = st.columns(2)

# --- 1. Panel DODAWANIA TOWARU ---
with col1:
    st.header("➕ Dodaj Towar")
    
    # Formularz dodawania
    with st.form("dodaj_form"):
        nowy_towar = st.text_input(
            "Nazwa nowego towaru:", 
            key='nowy_towar_input', 
            placeholder="np. Klawiatura"
        )
        submitted_add = st.form_submit_button("Dodaj do Magazynu")
        
        if submitted_add:
            dodaj_towar(nowy_towar.strip())

# --- 2. Panel USUWANIA TOWARU ---
with col2:
    st.header("➖ Usuń Towar")

    # Lista dostępnych towarów do usunięcia
    if st.session_state.magazyn:
        # Możemy użyć selectbox dla towarów, które faktycznie są na liście
        towar_do_usuniecia = st.selectbox(
            "Wybierz towar do usunięcia (usuwa tylko jedno wystąpienie):",
            sorted(list(set(st.session_state.magazyn))) # Unikalne i posortowane
        )
        
        if st.button(f"Usuń: {towar_do_usuniecia}"):
            usun_towar(towar_do_usuniecia)
    else:
        st.info("Magazyn jest pusty, brak towarów do usunięcia.")


# --- 3. Wyświetlanie Stanu Magazynu ---
st.header("📊 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    
    # 3a. Wyświetlanie jako tabela (używając Pandas dla lepszej wizualizacji)
    df = pd.Series(st.session_state.magazyn).value_counts().reset_index()
    df.columns = ['Nazwa Towaru', 'Ilość']
    
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True
    )

    # 3b. Wyświetlanie pełnej, nieprzetworzonej listy
    st.subheader("Pełna Lista (Surowe Dane):")
    st.code(st.session_state.magazyn)
    
else:
    st.info("Magazyn jest obecnie pusty.")

st.markdown("---")
st.caption("Aplikacja stworzona w Streamlit.")
