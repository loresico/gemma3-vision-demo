# Technical Notes

## mlx-vlm Library Compatibility Issue

### Problem Description

**Library Version:** mlx-vlm v0.3.5  
**Affected Model:** Gemma3 (mlx-community/gemma-3-4b-it-8bit)  
**Error Location:** `mlx_vlm/models/gemma3/gemma3.py:162`

#### Error Message
```
TypeError: expand_dims(): incompatible function arguments. The following argument types are supported:
    1. expand_dims(a: array, /, axis: Union[int, Sequence[int]], *, stream: Union[None, Stream, Device] = None) -> array

Invoked with types: ndarray, int
```

#### Root Cause
The `prepare_inputs_for_multimodal` method in the Gemma3 model receives `attention_mask` as a NumPy `ndarray` from the preprocessing pipeline, but attempts to use it directly with `mx.expand_dims()`, which requires an MLX `array` type.

Specifically, at line 162:
```python
attention_mask_expanded_1 = mx.expand_dims(attention_mask, 1)
```

The `attention_mask` variable is a NumPy array but needs to be an MLX array.

### Solution Implemented

#### Approach
A runtime monkey patch that wraps the `prepare_inputs_for_multimodal` static method to convert the `attention_mask` parameter before processing.

#### Implementation
Located in: `src/gemma3_vision_demo/app.py` (lines 19-49)

```python
from mlx_vlm.models.gemma3 import gemma3
import mlx.core as mx

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
    # Convert attention_mask to mx.array if it's not already
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

gemma3.Model.prepare_inputs_for_multimodal = _patched_prepare_inputs_for_multimodal
```

#### Why This Approach?
1. **Non-invasive**: Doesn't modify the installed library files
2. **Transparent**: Clearly documented in the code
3. **Safe**: Only affects this specific project
4. **Temporary**: Can be easily removed when upstream is fixed
5. **Publishable**: The code can be shared as-is with clear documentation

### Alternative Solutions Considered

#### 1. Fork mlx-vlm
- **Pros**: Clean fix at the source
- **Cons**: Maintenance burden, users need to install from fork

#### 2. Local library modification
- **Pros**: Direct fix in the library
- **Cons**: Not reproducible, breaks on library updates

#### 3. Wait for upstream fix
- **Pros**: No workaround needed
- **Cons**: Blocks development and usage

### Upstream Fix Status

**Status**: Not yet reported/fixed as of January 2025  
**Repository**: https://github.com/Blaizzy/mlx-vlm  
**Suggested Fix**: In `mlx_vlm/models/gemma3/gemma3.py`, line 130-131, add:

```python
# Ensure attention_mask is an MLX array
if not isinstance(attention_mask, mx.array):
    attention_mask = mx.array(attention_mask)
```

### When to Remove This Workaround

This patch can be safely removed when:
1. The issue is fixed in mlx-vlm upstream
2. The project upgrades to a fixed version
3. The project switches to a different model that doesn't have this issue

### Testing

Verified working with:
- mlx-vlm v0.3.5
- MLX v0.29.3
- Python 3.13
- macOS on Apple Silicon

### Related Documentation

- mlx-vlm GitHub: https://github.com/Blaizzy/mlx-vlm
- MLX Framework: https://github.com/ml-explore/mlx
- Issue discussion: See README.md "Known Issues" section
