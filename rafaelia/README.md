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

**Copyright (C) 2025 Rafael Melo Reis (rafaelmeloreisnovo)**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

### Legal Compliance and International Copyright

This software complies with international copyright law and is licensed in accordance with multiple international treaties, conventions, and frameworks including but not limited to:

**International Copyright Treaties:**
- Berne Convention for the Protection of Literary and Artistic Works
- WIPO Copyright Treaty (WCT) and WIPO Performances and Phonograms Treaty (WPPT)
- Universal Copyright Convention (UCC)
- Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS)
- UNESCO Convention on the Protection and Promotion of the Diversity of Cultural Expressions
- UNESCO conventions on cultural diversity and audiovisual works

**Human Rights and Fundamental Freedoms:**
- Universal Declaration of Human Rights (UDHR) Article 27 - Right to protection of intellectual property
- International Covenant on Economic, Social and Cultural Rights (ICESCR) Article 15 - Right to benefit from the protection of moral and material interests

**Regional and Multilateral Agreements:**
- Vienna Agreement for the Protection of Type Faces
- Montevideo Convention and related intellectual property frameworks
- European Union Copyright Directive
- Other applicable bilateral and multilateral copyright agreements

### Jurisdiction and Applicable Law

This software and its use is subject to applicable laws in multiple jurisdictions including international treaties, conventions, and domestic legislation regarding:

- **Copyright and Intellectual Property Rights**: Full compliance with copyright law, software licensing standards, and intellectual property protections
- **Data Protection and Privacy**: GDPR (European Union), LGPD (Brazil), and equivalent data protection regulations worldwide
- **Artificial Intelligence Ethics and Governance**: Responsible AI development, transparency, accountability, and ethical guidelines
- **Child Protection and Online Safety**: Protection of minors, child online protection acts, and related safeguards
- **Audio-Visual Works Protection**: Additional protections for multimedia and audio-visual content under Microsoft and international standards
- **Software Licensing and Distribution**: Open source licensing compliance, GPL compatibility, and software distribution law
- **Digital Rights Management**: Respect for technological protection measures and digital rights
- **Interoperability and Technical Standards**: Compliance with international technical standards and interoperability requirements

### Ethical Commitment

This software is developed with explicit consideration for:

- **Human Rights and Fundamental Freedoms**: Respect for dignity, liberty, and fundamental rights of all users
- **Protection of Children and Vulnerable Populations**: Safeguards against exploitation, abuse, or harmful content
- **Responsible AI Development and Deployment**: Ethical AI principles including fairness, transparency, and accountability
- **Data Privacy and Security Best Practices**: Strong data protection, encryption, and secure development practices
- **Environmental and Societal Impact**: Consideration for sustainability and positive societal contribution
- **Cultural Diversity and Accessibility**: Inclusive design and respect for diverse cultures and capabilities
- **Scientific and Spiritual Dialogue (CientiEspiritual)**: Integration of scientific rigor with ethical and spiritual considerations

### Institutional Reference

This work is associated with **Instituto Rafael** and follows the **"ESTADO FRACTAL HAJA"** ethical and legal framework established by Rafael Melo Reis (rafaelmeloreisnovo). This framework represents a comprehensive approach to software licensing that:

- Exceeds minimum legal requirements for copyright protection
- Integrates multiple international legal frameworks
- Emphasizes ethical use and societal responsibility
- Includes provisions for audit, monitoring, and automatic penalties for violations
- Establishes clear jurisdictional scope across multiple legal systems
- Protects the interests of creators, users, and society at large

### Automatic Penalties and Audit Clauses

Unauthorized use, distribution, or modification outside the terms of the GNU GPL v3 license may trigger:
- Automatic termination of license rights
- Financial penalties under applicable copyright law
- Legal action in multiple jurisdictions
- Requirement for independent audit of compliance
- Additional remedies as provided by law

### Firewall Divino and Security

This software incorporates ethical safeguards ("Firewall Divino") to ensure:
- Alignment with moral and ethical principles
- Protection against misuse for harmful purposes
- Compliance with spiritual and ethical guidelines
- Respect for human dignity and rights

### Monitoring and Compliance

Users and distributors of this software are expected to:
- Maintain compliance with all applicable laws and regulations
- Implement appropriate monitoring and audit procedures
- Report violations or concerns through official channels
- Cooperate with compliance audits when requested
- Maintain records demonstrating legal compliance

### Contact and Questions

For questions regarding licensing, compliance, ethical use, or to report violations, please contact the copyright holder through official repository channels at:

**GitHub**: rafaelmeloreisnovo  
**Repository**: Magisk_Rafaelia  
**Associated Institution**: Instituto Rafael

### Additional Resources

- Full GPL v3 License: See LICENSE file in repository root
- RAFAELIA Meta-Architecture: See project documentation
- Instituto Rafael Framework: See instituto_Rafael repository (same author)
- ESTADO FRACTAL HAJA: Comprehensive ethical and legal framework for software development

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
