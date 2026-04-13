import streamlit as st

def check_password():
    """Retorna True se o usuário tiver inserido a senha correta."""
    def password_entered():
        correct_password = st.secrets.get("app_password", None)
        
        if correct_password and st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Não armazena a senha na sessão
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input(
        "Por favor, insira a senha de acesso ao sistema do ECC:",
        type="password",
        on_change=password_entered,
        key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Senha incorreta. Tente novamente.")
    
    return False
