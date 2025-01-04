import gradio as gr
import dotenv
dotenv.load_dotenv()
from ingest import ingest_documents
from chat import chat_with_collection

def create_gradio_app():
    """
    Creates and launches a Gradio application with tabs for document ingestion and chat interaction.
    """
    with gr.Blocks() as demo:
        gr.Markdown("# Document query assistant")
        # Document ingestion tab
        with gr.Tab("Document Ingestion"):
            collection_name = gr.Textbox(label="Collection Name", autofocus=True)
            files = gr.File(
                label="Files to Ingest", 
                file_count="multiple",
                type="binary"
            )
            ingest_button = gr.Button("Ingest")
            ingest_output = gr.Textbox(label="Ingestion Result")
            ingest_button.click(
                ingest_documents,
                inputs=[collection_name, files],
                outputs=[ingest_output]
            )
        # Chat interaction tab
        with gr.Tab("Chat"):
            collection_name_chat = gr.Textbox(label="Collection Name", autofocus=True)
            gr.ChatInterface(
                title="Chat with Documents",
                description="Ask questions about the ingested documents",
                examples=[["Summarize the documents in one sentence.", "Maintenance document summary"]],
                type="messages",
                additional_inputs=[collection_name_chat],
                fn=chat_with_collection,
                autoscroll=True,
                submit_btn="Send Prompt",
                stop_btn="Stop Generation",
                show_progress="minimal"
            )

    demo.launch()

if __name__ == "__main__":
    create_gradio_app()