import streamlit as st

# Show a large title at the top of the page.
st.header('Welcome to Streamlit')

# Create a button the user can click.
# When the button is clicked, show a success message.
if st.button('Click here'):
    st.success('lets learn Streamlit!')
