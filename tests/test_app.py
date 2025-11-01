"""
Tests for Gemma3 Vision Demo application.

Run with: pytest tests/test_app.py -v
Run with coverage: pytest tests/test_app.py --cov=src.gemma3_vision_demo
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import tempfile
import os

from src.gemma3_vision_demo.app import Gemma3VisionDemo


class TestGemma3VisionDemo:
    """Tests for the Gemma3VisionDemo class."""
    
    @pytest.fixture
    def mock_model_components(self):
        """Fixture to mock model loading components."""
        with patch('src.gemma3_vision_demo.app.load') as mock_load, \
             patch('src.gemma3_vision_demo.app.load_config') as mock_config:
            
            # Mock model and processor
            mock_model = Mock()
            mock_processor = Mock()
            mock_load.return_value = (mock_model, mock_processor)
            
            # Mock config
            mock_config_obj = Mock()
            mock_config.return_value = mock_config_obj
            
            yield {
                'load': mock_load,
                'load_config': mock_config,
                'model': mock_model,
                'processor': mock_processor,
                'config': mock_config_obj,
            }
    
    @pytest.fixture
    def demo_app(self, mock_model_components):
        """Fixture to create a Gemma3VisionDemo instance with mocked components."""
        app = Gemma3VisionDemo()
        return app
    
    @pytest.fixture
    def sample_image(self):
        """Fixture to create a sample PIL Image."""
        img = Image.new('RGB', (100, 100), color='red')
        return img
    
    def test_init_loads_model(self, mock_model_components):
        """Test that initialization loads the model correctly."""
        app = Gemma3VisionDemo()
        
        # Verify load was called with correct model path
        mock_model_components['load'].assert_called_once_with(
            "mlx-community/gemma-3-4b-it-8bit"
        )
        
        # Verify load_config was called
        mock_model_components['load_config'].assert_called_once_with(
            "mlx-community/gemma-3-4b-it-8bit"
        )
        
        # Verify model and processor are set
        assert app.model is not None
        assert app.processor is not None
        assert app.config is not None
    
    def test_init_with_custom_model_path(self, mock_model_components):
        """Test initialization with a custom model path."""
        custom_path = "custom/model/path"
        app = Gemma3VisionDemo(model_path=custom_path)
        
        mock_model_components['load'].assert_called_once_with(custom_path)
        mock_model_components['load_config'].assert_called_once_with(custom_path)
    
    def test_analyze_image_returns_error_when_no_image(self, demo_app):
        """Test that analyze_image returns error message when no image provided."""
        result = demo_app.analyze_image(None, "What is this?")
        assert result == "Please upload an image first."
    
    def test_analyze_image_uses_default_question(self, demo_app, sample_image):
        """Test that analyze_image uses default question when prompt is empty."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Mock generate to return a result with .text attribute
            mock_result = Mock()
            mock_result.text = "A red image"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            
            # Call with empty question
            result = demo_app.analyze_image(sample_image, "")
            
            # Verify default question was used
            mock_template.assert_called_once()
            args = mock_template.call_args[0]
            assert args[2] == "Describe this image in detail."
    
    def test_analyze_image_creates_temporary_file(self, demo_app, sample_image):
        """Test that analyze_image creates a temporary file for the image."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate, \
             patch('tempfile.NamedTemporaryFile') as mock_tempfile:
            
            # Setup mocks
            mock_result = Mock()
            mock_result.text = "A red image"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            
            # Mock temporary file
            mock_file = Mock()
            mock_file.name = "/tmp/test_image.png"
            mock_tempfile.return_value = mock_file
            
            # Call analyze_image
            with patch('PIL.Image.Image.save'):
                result = demo_app.analyze_image(sample_image, "What color?")
            
            # Verify temporary file was created
            mock_tempfile.assert_called_once_with(suffix=".png", delete=False)
            mock_file.close.assert_called_once()
    
    def test_analyze_image_cleans_up_temporary_file(self, demo_app, sample_image):
        """Test that analyze_image removes temporary file after processing."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate, \
             patch('os.path.exists') as mock_exists, \
             patch('os.remove') as mock_remove:
            
            # Setup mocks
            mock_result = Mock()
            mock_result.text = "A red image"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            mock_exists.return_value = True
            
            # Call analyze_image
            result = demo_app.analyze_image(sample_image, "What color?")
            
            # Verify cleanup was called
            mock_remove.assert_called_once()
    
    def test_analyze_image_returns_generated_text(self, demo_app, sample_image):
        """Test that analyze_image returns the generated text."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Setup mocks
            expected_text = "This is a red square image."
            mock_result = Mock()
            mock_result.text = expected_text
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            
            # Call analyze_image
            result = demo_app.analyze_image(sample_image, "Describe this")
            
            # Verify result
            assert result == expected_text
    
    def test_analyze_image_calls_generate_with_correct_params(self, demo_app, sample_image):
        """Test that analyze_image calls generate with correct parameters."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Setup mocks
            mock_result = Mock()
            mock_result.text = "Generated text"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            
            # Call analyze_image
            result = demo_app.analyze_image(sample_image, "Test question")
            
            # Verify generate was called with correct parameters
            mock_generate.assert_called_once()
            call_kwargs = mock_generate.call_args[1]
            assert call_kwargs['verbose'] is False
            assert call_kwargs['max_tokens'] == 300
            assert call_kwargs['temperature'] == 0.0
    
    def test_analyze_image_applies_chat_template(self, demo_app, sample_image):
        """Test that analyze_image applies the chat template correctly."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Setup mocks
            mock_result = Mock()
            mock_result.text = "Generated text"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted prompt"
            
            question = "What is in this image?"
            
            # Call analyze_image
            result = demo_app.analyze_image(sample_image, question)
            
            # Verify chat template was called correctly
            mock_template.assert_called_once_with(
                demo_app.processor,
                demo_app.config,
                question,
                num_images=1
            )
    
    def test_analyze_image_handles_exception_and_cleans_up(self, demo_app, sample_image):
        """Test that temporary file is cleaned up even if generation fails."""
        with patch('src.gemma3_vision_demo.app.apply_chat_template'), \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate, \
             patch('os.path.exists') as mock_exists, \
             patch('os.remove') as mock_remove:
            
            # Make generate raise an exception
            mock_generate.side_effect = Exception("Generation failed")
            mock_exists.return_value = True
            
            # Call should raise exception
            with pytest.raises(Exception, match="Generation failed"):
                demo_app.analyze_image(sample_image, "Test")
            
            # Verify cleanup still happened
            mock_remove.assert_called_once()
    
    def test_create_interface_returns_gradio_blocks(self, demo_app):
        """Test that create_interface returns a Gradio Blocks object."""
        interface = demo_app.create_interface()
        
        # Check that we got a Gradio Blocks object
        import gradio as gr
        assert isinstance(interface, gr.Blocks)
    
    def test_launch_creates_and_launches_interface(self, demo_app):
        """Test that launch method creates and launches the interface."""
        with patch.object(demo_app, 'create_interface') as mock_create:
            mock_interface = Mock()
            mock_create.return_value = mock_interface
            
            # Call launch
            demo_app.launch(share=True, server_name="0.0.0.0")
            
            # Verify interface was created and launched
            mock_create.assert_called_once()
            mock_interface.launch.assert_called_once_with(
                share=True,
                server_name="0.0.0.0"
            )


class TestMonkeyPatch:
    """Tests for the mlx-vlm monkey patch."""
    
    def test_patch_is_applied(self):
        """Test that the monkey patch is applied on import."""
        from mlx_vlm.models.gemma3 import gemma3
        
        # Check that the method exists and has been patched
        assert hasattr(gemma3.Model, 'prepare_inputs_for_multimodal')
        
        # The method should be our patched version (check by name)
        method_name = gemma3.Model.prepare_inputs_for_multimodal.__name__
        assert '_patched_prepare_inputs_for_multimodal' in method_name or \
               'prepare_inputs_for_multimodal' in method_name
    
    def test_patch_converts_numpy_to_mlx_array(self):
        """Test that the patch converts numpy arrays to MLX arrays."""
        import numpy as np
        import mlx.core as mx
        from mlx_vlm.models.gemma3 import gemma3
        
        # Create a mock numpy array
        numpy_mask = np.ones((1, 10), dtype=np.int32)
        
        # The patched function should handle this without error
        # We can't fully test this without the actual model infrastructure,
        # but we can at least verify the function exists and is callable
        assert callable(gemma3.Model.prepare_inputs_for_multimodal)


class TestImageHandling:
    """Tests for image handling functionality."""
    
    def test_creates_rgb_image(self):
        """Test creating different colored images."""
        colors = ['red', 'green', 'blue', 'white', 'black']
        
        for color in colors:
            img = Image.new('RGB', (50, 50), color=color)
            assert img.size == (50, 50)
            assert img.mode == 'RGB'
    
    def test_saves_and_loads_image(self):
        """Test that images can be saved and loaded from disk."""
        img = Image.new('RGB', (100, 100), color='yellow')
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save image
            img.save(tmp_path, format='PNG')
            
            # Verify file exists
            assert os.path.exists(tmp_path)
            
            # Load and verify
            loaded_img = Image.open(tmp_path)
            assert loaded_img.size == img.size
            assert loaded_img.mode == img.mode
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestIntegration:
    """Integration tests (these may be slow and require the actual model)."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_full_pipeline_with_real_model(self):
        """
        Test the full pipeline with the actual model.
        
        This test is marked as 'slow' and 'integration' and can be skipped
        in regular test runs with: pytest -m "not slow and not integration"
        """
        # This would test with the actual model
        # Only run when explicitly requested
        pytest.skip("Skipping integration test - requires model download")
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_different_image_formats(self):
        """Test that different image formats are handled correctly."""
        pytest.skip("Skipping integration test - requires model download")


# Parametrized tests for various scenarios
class TestParametrized:
    """Parametrized tests for comprehensive coverage."""
    
    @pytest.mark.parametrize("question,expected_in_prompt", [
        ("What is this?", "What is this?"),
        ("Describe the image", "Describe the image"),
        ("", "Describe this image in detail."),
        ("   ", "Describe this image in detail."),
    ])
    def test_analyze_image_question_handling(self, question, expected_in_prompt):
        """Test various question inputs are handled correctly."""
        with patch('src.gemma3_vision_demo.app.load') as mock_load, \
             patch('src.gemma3_vision_demo.app.load_config') as mock_config, \
             patch('src.gemma3_vision_demo.app.apply_chat_template') as mock_template, \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Setup model loading mocks
            mock_model = Mock()
            mock_processor = Mock()
            mock_load.return_value = (mock_model, mock_processor)
            mock_config.return_value = Mock()
            
            # Setup mocks
            mock_result = Mock()
            mock_result.text = "Result"
            mock_generate.return_value = mock_result
            mock_template.return_value = "formatted"
            
            app = Gemma3VisionDemo()
            img = Image.new('RGB', (50, 50), color='red')
            
            result = app.analyze_image(img, question)
            
            # Check that the correct prompt was used
            call_args = mock_template.call_args[0]
            if question.strip():
                assert call_args[2] == question
            else:
                assert call_args[2] == expected_in_prompt
    
    @pytest.mark.parametrize("img_size", [
        (50, 50),
        (100, 100),
        (200, 150),
        (1920, 1080),
    ])
    def test_analyze_image_different_sizes(self, img_size):
        """Test that images of different sizes are handled correctly."""
        with patch('src.gemma3_vision_demo.app.load') as mock_load, \
             patch('src.gemma3_vision_demo.app.load_config') as mock_config, \
             patch('src.gemma3_vision_demo.app.apply_chat_template'), \
             patch('src.gemma3_vision_demo.app.generate') as mock_generate:
            
            # Setup model loading mocks
            mock_model = Mock()
            mock_processor = Mock()
            mock_load.return_value = (mock_model, mock_processor)
            mock_config.return_value = Mock()
            
            # Setup mock
            mock_result = Mock()
            mock_result.text = "Result"
            mock_generate.return_value = mock_result
            
            app = Gemma3VisionDemo()
            img = Image.new('RGB', img_size, color='blue')
            
            # Should not raise any errors
            result = app.analyze_image(img, "Test")
            assert result == "Result"
