"""Comprehensive code quality checker for all Python files."""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple


class CodeQualityChecker:
    """Check code quality metrics for Python files."""

    def __init__(self, root_dir: str = "src"):
        self.root = Path(root_dir)
        self.results: Dict[str, Dict] = {}

    def check_all(self) -> Dict[str, any]:
        """Run all quality checks."""
        py_files = list(self.root.rglob("*.py"))
        
        total_syntax_errors = 0
        total_lines = 0
        total_code_smells = 0
        total_functions = 0
        functions_with_docstrings = 0
        naming_violations = 0
        total_names = 0
        
        for file_path in py_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                lines = content.split("\n")
                total_lines += len(lines)
                
                # Check syntax
                try:
                    tree = ast.parse(content)
                except SyntaxError:
                    total_syntax_errors += 1
                    continue
                
                # Check code smells
                smells = self._check_code_smells(content, lines)
                total_code_smells += smells
                
                # Check docstrings
                funcs, with_docs = self._check_docstrings(tree)
                total_functions += funcs
                functions_with_docstrings += with_docs
                
                # Check naming
                violations, names = self._check_naming(tree)
                naming_violations += violations
                total_names += names
                
            except Exception:
                continue
        
        # Calculate metrics
        code_smell_pct = (total_code_smells / total_lines * 100) if total_lines else 0
        docstring_coverage = (functions_with_docstrings / total_functions * 100) if total_functions else 0
        naming_score = ((total_names - naming_violations) / total_names * 100) if total_names else 100
        
        return {
            "syntax_errors": total_syntax_errors,
            "code_smells": total_code_smells,
            "code_smell_percentage": round(code_smell_pct, 2),
            "total_lines": total_lines,
            "docstring_coverage": round(docstring_coverage, 2),
            "naming_conventions": round(naming_score, 2),
            "total_functions": total_functions,
            "functions_with_docs": functions_with_docstrings,
            "naming_violations": naming_violations,
            "total_names": total_names
        }
    
    def _check_code_smells(self, content: str, lines: List[str]) -> int:
        """Check for code smells."""
        smells = 0
        
        # Long lines (>79 chars)
        for line in lines:
            if len(line) > 79 and not line.strip().startswith("#"):
                smells += 1
        
        # Too many blank lines
        blank_count = 0
        for line in lines:
            if not line.strip():
                blank_count += 1
                if blank_count > 2:
                    smells += 1
            else:
                blank_count = 0
        
        return smells
    
    def _check_docstrings(self, tree: ast.AST) -> Tuple[int, int]:
        """Check docstring coverage."""
        total = 0
        with_docs = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                total += 1
                if ast.get_docstring(node):
                    with_docs += 1
        
        return total, with_docs
    
    def _check_naming(self, tree: ast.AST) -> Tuple[int, int]:
        """Check PEP8 naming conventions."""
        violations = 0
        total = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                total += 1
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    violations += 1
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total += 1
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    violations += 1
            
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    name = node.id
                    if name.isupper() and len(name) > 1:
                        # Constant
                        total += 1
                    elif not name.startswith('_'):
                        total += 1
                        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
                            violations += 1
        
        return violations, total


if __name__ == "__main__":
    checker = CodeQualityChecker("src")
    results = checker.check_all()
    
    print("=" * 70)
    print("CODE QUALITY REPORT")
    print("=" * 70)
    print(f"\nSyntax Errors: {results['syntax_errors']} (Target: 0)")
    print(f"Code Smells: {results['code_smells']} ({results['code_smell_percentage']}% of lines, Target: <10%)")
    print(f"Docstring Coverage: {results['docstring_coverage']}% (Target: >80%)")
    print(f"Naming Conventions: {results['naming_conventions']}% (Target: >90%)")
    print(f"\nTotal Lines: {results['total_lines']}")
    print(f"Total Functions/Classes: {results['total_functions']}")
    print(f"Functions with Docstrings: {results['functions_with_docs']}")
    print(f"Naming Violations: {results['naming_violations']}/{results['total_names']}")
    
    # Status
    print("\n" + "=" * 70)
    print("STATUS:")
    all_pass = (
        results['syntax_errors'] == 0 and
        results['code_smell_percentage'] < 10 and
        results['docstring_coverage'] >= 80 and
        results['naming_conventions'] >= 90
    )
    
    if all_pass:
        print("[PASS] ALL CODE QUALITY TARGETS MET")
    else:
        print("[WARN] SOME TARGETS NOT MET")
        if results['syntax_errors'] > 0:
            print(f"  - Fix {results['syntax_errors']} syntax errors")
        if results['code_smell_percentage'] >= 10:
            print(f"  - Reduce code smells to <10% (currently {results['code_smell_percentage']}%)")
        if results['docstring_coverage'] < 80:
            print(f"  - Increase docstring coverage to >80% (currently {results['docstring_coverage']}%)")
        if results['naming_conventions'] < 90:
            print(f"  - Improve naming conventions to >90% (currently {results['naming_conventions']}%)")
    print("=" * 70)
