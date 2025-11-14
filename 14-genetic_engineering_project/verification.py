# verification.py
import pkg_resources

required_packages = [
    "ipykernel",
    "jupyter",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "biopython",
]

print("Package Verification:")
print("=" * 30)

for package in required_packages:
    try:
        dist = pkg_resources.get_distribution(package)
        print(f"✓ {package}: {dist.version}")
    except pkg_resources.DistributionNotFound:
        print(f"✗ {package}: NOT INSTALLED")

print("\nSetup complete! You can now run your genetic engineering analysis.")
