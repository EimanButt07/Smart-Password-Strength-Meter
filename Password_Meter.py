import streamlit as st
import re
import random
import string

def check_password_strength(password):
    strength = 0
    feedback = []
    
    # Common weak passwords blacklist
    weak_passwords = ["password", "123456", "password123", "qwerty", "abc123", "letmein"]
    if password.lower() in weak_passwords:
        return 0, ["❌ This password is too common and easily guessed. Choose a stronger one."]
    
    # Check password length
    if len(password) >= 8:
        strength += 2  # More weight to length
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        feedback.append("❌ Include at least one uppercase letter.")
    
    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        feedback.append("❌ Include at least one lowercase letter.")
    
    # Check for numbers
    if re.search(r"\d", password):
        strength += 2  # Higher weight for numbers
    else:
        feedback.append("❌ Include at least one digit (0-9).")
    
    # Check for special characters
    if re.search(r"[!@#$%^&*]", password):
        strength += 2  # Higher weight for special characters
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    return strength, feedback

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

# Initialize session state for password history
if 'password_history' not in st.session_state:
    st.session_state['password_history'] = []

st.title("🔒 Password Strength Meter")
st.write("Enter a password to check its strength.")

col1, col2 = st.columns([2, 1])

with col1:
    password = st.text_input("Enter Password:", type="password")
    
    if password:
        strength, feedback = check_password_strength(password)
        st.session_state['password_history'].append(password)
        
        # Strength meter display
        st.write("### Strength Level:")
        if strength >= 7:
            st.success("✅ Strong Password - Your password is secure!")
        elif strength >= 4:
            st.warning("⚠️ Moderate Password - Improve it for better security.")
        else:
            st.error("❌ Weak Password - Consider making it stronger.")
        
        # Display feedback
        if feedback:
            st.write("### Suggestions to Improve:")
            for tip in feedback:
                st.write(f"- {tip}")
    
    # Password Generator Feature
    if st.button("🔄 Generate Strong Password"):
        strong_password = generate_strong_password()
        st.text_input("Suggested Strong Password:", value=strong_password, disabled=True)
        st.session_state['password_history'].append(strong_password)

# Password History in Sidebar
with col2:
    st.sidebar.title("📜 Password History")
    if st.session_state['password_history']:
        for idx, past_password in enumerate(reversed(st.session_state['password_history'][-5:]), 1):
            st.sidebar.text(f"{idx}. {past_password}")
    else:
        st.sidebar.write("No passwords entered yet.")
