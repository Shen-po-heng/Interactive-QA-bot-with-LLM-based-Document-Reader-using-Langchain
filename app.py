from interfaces.gradio_interface import create_gradio_interface

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(server_name="localhost", server_port=7860)
