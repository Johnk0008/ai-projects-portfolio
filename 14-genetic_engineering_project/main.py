"""
Genetic Engineering Data Analysis Application
Advanced CRISPR and Gene Therapy Analysis Tool
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple
import json
from dataclasses import dataclass


@dataclass
class GeneSequence:
    """Data class for storing gene sequence information"""

    name: str
    sequence: str
    length: int
    gc_content: float
    pam_sites: List[int]


class CRISPRAnalyzer:
    """Advanced CRISPR-Cas9 Genetic Sequence Analyzer"""

    def __init__(self):
        self.gene_data = {}
        self.crispr_results = {}
        self.pam_patterns = {
            "cas9": "NGG",
            "cas12a": "TTTV",
            "cas13": "Specific to RNA targets",
        }

    def load_gene_sequences(self, sequences: Dict[str, str]) -> None:
        """Load gene sequences for CRISPR analysis"""
        self.gene_data.update(sequences)
        print(f"✅ Loaded {len(sequences)} gene sequences for analysis")

    def validate_dna_sequence(self, sequence: str) -> bool:
        """Validate if sequence contains only valid DNA nucleotides"""
        valid_bases = {"A", "T", "C", "G", "N"}
        return all(base.upper() in valid_bases for base in sequence)

    def find_pam_sites(self, sequence: str, pam_type: str = "cas9") -> List[int]:
        """Find Protospacer Adjacent Motif (PAM) sites in DNA sequence"""
        if not self.validate_dna_sequence(sequence):
            raise ValueError("Invalid DNA sequence detected")

        pam_pattern = self.pam_patterns.get(pam_type, "NGG")
        sites = []

        # Convert pattern to regex-like search
        for i in range(len(sequence) - len(pam_pattern) + 1):
            window = sequence[i : i + len(pam_pattern)].upper()
            match = True

            for j, (pattern_char, seq_char) in enumerate(zip(pam_pattern, window)):
                if pattern_char == "N":
                    continue  # N matches any base
                elif pattern_char != seq_char:
                    match = False
                    break

            if match:
                sites.append(i)

        return sites

    def calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content percentage in DNA sequence"""
        if not sequence:
            return 0.0

        sequence_upper = sequence.upper()
        gc_count = sequence_upper.count("G") + sequence_upper.count("C")
        return (gc_count / len(sequence)) * 100

    def analyze_gene_editing_efficiency(self, sequence: str, gc_content: float) -> str:
        """Predict CRISPR editing efficiency based on sequence characteristics"""
        if gc_content < 30:
            return "Low efficiency - GC content too low"
        elif gc_content > 70:
            return "Low efficiency - GC content too high"
        elif 40 <= gc_content <= 60:
            return "High efficiency - Optimal GC content"
        else:
            return "Moderate efficiency"

    def analyze_sequences(self) -> Dict:
        """Comprehensive analysis of all loaded gene sequences"""
        results = {}

        for gene_name, sequence in self.gene_data.items():
            if not self.validate_dna_sequence(sequence):
                print(f"⚠️  Skipping invalid sequence: {gene_name}")
                continue

            pam_sites = self.find_pam_sites(sequence)
            gc_content = self.calculate_gc_content(sequence)
            editing_efficiency = self.analyze_gene_editing_efficiency(
                sequence, gc_content
            )

            results[gene_name] = {
                "length": len(sequence),
                "pam_sites": len(pam_sites),
                "gc_content": gc_content,
                "pam_locations": pam_sites[:10],  # First 10 locations
                "editing_efficiency": editing_efficiency,
                "sequence_preview": (
                    sequence[:50] + "..." if len(sequence) > 50 else sequence
                ),
            }

        self.crispr_results = results
        return results

    def generate_comprehensive_report(self) -> str:
        """Generate detailed analysis report"""
        if not self.crispr_results:
            return "No analysis results available. Run analyze_sequences() first."

        report = []
        report.append("=" * 60)
        report.append("🧬 COMPREHENSIVE CRISPR GENE ANALYSIS REPORT")
        report.append("=" * 60)

        for gene, data in self.crispr_results.items():
            report.append(f"\n📊 GENE: {gene}")
            report.append(f"   • Sequence Length: {data['length']} bp")
            report.append(f"   • GC Content: {data['gc_content']:.2f}%")
            report.append(f"   • PAM Sites Found: {data['pam_sites']}")
            report.append(f"   • Editing Efficiency: {data['editing_efficiency']}")
            report.append(f"   • First 5 PAM Locations: {data['pam_locations'][:5]}")
            report.append(f"   • Sequence Preview: {data['sequence_preview']}")

        # Summary statistics
        total_genes = len(self.crispr_results)
        avg_gc = np.mean([data["gc_content"] for data in self.crispr_results.values()])
        total_pam_sites = sum(
            [data["pam_sites"] for data in self.crispr_results.values()]
        )

        report.append("\n" + "=" * 60)
        report.append("📈 SUMMARY STATISTICS")
        report.append("=" * 60)
        report.append(f"   • Total Genes Analyzed: {total_genes}")
        report.append(f"   • Average GC Content: {avg_gc:.2f}%")
        report.append(f"   • Total PAM Sites: {total_pam_sites}")
        report.append(f"   • PAM Sites per Gene: {total_pam_sites/total_genes:.1f}")

        return "\n".join(report)


def create_advanced_visualization(
    results: Dict, save_path: str = "crispr_analysis.png"
):
    """Create comprehensive visualization of CRISPR analysis results"""
    if not results:
        print("No results to visualize")
        return

    genes = list(results.keys())
    gc_contents = [results[gene]["gc_content"] for gene in genes]
    pam_counts = [results[gene]["pam_sites"] for gene in genes]
    sequence_lengths = [results[gene]["length"] for gene in genes]

    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(
        "Advanced CRISPR Genetic Engineering Analysis", fontsize=16, fontweight="bold"
    )

    # 1. GC Content Bar Chart
    bars = ax1.bar(
        genes,
        gc_contents,
        color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
    )
    ax1.set_title("GC Content Distribution by Gene", fontweight="bold")
    ax1.set_ylabel("GC Content (%)")
    ax1.tick_params(axis="x", rotation=45)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
        )

    # 2. PAM Sites vs Sequence Length Scatter
    scatter = ax2.scatter(
        pam_counts, sequence_lengths, s=100, c=gc_contents, cmap="viridis", alpha=0.7
    )
    ax2.set_xlabel("Number of PAM Sites")
    ax2.set_ylabel("Sequence Length (bp)")
    ax2.set_title("PAM Sites vs Sequence Length", fontweight="bold")
    plt.colorbar(scatter, ax=ax2, label="GC Content (%)")

    # 3. PAM Sites Distribution
    ax3.bar(genes, pam_counts, color="lightcoral", edgecolor="darkred", linewidth=1.2)
    ax3.set_title("PAM Sites Distribution by Gene", fontweight="bold")
    ax3.set_ylabel("Number of PAM Sites")
    ax3.tick_params(axis="x", rotation=45)

    # 4. Efficiency Analysis Pie Chart
    efficiency_labels = ["High", "Moderate", "Low"]
    efficiency_counts = [0, 0, 0]

    for gene_data in results.values():
        eff = gene_data["editing_efficiency"]
        if "High" in eff:
            efficiency_counts[0] += 1
        elif "Moderate" in eff:
            efficiency_counts[1] += 1
        else:
            efficiency_counts[2] += 1

    colors = ["#2E8B57", "#FFA500", "#DC143C"]
    ax4.pie(
        efficiency_counts,
        labels=efficiency_labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )
    ax4.set_title("CRISPR Editing Efficiency Distribution", fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"✅ Visualization saved as: {save_path}")


def main():
    """Main application function with enhanced features"""

    print("🧬 CRISPR Genetic Engineering Analysis Tool")
    print("=" * 50)

    # Enhanced sample gene sequences (real gene examples)
    sample_sequences = {
        "BRCA1": "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG",
        "TP53": "GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
        "CFTR": "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG",
        "APOE": "GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
        "HBB": "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG",
    }

    # Initialize analyzer
    analyzer = CRISPRAnalyzer()

    try:
        # Load and analyze sequences
        analyzer.load_gene_sequences(sample_sequences)
        results = analyzer.analyze_sequences()

        # Generate and display report
        report = analyzer.generate_comprehensive_report()
        print(report)

        # Create advanced visualization
        create_advanced_visualization(results, "genetic_engineering_analysis.png")

        # Save results to JSON
        with open("crispr_analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("✅ Results saved to: crispr_analysis_results.json")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")


if __name__ == "__main__":
    main()
