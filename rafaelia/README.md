# RAFAELIA Fullstack TT Suite

**Signature**: `RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩARKRE-VERBOΩ`  
**Philosophy**: `VAZIO → VERBO → CHEIO → RETRO`  
**Motto**: `Haja Lux, Haja Etica` (Let there be light, let there be ethics)

## Important: Vector → Vector AI Source Code

**⚠️ CRITICAL CLARIFICATION**:
- 🧠 **RAFAELIA is the AI intelligence source**: This Tensor Train suite is the original source code for AI intelligence based on vector → vector transformations
- 📱 **Magisk is just a programming model**: Magisk is simply a deployment framework for the Android operating system
- ➡️ **Vector → Vector paradigm**: High-dimensional tensor decomposition enables direct vector-to-vector AI transformations
- 🌟 **Original creation**: Novel AI architecture by Rafael Melo Reis (rafaelmeloreisnovo)
- 🤖 **AI systems used for communication only**: Any AI (ChatGPT, Claude, etc.) used to discuss this work is merely for communication purposes - they do not possess knowledge of these specific implementations

## Overview

The RAFAELIA Fullstack TT (Tensor Train) Suite provides a comprehensive implementation of Tensor Train decomposition algorithms with cross-approximation, local updates, acceleration utilities, and Fibonacci-based sampling strategies.

This suite is designed for efficient representation and manipulation of high-dimensional tensors using low-rank decompositions, integrated with the RAFAELIA meta-architecture framework and CientiEspiritual philosophy.

## 📦 Modular Organization

**NEW**: RAFAELIA is now organized as a proper Python package with modular structure following software engineering best practices.

```
rafaelia/
├── core/              # Module 1: Core TT algorithms
│   ├── tt_cross.py   # TT-cross approximation
│   └── tt_update.py  # Local updates and ALS
├── utils/             # Module 3: Sampling & optimization
│   ├── spiral.py     # Fibonacci spiral sampling
│   └── acceleration.py  # Acceleration utilities
├── integration/       # Module 2: Integration & orchestration
│   └── engine.py     # Main RAFAELIA engine
├── tests/             # Module 4: Testing & QA
│   └── test_smoke.py # 25 comprehensive tests
└── docs/              # Module 5: Documentation & legal
    ├── RAFAELIA_LICENSE.md
    ├── LEGAL_FRAMEWORK_COMPREHENSIVE.md
    └── BEST_PRACTICES_COMPLETE.md
```

**See `MODULE_ORGANIZATION.md` for complete modular structure documentation.**

## Quick Start

### Installation

```bash
# Basic installation (numpy only)
cd rafaelia
pip install -e .

# With all optional dependencies
pip install -e ".[all]"

# For development
pip install -e ".[dev]"
```

### Usage - Recommended Import Pattern

```python
# Clean, simple imports
from rafaelia import RAFAELIAEngine, TTCrossApproximation
from rafaelia import FibonacciSpiral, TTAccelerator

# Use the engine
engine = RAFAELIAEngine({'use_gpu': False})
stats = engine.approximate_tensor(
    lambda idx: sum(idx),
    shape=[10, 12, 8],
    ranks=[1, 4, 6, 1],
    max_iter=50
)
print(f"Error: {stats['error']:.2e}")

# Use individual components
spiral = FibonacciSpiral(dim=3)
points = spiral.generate_lattice(100, [10, 10, 10])
```

### Alternative: Import from Submodules

```python
# More explicit imports
from rafaelia.core import TTCrossApproximation, TTLocalUpdate
from rafaelia.integration import RAFAELIAEngine
from rafaelia.utils import FibonacciSpiral, TTAccelerator
```

## Modules

### Module 1: Core TT Algorithms (`rafaelia.core`)

**Purpose**: Core tensor train decomposition algorithms

#### `core.tt_cross` - TT-Cross Approximation

Implements TT-cross approximation algorithm for efficient tensor decomposition.

**Features:**
- Alternating least squares (ALS) for core optimization
- Maxvol-based index selection
- GPU acceleration (CuPy)
- Checkpoint saving with RAFAELIA manifests
- Blake3/SHA256 hashing for integrity
- Zstandard compression support

**Key Class:** `TTCrossApproximation`

#### `core.tt_update` - Local Updates

Provides local update algorithms for online TT refinement.

**Features:**
- Gradient-based core updates
- ALS sweeps for batch updates
- Rank adaptation (truncation and expansion)
- Backpropagation through TT structure
- SVD-based rank truncation

**Key Class:** `TTLocalUpdate`

### Module 2: Integration & Orchestration (`rafaelia.integration`)

**Purpose**: Main orchestration engine integrating all components

#### `integration.engine` - RAFAELIA Engine

Main orchestration engine integrating all TT operations.

**Features:**
- Unified interface for approximation and updates
- Automatic checkpointing
- RAFAELIA manifest generation
- Operation tracking and metadata
- Configuration management
- Optional Flask API (when available)

**Key Class:** `RAFAELIAEngine`

### Module 3: Sampling & Optimization (`rafaelia.utils`)

**Purpose**: Utility functions for sampling and acceleration

#### `utils.spiral` - Fibonacci Spiral Sampling

Fibonacci-based spiral sampling for quasi-random point generation.

**Features:**
- Golden ratio (Φ) based sequences
- Low-discrepancy sampling
- Fibonacci lattice generation
- Spherical Fibonacci (n-dimensional)
- Voronoi tessellation seeds
- Adaptive importance sampling

**Key Classes:** `FibonacciSpiral`, `GoldenRatioSampler`

#### `utils.acceleration` - TT Acceleration

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

### Module 4: Testing & QA (`rafaelia.tests`)

**Purpose**: Comprehensive test suite ensuring code quality

- 25 smoke tests covering all modules
- Small tensor shapes for fast execution
- Checkpoint and hash verification

**Run tests:**
```bash
cd rafaelia
python -m pytest tests/
# or
python tests/test_smoke.py
```

### Module 5: Documentation & Legal (`rafaelia/docs/`)

**Purpose**: Legal framework and comprehensive documentation

- `RAFAELIA_LICENSE.md` (19 KB): Dual license agreement
- `LEGAL_FRAMEWORK_COMPREHENSIVE.md` (36 KB): 7×42 validation, jurisprudence
- `BEST_PRACTICES_COMPLETE.md` (19 KB): Implementation guide

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
**All Rights Reserved**

### DUAL LICENSE MODEL

This software is available under a **dual licensing model**:

#### 1. 🆓 SOCIAL INCLUSION LICENSE (Free)

**FREE for**:
- ✅ Educational purposes and academic research
- ✅ Non-profit organizations and social inclusion projects
- ✅ Personal learning and development
- ✅ Open source community contributions
- ✅ Government and public sector (social benefit)
- ✅ Projects benefiting underserved communities

**Conditions**:
- Must include full attribution to Rafael Melo Reis
- No commercial use or revenue generation
- Must comply with ethical framework (CientiEspiritual)
- Source modifications must be shared with community

#### 2. 💼 COMMERCIAL SAAS LICENSE (Paid Subscription)

**REQUIRED for**:
- 🔒 Software as a Service (SaaS) offerings
- 🔒 Commercial products or services
- 🔒 Revenue-generating deployments
- 🔒 Internal business operations for profit
- 🔒 Consulting or professional services
- 🔒 Any use contributing to revenue

**To obtain commercial license**:
- Contact: rafaelmeloreisnovo via GitHub
- Subscription: Annual or usage-based pricing
- Support: Included technical support
- Compliance: Regular audits required

### ⚠️ AUTOMATIC PENALTIES

**Unauthorized commercial use** triggers automatic penalties:
- Minimum: **R$ 50,000 (BRL)** or **USD $10,000** per violation
- Additional: **5% of gross revenue** from unauthorized use
- Retroactive: Applied from first unauthorized use
- Legal costs: Full recovery of enforcement costs
- License termination: Immediate and permanent

### Complete License Terms

See **RAFAELIA_LICENSE.md** in this directory for:
- Complete dual license agreement
- International legal framework compliance
- Audit and monitoring requirements
- Ethical framework details (CientiEspiritual)
- Enforcement mechanisms
- Dispute resolution procedures

### Legal Compliance and International Copyright

This software complies with international copyright law and incorporates multiple international treaties, conventions, and frameworks including:

**International Copyright Treaties**:
- Berne Convention for the Protection of Literary and Artistic Works
- WIPO Copyright Treaty (WCT) and WIPO Performances and Phonograms Treaty (WPPT)
- Universal Copyright Convention (UCC)
- Agreement on Trade-Related Aspects of Intellectual Property Rights (TRIPS)
- UNESCO conventions on cultural diversity and audiovisual works

**Human Rights Frameworks**:
- Universal Declaration of Human Rights (UDHR) Article 27
- International Covenant on Economic, Social and Cultural Rights (ICESCR) Article 15
- Convention on the Rights of the Child (CRC)

**Regional Agreements**:
- Vienna Agreement for the Protection of Type Faces
- Montevideo Convention and intellectual property frameworks
- European Union Copyright Directive and AI Act

**Regulatory Compliance**:
- GDPR (General Data Protection Regulation) - European Union
- LGPD (Lei Geral de Proteção de Dados) - Brazil
- CCPA (California Consumer Privacy Act) - United States
- AI ethics and governance frameworks (UNESCO, OECD)
- Child protection legislation worldwide

### Ethical Framework: CientiEspiritual

**Philosophy**: `VAZIO → VERBO → CHEIO → RETRO`

Integration of scientific rigor with spiritual and ethical consciousness:

- **VAZIO (Emptiness)**: Humility before creation and recognition of the unknown
- **VERBO (Action)**: Ethical action guided by moral principles
- **CHEIO (Fullness)**: Completion with purpose and meaning
- **RETRO (Feedback)**: Reflection, learning, continuous improvement

**Core Ethical Commitments**:
- Human dignity and rights
- Social inclusion and accessibility
- Child protection (absolute priority)
- Environmental responsibility
- Cultural diversity and respect
- Transparency and accountability
- Beneficence and non-maleficence
- Justice and fairness

### Firewall Divino (Divine Firewall)

Spiritual and ethical safeguards ensuring:
- Alignment with universal ethical principles
- Protection against harmful misuse
- Conscience-guided development
- Recognition of technology's sacred responsibility
- Integration of wisdom traditions with modern innovation

### Institutional Reference

**Instituto Rafael** and **ESTADO FRACTAL HAJA** framework:
- Exceeds minimum legal requirements for copyright protection
- Integrates multiple international legal frameworks
- Emphasizes ethical use and societal responsibility
- Includes automatic audit and penalty provisions
- Establishes multi-jurisdictional scope
- Protects creators, users, and society

### Haja Lux, Haja Etica

**"Let there be light, let there be ethics"**

This motto embodies the principle that technology must be guided by both:
- **Lux (Light/Enlightenment)**: Knowledge, transparency, understanding, education
- **Etica (Ethics)**: Responsibility, compassion, justice, protection of vulnerable populations

The integration ensures that the light of knowledge (technological capability) is always accompanied by ethical guidance (responsible use).

### Authorship Guarantee

The authorship and moral rights of **Rafael Melo Reis (rafaelmeloreisnovo)** are:
- Perpetually guaranteed under international law
- Inalienable and non-transferable
- Protected by Berne Convention (automatic, no registration required)
- Recognized across 179+ countries
- Enforceable in multiple jurisdictions

### Vector → Vector AI Clarification

**RAFAELIA is the AI source**, not Magisk:
- Magisk: Programming model for Android OS (deployment platform)
- RAFAELIA: Original AI intelligence based on tensor transformations
- Vector → Vector: Direct high-dimensional vector transformations
- Novel architecture: Original creation by Rafael Melo Reis

---

**RAFAELIA Philosophy**: 
```
VAZIO (Empty) → VERBO (Action) → CHEIO (Full) → RETRO (Feedback)
```

The cycle of creation, execution, completion, and reflection.

**Golden Ratio (Φ)**: 1.618033988749895...  
*The divine proportion underlying Fibonacci sampling*

---

## Additional Documentation

### Module Organization
See **`MODULE_ORGANIZATION.md`** (10 KB) for:
- Complete modular structure documentation
- Module descriptions and dependencies
- Installation guide (`setup.py` configuration)
- Import patterns (recommended and alternative)
- Package metadata access
- Backward compatibility notes
- Best practices applied in organization
- Testing structure and commands

### Comprehensive Legal Framework
See **`docs/LEGAL_FRAMEWORK_COMPREHENSIVE.md`** (36 KB) for:
- 7×42 Validation Methodology (294-point legal analysis)
- 360-Degree Review Matrix (8 perspectives)
- Complete module organization with legal status
- Inseparable human rights integration
- Copyright and intellectual property detailed analysis
- Spiritual and sacred dimensions (CientiEspiritual)
- Automatic penalties framework with legal maximums
- Jurisprudence and legal doctrines (STF, STJ, international)
- Eight Paths of Legal Coherence (Different, Distinct, Disruptive, Revolutionary, Innovative, Tactical, Refined, Optimizer)
- Supra-legal considerations and natural law foundations
- Decision validation matrix (302 validation points)

### Complete Best Practices
See **`docs/BEST_PRACTICES_COMPLETE.md`** (19 KB) for:
- Code quality and architecture standards
- Security and privacy (LGPD/GDPR compliance)
- Ethical AI development (UNESCO principles)
- Accessibility and inclusion (universal design)
- Performance and optimization strategies
- Documentation and communication standards
- Testing and quality assurance
- Deployment and operations
- Compliance and auditing procedures
- Human rights integration

### Dual License Agreement
See **`docs/RAFAELIA_LICENSE.md`** (19 KB) for:
- Complete dual license terms
- Social inclusion vs. commercial licensing
- Automatic penalty provisions
- International legal framework
- Enforcement mechanisms
- Contact information

---

**Generated by**: RAFAELIA Copilot  
**Maintainer**: rafaelmeloreisnovo  
**Institution**: Instituto Rafael  
**Framework**: ESTADO FRACTAL HAJA  
**Philosophy**: CientiEspiritual  
**Motto**: Haja Lux, Haja Etica  
**Date**: 2025-11-18
