"""
Gemma 3 Vision Q&A Demo Application

Demo project exploring Google DeepMind's Gemma 3 multimodal capabilities.
Built with modern Python tooling (uv) as a learning exercise.
"""

from __future__ import annotations

from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
import gradio as gr
from PIL import Image
import tempfile
import os
import mlx.core as mx

# ============================================================================
# WORKAROUND: Fix for mlx-vlm v0.3.5 Gemma3 attention_mask bug
# ============================================================================
# Issue: In mlx-vlm v0.3.5, the Gemma3 model's prepare_inputs_for_multimodal
# method receives attention_mask as a NumPy array but tries to use it with
# mx.expand_dims(), which requires an MLX array, causing a TypeError.
#
# Location: mlx_vlm/models/gemma3/gemma3.py:162
# Error: "expand_dims(): incompatible function arguments"
#
# This patch converts the attention_mask to an mx.array before processing.
# Once this is fixed upstream, this workaround can be removed.
#
# Related: https://github.com/Blaizzy/mlx-vlm/issues
# ============================================================================
from mlx_vlm.models.gemma3 import gemma3

_original_prepare = gemma3.Model.prepare_inputs_for_multimodal

@staticmethod
def _patched_prepare_inputs_for_multimodal(
    hidden_size,
    pad_token_id,
    image_token_index,
    image_features,
    inputs_embeds,
    input_ids,
    attention_mask,
):
    """
    Patched version that ensures attention_mask is an mx.array.
    
    This wrapper converts attention_mask from NumPy array to MLX array
    before calling the original function.
    """
    if not isinstance(attention_mask, mx.array):
        attention_mask = mx.array(attention_mask)
    
    return _original_prepare(
        hidden_size,
        pad_token_id,
        image_token_index,
        image_features,
        inputs_embeds,
        input_ids,
        attention_mask,
    )

# Apply the patch
gemma3.Model.prepare_inputs_for_multimodal = _patched_prepare_inputs_for_multimodal


def build_custom_theme(
    base_theme: str = "default",
    primary_color: str = "blue", 
    secondary_color: str = "cyan",
    neutral_color: str = "slate"
) -> gr.Theme:
    """
    Build a custom Gradio theme with configurable colors.
    
    Args:
        base_theme: Base theme to use ("soft", "default", "glass", "monochrome", "ocean")
        primary_color: Primary color hue (e.g., "blue", "green", "red", "purple", "orange")
        secondary_color: Secondary color hue
        neutral_color: Neutral color hue (e.g., "slate", "gray", "zinc", "neutral", "stone")
    
    Returns:
        Configured Gradio theme
        
    Examples:
        >>> # Blue/cyan theme (default)
        >>> theme = build_custom_theme()
        
        >>> # Purple/pink theme
        >>> theme = build_custom_theme(primary_color="purple", secondary_color="pink")
        
        >>> # Green monochrome
        >>> theme = build_custom_theme(base_theme="monochrome", primary_color="green")
    """
    # Select base theme
    theme_map = {
        "soft": gr.themes.Soft,
        "default": gr.themes.Default,
        "glass": gr.themes.Glass,
        "monochrome": gr.themes.Monochrome,
        "ocean": gr.themes.Ocean,
    }
    
    base = theme_map.get(base_theme.lower(), gr.themes.Soft)
    
    # Create theme with custom colors
    return base(
        primary_hue=primary_color,
        secondary_hue=secondary_color,
        neutral_hue=neutral_color,
    ).set(
        # Button styling
        button_primary_background_fill="*primary_500",
        button_primary_background_fill_hover="*primary_600",
        button_primary_text_color="white",
        # Input styling
        input_background_fill="*neutral_50",
        input_border_color="*primary_200",
        # Block styling  
        block_background_fill="white",
        block_label_background_fill="*primary_50",
        block_label_text_color="*primary_700",
        block_title_text_color="*primary_800",
    )


class Gemma3VisionDemo:
    """Gemma 3 multimodal Q&A application"""
    
    def __init__(self, model_path: str = "mlx-community/gemma-3-4b-it-8bit"):
        """Initialize with Gemma 3 model"""
        print(f"Loading Gemma 3 from {model_path}...")
        self.model, self.processor = load(model_path)
        self.config = load_config(model_path)
        print("Model loaded successfully!")
    
    def analyze_image(self, image: Image.Image | None, question: str) -> str:
        """
        Analyze image and answer questions using Gemma 3
        
        Args:
            image: PIL Image to analyze
            question: Question about the image
            
        Returns:
            Model's response as string
        """
        if image is None:
            return "Please upload an image first."
        
        if not question.strip():
            question = "Describe this image in detail."
        
        # Save PIL Image to temporary file (mlx_vlm expects file path or URL)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_file.close()
        image_path = tmp_file.name
        image.save(image_path, format="PNG")
        
        try:
            # Format prompt for Gemma 3
            prompt = apply_chat_template(
                self.processor,
                self.config,
                question,
                num_images=1
            )
            
            # Generate response
            output = generate(
                self.model,
                self.processor,
                prompt,
                image_path,
                verbose=False,
                max_tokens=300,
                temperature=0.0
            )
            
            return output.text
        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.remove(image_path)
    
    def create_interface(self) -> gr.Blocks:
        """Create Gradio interface"""
        # Build custom theme - change colors here to experiment!
        # Try: primary_color="purple", secondary_color="pink"
        # Or: base_theme="glass", primary_color="green"
        custom_theme = build_custom_theme(
            base_theme="default",
            primary_color="orange",
            secondary_color="cyan",
            neutral_color="slate"
        )
        
        with gr.Blocks(theme=custom_theme, title="Gemma 3 Vision Demo", css="""
            .gradio-container {
                max-width: 1200px !important;
            }
            footer {visibility: hidden}
        """) as demo:
            gr.Markdown("""
            # Gemma 3 Vision Q&A Demo
            
            **Learning Project**: Exploring Google DeepMind's Gemma 3 multimodal capabilities
            
            Upload an image and ask questions. The model can:
            - Describe image contents and identify objects
            - Answer specific questions about visual elements
            - Analyze scenes and spatial relationships
            - Perform basic OCR and text extraction
            
            *Running locally on Apple Silicon using MLX optimization*
            
            ---
            """)
            
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(type="pil", label="Upload Image")
                    question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="What do you see in this image?",
                        lines=2
                    )
                    submit_btn = gr.Button("Ask Gemma 3", variant="primary")
                
                with gr.Column():
                    output = gr.Markdown(label="Answer", value="*Waiting for your question...*")
            
            # Example questions
            gr.Examples(
                examples=[
                    [None, "Describe this image in detail"],
                    [None, "What objects can you identify?"],
                    [None, "What is the main subject?"],
                    [None, "What type of location is this?"],
                    [None, "Is this indoors or outdoors?"],
                ],
                inputs=[image_input, question_input],
            )
            
            submit_btn.click(
                fn=self.analyze_image,
                inputs=[image_input, question_input],
                outputs=output
            )
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the Gradio interface"""
        demo = self.create_interface()
        demo.launch(**kwargs)


def main():
    """Main entry point"""
    app = Gemma3VisionDemo()
    app.launch(share=False)


if __name__ == "__main__":
    main()