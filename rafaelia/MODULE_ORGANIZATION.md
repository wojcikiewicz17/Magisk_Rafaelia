# RAFAELIA Module Organization

**Copyright (C) 2025 Rafael Melo Reis (rafaelmeloreisnovo)**  
**All Rights Reserved**

This document describes the modular organization of the RAFAELIA Fullstack TT Suite following software engineering best practices.

---

## Module Structure

```
rafaelia/
├── __init__.py                          # Main package interface
├── setup.py                             # Package installation configuration
│
├── core/                                # Module 1: Core TT Algorithms
│   ├── __init__.py
│   ├── tt_cross.py                      # TT-cross approximation (TTCrossApproximation)
│   └── tt_update.py                     # Local updates and ALS (TTLocalUpdate)
│
├── utils/                               # Module 3: Sampling & Optimization
│   ├── __init__.py
│   ├── spiral.py                        # Fibonacci spiral sampling (FibonacciSpiral, GoldenRatioSampler)
│   └── acceleration.py                  # Acceleration utilities (TTAccelerator)
│
├── integration/                         # Module 2: Integration & Orchestration
│   ├── __init__.py
│   └── engine.py                        # Main engine (RAFAELIAEngine)
│
├── tests/                               # Module 4: Testing & QA
│   ├── __init__.py
│   └── test_smoke.py                    # Smoke tests (25 tests)
│
├── docs/                                # Module 5: Documentation & Legal
│   ├── RAFAELIA_LICENSE.md              # Dual license agreement (19 KB)
│   ├── LEGAL_FRAMEWORK_COMPREHENSIVE.md # Legal analysis (36 KB)
│   └── BEST_PRACTICES_COMPLETE.md       # Implementation guide (19 KB)
│
└── README.md                            # Main documentation & quick start
```

---

## Module Descriptions

### Module 1: Core TT Algorithms (`rafaelia.core`)

**Purpose**: Core tensor train decomposition algorithms

**Components**:
- `tt_cross.py` (TTCrossApproximation): TT-cross approximation with maxvol index selection
- `tt_update.py` (TTLocalUpdate): Local updates via ALS sweeps, rank adaptation

**Legal Status**: Original works of authorship, fully copyrighted  
**Rights**: All economic and moral rights reserved to Rafael Melo Reis  
**Best Practices**: Clean code architecture, comprehensive documentation, safe fallbacks  
**Ethical Considerations**: AI safety, transparency, responsible deployment

**Usage**:
```python
from rafaelia.core import TTCrossApproximation, TTLocalUpdate

# TT-cross approximation
tt_cross = TTCrossApproximation(shape=[10, 12, 8], ranks=[1, 4, 6, 1])
result = tt_cross.approximate(tensor_function, max_iter=50)

# Local updates
tt_update = TTLocalUpdate(cores)
updated_cores = tt_update.als_sweep(tensor_function, indices)
```

### Module 2: Integration & Orchestration (`rafaelia.integration`)

**Purpose**: Main orchestration engine integrating all components

**Components**:
- `engine.py` (RAFAELIAEngine): Main RAFAELIA engine with auto-checkpointing, configuration management

**Legal Status**: Derivative work incorporating Core modules, independently copyrightable  
**Rights**: Compilation copyright, integration design rights  
**Best Practices**: Modular design, extensibility, backward compatibility  
**Ethical Considerations**: User autonomy, data privacy, fair use provisions

**Usage**:
```python
from rafaelia.integration import RAFAELIAEngine

engine = RAFAELIAEngine({'use_gpu': False})
stats = engine.approximate_tensor(
    tensor_func,
    shape=[10, 12, 8],
    ranks=[1, 4, 6, 1],
    max_iter=50
)
```

### Module 3: Sampling & Optimization (`rafaelia.utils`)

**Purpose**: Utility functions for sampling and acceleration

**Components**:
- `spiral.py` (FibonacciSpiral, GoldenRatioSampler): Fibonacci-based sampling, golden ratio sequences
- `acceleration.py` (TTAccelerator): Batch evaluation, caching, profiling

**Legal Status**: Mathematical implementations with creative expression  
**Rights**: Algorithm expression copyright  
**Best Practices**: Performance optimization, resource efficiency, accessibility  
**Ethical Considerations**: Computational equity, environmental responsibility

**Usage**:
```python
from rafaelia.utils import FibonacciSpiral, TTAccelerator

# Fibonacci spiral sampling
spiral = FibonacciSpiral(dim=3)
points = spiral.generate_lattice(n_points=100, shape=[10, 10, 10])

# Acceleration
accelerator = TTAccelerator()
results = accelerator.batch_evaluate(tensor_func, indices_list)
```

### Module 4: Testing & Quality Assurance (`rafaelia.tests`)

**Purpose**: Comprehensive test suite ensuring code quality

**Components**:
- `test_smoke.py`: 25 smoke tests covering all modules

**Legal Status**: Test code as creative work, documentation function  
**Rights**: Copyrighted as part of overall work  
**Best Practices**: Comprehensive coverage, maintainability, CI/CD integration  
**Ethical Considerations**: Quality assurance, user trust, safety verification

**Usage**:
```bash
cd rafaelia
python -m pytest tests/
# or
python tests/test_smoke.py
```

### Module 5: Documentation & Legal (`rafaelia/docs/`)

**Purpose**: Legal framework and comprehensive documentation

**Components**:
- `RAFAELIA_LICENSE.md` (19 KB): Dual license agreement
- `LEGAL_FRAMEWORK_COMPREHENSIVE.md` (36 KB): 7×42 validation, jurisprudence
- `BEST_PRACTICES_COMPLETE.md` (19 KB): Implementation guide

**Legal Status**: Legal instrument and creative documentation  
**Rights**: Copyright in expression, legal enforceability  
**Best Practices**: Clarity, comprehensiveness, accessibility  
**Ethical Considerations**: Transparency, informed consent

---

## Installation

### Standard Installation (numpy only)
```bash
cd rafaelia
pip install -e .
```

### With Optional Dependencies
```bash
# GPU acceleration
pip install -e ".[gpu]"

# All optimizations
pip install -e ".[all]"

# Development tools
pip install -e ".[dev]"
```

---

## Import Patterns

### Recommended: Use top-level imports
```python
# Clean, simple imports
from rafaelia import TTCrossApproximation, TTLocalUpdate, RAFAELIAEngine
from rafaelia import FibonacciSpiral, TTAccelerator

# Use the classes
engine = RAFAELIAEngine()
spiral = FibonacciSpiral(dim=3)
```

### Alternative: Import from submodules
```python
# More explicit
from rafaelia.core import TTCrossApproximation, TTLocalUpdate
from rafaelia.integration import RAFAELIAEngine
from rafaelia.utils import FibonacciSpiral, TTAccelerator
```

### For advanced users: Direct module imports
```python
# Full control
import rafaelia.core.tt_cross as tt_cross
import rafaelia.integration.engine as engine

approximation = tt_cross.TTCrossApproximation(...)
eng = engine.RAFAELIAEngine(...)
```

---

## Package Metadata

Access package information programmatically:

```python
import rafaelia

print(rafaelia.__version__)        # "1.0.0"
print(rafaelia.__author__)         # "Rafael Melo Reis (rafaelmeloreisnovo)"
print(rafaelia.__copyright__)      # "Copyright (C) 2025 Rafael Melo Reis"
print(rafaelia.__license__)        # "Dual License - See RAFAELIA_LICENSE.md"
print(rafaelia.__institution__)    # "Instituto Rafael"
print(rafaelia.__framework__)      # "ESTADO FRACTAL HAJA"
print(rafaelia.__philosophy__)     # "CientiEspiritual"
```

---

## Backward Compatibility

The original standalone scripts are maintained for compatibility:

```python
# Legacy imports still work
from rafaelia.RAFAELIA_TT_CROSS_FULL import TTCrossApproximation
from rafaelia.RAFAELIA_ENGINE_FULLSTACK import RAFAELIAEngine
```

However, new code should use the modular imports for better organization.

---

## Best Practices Applied

This module organization follows the best practices documented in `BEST_PRACTICES_COMPLETE.md`:

1. **Code Quality & Architecture**:
   - Single Responsibility Principle: Each module has one clear purpose
   - DRY: Shared code in appropriate modules
   - Clean imports and namespace management

2. **Modularity**:
   - Clear separation between core algorithms, utilities, and integration
   - Each module independently testable
   - Loose coupling, high cohesion

3. **Accessibility**:
   - Simple top-level imports for ease of use
   - Advanced import patterns for power users
   - Comprehensive documentation at every level

4. **Maintainability**:
   - Clear module boundaries
   - Self-documenting structure
   - Easy to extend and modify

5. **Professional Standards**:
   - Proper `__init__.py` files
   - setup.py for installation
   - Package metadata
   - Standard Python project layout

---

## Module Dependencies

```
rafaelia (main package)
│
├── core/                     # No internal dependencies
│   ├── tt_cross.py          # → numpy, hashlib, json (stdlib)
│   └── tt_update.py         # → numpy, time (stdlib)
│
├── utils/                    # No internal dependencies
│   ├── spiral.py            # → numpy, math (stdlib)
│   └── acceleration.py      # → numpy, time (stdlib)
│
└── integration/              # Depends on core/
    └── engine.py            # → core.tt_cross, core.tt_update, utils.*
```

**Dependency Philosophy**: 
- Core modules are self-contained (no cross-dependencies)
- Integration layer orchestrates core and utils
- Clean, acyclic dependency graph

---

## Testing Structure

```python
# Run all tests
python -m pytest rafaelia/tests/

# Run specific test categories
python -m pytest rafaelia/tests/test_smoke.py::TestTTCross
python -m pytest rafaelia/tests/test_smoke.py::TestEngine

# With coverage
python -m pytest --cov=rafaelia rafaelia/tests/
```

**Test Organization**:
- 25 smoke tests total
- Organized by module (TestTTCross, TestTTUpdate, TestEngine, etc.)
- Small tensor shapes for fast execution
- Checkpoint and hash verification

---

## License and Legal

**Dual License Model**:
- **Free**: Social inclusion (education, research, non-profit)
- **Paid**: Commercial SaaS and revenue-generating use

**Complete Legal Framework**:
- 7×42 validation methodology (294 points)
- 360° review (8 perspectives)
- Total: 302 validation points
- See `docs/LEGAL_FRAMEWORK_COMPREHENSIVE.md`

**Best Practices**:
- See `docs/BEST_PRACTICES_COMPLETE.md`
- UNESCO AI ethics, LGPD/GDPR compliance
- Accessibility, security, ethical AI

---

**Copyright (C) 2025 Rafael Melo Reis (rafaelmeloreisnovo)**  
**All Rights Reserved**

**Institution**: Instituto Rafael  
**Framework**: ESTADO FRACTAL HAJA  
**Philosophy**: CientiEspiritual  
**Motto**: Haja Lux, Haja Etica
