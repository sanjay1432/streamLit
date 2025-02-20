import streamlit as st
import random
import string
import pyperclip
import time

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special):
    # Initialize character pool
    characters = ''
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Check if at least one character type is selected
    if not characters:
        return None
    
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Ensure at least one character of each selected type is included
    if use_uppercase and not any(c.isupper() for c in password):
        password = random.choice(string.ascii_uppercase) + password[1:]
    if use_lowercase and not any(c.islower() for c in password):
        password = random.choice(string.ascii_lowercase) + password[1:]
    if use_numbers and not any(c.isdigit() for c in password):
        password = random.choice(string.digits) + password[1:]
    if use_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        password = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?") + password[1:]
    
    return password

def calculate_password_strength(password):
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 3
        feedback.append("✅ Good length (12+ characters)")
    elif len(password) >= 8:
        score += 2
        feedback.append("✅ Decent length (8+ characters)")
    else:
        feedback.append("❌ Password is too short (less than 8 characters)")
    
    # Character type checks
    if any(c.isupper() for c in password):
        score += 1
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ Missing uppercase letters")
        
    if any(c.islower() for c in password):
        score += 1
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ Missing lowercase letters")
        
    if any(c.isdigit() for c in password):
        score += 1
        feedback.append("✅ Contains numbers")
    else:
        feedback.append("❌ Missing numbers")
        
    if any(c in string.punctuation for c in password):
        score += 1
        feedback.append("✅ Contains special characters")
    else:
        feedback.append("❌ Missing special characters")
    
    # Calculate strength
    if score >= 6:
        strength = "Strong"
        color = "green"
    elif score >= 4:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Weak"
        color = "red"
    
    return strength, color, feedback

def main():
    st.title("🔐 Random Password Generator")
    
    # Password generation options
    st.header("Password Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.slider("Password Length", min_value=4, max_value=32, value=12)
        use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
        use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
    
    with col2:
        use_numbers = st.checkbox("Include Numbers", value=True)
        use_special = st.checkbox("Include Special Characters", value=True)
    
    if st.button("Generate Password"):
        password = generate_password(
            length, 
            use_uppercase, 
            use_lowercase, 
            use_numbers, 
            use_special
        )
        
        if password is None:
            st.error("Please select at least one character type!")
        else:
            # Store password in session state
            st.session_state.current_password = password
            
            # Display password in a "code" block for better visibility
            st.code(password)
            
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard"):
                pyperclip.copy(password)
                st.success("Password copied to clipboard!")
            
            # Password strength analysis
            strength, color, feedback = calculate_password_strength(password)
            
            st.markdown("---")
            st.subheader("Password Strength Analysis")
            
            # Display strength with colored text
            st.markdown(f"Strength: :{color}[**{strength}**]")
            
            # Display feedback
            for item in feedback:
                st.write(item)
    
    # Password tips
    with st.expander("Password Security Tips"):
        st.write("""
        1. Use passwords that are at least 12 characters long
        2. Include a mix of:
           - Uppercase letters (A-Z)
           - Lowercase letters (a-z)
           - Numbers (0-9)
           - Special characters (!@#$%^&*)
        3. Don't use personal information
        4. Use different passwords for different accounts
        5. Consider using a password manager
        """)

if __name__ == "__main__":
    main()
