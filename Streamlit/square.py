import streamlit as st

x = st.number_input('Enter a number', min_value=0, max_value=100, value=50, step=1)

if st.button('Calculate Square'):
    square = x ** 2
    st.success(f'The square of {x} is {square}')
