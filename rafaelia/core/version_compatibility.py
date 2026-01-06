# Copyright 2025, Rafael Melo Reis (rafaelmeloreisnovo)
# Instituto Rafael - CientiEspiritual Philosophy
#
# This file is part of Magisk_Rafaelia.
#
# Magisk_Rafaelia is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
RAFAELIA Version Compatibility Module

This module provides comprehensive version compatibility checking and migration
support for upgrades and downgrades between different RAFAELIA versions.

Features:
- Semantic version parsing and comparison
- Forward and backward compatibility checks
- Data migration support for version transitions
- Breaking change detection and warnings
- Automatic compatibility layer selection

Part of Magisk_Rafaelia RAFAELIA Framework
Philosophy: VAZIO → VERBO → CHEIO → RETRO (Maintaining compatibility across versions)

Copyright (C) 2025 Rafael Melo Reis (rafaelmeloreisnovo)
Instituto Rafael - CientiEspiritual Philosophy
All Rights Reserved.
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


# Module-level constants
DEFAULT_VERSION = "1.0.0"
BREAKING_CHANGES_CONFIG = "version_breaking_changes.json"
DEPRECATIONS_CONFIG = "version_deprecations.json"


class CompatibilityLevel(Enum):
    """Compatibility levels between versions."""
    FULLY_COMPATIBLE = "fully_compatible"      # No changes needed
    FORWARD_COMPATIBLE = "forward_compatible"  # Newer -> Older works
    BACKWARD_COMPATIBLE = "backward_compatible" # Older -> Newer works
    MIGRATION_REQUIRED = "migration_required"  # Requires data migration
    BREAKING_CHANGE = "breaking_change"        # Incompatible, manual intervention needed


@dataclass
class SemanticVersion:
    """Represents a semantic version (major.minor.patch-prerelease+build)."""
    major: int
    minor: int
    patch: int
    prerelease: str = ""
    build: str = ""
    
    @classmethod
    def parse(cls, version_str: str) -> 'SemanticVersion':
        """
        Parse a semantic version string.
        
        Examples:
            - "1.0.0"
            - "2.1.3-alpha"
            - "3.0.0-beta.1+build.123"
        """
        # Semantic version regex pattern
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z\-\.]+))?(?:\+([0-9A-Za-z\-\.]+))?$'
        match = re.match(pattern, version_str.strip())
        
        if not match:
            raise ValueError(f"Invalid semantic version: {version_str}")
        
        major, minor, patch, prerelease, build = match.groups()
        return cls(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            prerelease=prerelease or "",
            build=build or ""
        )
    
    def __str__(self) -> str:
        """String representation of version."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version
    
    def __lt__(self, other: 'SemanticVersion') -> bool:
        """Compare versions (less than)."""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        
        # Prerelease versions have lower precedence than normal versions
        if self.prerelease and not other.prerelease:
            return True
        if not self.prerelease and other.prerelease:
            return False
        
        return self.prerelease < other.prerelease
    
    def __eq__(self, other: 'SemanticVersion') -> bool:
        """Compare versions (equality)."""
        return (self.major == other.major and 
                self.minor == other.minor and 
                self.patch == other.patch and
                self.prerelease == other.prerelease)
    
    def __le__(self, other: 'SemanticVersion') -> bool:
        return self < other or self == other
    
    def __gt__(self, other: 'SemanticVersion') -> bool:
        return not self <= other
    
    def __ge__(self, other: 'SemanticVersion') -> bool:
        return not self < other


@dataclass
class CompatibilityCheck:
    """Result of a compatibility check between two versions."""
    from_version: SemanticVersion
    to_version: SemanticVersion
    level: CompatibilityLevel
    is_upgrade: bool
    warnings: List[str]
    migration_steps: List[str]
    breaking_changes: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'from_version': str(self.from_version),
            'to_version': str(self.to_version),
            'level': self.level.value,
            'is_upgrade': self.is_upgrade,
            'warnings': self.warnings,
            'migration_steps': self.migration_steps,
            'breaking_changes': self.breaking_changes
        }


class VersionCompatibilityChecker:
    """
    Check compatibility between different RAFAELIA versions.
    
    Provides detailed analysis of version transitions including:
    - Compatibility level assessment
    - Required migration steps
    - Breaking change detection
    - Deprecation warnings
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the compatibility checker."""
        self.logger = logging.getLogger("RAFAELIA.VersionCompatibility")
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        
        # Load breaking changes from config file or use defaults
        self.breaking_changes = self._load_breaking_changes()
        
        # Load deprecations from config file or use defaults
        self.deprecations = self._load_deprecations()
    
    def _load_breaking_changes(self) -> Dict:
        """Load breaking changes from config file or use defaults."""
        config_file = self.config_dir / BREAKING_CHANGES_CONFIG
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    # Convert string keys to tuples with error handling
                    result = {}
                    for k, v in data.items():
                        try:
                            key_parts = k.split(',')
                            if len(key_parts) == 2:
                                result[tuple(map(int, key_parts))] = v
                            else:
                                self.logger.warning(f"Skipping malformed key: {k}")
                        except ValueError as e:
                            self.logger.warning(f"Could not parse key '{k}': {e}")
                    return result
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Could not load breaking changes config: {e}")
        
        # Default breaking changes
        return {
            (1, 2): ["API endpoint structure changed", "Config format updated"],
            (2, 3): ["State matrix expanded to 1008 states", "Audit log format v3"],
        }
    
    def _load_deprecations(self) -> Dict:
        """Load deprecations from config file or use defaults."""
        config_file = self.config_dir / DEPRECATIONS_CONFIG
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Could not load deprecations config: {e}")
        
        # Default deprecations
        return {
            "1.5.0": ["Legacy telemetry API (use v2)"],
            "2.0.0": ["Old config format (use YAML)"],
        }
    
    def check_compatibility(
        self, 
        from_version: str, 
        to_version: str
    ) -> CompatibilityCheck:
        """
        Check compatibility between two versions.
        
        Args:
            from_version: Current version string
            to_version: Target version string
            
        Returns:
            CompatibilityCheck object with detailed analysis
        """
        try:
            from_ver = SemanticVersion.parse(from_version)
            to_ver = SemanticVersion.parse(to_version)
        except ValueError as e:
            self.logger.error(f"Invalid version format: {e}")
            raise
        
        is_upgrade = to_ver > from_ver
        warnings = []
        migration_steps = []
        breaking_changes = []
        
        # Check for breaking changes
        if from_ver.major != to_ver.major:
            # Major version change - potential breaking changes
            change_key = (from_ver.major, to_ver.major) if is_upgrade else (to_ver.major, from_ver.major)
            breaking_changes = self.breaking_changes.get(change_key, [])
            
            if breaking_changes:
                level = CompatibilityLevel.BREAKING_CHANGE
            else:
                level = CompatibilityLevel.MIGRATION_REQUIRED
                migration_steps.append(f"Major version transition: {from_ver.major} → {to_ver.major}")
        
        elif from_ver.minor != to_ver.minor:
            # Minor version change - backward compatible for upgrades
            if is_upgrade:
                level = CompatibilityLevel.BACKWARD_COMPATIBLE
                warnings.append("Feature additions may be present")
            else:
                level = CompatibilityLevel.FORWARD_COMPATIBLE
                warnings.append("Some features from newer version may not work")
        
        else:
            # Patch version change - fully compatible
            level = CompatibilityLevel.FULLY_COMPATIBLE
        
        # Check for deprecation warnings
        for dep_version, dep_list in self.deprecations.items():
            dep_ver = SemanticVersion.parse(dep_version)
            if from_ver < dep_ver <= to_ver:
                warnings.extend([f"Deprecated: {dep}" for dep in dep_list])
        
        # Generate migration steps for major transitions
        if level in [CompatibilityLevel.MIGRATION_REQUIRED, CompatibilityLevel.BREAKING_CHANGE]:
            migration_steps.extend(self._generate_migration_steps(from_ver, to_ver))
        
        return CompatibilityCheck(
            from_version=from_ver,
            to_version=to_ver,
            level=level,
            is_upgrade=is_upgrade,
            warnings=warnings,
            migration_steps=migration_steps,
            breaking_changes=breaking_changes
        )
    
    def _generate_migration_steps(
        self, 
        from_ver: SemanticVersion, 
        to_ver: SemanticVersion
    ) -> List[str]:
        """Generate migration steps for version transition."""
        steps = []
        
        # Example migration steps
        if from_ver.major == 1 and to_ver.major == 2:
            steps.extend([
                "Backup current configuration",
                "Export audit logs to v2 format",
                "Update state matrix definitions",
                "Migrate telemetry data schema",
                "Verify all modules are v2 compatible"
            ])
        
        if from_ver.major == 2 and to_ver.major == 1:
            steps.extend([
                "Warning: Downgrade may lose data",
                "Export v2 data to v1 compatible format",
                "Disable v2-only features",
                "Restore v1 configuration format"
            ])
        
        return steps
    
    def can_safely_transition(
        self, 
        from_version: str, 
        to_version: str
    ) -> Tuple[bool, str]:
        """
        Check if version transition is safe.
        
        Returns:
            (is_safe, message) tuple
        """
        check = self.check_compatibility(from_version, to_version)
        
        if check.level == CompatibilityLevel.BREAKING_CHANGE:
            return False, f"Breaking changes detected: {', '.join(check.breaking_changes)}"
        
        if check.level == CompatibilityLevel.MIGRATION_REQUIRED:
            if check.migration_steps:
                return False, f"Migration required: {len(check.migration_steps)} steps needed"
        
        return True, f"Transition is {check.level.value}"
    
    def get_current_version(self, config_path: Optional[Path] = None) -> str:
        """
        Get current RAFAELIA version from config or manifest.
        
        Args:
            config_path: Optional path to config file
            
        Returns:
            Version string
        """
        # Try to read from RAFAELIA_MANIFEST.json
        manifest_paths = [
            Path("RAFAELIA_MANIFEST.json"),
            Path("/data/adb/rafaelia/version.json"),
        ]
        
        if config_path:
            manifest_paths.insert(0, config_path)
        
        for path in manifest_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        version = data.get('version') or data.get('build', {}).get('version')
                        if version:
                            return version
                except (json.JSONDecodeError, IOError) as e:
                    self.logger.warning(f"Could not read version from {path}: {e}")
        
        # Return default version if not found
        return DEFAULT_VERSION


# Module-level convenience functions
def check_upgrade_compatibility(from_version: str, to_version: str) -> CompatibilityCheck:
    """Check if upgrade from one version to another is compatible."""
    checker = VersionCompatibilityChecker()
    return checker.check_compatibility(from_version, to_version)


def check_downgrade_compatibility(from_version: str, to_version: str) -> CompatibilityCheck:
    """Check if downgrade from one version to another is compatible."""
    checker = VersionCompatibilityChecker()
    return checker.check_compatibility(from_version, to_version)


def get_migration_guide(from_version: str, to_version: str) -> Dict:
    """Get detailed migration guide for version transition."""
    checker = VersionCompatibilityChecker()
    check = checker.check_compatibility(from_version, to_version)
    return check.to_dict()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    checker = VersionCompatibilityChecker()
    
    # Test various version transitions
    test_cases = [
        ("1.0.0", "1.0.1"),  # Patch update
        ("1.0.0", "1.1.0"),  # Minor update
        ("1.0.0", "2.0.0"),  # Major update
        ("2.0.0", "1.0.0"),  # Major downgrade
    ]
    
    for from_v, to_v in test_cases:
        print(f"\n{'='*60}")
        print(f"Checking: {from_v} → {to_v}")
        print(f"{'='*60}")
        
        result = checker.check_compatibility(from_v, to_v)
        print(f"Compatibility: {result.level.value}")
        print(f"Direction: {'Upgrade' if result.is_upgrade else 'Downgrade'}")
        
        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")
        
        if result.migration_steps:
            print("\nMigration Steps:")
            for i, step in enumerate(result.migration_steps, 1):
                print(f"  {i}. {step}")
        
        if result.breaking_changes:
            print("\nBreaking Changes:")
            for change in result.breaking_changes:
                print(f"  ❌ {change}")
        
        safe, msg = checker.can_safely_transition(from_v, to_v)
        print(f"\nSafe to transition: {'✅ Yes' if safe else '❌ No'} - {msg}")
