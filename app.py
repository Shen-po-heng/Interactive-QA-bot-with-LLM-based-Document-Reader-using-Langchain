from interfaces.gradio_interface import create_gradio_interface

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(server_name="0.0.0.0", server_port=7860)
