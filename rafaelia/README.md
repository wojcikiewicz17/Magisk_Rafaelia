# RAFAELIA Fullstack TT Suite

**Signature**: `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩARKRE-VERBOΩ`  
**Philosophy**: `VAZIO → VERBO → CHEIO → RETRO`

## Overview

The RAFAELIA Fullstack TT (Tensor Train) Suite provides a comprehensive implementation of Tensor Train decomposition algorithms with cross-approximation, local updates, acceleration utilities, and Fibonacci-based sampling strategies.

This suite is designed for efficient representation and manipulation of high-dimensional tensors using low-rank decompositions, integrated with the RAFAELIA meta-architecture framework.

## Modules

### 1. RAFAELIA_TT_CROSS_FULL.py

Implements TT-cross approximation algorithm for efficient tensor decomposition.

**Features:**
- Alternating least squares (ALS) for core optimization
- Maxvol-based index selection
- GPU acceleration (CuPy)
- Checkpoint saving with RAFAELIA manifests
- Blake3/SHA256 hashing for integrity
- Zstandard compression support

**Key Class:** `TTCrossApproximation`

### 2. RAFAELIA_TT_UPDATE_FULL.py

Provides local update algorithms for online TT refinement.

**Features:**
- Gradient-based core updates
- ALS sweeps for batch updates
- Rank adaptation (truncation and expansion)
- Backpropagation through TT structure
- SVD-based rank truncation

**Key Class:** `TTLocalUpdate`

### 3. RAFAELIA_ENGINE_FULLSTACK.py

Main orchestration engine integrating all TT operations.

**Features:**
- Unified interface for approximation and updates
- Automatic checkpointing
- RAFAELIA manifest generation
- Operation tracking and metadata
- Configuration management
- Optional Flask API (when available)

**Key Class:** `RAFAELIAEngine`

### 4. RAFAELIA_SPIRAL_FIBONACCI.py

Fibonacci-based spiral sampling for quasi-random point generation.

**Features:**
- Golden ratio (Φ) based sequences
- Low-discrepancy sampling
- Fibonacci lattice generation
- Spherical Fibonacci (n-dimensional)
- Voronoi tessellation seeds
- Adaptive importance sampling

**Key Classes:** `FibonacciSpiral`, `GoldenRatioSampler`

### 5. RAFAELIA_TT_ACCEL.py

Acceleration utilities for TT operations.

**Features:**
- Batch evaluation with vectorization
- LRU caching for results
- Performance profiling
- Numba JIT compilation
- GPU kernel acceleration
- Core optimization (sparsification)
- Parallel sampling support

**Key Classes:** `TTAccelerator`, `TTCache`, `PerformanceProfiler`

## Dependencies

### Required
- `numpy` - Core numerical operations

### Optional (with safe fallbacks)
- `cupy` - GPU acceleration
- `numba` - JIT compilation
- `scipy` - Advanced linear algebra
- `blake3` - Fast cryptographic hashing
- `zstandard` - Compression
- `flask` - Web API (engine only)

**Note:** All modules gracefully fall back to numpy-only operation when optional dependencies are unavailable.

## Installation

```bash
# Clone repository
git clone https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia/rafaelia

# Install required dependency
pip install numpy

# Install optional dependencies (recommended)
pip install cupy-cuda11x  # Replace with your CUDA version
pip install numba scipy blake3 zstandard flask
```

## Usage Examples

### Quick Start - TT-Cross Approximation

```bash
# Run TT-cross demo
python3 RAFAELIA_TT_CROSS_FULL.py
```

```python
from RAFAELIA_TT_CROSS_FULL import TTCrossApproximation

# Define function to approximate
def my_function(indices):
    return sum(indices) + np.prod(indices) * 0.1

# Create approximation
shape = [10, 12, 8]
ranks = [1, 3, 4, 1]
tt = TTCrossApproximation(shape, ranks)

# Approximate
stats = tt.cross_approximation(my_function, max_iter=50, verbose=True)

# Evaluate at point
value = tt.evaluate([5, 6, 4])

# Save checkpoint
tt.save_checkpoint('my_checkpoint.json')
```

### Local Updates

```bash
# Run TT-update demo
python3 RAFAELIA_TT_UPDATE_FULL.py
```

```python
from RAFAELIA_TT_UPDATE_FULL import TTLocalUpdate

# Create from existing cores
tt_update = TTLocalUpdate(cores, use_gpu=False)

# Define target data
target_data = {
    (1, 2, 3): 5.0,
    (4, 5, 6): 8.2,
    # ... more samples
}

# Perform ALS updates
stats = tt_update.als_sweep(target_data, n_iterations=10, verbose=True)

# Adapt ranks
tt_update.rank_adaptation(core_idx=1, new_rank=5, method='expand')
```

### Fullstack Engine

```bash
# Run engine demo
python3 RAFAELIA_ENGINE_FULLSTACK.py
```

```python
from RAFAELIA_ENGINE_FULLSTACK import RAFAELIAEngine

# Configure engine
config = {
    'use_gpu': False,
    'checkpoint_dir': './checkpoints',
    'auto_checkpoint': True,
    'compression': True
}

engine = RAFAELIAEngine(config)

# Approximate tensor
stats = engine.approximate_tensor(
    func=my_function,
    shape=[10, 12, 8],
    ranks=[1, 3, 4, 1],
    max_iter=50
)

# Update with new data
engine.update_tensor(target_data, n_iterations=10)

# Evaluate
value = engine.evaluate([5, 6, 4])

# Generate manifest
manifest = engine.generate_manifest('manifest.json')
```

### Fibonacci Spiral Sampling

```bash
# Run spiral demo
python3 RAFAELIA_SPIRAL_FIBONACCI.py
```

```python
from RAFAELIA_SPIRAL_FIBONACCI import FibonacciSpiral

# Create spiral generator
spiral = FibonacciSpiral(dimension=3, shape=[10, 12, 8])

# Generate quasi-random points
points = spiral.generate_points(n_points=100)

# Fibonacci lattice
lattice = spiral.fibonacci_lattice(n_points=50)

# Spherical sampling
sphere_points = spiral.spherical_fibonacci(n_points=200)
```

### Acceleration

```bash
# Run acceleration demo
python3 RAFAELIA_TT_ACCEL.py
```

```python
from RAFAELIA_TT_ACCEL import TTAccelerator

# Initialize accelerator
accel = TTAccelerator(use_gpu=False, use_cache=True, cache_size=1000)

# Batch evaluation
values = accel.batch_evaluate(cores, indices_batch)

# Optimize cores
optimized = accel.optimize_core_contraction(cores)

# Get statistics
stats = accel.get_stats()
```

## Running Tests

```bash
# Run smoke tests
cd tests
python3 test_smoke.py

# Run with verbose output
python3 test_smoke.py -v
```

## CLI Examples

```bash
# Run all demos sequentially
for module in RAFAELIA_TT_CROSS_FULL RAFAELIA_TT_UPDATE_FULL \
              RAFAELIA_ENGINE_FULLSTACK RAFAELIA_SPIRAL_FIBONACCI \
              RAFAELIA_TT_ACCEL; do
    echo "Running $module..."
    python3 ${module}.py
    echo ""
done

# Run with small test shapes (fast)
python3 -c "
from RAFAELIA_ENGINE_FULLSTACK import RAFAELIAEngine
import numpy as np

engine = RAFAELIAEngine()
shape = [3, 4, 5]
ranks = [1, 2, 2, 1]

def test_func(idx):
    return sum(idx)

stats = engine.approximate_tensor(test_func, shape, ranks, max_iter=5)
print(f'Done: error={stats[\"error\"]:.2e}')
"
```

## Architecture

### Tensor Train Decomposition

A d-dimensional tensor A is represented as:

```
A[i₁, i₂, ..., iₐ] = G₁[i₁] × G₂[i₂] × ... × Gₐ[iₐ]
```

Where each Gₖ is a 3D core tensor of shape `[rₖ₋₁, nₖ, rₖ]` with r₀ = rₐ = 1.

### TT-Cross Algorithm

1. Initialize random cores
2. Left-to-right sweep: optimize each core using sampled values
3. Right-to-left sweep: refine cores
4. Check convergence
5. Repeat until error < ε or max iterations

### Local Updates

1. Compute gradient of loss w.r.t. each core
2. Apply gradient descent step
3. Perform ALS sweep (alternating optimization)
4. Optionally adapt ranks using SVD truncation

### Fibonacci Sampling

Uses golden ratio (Φ ≈ 1.618) to generate low-discrepancy sequences:

```
xₙ = (n × 1/Φ) mod 1
```

Provides better coverage than uniform random sampling.

## RAFAELIA Integration

All modules include:

- **RAFAELIA Signature**: `RAFCODE-Φ-∆RafaelVerboΩ`
- **Philosophy**: `VAZIO → VERBO → CHEIO → RETRO`
- **Manifests**: JSON files with metadata and integrity hashes
- **Checkpointing**: Automatic save/load with compression
- **Hashing**: SHA256 and Blake3 for data integrity

### Manifest Structure

```json
{
  "signature": "RAFCODE-Φ-∆RafaelVerboΩ",
  "module": "TT_CROSS_FULL",
  "philosophy": "VAZIO → VERBO → CHEIO → RETRO",
  "timestamp": 1699999999.999,
  "metadata": { ... },
  "hashes": {
    "sha256": "abc123...",
    "blake3": "def456..."
  }
}
```

## Security Notes

- **Optional Dependencies**: blake3 and zstd are optional; system works without them
- **No Tokens in Code**: No API keys or secrets are stored in source files
- **Checksums**: All saved data includes integrity hashes
- **Safe Fallbacks**: All operations degrade gracefully without optional dependencies
- **No Network Access**: Core algorithms run entirely offline

⚠️ **Warning**: Do not place authentication tokens or API keys in PR descriptions or code files.

## Performance Tips

1. **Enable GPU**: Install CuPy for 10-100x speedup on large tensors
2. **Use Caching**: Enable cache in TTAccelerator for repeated evaluations
3. **Optimize Ranks**: Use rank adaptation to balance accuracy vs speed
4. **Batch Operations**: Process multiple samples together for vectorization
5. **Enable Compression**: Use zstd for smaller checkpoint files

## Troubleshooting

### Import Errors
- **Solution**: Install numpy (`pip install numpy`)
- Optional deps can be skipped; code will use safe fallbacks

### GPU Errors
- **Solution**: Set `use_gpu=False` in configuration
- CuPy requires CUDA-compatible GPU

### Memory Issues
- **Solution**: Reduce tensor shape or ranks
- Use rank adaptation to lower memory usage
- Enable checkpoint compression

### Slow Performance
- **Solution**: Install optional dependencies (numba, cupy)
- Reduce max_iter or use smaller test cases
- Enable caching in accelerator

## Contributing

Contributions should maintain:
- RAFAELIA signature and philosophy references
- Safe fallback behavior for optional dependencies
- Comprehensive docstrings
- Checkpoint/manifest generation
- Unit tests in tests/test_smoke.py

## References

- **TT-Cross**: I. V. Oseledets, "Tensor-Train Decomposition", SIAM J. Sci. Comput., 2011
- **Golden Ratio Sampling**: Fibonacci sphere algorithm, Gonzalez, 2009
- **RAFAELIA Meta-Architecture**: See `docs/RAFAELIA_META_ARCHITECTURE.md`
- **RAFAELIA Manifest**: See `RAFAELIA_MANIFEST.json` in repository root

## License

See LICENSE file in repository root.

---

**RAFAELIA Philosophy**: 
```
VAZIO (Empty) → VERBO (Action) → CHEIO (Full) → RETRO (Feedback)
```

The cycle of creation, execution, completion, and reflection.

**Golden Ratio (Φ)**: 1.618033988749895...  
*The divine proportion underlying Fibonacci sampling*

---

**Generated by**: RAFAELIA Copilot  
**Maintainer**: rafaelmeloreisnovo  
**Date**: 2025-11-18
