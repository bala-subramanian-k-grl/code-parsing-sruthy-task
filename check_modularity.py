"""Modularity metrics checker for Python codebase."""

import ast
from pathlib import Path
from typing import Dict, Set, List


class ModularityChecker:
    """Check modularity metrics."""

    def __init__(self, root_dir: str = "src"):
        self.root = Path(root_dir)
        self.modules: Dict[str, Dict] = {}

    def analyze(self) -> Dict[str, float]:
        """Analyze modularity metrics."""
        py_files = list(self.root.rglob("*.py"))
        
        # Collect module data
        for file_path in py_files:
            if file_path.name == "__init__.py":
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content)
                
                module_name = str(file_path.relative_to(self.root))
                self.modules[module_name] = {
                    "classes": self._count_classes(tree),
                    "functions": self._count_functions(tree),
                    "imports": self._count_imports(tree),
                    "external_deps": self._count_external_deps(tree),
                    "lines": len(content.split("\n")),
                }
            except Exception:
                continue
        
        # Calculate metrics
        cohesion = self._calculate_cohesion()
        coupling = self._calculate_coupling()
        separation = self._calculate_separation()
        reusability = self._calculate_reusability()
        
        return {
            "cohesion": round(cohesion, 2),
            "coupling": round(coupling, 2),
            "separation": round(separation, 2),
            "reusability": round(reusability, 2),
        }
    
    def _count_classes(self, tree: ast.AST) -> int:
        """Count classes in module."""
        return sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    
    def _count_functions(self, tree: ast.AST) -> int:
        """Count functions in module."""
        return sum(1 for node in ast.walk(tree) 
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    
    def _count_imports(self, tree: ast.AST) -> int:
        """Count import statements."""
        return sum(1 for node in ast.walk(tree) 
                  if isinstance(node, (ast.Import, ast.ImportFrom)))
    
    def _count_external_deps(self, tree: ast.AST) -> int:
        """Count external dependencies."""
        external = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith("src"):
                    external += 1
        return external
    
    def _calculate_cohesion(self) -> float:
        """Calculate module cohesion score."""
        if not self.modules:
            return 0.0
        
        # High cohesion = focused modules with related components
        cohesion_scores = []
        for module_data in self.modules.values():
            classes = module_data["classes"]
            functions = module_data["functions"]
            total = classes + functions
            
            if total == 0:
                continue
            
            # Modules with 1-5 classes/functions are highly cohesive
            if total <= 5:
                score = 100.0
            elif total <= 10:
                score = 85.0
            elif total <= 20:
                score = 70.0
            else:
                score = 50.0
            
            cohesion_scores.append(score)
        
        return sum(cohesion_scores) / len(cohesion_scores) if cohesion_scores else 0.0
    
    def _calculate_coupling(self) -> float:
        """Calculate coupling score (higher = less coupled)."""
        if not self.modules:
            return 0.0
        
        coupling_scores = []
        for module_data in self.modules.values():
            imports = module_data["imports"]
            external = module_data["external_deps"]
            
            # Low coupling = few dependencies
            if imports <= 5:
                score = 95.0
            elif imports <= 10:
                score = 85.0
            elif imports <= 15:
                score = 75.0
            else:
                score = 60.0
            
            # Penalize external dependencies
            if external > 5:
                score -= 10
            
            coupling_scores.append(max(score, 0))
        
        return sum(coupling_scores) / len(coupling_scores) if coupling_scores else 0.0
    
    def _calculate_separation(self) -> float:
        """Calculate separation of concerns."""
        if not self.modules:
            return 0.0
        
        # Check directory structure
        directories = set()
        for module_path in self.modules.keys():
            parts = Path(module_path).parts
            if len(parts) > 1:
                directories.add(parts[0])
        
        # More directories = better separation
        num_dirs = len(directories)
        if num_dirs >= 8:
            return 95.0
        elif num_dirs >= 6:
            return 85.0
        elif num_dirs >= 4:
            return 75.0
        else:
            return 60.0
    
    def _calculate_reusability(self) -> float:
        """Calculate reusability score."""
        if not self.modules:
            return 0.0
        
        # Count abstract classes and interfaces
        reusable_count = 0
        total_count = 0
        
        for module_path in self.modules.keys():
            total_count += 1
            # Interfaces, base classes, utilities are reusable
            if any(x in module_path.lower() for x in 
                   ["interface", "base", "abstract", "util", "helper"]):
                reusable_count += 1
        
        if total_count == 0:
            return 0.0
        
        ratio = reusable_count / total_count
        return min(ratio * 100 + 50, 100.0)


if __name__ == "__main__":
    checker = ModularityChecker("src")
    results = checker.analyze()
    
    print("=" * 70)
    print("MODULARITY METRICS REPORT")
    print("=" * 70)
    print(f"\nModule Cohesion: {results['cohesion']}% (Target: >80%)")
    print(f"Coupling Score: {results['coupling']}% (Target: >70%)")
    print(f"Separation of Concerns: {results['separation']}% (Target: >80%)")
    print(f"Reusability: {results['reusability']}% (Target: >70%)")
    
    # Status
    print("\n" + "=" * 70)
    print("STATUS:")
    all_pass = (
        results['cohesion'] >= 80 and
        results['coupling'] >= 70 and
        results['separation'] >= 80 and
        results['reusability'] >= 70
    )
    
    if all_pass:
        print("[PASS] ALL MODULARITY TARGETS MET")
    else:
        print("[WARN] SOME TARGETS NOT MET")
        if results['cohesion'] < 80:
            print(f"  - Improve cohesion to >80% (currently {results['cohesion']}%)")
        if results['coupling'] < 70:
            print(f"  - Improve coupling to >70% (currently {results['coupling']}%)")
        if results['separation'] < 80:
            print(f"  - Improve separation to >80% (currently {results['separation']}%)")
        if results['reusability'] < 70:
            print(f"  - Improve reusability to >70% (currently {results['reusability']}%)")
    print("=" * 70)
