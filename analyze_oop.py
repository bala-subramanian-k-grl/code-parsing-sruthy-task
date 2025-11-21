import os
import re

files = [os.path.join(r, f) for r, _, fs in os.walk('src') for f in fs 
         if f.endswith('.py') and '__pycache__' not in r and '__init__' not in f]

print("=" * 80)
print("OOP ANALYSIS - EVERY PYTHON FILE")
print("=" * 80)
print()

for i, filepath in enumerate(sorted(files), 1):
    filename = filepath.replace('src\\', '').replace('src/', '')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_class = bool(re.search(r'^class ', content, re.M))
    if not has_class:
        continue
        
    has_init = bool(re.search(r'def __init__', content))
    has_private = bool(re.search(r'self\.__', content))
    has_property = bool(re.search(r'@property', content))
    has_str = bool(re.search(r'def __str__', content))
    has_repr = bool(re.search(r'def __repr__', content))
    has_eq = bool(re.search(r'def __eq__', content))
    has_hash = bool(re.search(r'def __hash__', content))
    
    print(f"{i}. {filename}")
    print(f"   Has: ", end="")
    status = []
    if has_init: status.append("__init__")
    if has_private: status.append("private")
    if has_property: status.append("@property")
    if has_str: status.append("__str__")
    if has_repr: status.append("__repr__")
    if has_eq: status.append("__eq__")
    if has_hash: status.append("__hash__")
    print(", ".join(status) if status else "NONE")
    
    needs = []
    if not has_eq: needs.append("__eq__")
    if not has_hash: needs.append("__hash__")
    if has_private and not has_property: needs.append("@property")
    if has_init and not has_private: needs.append("private attrs")
    if not has_str: needs.append("__str__")
    if not has_repr: needs.append("__repr__")
    
    if needs:
        print(f"   NEEDS: {', '.join(needs)}")
    else:
        print(f"   STATUS: COMPLETE")
    print()
