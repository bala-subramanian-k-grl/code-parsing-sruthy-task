import os
import re

files = [os.path.join(r, f) for r, _, fs in os.walk('src') 
         for f in fs if f.endswith('.py') and '__pycache__' not in r]

# Count everything
classes = 0
inheritance = 0
abstract_classes = 0
private_attrs = 0
properties = 0
special_methods = 0
protected_methods = 0

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    classes += len(re.findall(r'^class \w+', content, re.M))
    inheritance += len(re.findall(r'class \w+\([^)]+\)', content))
    abstract_classes += len(re.findall(r'class \w+.*ABC', content))
    private_attrs += len(re.findall(r'self\.__\w+', content))
    properties += len(re.findall(r'@property', content))
    special_methods += len(re.findall(r'def __\w+__', content))
    protected_methods += len(re.findall(r'def _\w+', content))

print("=" * 60)
print("ACTUAL OOP METRICS")
print("=" * 60)
print(f"Total classes: {classes}")
print(f"Classes with inheritance: {inheritance}")
print(f"Abstract classes: {abstract_classes}")
print(f"Private attributes: {private_attrs}")
print(f"Properties: {properties}")
print(f"Special methods: {special_methods}")
print(f"Protected methods: {protected_methods}")
print()

# Calculate scores
encapsulation_score = min(100, (private_attrs + properties) / classes * 10) if classes else 0
inheritance_score = min(100, inheritance / classes * 100) if classes else 0
polymorphism_score = min(100, special_methods / classes * 10) if classes else 0
abstraction_score = min(100, abstract_classes / classes * 100) if classes else 0

print("COMPONENT SCORES:")
print(f"Encapsulation: {encapsulation_score:.1f}%")
print(f"Inheritance: {inheritance_score:.1f}%")
print(f"Polymorphism: {polymorphism_score:.1f}%")
print(f"Abstraction: {abstraction_score:.1f}%")
print()

# Weighted average (typical OOP scoring)
oop_score = (
    encapsulation_score * 0.30 +
    inheritance_score * 0.20 +
    polymorphism_score * 0.20 +
    abstraction_score * 0.15 +
    85 * 0.15  # Assume good composition/patterns
)

print(f"ESTIMATED OOP SCORE: {oop_score:.1f}")
print()
print("To reach 60:")
needed = 60 - oop_score
print(f"Need: +{needed:.1f} points")
print()
print("Options:")
print(f"1. Improve encapsulation to 100%: +{(100-encapsulation_score)*0.30:.1f} points")
print(f"2. Improve polymorphism to 100%: +{(100-polymorphism_score)*0.20:.1f} points")
