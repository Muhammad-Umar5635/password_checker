import streamlit as st
import requests
import hashlib
import secrets
import string
import plotly.graph_objects as go

def check_password_strength(password):
    criteria = {"Length": len(password) >= 12,
                "Uppercase": any(c.isupper() for c in password),
                "Lowercase": any(c.islower() for c in password),
                "Digits": any(c.isdigit() for c in password),
                "Symbols": any(c in string.punctuation for c in password)}
    
    score = sum(criteria.values())
    return score, criteria

def check_pwned_password(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1_password[:5]}")
    return sha1_password[5:] in response.text

def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def plot_comparison(criteria1, criteria2):
    categories = list(criteria1.keys())
    values1 = [int(criteria1[cat]) for cat in categories]
    values2 = [int(criteria2[cat]) for cat in categories]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=categories, y=values1, name="Password 1", marker_color='royalblue'))
    fig.add_trace(go.Bar(x=categories, y=values2, name="Password 2", marker_color='orangered'))
    
    fig.update_layout(title="Password Strength Criteria Comparison",
                      barmode='group',
                      xaxis_title="Criteria",
                      yaxis_title="Met (1) / Not Met (0)",
                      template="plotly_dark")
    st.plotly_chart(fig)

st.set_page_config(page_title="🔐 Advanced Password Strength Analyzer", layout="wide")
st.title("🔐 Password Strength Analyzer")
st.subheader("Check and Compare Password Security!")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    password1 = st.text_input("🔑 Enter first password:", type="password")
with col2:
    password2 = st.text_input("🔑 Enter second password:", type="password")

if password1 and password2:
    score1, criteria1 = check_password_strength(password1)
    score2, criteria2 = check_password_strength(password2)
    
    st.markdown("### Strength Comparison")
    st.write(f"🔹 **Password 1 Score:** {score1}/5 ({'Weak' if score1 <=2 else 'Moderate' if score1 == 3 else 'Strong'})")
    st.write(f"🔹 **Password 2 Score:** {score2}/5 ({'Weak' if score2 <=2 else 'Moderate' if score2 == 3 else 'Strong'})")
    
    plot_comparison(criteria1, criteria2)
    
    if score1 > score2:
        st.success("✅ First password is stronger!")
    elif score1 < score2:
        st.success("✅ Second password is stronger!")
    else:
        st.info("⚖️ Both passwords have the same strength.")
    
    st.markdown("---")
    if check_pwned_password(password1):
        st.error("⚠️ First password has been found in a data breach!")
    if check_pwned_password(password2):
        st.error("⚠️ Second password has been found in a data breach!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Compare Another Pair"):
            st.rerun()
    with col2:
        if st.button("🔑 Generate Strong Password"):
            st.text_input("Secure Password:", generate_strong_password(), disabled=True)
