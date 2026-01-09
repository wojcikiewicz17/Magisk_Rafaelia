# Copyright 2025, Rafael Melo Reis (rafaelmeloreisnovo)
# Instituto Rafael - CientiEspiritual Philosophy
#
# This file is part of Magisk_Rafaelia.
#
# Magisk_Rafaelia is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for bug handler module."""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.bug_handler import (
    BugCategory,
    BugSeverity,
    BugReport,
    StateInvariant,
    BugHandler,
    DeterministicValidator,
    handle_bug,
    check_invariants
)


class TestBugCategory(unittest.TestCase):
    """Test BugCategory enum."""
    
    def test_categories_exist(self):
        """Test that all expected categories exist."""
        self.assertIsNotNone(BugCategory.LOGICAL)
        self.assertIsNotNone(BugCategory.TECHNICAL)
        self.assertIsNotNone(BugCategory.COMPATIBILITY)
        self.assertIsNotNone(BugCategory.UNKNOWN)


class TestBugSeverity(unittest.TestCase):
    """Test BugSeverity enum."""
    
    def test_severities_exist(self):
        """Test that all expected severities exist."""
        self.assertIsNotNone(BugSeverity.CRITICAL)
        self.assertIsNotNone(BugSeverity.HIGH)
        self.assertIsNotNone(BugSeverity.MEDIUM)
        self.assertIsNotNone(BugSeverity.LOW)
        self.assertIsNotNone(BugSeverity.INFO)


class TestBugReport(unittest.TestCase):
    """Test BugReport dataclass."""
    
    def test_create_bug_report(self):
        """Test creating a bug report."""
        report = BugReport(
            category=BugCategory.LOGICAL,
            severity=BugSeverity.HIGH,
            message="Test bug",
            context={'test': 'value'}
        )
        
        self.assertEqual(report.category, BugCategory.LOGICAL)
        self.assertEqual(report.severity, BugSeverity.HIGH)
        self.assertEqual(report.message, "Test bug")
        self.assertIn('test', report.context)
    
    def test_to_dict(self):
        """Test converting bug report to dictionary."""
        report = BugReport(
            category=BugCategory.TECHNICAL,
            severity=BugSeverity.MEDIUM,
            message="Test bug",
            context={}
        )
        
        report_dict = report.to_dict()
        self.assertIn('category', report_dict)
        self.assertIn('severity', report_dict)
        self.assertIn('message', report_dict)
        self.assertEqual(report_dict['category'], 'technical')
        self.assertEqual(report_dict['severity'], 'medium')


class TestStateInvariant(unittest.TestCase):
    """Test StateInvariant class."""
    
    def test_create_invariant(self):
        """Test creating an invariant."""
        invariant = StateInvariant(
            name="test_invariant",
            condition=lambda: True,
            error_message="Test error"
        )
        
        self.assertEqual(invariant.name, "test_invariant")
        self.assertTrue(invariant.check())
    
    def test_failing_invariant(self):
        """Test an invariant that fails."""
        invariant = StateInvariant(
            name="fail_invariant",
            condition=lambda: False,
            error_message="This should fail"
        )
        
        self.assertFalse(invariant.check())
    
    def test_invariant_with_exception(self):
        """Test invariant that raises exception."""
        def raise_error():
            raise ValueError("Test error")
        
        invariant = StateInvariant(
            name="error_invariant",
            condition=raise_error,
            error_message="Error in check"
        )
        
        self.assertFalse(invariant.check())


class TestBugHandler(unittest.TestCase):
    """Test BugHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = BugHandler(strict_mode=False)
    
    def test_add_invariant(self):
        """Test adding an invariant."""
        invariant = StateInvariant(
            name="test",
            condition=lambda: True,
            error_message="Test"
        )
        
        self.handler.add_invariant(invariant)
        self.assertEqual(len(self.handler.invariants), 1)
    
    def test_check_invariants_passing(self):
        """Test checking passing invariants."""
        invariant = StateInvariant(
            name="passing",
            condition=lambda: True,
            error_message="Should not fail"
        )
        
        self.handler.add_invariant(invariant)
        violations = self.handler.check_invariants()
        self.assertEqual(len(violations), 0)
    
    def test_check_invariants_failing(self):
        """Test checking failing invariants."""
        invariant = StateInvariant(
            name="failing",
            condition=lambda: False,
            error_message="Should fail"
        )
        
        self.handler.add_invariant(invariant)
        violations = self.handler.check_invariants()
        self.assertEqual(len(violations), 1)
    
    def test_handle_exception_logical(self):
        """Test handling a logical exception."""
        try:
            raise ValueError("Invalid value")
        except Exception as e:
            report = self.handler.handle_exception(e)
            
        self.assertEqual(report.category, BugCategory.LOGICAL)
        self.assertIsNotNone(report.exception)
        self.assertIsNotNone(report.traceback_info)
    
    def test_handle_exception_compatibility(self):
        """Test handling a compatibility exception."""
        try:
            raise ImportError("Module not found")
        except Exception as e:
            report = self.handler.handle_exception(e)
            
        self.assertEqual(report.category, BugCategory.COMPATIBILITY)
    
    def test_handle_exception_with_recovery(self):
        """Test handling exception with recovery."""
        def recovery_func():
            return True
        
        try:
            raise RuntimeError("Test error")
        except Exception as e:
            report = self.handler.handle_exception(
                e,
                recovery_callback=recovery_func
            )
            
        self.assertTrue(report.recovery_attempted)
        self.assertTrue(report.recovery_successful)
    
    def test_classify_exception(self):
        """Test exception classification."""
        # Logical
        logical_exc = ValueError("Invalid state")
        self.assertEqual(
            self.handler._classify_exception(logical_exc),
            BugCategory.LOGICAL
        )
        
        # Compatibility
        compat_exc = ImportError("Module not found")
        self.assertEqual(
            self.handler._classify_exception(compat_exc),
            BugCategory.COMPATIBILITY
        )
        
        # Technical
        tech_exc = OSError("File not found")
        self.assertEqual(
            self.handler._classify_exception(tech_exc),
            BugCategory.TECHNICAL
        )
    
    def test_validate_state(self):
        """Test state validation."""
        state = {'key1': 'value1', 'key2': 42}
        expected = {'key1': 'value1'}
        
        self.assertTrue(self.handler.validate_state(state, expected))
    
    def test_validate_state_missing_key(self):
        """Test state validation with missing key."""
        state = {'key1': 'value1'}
        expected = {'key1': 'value1', 'key2': 42}
        
        self.assertFalse(self.handler.validate_state(state, expected))
    
    def test_validate_state_wrong_value(self):
        """Test state validation with wrong value."""
        state = {'key1': 'value1'}
        expected = {'key1': 'value2'}
        
        self.assertFalse(self.handler.validate_state(state, expected))
    
    def test_get_statistics(self):
        """Test getting statistics."""
        # Generate some bugs
        try:
            raise ValueError("Test")
        except Exception as e:
            self.handler.handle_exception(e)
        
        stats = self.handler.get_statistics()
        
        self.assertIn('total_bugs', stats)
        self.assertIn('by_category', stats)
        self.assertIn('by_severity', stats)
        self.assertEqual(stats['total_bugs'], 1)
    
    def test_get_reports(self):
        """Test getting reports."""
        # Generate bug reports
        try:
            raise ValueError("Test 1")
        except Exception as e:
            self.handler.handle_exception(e, category=BugCategory.LOGICAL)
        
        try:
            raise ImportError("Test 2")
        except Exception as e:
            self.handler.handle_exception(e, category=BugCategory.COMPATIBILITY)
        
        # Get all reports
        all_reports = self.handler.get_reports()
        self.assertEqual(len(all_reports), 2)
        
        # Get filtered reports
        logical_reports = self.handler.get_reports(category=BugCategory.LOGICAL)
        self.assertEqual(len(logical_reports), 1)
    
    def test_clear_reports(self):
        """Test clearing reports."""
        try:
            raise ValueError("Test")
        except Exception as e:
            self.handler.handle_exception(e)
        
        self.assertEqual(self.handler.stats['total_bugs'], 1)
        
        self.handler.clear_reports()
        
        self.assertEqual(self.handler.stats['total_bugs'], 0)
        self.assertEqual(len(self.handler.bug_reports), 0)


class TestDeterministicValidator(unittest.TestCase):
    """Test DeterministicValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = BugHandler(strict_mode=False)
        self.validator = DeterministicValidator(self.handler)
    
    def test_validate_input_valid(self):
        """Test validating valid input."""
        result = self.validator.validate_input(42, int)
        self.assertTrue(result)
    
    def test_validate_input_wrong_type(self):
        """Test validating input with wrong type."""
        result = self.validator.validate_input("not_an_int", int)
        self.assertFalse(result)
    
    def test_validate_input_with_constraints(self):
        """Test validating input with constraints."""
        constraints = {
            'positive': lambda x: x > 0,
            'less_than_100': lambda x: x < 100
        }
        
        result = self.validator.validate_input(42, int, constraints)
        self.assertTrue(result)
    
    def test_validate_input_constraint_violation(self):
        """Test validating input that violates constraints."""
        constraints = {
            'positive': lambda x: x > 0
        }
        
        result = self.validator.validate_input(-5, int, constraints)
        self.assertFalse(result)
    
    def test_validate_preconditions(self):
        """Test validating preconditions."""
        conditions = {
            'initialized': True,
            'has_data': True
        }
        
        result = self.validator.validate_preconditions(conditions)
        self.assertTrue(result)
    
    def test_validate_preconditions_fail(self):
        """Test validating failing preconditions."""
        conditions = {
            'initialized': True,
            'has_data': False
        }
        
        result = self.validator.validate_preconditions(conditions)
        self.assertFalse(result)
    
    def test_validate_postconditions(self):
        """Test validating postconditions."""
        conditions = {
            'data_saved': True,
            'state_valid': True
        }
        
        result = self.validator.validate_postconditions(conditions)
        self.assertTrue(result)


class TestGlobalFunctions(unittest.TestCase):
    """Test module-level convenience functions."""
    
    def test_handle_bug(self):
        """Test handle_bug convenience function."""
        try:
            raise ValueError("Test error")
        except Exception as e:
            report = handle_bug(e)
            
        self.assertIsNotNone(report)
        self.assertIsInstance(report, BugReport)
    
    def test_check_invariants(self):
        """Test check_invariants convenience function."""
        violations = check_invariants()
        self.assertIsInstance(violations, list)


if __name__ == '__main__':
    unittest.main()
