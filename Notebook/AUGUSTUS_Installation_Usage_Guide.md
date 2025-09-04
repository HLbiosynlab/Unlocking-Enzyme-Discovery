AUGUSTUS Installation & Usage Guide

AUGUSTUS is a gene prediction tool that supports both pre-trained species models and custom training for new species.
Due to its complexity, we recommend using conda for installation.

🔹 Installation

```conda install augustus```

🔹 Basic Usage
1. If a trained species model exists

Check available species:

```augustus --species=help```


Run gene prediction (example: Arabidopsis thaliana):

```augustus --species=arabidopsis test.fa > test.gff```

2. If no trained species model exists — Training required
Training & Test Dataset Requirements

    According to the official AUGUSTUS documentation, a reliable gene structure dataset should meet the following criteria:

    Gene coding regions should include a few kb upstream; at least 200 genes are recommended, with enough exons for intron model training.

    Accurate gene structures — start and stop codons must be correct (perfect annotation is not required).

    Non-redundant sequences — any two genes should have <70% amino acid identity.

    No overlapping genes; one transcript per gene; GenBank format is required.

    Test set should contain 100–200 random genes for statistical evaluation.

    Possible data sources:

        GenBank

        EST/mRNA-seq assemblies (e.g., PASA)

        Orthologous protein spliced alignments (e.g., GeneWise)

        Closely related species data

Training Workflow Example (Spinach)

Replace spinach with your species name as needed.

(1) Convert GFF3 to GenBank

```perl gff2gbSmallDNA.pl spinach_gene_v1.gff3 spinach_genome_v1.fa 1000 genes.raw.gb```

(2) Initial training & capture errors

```etraining --species=generic --stopCodonExcludedFromCDS=false genes.raw.gb 2> train.err```

(3) Filter problematic gene structures

```cat train.err | perl -pe 's/.*in sequence (\S+): .*/$1/' > badgenes.lst```

```filterGenes.pl badgenes.lst genes.raw.gb > genes.gb```

(4) Extract protein sequences

```grep '/gene' genes.gb | sort | uniq | sed 's/\/gene=//g' | sed 's/\"//g' | awk '{print $1}' > geneSet.lst```

```seqkit grep -f geneSet.lst spinach_pep_v1.fa > geneSet.lst.fa```

(5) Remove redundant genes (≥70% identity)

```makeblastdb -in geneSet.lst.fa -dbtype prot -parse_seqids -out geneSet.lst.fa```

```blastp -db geneSet.lst.fa -query geneSet.lst.fa -out geneSet.lst.fa.blastp -evalue 1e-5 -outfmt 6 -num_threads 8```

```python delete_high_identity_gene.py geneSet.lst.fa.blastp spinach_gene_v1.gff3```

(6) Convert filtered GFF3 to GenBank

```perl gff2gbSmallDNA.pl gene_filter.gff3 spinach_genome_v1.fa 1000 genes.gb.filter```

(7) Split into training & test sets

```randomSplit.pl genes.gb.filter 100```

(8) Initialize species parameters & train

```new_species.pl --species=spinach```

```etraining --species=spinach genes.gb.filter.train```

(9) Test & compare with related species

```augustus --species=spinach genes.gb.filter.test | tee firsttest.out```

```augustus --species=arabidopsis genes.gb.filter.test | tee firsttest_ara.out```

(10) Optimize parameters (optional)
```optimize_augustus.pl --species=spinach --rounds=5 --cpus=8 genes.gb.filter.train```

(11) Retrain & re-test

```etraining --species=spinach genes.gb.filter.train```

```augustus --species=spinach genes.gb.filter.test | tee secondtest.out```

(12) CRF Training (optional)

```etraining --species=spinach --CRF=1 genes.gb.filter.train```

```augustus --species=spinach genes.gb.filter.test | tee secondtest.out.withCRF```


📊 Key Evaluation Metrics

    TP (True Positive): predicted correctly as gene

    FP (False Positive): predicted as gene but not actually a gene

    FN (False Negative): missed gene

    TN (True Negative): correctly predicted as non-gene

    Sensitivity = TP / (TP + FN) — proportion of real genes correctly predicted

    Specificity = TN / (TN + FP) — proportion of non-genes correctly predicted

    Goal: minimize both false positives and false negatives.

📌 Notes

    If sensitivity <20% after training, your training set may be too small — add more data.

    CRF training may improve accuracy; compare results before and after.

    Once satisfied with training, use the trained model for genome-wide predictions.