# app.py

import streamlit as st

def main():
    st.title("My Streamlit App")
    name = st.text_input("Enter your name:")
    st.write(f"Hello, {name}!")

    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f"You are {age} years old.")

    if st.button("Click me"):
        st.write("Button clicked!")

if __name__ == "__main__":
    main()
