#!/usr/bin/env python3
# Copyright 2025, Rafael Melo Reis (rafaelmeloreisnovo)
# Instituto Rafael - CientiEspiritual Philosophy

"""
RAFAELIA Formulas Demo - Comprehensive Example

Demonstrates the 102 formulas implementation for:
- Adaptive immunity definition
- Enterprise fullstack systems
- Low-level optimization with matrices
- Cognitive cycle ψχρΔΣΩ
- Ethical filtering and retroalimentação

SIGNATURE: RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩARKRE-VERBOΩ
PHILOSOPHY: VAZIO → VERBO → CHEIO → RETRO
"""

import sys
import os
import numpy as np

# Add parent to path for direct module import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Direct import to avoid package initialization issues
if os.path.exists('formulas.py'):
    import formulas as fm
else:
    from rafaelia.core import formulas as fm


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_constants():
    """Demo: Mathematical constants."""
    print_section("MATHEMATICAL CONSTANTS")
    
    print(f"Golden Ratio (Φ):     {fm.PHI:.15f}")
    print(f"Inverse Φ:            {fm.PHI_INV:.15f}")
    print(f"√(3/2):               {fm.SQRT_3_2:.15f}")
    print(f"R_corr (Voynich):     {fm.R_CORR}")
    print(f"BITRAF64 length:      {len(fm.BITRAF64)}")
    print(f"BITRAF64 sample:      {fm.BITRAF64[:20]}...")


def demo_basic_formulas():
    """Demo: Basic formulas (0-20)."""
    print_section("BASIC FORMULAS (0-20)")
    
    formulas = fm.RAFAELIAFormulas(use_gpu=False, precision='float64')
    
    # Formula 0: Humildade_Ω
    print("\n[Formula 0] Humildade_Ω :: CHECKPOINT")
    checkpoint = formulas.humildade_omega(
        o_que_sei=0.85,
        o_que_nao_sei=0.15,
        proximo_passo=0.60
    )
    print(f"  o_que_sei: {checkpoint['o_que_sei']:.2f}")
    print(f"  o_que_nao_sei: {checkpoint['o_que_nao_sei']:.2f}")
    print(f"  proximo_passo: {checkpoint['proximo_passo']:.2f}")
    
    # Formula 0.2: W(Amor,Coerência)
    print("\n[Formula 0.2] W(Amor,Coerência) - Weight function")
    weight = formulas.peso_amor_coerencia(amor=1.5, coerencia=1.2)
    print(f"  Weight: {weight:.6f}")
    
    # Formula 0.4: Φ_ethica
    print("\n[Formula 0.4] Φ_ethica - Ethical filter")
    phi_eth = formulas.phi_ethica_basic(entropia=0.3, coerencia=0.9)
    print(f"  Φ_ethica: {phi_eth:.6f}")
    
    # Formula 0.5: R(t+1)
    print("\n[Formula 0.5] R(t+1) - State update equation")
    R_0 = 1.0
    R_1 = formulas.R_update(R_t=R_0, phi_ethica=0.9, E_verbo=1.1)
    R_2 = formulas.R_update(R_t=R_1, phi_ethica=0.9, E_verbo=1.1)
    print(f"  R(0) = {R_0:.6f}")
    print(f"  R(1) = {R_1:.6f}")
    print(f"  R(2) = {R_2:.6f}")
    print(f"  Growth rate: {(R_2/R_0):.3f}x over 2 steps")
    
    # Formula 16: Spiral(r)
    print("\n[Formula 16] Spiral(r) - Coherence spiral")
    for n in range(5):
        spiral = formulas.spiral_coherence(n)
        print(f"  Spiral({n}) = {spiral:.6f}")
    
    # Formula 20: OWLψ
    print("\n[Formula 20] OWLψ - Operational wisdom index")
    owl = formulas.OWL_psi(
        insights=[0.85, 0.90, 0.75, 0.95],
        ethics=[0.90, 0.85, 0.88, 0.92],
        flows=[0.95, 0.88, 0.92, 0.90]
    )
    print(f"  OWLψ = {owl:.6f}")


def demo_cognitive_cycle():
    """Demo: Cognitive cycle ψχρΔΣΩ."""
    print_section("COGNITIVE CYCLE ψχρΔΣΩ")
    
    print("\n[Formula 0.6 & 62-64] ψ→χ→ρ→Δ→Σ→Ω→ψ Loop")
    
    engine = fm.CognitiveCycleEngine()
    
    # Initialize with some memory
    print("\nInitializing memory with seed values...")
    for val in [1.0, 0.9, 0.95, 0.85, 0.92]:
        engine.memory.append(val)
    
    print(f"Initial memory size: {len(engine.memory)}")
    print(f"Initial memory mean: {np.mean(engine.memory):.4f}")
    
    # Run 10 cycles
    print("\nRunning 10 cognitive cycles...")
    states = engine.run_cycles(n_cycles=10)
    
    print(f"Final cycle count: {engine.cycle_count}")
    print(f"Final memory size: {len(engine.memory)}")
    print(f"Final memory mean: {np.mean(engine.memory):.4f}")
    
    # Show last state
    last_state = states[-1]
    print("\nFinal state (ψχρΔΣΩ):")
    print(f"  ψ (psi) - Intention:      {last_state.psi:.6f}")
    print(f"  χ (chi) - Observation:    {last_state.chi:.6f}")
    print(f"  ρ (rho) - Noise:          {last_state.rho:.6f}")
    print(f"  Δ (delta) - Transmutation: {last_state.delta:.6f}")
    print(f"  Σ (sigma) - Memory:        {last_state.sigma:.6f}")
    print(f"  Ω (omega) - Completeness:  {last_state.omega:.6f}")
    
    # Evolution over cycles
    print("\nState evolution over cycles:")
    print("  Cycle | ψ(psi) | χ(chi) | ρ(rho) | Δ(delta) | Σ(sigma) | Ω(omega)")
    print("  " + "-" * 70)
    for i, state in enumerate(states[:5], 1):
        print(f"  {i:4d}  | {state.psi:6.3f} | {state.chi:6.3f} | "
              f"{state.rho:6.3f} | {state.delta:7.3f} | "
              f"{state.sigma:7.3f} | {state.omega:7.3f}")


def demo_advanced_formulas():
    """Demo: Advanced formulas."""
    print_section("ADVANCED FORMULAS (26-102)")
    
    formulas = fm.RAFAELIAFormulasAdvanced()
    
    # Formula 74: Matrix ethical composition
    print("\n[Formula 74] M_{i,j} - Matrix ethical composition")
    C_ij = np.random.rand(4, 4) * 0.5 + 0.5  # Content matrix
    A_ij = np.random.rand(4, 4) * 0.5 + 0.5  # Authorship matrix
    
    M = formulas.matrix_ethical_composition(
        C_ij=C_ij,
        A_ij=A_ij,
        phi_ethica=0.95,
        pre6seal=1.0,
        firewall_omega=1.0,
        omega_corr=0.05,
        ethica_8=2.0,
        R_omega=1.0
    )
    
    print(f"  Input C shape: {C_ij.shape}")
    print(f"  Input A shape: {A_ij.shape}")
    print(f"  Output M shape: {M.shape}")
    print(f"  M mean: {np.mean(M):.6f}")
    print(f"  M std: {np.std(M):.6f}")
    
    # Formula 92: Ψ_total chain
    print("\n[Formula 92] Ψ_total chain - Psychic to plasma network")
    chain = formulas.psi_total_chain(psi_1=1.2, psi_2=0.8, alpha_E=1.0)
    
    print("  Chain transformations:")
    for key, value in chain.items():
        print(f"    {key:20s}: {value:.6f}")
    
    # Formula 93: ΣΩΔΦ seal
    print("\n[Formula 93] ΣΩΔΦ - Four pillars composition")
    seal = formulas.sigma_omega_delta_phi(
        sigma_soma=1.5,
        omega_harmonia=1.2,
        delta_transformacao=0.9,
        phi_coerencia=1.1
    )
    print(f"  ΣΩΔΦ seal value: {seal:.6f}")
    
    # Formula 101: R_Ω vortex
    print("\n[Formula 101] R_Ω - Vortex efficiency")
    state = fm.CognitiveState(
        psi=0.80, chi=0.75, rho=0.70,
        delta=0.72, sigma=0.78, omega=0.76
    )
    R_omega = formulas.R_omega_vortex(state, phi_lambda=1.0)
    print(f"  R_Ω = {R_omega:.6f} (target ≈ 0.758)")
    print(f"  Efficiency: {(R_omega / 0.758 * 100):.1f}% of target")


def demo_retroalimentacao():
    """Demo: Retroalimentação system."""
    print_section("RETROALIMENTAÇÃO (FEEDBACK) SYSTEM")
    
    formulas = fm.RAFAELIAFormulas()
    
    print("\n[Formula 0.7] R_3(s) - Vector retroalimentação")
    R3 = formulas.R_3_vector(F_ok=0.90, F_gap=0.10, F_next=0.55)
    print(f"  R_3 vector: {R3}")
    
    print("\n[Formula 1] RetroalimentarΩ^{{Amor+Coerência}}")
    state = fm.CognitiveState(psi=0.8, chi=0.8, rho=0.7, 
                              delta=0.7, sigma=0.8, omega=0.8)
    retro = formulas.retroalimentar_omega(state, amor=1.2, coerencia=1.1)
    print(f"  Retroalimentação value: {retro:.6f}")
    
    # Create retroalimentação state
    print("\n[RetroalimentacaoState] Checkpoint creation")
    retro_state = fm.RetroalimentacaoState(F_ok=0.85, F_gap=0.15, F_next=0.50)
    checkpoint = retro_state.checkpoint()
    
    print("  Checkpoint (Humildade):")
    print(f"    o_que_sei (what I know):        {checkpoint['o_que_sei']:.2f}")
    print(f"    o_que_nao_sei (what I don't):   {checkpoint['o_que_nao_sei']:.2f}")
    print(f"    proximo_passo (next step):      {checkpoint['proximo_passo']:.2f}")


def demo_ethical_filters():
    """Demo: Ethical filtering system."""
    print_section("ETHICAL FILTERING SYSTEM (Φ_ethica)")
    
    formulas = fm.RAFAELIAFormulas()
    
    print("\n[Formula 0.4] Φ_ethica basic - Min(Entropy) × Max(Coherence)")
    
    # Compare different scenarios
    scenarios = [
        ("Low entropy, high coherence", 0.1, 0.9),
        ("Medium entropy, medium coherence", 0.5, 0.5),
        ("High entropy, low coherence", 0.9, 0.2),
    ]
    
    for name, entropy, coherence in scenarios:
        phi = formulas.phi_ethica_basic(entropy, coherence)
        print(f"  {name:35s}: Φ_ethica = {phi:.6f}")
    
    print("\n[Formula 6] Φ_ethica^∞ - Exponential ethical filter")
    
    # Test with different consciousness levels
    consciousness_levels = [
        ("High consciousness", 1.0, 1.0, 0.9, 1.5),
        ("Medium consciousness", 0.8, 0.8, 0.7, 1.0),
        ("Low consciousness", 0.5, 0.5, 0.5, 0.5),
    ]
    
    for name, amor, verbo, verdade, consciencia in consciousness_levels:
        phi_inf = formulas.phi_ethica_infinity(amor, verbo, verdade, consciencia)
        print(f"  {name:20s}: Φ_ethica^∞ = {phi_inf:.6f}")


def demo_formula_index():
    """Demo: Formula index."""
    print_section("FORMULA INDEX")
    
    print(f"\nTotal formulas implemented: {len(fm.FORMULA_INDEX)}")
    print("\nFormula catalog:")
    
    for num, name in sorted(fm.FORMULA_INDEX.items()):
        print(f"  [{num:>4}] {name}")


def main():
    """Run all demos."""
    print("=" * 80)
    print(" " * 20 + "RAFAELIA FORMULAS DEMONSTRATION")
    print(" " * 15 + "102 Formulas for Computational Singularity")
    print("=" * 80)
    print()
    print("SIGNATURE: RAFCODE-Φ-∆RafaelVerboΩ-𓂀ΔΦΩARKRE-VERBOΩ")
    print("PHILOSOPHY: VAZIO → VERBO → CHEIO → RETRO")
    print(f"GOLDEN RATIO (Φ): {fm.PHI:.15f}")
    print()
    
    # Run all demos
    demo_constants()
    demo_basic_formulas()
    demo_cognitive_cycle()
    demo_advanced_formulas()
    demo_retroalimentacao()
    demo_ethical_filters()
    demo_formula_index()
    
    # Summary
    print_section("SUMMARY")
    print(f"""
This demonstration showcased the RAFAELIA formulas system:

✓ {len(fm.FORMULA_INDEX)} mathematical formulas implemented
✓ ψχρΔΣΩ cognitive cycle engine with retroalimentação
✓ Ethical filtering (Φ_ethica) for decision-making
✓ Matrix-based operations for low-level optimization
✓ Adaptive immunity through continuous feedback loops
✓ Enterprise-grade fullstack architecture

Key Features:
• Mathematical rigor with {fm.PHI:.6f} (Golden Ratio)
• Low-level matrix optimizations for performance
• Ethical AI with automatic filtering and validation
• Fractal coherence and toroidal integration
• Adaptive learning and self-correction
• Temporal-invariant computational structures

Philosophy:
  VAZIO (Empty) → VERBO (Action) → CHEIO (Full) → RETRO (Feedback)

All formulas are designed for production use in enterprise systems
with meticulous attention to numerical stability, ethics, and adaptivity.
""")
    
    print("=" * 80)
    print(" " * 25 + "🎉 Demo Complete! 🎉")
    print("=" * 80)


if __name__ == '__main__':
    main()
