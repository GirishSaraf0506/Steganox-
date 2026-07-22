"""
Steganox - Hugging Face Spaces (Gradio)
LSB Steganography + AES-256 Encryption
"""

import gradio as gr
import tempfile
import os
from PIL import Image

from steganox.core.steganography import SteganoxEngine
from steganox.core.validation import validate_image, validate_password_strength

engine = SteganoxEngine()


def embed_message(image, message, password):
    if image is None:
        return None, "❌ Please upload a carrier image."
    if not message.strip():
        return None, "❌ Message cannot be empty."
    if not password:
        return None, "❌ Password cannot be empty."

    _, pwd_info = validate_password_strength(password)
    warnings = "\n".join(pwd_info["issues"]) if pwd_info["issues"] else ""

    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_in:
            image.save(tmp_in.name)
            input_path = tmp_in.name

        result = engine.embed(input_path, message, password)

        output_path = tempfile.mktemp(suffix=".png")
        result.save(output_path)
        os.unlink(input_path)

        status = "✅ Message embedded successfully!"
        if warnings:
            status += f"\n⚠️ Weak password warnings:\n{warnings}"

        return output_path, status

    except ValueError as e:
        return None, f"❌ {e}"
    except Exception as e:
        return None, f"❌ Unexpected error: {e}"


def extract_message(image, password):
    if image is None:
        return "❌ Please upload a stego-image."
    if not password:
        return "❌ Password cannot be empty."

    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_in:
            image.save(tmp_in.name)
            input_path = tmp_in.name

        message = engine.extract(input_path, password)
        os.unlink(input_path)
        return f"✅ Extracted message:\n\n{message}"

    except ValueError as e:
        return f"❌ {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


with gr.Blocks(
    title="🔐 Steganox",
    theme=gr.themes.Base(
        primary_hue="cyan",
        neutral_hue="slate",
    ),
    css="""
        .gradio-container { max-width: 800px; margin: auto; }
        h1 { text-align: center; }
        .subtitle { text-align: center; color: #888; margin-bottom: 20px; }
    """,
) as demo:
    gr.Markdown("# 🔐 Steganox")
    gr.Markdown(
        "<p class='subtitle'>Applied Steganography + AES-256 Cryptography — "
        "Hide secret messages inside images</p>"
    )

    with gr.Tabs():
        # ── Embed Tab ──────────────────────────────────────
        with gr.Tab("🔒 Embed Message"):
            with gr.Row():
                with gr.Column():
                    embed_image = gr.Image(type="pil", label="Carrier Image (PNG/BMP/JPG)")
                    embed_message_input = gr.Textbox(
                        label="Secret Message",
                        placeholder="Enter your secret message...",
                        lines=4,
                    )
                    embed_password = gr.Textbox(
                        label="Password (12+ chars recommended)",
                        type="password",
                        placeholder="Strong password",
                    )
                    embed_btn = gr.Button("🔐 Embed & Download", variant="primary")

                with gr.Column():
                    embed_output_image = gr.Image(
                        type="filepath", label="Stego Image (download this)"
                    )
                    embed_status = gr.Textbox(label="Status", lines=3, interactive=False)

            embed_btn.click(
                fn=embed_message,
                inputs=[embed_image, embed_message_input, embed_password],
                outputs=[embed_output_image, embed_status],
            )

        # ── Extract Tab ────────────────────────────────────
        with gr.Tab("🔓 Extract Message"):
            with gr.Row():
                with gr.Column():
                    extract_image = gr.Image(type="pil", label="Stego Image")
                    extract_password = gr.Textbox(
                        label="Password",
                        type="password",
                        placeholder="Enter password used during embedding",
                    )
                    extract_btn = gr.Button("🔓 Extract Message", variant="primary")

                with gr.Column():
                    extract_result = gr.Textbox(label="Result", lines=8, interactive=False)

            extract_btn.click(
                fn=extract_message,
                inputs=[extract_image, extract_password],
                outputs=[extract_result],
            )

    gr.Markdown(
        """
        ---
        **How it works:**
        - 🔐 **Embed**: Your message is encrypted with AES-256-GCM, then hidden in the image's pixel LSBs
        - 🔓 **Extract**: The hidden bits are read and decrypted using your password
        - 👁️ Changes are imperceptible — the stego image looks identical to the original

        [GitHub](https://github.com/GirishSaraf0506/Steganox-) | MIT License
        """
    )

if __name__ == "__main__":
    demo.launch()
