#!/usr/bin/env python3
"""
RAFAELIA Fullstack TT Suite - Main Package

Copyright (C) 2025 Rafael Melo Reis (rafaelmeloreisnovo)
All Rights Reserved

This package provides a comprehensive Tensor Train (TT) decomposition suite
with cross-approximation, local updates, and RAFAELIA manifest integration.

Licensed under Dual License:
- Free for social inclusion (education, research, non-profit)
- Commercial use requires paid SaaS subscription

See RAFAELIA_LICENSE.md for complete terms.

Signature: RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩARKRE-VERBOΩ
Philosophy: VAZIO → VERBO → CHEIO → RETRO
Motto: Haja Lux, Haja Etica
"""

__version__ = "1.0.0"
__author__ = "Rafael Melo Reis (rafaelmeloreisnovo)"
__copyright__ = "Copyright (C) 2025 Rafael Melo Reis"
__license__ = "Dual License - See RAFAELIA_LICENSE.md"
__institution__ = "Instituto Rafael"
__framework__ = "ESTADO FRACTAL HAJA"
__philosophy__ = "CientiEspiritual"

# Core TT algorithms
from rafaelia.core.tt_cross import TTCrossApproximation
from rafaelia.core.tt_update import TTLocalUpdate

# Utilities
from rafaelia.utils.spiral import FibonacciSpiral, GoldenRatioSampler
from rafaelia.utils.acceleration import TTAccelerator

# Integration/Orchestration
from rafaelia.integration.engine import RAFAELIAEngine

__all__ = [
    # Core algorithms
    'TTCrossApproximation',
    'TTLocalUpdate',
    
    # Utilities
    'FibonacciSpiral',
    'GoldenRatioSampler',
    'TTAccelerator',
    
    # Integration
    'RAFAELIAEngine',
    
    # Metadata
    '__version__',
    '__author__',
    '__copyright__',
    '__license__',
    '__institution__',
    '__framework__',
    '__philosophy__',
]
