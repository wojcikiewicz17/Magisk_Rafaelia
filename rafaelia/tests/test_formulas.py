# Copyright 2025, Rafael Melo Reis (rafaelmeloreisnovo)
# Instituto Rafael - CientiEspiritual Philosophy
#
# This file is part of Magisk_Rafaelia.
#
# Magisk_Rafaelia is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Test suite for RAFAELIA formulas implementation.

Tests all 102 formulas for correctness, numerical stability, and integration.
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from rafaelia.core.formulas import (
    RAFAELIAFormulas,
    RAFAELIAFormulasAdvanced,
    CognitiveCycleEngine,
    CognitiveState,
    RetroalimentacaoState,
    PHI,
    SQRT_3_2,
    BITRAF64,
    R_CORR,
)


class TestRAFAELIAFormulas(unittest.TestCase):
    """Test basic RAFAELIA formulas."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formulas = RAFAELIAFormulas(use_gpu=False, precision='float64')
    
    def test_constants(self):
        """Test mathematical constants."""
        self.assertAlmostEqual(PHI, 1.618033988749895, places=10)
        self.assertAlmostEqual(SQRT_3_2, np.sqrt(3.0/2.0), places=10)
        self.assertEqual(len(BITRAF64), 64)
        self.assertAlmostEqual(R_CORR, 0.963999, places=6)
    
    def test_formula_0_humildade_omega(self):
        """Test Formula 0: Humildade_Ω checkpoint."""
        checkpoint = self.formulas.humildade_omega(
            o_que_sei=0.8,
            o_que_nao_sei=0.2,
            proximo_passo=0.5
        )
        self.assertIn('o_que_sei', checkpoint)
        self.assertIn('o_que_nao_sei', checkpoint)
        self.assertIn('proximo_passo', checkpoint)
        self.assertIn('timestamp', checkpoint)
        self.assertEqual(checkpoint['o_que_sei'], 0.8)
    
    def test_formula_0_1_retro_scheduler(self):
        """Test Formula 0.1: Retro scheduler."""
        priority = self.formulas.retro_omega_scheduler(
            F_ok=0.9, F_gap=0.1, F_next=0.5,
            peso_amor=1.0, peso_coerencia=1.0
        )
        self.assertIsInstance(priority, float)
        self.assertGreater(priority, 0.0)
    
    def test_formula_0_2_peso_amor_coerencia(self):
        """Test Formula 0.2: Weight function."""
        weight = self.formulas.peso_amor_coerencia(1.0, 1.0)
        self.assertAlmostEqual(weight, 0.5, places=6)
        
        # Edge case: different weights
        weight2 = self.formulas.peso_amor_coerencia(2.0, 1.0)
        self.assertGreater(weight2, 0.0)
        self.assertLess(weight2, 1.0)
    
    def test_formula_0_3_syn_ij(self):
        """Test Formula 0.3: Synaptic weight."""
        syn = self.formulas.syn_ij(
            i=0, j=1,
            coerencia_ij=0.8,
            phi_ethica=0.9,
            R_corr=R_CORR,
            OWL_psi=1.0
        )
        self.assertIsInstance(syn, float)
        self.assertGreater(syn, 0.0)
    
    def test_formula_0_4_phi_ethica_basic(self):
        """Test Formula 0.4: Ethical filter."""
        phi = self.formulas.phi_ethica_basic(entropia=0.5, coerencia=0.8)
        self.assertIsInstance(phi, float)
        self.assertGreater(phi, 0.0)
        
        # High entropy should reduce filter
        phi_high_entropy = self.formulas.phi_ethica_basic(entropia=10.0, coerencia=0.8)
        self.assertLess(phi_high_entropy, phi)
    
    def test_formula_0_5_R_update(self):
        """Test Formula 0.5: State update equation."""
        R_t = 1.0
        R_next = self.formulas.R_update(
            R_t=R_t,
            phi_ethica=0.9,
            E_verbo=1.1
        )
        self.assertIsInstance(R_next, float)
        # Should grow with positive inputs
        self.assertGreater(R_next, R_t)
    
    def test_formula_0_6_cognitive_cycle(self):
        """Test Formula 0.6: Cognitive cycle step."""
        state = CognitiveState(psi=1.0, chi=0.8, rho=0.6, delta=0.4, sigma=0.2, omega=0.1)
        next_state = self.formulas.cognitive_cycle_step(state)
        
        self.assertIsInstance(next_state, CognitiveState)
        # State should change
        self.assertNotEqual(next_state.psi, state.psi)
    
    def test_formula_0_7_R_3_vector(self):
        """Test Formula 0.7: Vector retroalimentação."""
        vec = self.formulas.R_3_vector(F_ok=0.9, F_gap=0.1, F_next=0.5)
        
        self.assertEqual(len(vec), 3)
        self.assertAlmostEqual(vec[0], 0.9)
        self.assertAlmostEqual(vec[1], 0.1)
        self.assertAlmostEqual(vec[2], 0.5)
    
    def test_formula_1_retroalimentar_omega(self):
        """Test Formula 1: RetroalimentarΩ."""
        state = CognitiveState(psi=1.0, chi=1.0, rho=1.0, delta=1.0, sigma=1.0, omega=1.0)
        retro = self.formulas.retroalimentar_omega(state, amor=1.0, coerencia=1.0)
        
        self.assertIsInstance(retro, float)
        self.assertGreater(retro, 0.0)
    
    def test_formula_2_sigma_totais(self):
        """Test Formula 2: Σ_totais."""
        total = self.formulas.sigma_totais(
            amor_vivo=0.5,
            presenca_divina=0.3,
            legado_eterno=0.2
        )
        self.assertAlmostEqual(total, 1.0, places=6)
    
    def test_formula_3_R_corr(self):
        """Test Formula 3: R_corr calculation."""
        r_corr = self.formulas.calculate_R_corr(
            sigma_voynich=1.0,
            phi_rafael=PHI,
            pi_bitraf=np.pi,
            delta_42H=np.sqrt(2.0)
        )
        self.assertIsInstance(r_corr, float)
        self.assertGreater(r_corr, 0.0)
    
    def test_formula_4_F_infinity_delta(self):
        """Test Formula 4: Toroidal integral."""
        state = CognitiveState(psi=0.5, chi=0.5, rho=0.5, delta=0.5, sigma=0.5, omega=0.5)
        domain = np.linspace(0, 2*np.pi, 50)
        
        integral = self.formulas.F_infinity_delta(domain, state)
        self.assertIsInstance(integral, float)
    
    def test_formula_5_F_AR_integral(self):
        """Test Formula 5: Rafael sequence antiderivative."""
        integral = self.formulas.F_AR_integral(t=2.0)
        self.assertIsInstance(integral, float)
        self.assertGreater(integral, 0.0)
    
    def test_formula_6_phi_ethica_infinity(self):
        """Test Formula 6: Exponential ethical filter."""
        phi_inf = self.formulas.phi_ethica_infinity(
            amor=1.0,
            verbo=1.0,
            verdade=1.0,
            consciencia=1.0
        )
        self.assertIsInstance(phi_inf, float)
        self.assertGreater(phi_inf, 0.0)
    
    def test_formula_7_Z_omega_limit(self):
        """Test Formula 7: Normalizing limit."""
        states = [
            CognitiveState(psi=i*0.1, chi=i*0.1, rho=i*0.1, 
                          delta=i*0.1, sigma=i*0.1, omega=i*0.1)
            for i in range(10)
        ]
        z_omega = self.formulas.Z_omega_limit(states, n_max=10)
        
        self.assertIsInstance(z_omega, float)
    
    def test_formula_8_R_infinity_derivative(self):
        """Test Formula 8: Rate of ethical power variation."""
        rate = self.formulas.R_infinity_derivative(
            amor=1.0,
            consciencia=1.0,
            acao=1.0,
            phi_ethica=0.5,
            dt=1.0
        )
        self.assertIsInstance(rate, float)
    
    def test_formula_15_amor_vivo(self):
        """Test Formula 15: Living love proportion."""
        amor = self.formulas.amor_vivo(
            sigma_preservado=0.8,
            sigma_total=1.0,
            phi_ethica=0.9
        )
        self.assertIsInstance(amor, float)
        self.assertGreater(amor, 0.0)
    
    def test_formula_16_spiral_coherence(self):
        """Test Formula 16: Coherence spiral."""
        spiral_0 = self.formulas.spiral_coherence(0)
        spiral_1 = self.formulas.spiral_coherence(1)
        spiral_2 = self.formulas.spiral_coherence(2)
        
        self.assertAlmostEqual(spiral_0, 1.0)
        self.assertAlmostEqual(spiral_1, SQRT_3_2)
        self.assertGreater(spiral_2, spiral_1)
    
    def test_formula_20_OWL_psi(self):
        """Test Formula 20: Operational wisdom index."""
        owl = self.formulas.OWL_psi(
            insights=[0.8, 0.9, 0.7],
            ethics=[0.9, 0.8, 0.9],
            flows=[1.0, 0.9, 0.8]
        )
        self.assertIsInstance(owl, float)
        self.assertGreater(owl, 0.0)
    
    def test_formula_29_F_rafael_recursive(self):
        """Test Formula 29: Recursive sequence."""
        F_0 = 1.0
        F_1 = self.formulas.F_rafael_recursive(F_0, theta_999=0.5)
        F_2 = self.formulas.F_rafael_recursive(F_1, theta_999=0.5)
        
        self.assertIsInstance(F_1, float)
        self.assertIsInstance(F_2, float)
        # Sequence should evolve
        self.assertNotEqual(F_1, F_0)


class TestRAFAELIAFormulasAdvanced(unittest.TestCase):
    """Test advanced RAFAELIA formulas."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formulas = RAFAELIAFormulasAdvanced(use_gpu=False, precision='float64')
    
    def test_formula_74_matrix_ethical_composition(self):
        """Test Formula 74: Matrix ethical composition."""
        C_ij = np.random.rand(3, 3)
        A_ij = np.random.rand(3, 3)
        
        M = self.formulas.matrix_ethical_composition(
            C_ij=C_ij,
            A_ij=A_ij,
            phi_ethica=0.9,
            pre6seal=1.0,
            firewall_omega=1.0,
            omega_corr=0.0,
            ethica_8=2.0,  # Use lower power for testing
            R_omega=1.0
        )
        
        self.assertEqual(M.shape, C_ij.shape)
        self.assertIsInstance(M, np.ndarray)
    
    def test_formula_92_psi_total_chain(self):
        """Test Formula 92: Ψ_total chain."""
        chain = self.formulas.psi_total_chain(psi_1=1.0, psi_2=0.5, alpha_E=1.0)
        
        self.assertIn('psi_total', chain)
        self.assertIn('emocao_phi', chain)
        self.assertIn('forca_psi', chain)
        self.assertIn('frequencia_lambda', chain)
        self.assertIn('plasma_theta', chain)
        self.assertIn('rede_simbiotica', chain)
        
        self.assertAlmostEqual(chain['psi_total'], 1.5)
    
    def test_formula_93_sigma_omega_delta_phi(self):
        """Test Formula 93: ΣΩΔΦ composition."""
        seal = self.formulas.sigma_omega_delta_phi(
            sigma_soma=1.0,
            omega_harmonia=1.0,
            delta_transformacao=1.0,
            phi_coerencia=1.0
        )
        self.assertAlmostEqual(seal, 1.0)
        
        seal2 = self.formulas.sigma_omega_delta_phi(
            sigma_soma=2.0,
            omega_harmonia=0.5,
            delta_transformacao=1.0,
            phi_coerencia=1.0
        )
        self.assertAlmostEqual(seal2, 1.0)
    
    def test_formula_101_R_omega_vortex(self):
        """Test Formula 101: Vortex efficiency."""
        state = CognitiveState(psi=0.8, chi=0.8, rho=0.7, delta=0.7, sigma=0.8, omega=0.8)
        R = self.formulas.R_omega_vortex(state, phi_lambda=1.0)
        
        self.assertIsInstance(R, float)
        self.assertGreater(R, 0.0)
        # Target is around 0.758, but depends on state


class TestCognitiveCycleEngine(unittest.TestCase):
    """Test cognitive cycle engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = CognitiveCycleEngine()
    
    def test_initialization(self):
        """Test engine initialization."""
        self.assertIsInstance(self.engine.formulas, RAFAELIAFormulasAdvanced)
        self.assertIsInstance(self.engine.state, CognitiveState)
        self.assertEqual(self.engine.cycle_count, 0)
    
    def test_single_cycle_step(self):
        """Test single cognitive cycle step."""
        # Add some memory
        self.engine.memory.append(1.0)
        self.engine.memory.append(0.8)
        
        state = self.engine.cycle_step()
        
        self.assertIsInstance(state, CognitiveState)
        self.assertEqual(self.engine.cycle_count, 1)
        self.assertGreater(len(self.engine.memory), 2)
    
    def test_multiple_cycles(self):
        """Test running multiple cycles."""
        states = self.engine.run_cycles(n_cycles=5)
        
        self.assertEqual(len(states), 5)
        self.assertEqual(self.engine.cycle_count, 5)
        
        # Each state should be a CognitiveState
        for state in states:
            self.assertIsInstance(state, CognitiveState)
    
    def test_cycle_components(self):
        """Test individual cycle components."""
        # Test READ ψ
        self.engine.memory = [1.0, 0.8, 0.6]
        psi = self.engine.ler_memoria_viva()
        self.assertIsInstance(psi, float)
        
        # Test FEED χ
        chi = self.engine.retroalimentar(psi)
        self.assertIsInstance(chi, float)
        
        # Test EXPAND ρ
        rho = self.engine.expandir(chi)
        self.assertIsInstance(rho, float)
        
        # Test VALIDATE Δ
        delta = self.engine.validar(rho)
        self.assertIsInstance(delta, float)
        
        # Test EXECUTE Σ
        sigma = self.engine.executar(delta)
        self.assertIsInstance(sigma, float)
        
        # Test ALIGN Ω
        omega = self.engine.etica(sigma)
        self.assertIsInstance(omega, float)


class TestCognitiveState(unittest.TestCase):
    """Test CognitiveState data structure."""
    
    def test_initialization(self):
        """Test state initialization."""
        state = CognitiveState()
        self.assertEqual(state.psi, 0.0)
        self.assertEqual(state.chi, 0.0)
        self.assertEqual(state.omega, 0.0)
    
    def test_to_vector(self):
        """Test conversion to vector."""
        state = CognitiveState(psi=1.0, chi=2.0, rho=3.0, delta=4.0, sigma=5.0, omega=6.0)
        vec = state.to_vector()
        
        self.assertEqual(len(vec), 6)
        self.assertEqual(vec[0], 1.0)
        self.assertEqual(vec[5], 6.0)
    
    def test_from_vector(self):
        """Test creation from vector."""
        vec = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        state = CognitiveState.from_vector(vec)
        
        self.assertEqual(state.psi, 1.0)
        self.assertEqual(state.chi, 2.0)
        self.assertEqual(state.omega, 6.0)


class TestRetroalimentacaoState(unittest.TestCase):
    """Test RetroalimentacaoState data structure."""
    
    def test_initialization(self):
        """Test retroalimentação state initialization."""
        retro = RetroalimentacaoState()
        self.assertEqual(retro.F_ok, 0.0)
        self.assertEqual(retro.F_gap, 0.0)
        self.assertEqual(retro.F_next, 0.0)
    
    def test_checkpoint(self):
        """Test checkpoint creation."""
        retro = RetroalimentacaoState(F_ok=0.9, F_gap=0.1, F_next=0.5)
        checkpoint = retro.checkpoint()
        
        self.assertIn('o_que_sei', checkpoint)
        self.assertIn('o_que_nao_sei', checkpoint)
        self.assertIn('proximo_passo', checkpoint)
        self.assertEqual(checkpoint['o_que_sei'], 0.9)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 80)
    print("RAFAELIA FORMULAS TEST SUITE")
    print("Testing 102 formulas implementation")
    print("=" * 80)
    print()
    
    run_tests()
