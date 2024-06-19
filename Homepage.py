import streamlit as st


def main():
    st.set_page_config(
        page_title="Project M",
        page_icon="👋",
    )

    st.title("Stay tuned...")
    st.sidebar.success("Select a page above.")


if __name__ == '__main__':
    main()
