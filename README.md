# Pannopi - from reads to functional annotation pipeline
 
## Workflow
![alt text](./markdown/workflow_pannopi.png)
## Dependencies
1) [Eggnog-mapper](https://github.com/eggnogdb/eggnog-mapper) - to download [EggNOG v5](http://eggnog5.embl.de/#/app/home) database for functional annotation
2) [BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) - to download and create BLAST NT database for genome content identification and filtering
3) [Mamba](https://github.com/mamba-org/mamba) - to install all the tool included in Pannopi
4) [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) - to run Pannopi
## Install, set and run
Pannopi is available in conda, to install and set is use following commands:
1) Download Pannopi in separate conda envieronment: `conda create -n pannopi -c conda-forge -c bioconda -c aglab pannopi`
2) Activate the envieronment: `conda activate pannopi`
3) Eggnog-mapper databae (~50GB) is required to run Pannopi. BLAST NT (~110 GB) is needed for genome 
   filtration, but not necessary. You can download each of it together or separately or set your own ones, 
   if you have it already. Use `pannopi_download_db` tool to set or download databases. Examples:
   ```
   # Download all databases
   pannopi_download_db -m all -o /path/to/database/directory
  
   # Download eggnog-mapper/blast database 
   pannopi_download_db -m eggnog/blast -o /path/to/database/directory
   
   # Set yours eggnog or blast database
   pannopi_download_db -m set -e /path/to/eggnog/database -b /path/to/blast/database/nt
   ```
4) To run Pannopi on your reads use one of the following commands: 
   ```
   # If you have only short reads
   pannopi -m short -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -r /path/to/reference.fasta -t 32 -o /path/to/outdir
      
   # If you have only long reads
   pannopi -m long -l /path/to/long_read.fastq -t 32 -o /path/to/outdir
      
   # If you have both short and long reads
   pannopi -m hybrid -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -l /path/to/long_read.fastq -t 32 -o /path/to/outdir
   ```

## Assembly Modes
1) **Short** - mode for analysis of short reads. Starts with preparation of reads with [v2trim]() and [rmdup](). 
   Data preparation QC with [FastQC](), [Jellyfish]() and [GenomeScope](). Assembly with  
2) **Long** - mode for analysis of short reads. 
3) **Hybrid** - mode for analysis of both short- and long-reads with hybrid assembly. Reads QC as in **Short** mode.

## Filtration and Assembly QC
1) Filtration of technical sequences contamination with [Contera](). If BLAST NT database is provided Contera will report 
   about genome taxonomic content.
2) Statistical QC of assembly with [QUAST]().
3) ANI analysis with FastANI. Works only if reference (or close) genome are provided with `-r` argument.

## Annotation
1) Structural annotation with [Prokka]()
2) Functional annotation with [eggnog-mapper]
3) Antibiotic resistance, virulence, plasmid and serotype (only for E. Coli) genes with [Abricate]()
4) MLST genes with [MLST]()
5) CRISPRs with [CRISPRCasFinder]() in progress..
6) Genome visualisation with [pyCircos]()

## Command line options 

```
-m (–mode). Mode to run the pipeline [short, long or hybrid]. Single
for paired-end Illumina reads, long for long-reads, hybrid for hybrid
assembly with both short and long reads. [Required]
-1 (–forward). Path to forward read FASTQ file. [Required for short and hybrid modes]
-2 (–reverse). Path to reverse read FASTQ file. [Required for short and hybrid modes]
-l (–long-read). Path to reverse read FASTQ file. [Required for long and hybrid modes]
-r (–reference). Path to reference genome in FASTA format.
-t (–threads). Number of threads to use [Default is 4].
-o (–outdir). Path to output directory to store results. [Required]
parameter.
-d (–debug). Debug mode to check pipeline workflow.
-h (–help). Help message with arguments description.
```
