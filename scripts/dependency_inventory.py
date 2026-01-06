#!/usr/bin/env python3
"""
Dependency Inventory Script
Analyzes and tracks all external dependencies for Magisk_Rafaelia

This script inventories:
- Rust dependencies (Cargo.toml files)
- Native dependencies (CMakeLists.txt, Android.mk)
- Python dependencies (requirements.txt, imports)
- Build-time dependencies (NDK, toolchains)
- Runtime dependencies (shared libraries)

Usage:
    ./scripts/dependency_inventory.py [--output report.json] [--check-updates]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional

# Handle missing toml module gracefully
try:
    import toml
    HAS_TOML = True
except ImportError:
    HAS_TOML = False
    print("⚠️  Warning: toml module not available. Cargo.toml parsing will be limited.")


class DependencyInventory:
    """Manages dependency inventory for the project"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.dependencies = {
            'rust': {},
            'native': {},
            'python': {},
            'build': {},
            'runtime': {}
        }
    
    def analyze_rust_dependencies(self) -> Dict:
        """Analyze Rust dependencies from Cargo.toml files"""
        print("📦 Analyzing Rust dependencies...")
        rust_deps = {}
        
        if not HAS_TOML:
            print("  Skipping detailed Cargo.toml analysis (toml module not available)")
            return rust_deps
        
        cargo_files = list(self.repo_root.rglob('Cargo.toml'))
        
        for cargo_file in cargo_files:
            try:
                with open(cargo_file, 'r') as f:
                    cargo_data = toml.load(f)
                
                rel_path = cargo_file.relative_to(self.repo_root)
                
                if 'dependencies' in cargo_data:
                    for dep_name, dep_spec in cargo_data['dependencies'].items():
                        if isinstance(dep_spec, str):
                            version = dep_spec
                            features = []
                            optional = False
                        elif isinstance(dep_spec, dict):
                            version = dep_spec.get('version', 'unknown')
                            features = dep_spec.get('features', [])
                            optional = dep_spec.get('optional', False)
                        else:
                            continue
                        
                        if dep_name not in rust_deps:
                            rust_deps[dep_name] = {
                                'version': version,
                                'used_in': [],
                                'features': set(),
                                'optional': optional,
                                'is_external': not dep_spec.get('path') if isinstance(dep_spec, dict) else True
                            }
                        
                        rust_deps[dep_name]['used_in'].append(str(rel_path))
                        rust_deps[dep_name]['features'].update(features)
            
            except Exception as e:
                print(f"⚠️  Error reading {cargo_file}: {e}")
        
        # Convert sets to lists for JSON serialization
        for dep_name, dep_info in rust_deps.items():
            dep_info['features'] = list(dep_info['features'])
        
        return rust_deps
    
    def analyze_native_dependencies(self) -> Dict:
        """Analyze native C/C++ dependencies"""
        print("🔧 Analyzing native dependencies...")
        native_deps = {}
        
        # Look for common patterns in CMakeLists.txt and Android.mk
        cmake_files = list(self.repo_root.rglob('CMakeLists.txt'))
        android_mk_files = list(self.repo_root.rglob('Android.mk'))
        
        # Pattern for find_package, target_link_libraries, etc.
        patterns = {
            'find_package': re.compile(r'find_package\s*\(\s*(\w+)'),
            'target_link': re.compile(r'target_link_libraries\s*\([^)]*\s+([\w\-\.]+)'),
            'local_ldlibs': re.compile(r'LOCAL_LDLIBS\s*[+:]=\s*-l(\w+)'),
            'shared_libraries': re.compile(r'LOCAL_SHARED_LIBRARIES\s*[+:]=\s*(\w+)'),
        }
        
        for cmake_file in cmake_files:
            try:
                with open(cmake_file, 'r') as f:
                    content = f.read()
                
                rel_path = cmake_file.relative_to(self.repo_root)
                
                for pattern_name, pattern in patterns.items():
                    for match in pattern.finditer(content):
                        lib_name = match.group(1)
                        
                        if lib_name not in native_deps:
                            native_deps[lib_name] = {
                                'type': 'native_library',
                                'used_in': [],
                                'link_type': 'unknown'
                            }
                        
                        native_deps[lib_name]['used_in'].append(str(rel_path))
            
            except Exception as e:
                print(f"⚠️  Error reading {cmake_file}: {e}")
        
        return native_deps
    
    def analyze_python_dependencies(self) -> Dict:
        """Analyze Python dependencies"""
        print("🐍 Analyzing Python dependencies...")
        python_deps = {}
        
        # Check requirements.txt if exists
        req_file = self.repo_root / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package==version or package>=version
                        match = re.match(r'([a-zA-Z0-9\-_]+)([>=<~!]+)([0-9\.]+.*)', line)
                        if match:
                            pkg_name, op, version = match.groups()
                            python_deps[pkg_name] = {
                                'version': f'{op}{version}',
                                'source': 'requirements.txt'
                            }
        
        # Scan Python files for imports
        python_files = list(self.repo_root.rglob('*.py'))
        import_pattern = re.compile(r'^(?:from|import)\s+([a-zA-Z0-9_]+)')
        
        stdlib_modules = {
            'os', 'sys', 're', 'json', 'argparse', 'subprocess', 
            'pathlib', 'typing', 'collections', 'itertools', 'functools',
            'datetime', 'time', 'math', 'random', 'hashlib', 'urllib',
            'http', 'email', 'xml', 'html', 'logging', 'unittest'
        }
        
        imported_modules = set()
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        match = import_pattern.match(line.strip())
                        if match:
                            module = match.group(1)
                            if module not in stdlib_modules:
                                imported_modules.add(module)
            except Exception:
                pass
        
        # Add imported modules not in requirements
        for module in imported_modules:
            if module not in python_deps:
                python_deps[module] = {
                    'version': 'unknown',
                    'source': 'import_scan'
                }
        
        return python_deps
    
    def analyze_build_dependencies(self) -> Dict:
        """Analyze build-time dependencies"""
        print("🔨 Analyzing build dependencies...")
        build_deps = {}
        
        # Check for NDK
        ndk_version = self._check_ndk_version()
        if ndk_version:
            build_deps['android_ndk'] = {
                'version': ndk_version,
                'required': True,
                'type': 'toolchain'
            }
        
        # Check for Rust toolchain
        rust_version = self._check_rust_version()
        if rust_version:
            build_deps['rust'] = {
                'version': rust_version,
                'required': True,
                'type': 'toolchain'
            }
        
        # Check for Python
        python_version = self._check_python_version()
        if python_version:
            build_deps['python'] = {
                'version': python_version,
                'required': True,
                'type': 'interpreter'
            }
        
        # Check for Java/Kotlin
        java_version = self._check_java_version()
        if java_version:
            build_deps['java'] = {
                'version': java_version,
                'required': True,
                'type': 'toolchain'
            }
        
        return build_deps
    
    def _check_ndk_version(self) -> Optional[str]:
        """Check Android NDK version"""
        try:
            ndk_root = os.environ.get('ANDROID_NDK_ROOT')
            if ndk_root:
                prop_file = Path(ndk_root) / 'source.properties'
                if prop_file.exists():
                    with open(prop_file, 'r') as f:
                        for line in f:
                            if line.startswith('Pkg.Revision'):
                                return line.split('=')[1].strip()
        except Exception:
            pass
        return None
    
    def _check_rust_version(self) -> Optional[str]:
        """Check Rust version"""
        try:
            result = subprocess.run(
                ['rustc', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip().split()[1]
        except Exception:
            pass
        return None
    
    def _check_python_version(self) -> Optional[str]:
        """Check Python version"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _check_java_version(self) -> Optional[str]:
        """Check Java version"""
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse version from stderr
                version_line = result.stderr.split('\n')[0]
                match = re.search(r'version "([^"]+)"', version_line)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None
    
    def analyze_runtime_dependencies(self) -> Dict:
        """Analyze runtime shared library dependencies"""
        print("📚 Analyzing runtime dependencies...")
        runtime_deps = {}
        
        # Look for compiled binaries in out/ directory
        out_dir = self.repo_root / 'out'
        if out_dir.exists():
            # Find .so and executable files
            for file_path in out_dir.rglob('*'):
                if file_path.is_file():
                    if file_path.suffix in ['.so', ''] and not file_path.name.endswith('.txt'):
                        deps = self._get_shared_lib_dependencies(file_path)
                        for dep in deps:
                            if dep not in runtime_deps:
                                runtime_deps[dep] = {
                                    'type': 'shared_library',
                                    'used_by': []
                                }
                            runtime_deps[dep]['used_by'].append(str(file_path.name))
        
        return runtime_deps
    
    def _get_shared_lib_dependencies(self, binary_path: Path) -> List[str]:
        """Get shared library dependencies of a binary using ldd/readelf"""
        deps = []
        
        try:
            # Try readelf first (more reliable, works on cross-compiled binaries)
            result = subprocess.run(
                ['readelf', '-d', str(binary_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'NEEDED' in line:
                        match = re.search(r'\[([^\]]+)\]', line)
                        if match:
                            deps.append(match.group(1))
        except Exception:
            # Fallback to ldd (won't work for cross-compiled binaries)
            try:
                result = subprocess.run(
                    ['ldd', str(binary_path)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        match = re.match(r'\s*([^\s]+)\s+=>', line)
                        if match:
                            deps.append(match.group(1))
            except Exception:
                pass
        
        return deps
    
    def analyze_all(self) -> Dict:
        """Run all analyses"""
        print("🔍 Starting comprehensive dependency analysis...\n")
        
        self.dependencies['rust'] = self.analyze_rust_dependencies()
        self.dependencies['native'] = self.analyze_native_dependencies()
        self.dependencies['python'] = self.analyze_python_dependencies()
        self.dependencies['build'] = self.analyze_build_dependencies()
        self.dependencies['runtime'] = self.analyze_runtime_dependencies()
        
        return self.dependencies
    
    def generate_report(self, output_file: Optional[Path] = None):
        """Generate dependency report"""
        report = {
            'version': '1.0',
            'timestamp': subprocess.run(
                ['date', '+%Y-%m-%d %H:%M:%S'],
                capture_output=True,
                text=True
            ).stdout.strip(),
            'repository': str(self.repo_root),
            'dependencies': self.dependencies,
            'summary': {
                'rust_dependencies': len(self.dependencies['rust']),
                'native_dependencies': len(self.dependencies['native']),
                'python_dependencies': len(self.dependencies['python']),
                'build_dependencies': len(self.dependencies['build']),
                'runtime_dependencies': len(self.dependencies['runtime']),
                'total_external': self._count_external_deps()
            }
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n✅ Report saved to: {output_file}")
        else:
            print("\n" + "="*80)
            print("DEPENDENCY INVENTORY REPORT")
            print("="*80)
            print(json.dumps(report, indent=2))
        
        return report
    
    def _count_external_deps(self) -> int:
        """Count total external dependencies"""
        count = 0
        
        # Rust external deps
        for dep_name, dep_info in self.dependencies['rust'].items():
            if dep_info.get('is_external', True):
                count += 1
        
        # Native deps
        count += len(self.dependencies['native'])
        
        # Python external deps
        count += len(self.dependencies['python'])
        
        return count
    
    def print_summary(self):
        """Print a summary of dependencies"""
        print("\n" + "="*80)
        print("📊 DEPENDENCY SUMMARY")
        print("="*80)
        
        print(f"\n🦀 Rust Dependencies: {len(self.dependencies['rust'])}")
        external_rust = sum(1 for d in self.dependencies['rust'].values() if d.get('is_external', True))
        print(f"   - External: {external_rust}")
        print(f"   - Internal: {len(self.dependencies['rust']) - external_rust}")
        
        print(f"\n🔧 Native Dependencies: {len(self.dependencies['native'])}")
        
        print(f"\n🐍 Python Dependencies: {len(self.dependencies['python'])}")
        
        print(f"\n🔨 Build Dependencies: {len(self.dependencies['build'])}")
        for name, info in self.dependencies['build'].items():
            print(f"   - {name}: {info.get('version', 'unknown')}")
        
        print(f"\n📚 Runtime Dependencies: {len(self.dependencies['runtime'])}")
        
        total_external = self._count_external_deps()
        print(f"\n📦 Total External Dependencies: {total_external}")
        
        print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze and track dependencies for Magisk_Rafaelia'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output JSON file for the report'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Repository root directory'
    )
    
    args = parser.parse_args()
    
    # Create inventory manager
    inventory = DependencyInventory(args.repo_root)
    
    # Run analysis
    inventory.analyze_all()
    
    # Print summary
    inventory.print_summary()
    
    # Generate report
    inventory.generate_report(args.output)
    
    print("\n✅ Dependency inventory complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
