# import streamlit as st
# from streamlit_mic_recorder import mic_recorder
#
# st.set_page_config(

    # page_title="AI Email Assistant",
#
#
#
#     layout="wide"
#
# )
#
# st.title("AI Email Assistant")
#
# st.subheader(
#
#     "Voice Input"
#
# )
#
# audio = mic_recorder(
#
#     start_prompt="Start Recording",
#
#     stop_prompt="⏹Stop Recording",
#
#     key="recorder"
#
# )
#
# if audio:
#
#     st.success(
#
#         "Audio recorded successfully!"
#
#     )
#
#     st.write(
#
#         audio.keys()
#
#     )
#
# if audio:
#
#     st.audio(
#
#         audio["bytes"],
#
#         format="audio/wav"
#
#     )
#
# st.write(
#
#     "Speak or type instructions to generate emails."
#
# )
#
# instruction = st.chat_input(
#
#     "Type your email instruction..."
#
# )
#
# if instruction:
#
#     st.chat_message(
#
#         "user"
#
#     ).write(
#
#         instruction
#
#     )
# st.divider()
#
# st.subheader(
#
#     "📧 Email Preview"
#
# )
#
# receiver = st.text_input(
#
#     "Recipient Email"
#
# )
#
# subject = st.text_input(
#
#     "Subject"
#
# )
#
# body = st.text_area(
#
#     "Body",
#
#     height=250
#
# )
#
# if st.button(
#
#     "📨 Send Email",
#
#     use_container_width=True
#
# ):
#
#     st.success(
#
#         "Email sent successfully!"
#
#     )
#
