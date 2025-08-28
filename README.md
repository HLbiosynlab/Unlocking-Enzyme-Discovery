![release](https://img.shields.io/github/v/release/HLbiosynlab/Unlocking-Enzyme-Discovery)
![last-commit](https://img.shields.io/github/last-commit/HLbiosynlab/Unlocking-Enzyme-Discovery)
![issues](https://img.shields.io/github/issues/HLbiosynlab/Unlocking-Enzyme-Discovery)
![pull-requests](https://img.shields.io/github/issues-pr/HLbiosynlab/Unlocking-Enzyme-Discovery)
![license](https://img.shields.io/github/license/HLbiosynlab/Unlocking-Enzyme-Discovery)
![stars](https://img.shields.io/github/stars/HLbiosynlab/Unlocking-Enzyme-Discovery?style=social)
# Unlocking-Enzyme-Discovery

An integrated machine learning and bioinformatics pipeline for discovering scarce, high-value enzymes from vast, under-annotated genomic repositories.

## 📌 Overview
High-throughput sequencing has generated massive genomic datasets, yet the lack of precise annotation severely hampers enzyme discovery.  
This project presents a **robust, generalizable framework** that integrates phylogenetic analysis, protein language models, and multi-level contact scoring to identify and prioritize functional enzyme variants at scale.

## 🔬 Key Features
1. **High-resolution, cross-kingdom phylogenetic database**  
   - Covers bacterial, fungal, plant, and metagenomic sequences
   - Avoids redundancy while maximizing evolutionary diversity

2. **Multi-locus phylogenetic mining**  
   - Detects candidate enzymes via conserved multi-locus signatures

3. **Evolutionary-scale protein language model prediction**  
   - Predicts enzyme activities directly from protein sequences

4. **Multi-level residue–atom contact rescoring**  
   - Eliminates false positives from docking and enriches high-value hits

## 🧪 Application to the r-BOX Pathway
- Target enzymes: **FadB**, **BktB**, **Ter**, and **YdiI**
- Discovered numerous previously undocumented homologs
- Achieved **R² = 0.68** in activity prediction
- Reduced RMSE on high-value targets by **11%** compared to prior SOTA (*UniKP*)
- Improved early enrichment (**EF1%**) by **16×**

## 📈 Experimental Validation
- **FadB** engineering increased titers from:
  - 0.65 g/L (shake flasks) → 1.7 g/L  
  - Up to 10.2 g/L in a fermenter

## 📂 Repository Structure

