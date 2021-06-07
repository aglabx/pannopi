rule results:
    input:
        assembly = rules.assembly.output.assembly,
        assembly_filtered = rules.contera.output,
        scope = rules.genomescope.output,
        fast1 = rules.fastqc1.output,
        fast2 = rules.fastqc2.output,
        quast = rules.quast.output,
        proteins = rules.annotation.output.annotation_faa,
        prokka_results = rules.annotatiom.output.report_txt,
        functional_annotation = rules.eggnog.output.eggnog_out_annotation,
        busco = rules.busco.output.busco_outfile,
        ncbi = rules.ncbi.output,
        megares = rules.megares.output,
        plasmid = rules.plasmids.output,
        virulence = rules.virulence.output,
        fastani = rules.fastani.output,
    output:
        results_file = config["results_file"],
    params:
        pannopi_results = "../../tools/pannopi_report.py"
        path = directory(config["results_path"])
    shell:
        "{params.pannopi_results} -f {input.fastani} -q {input.quast} -b {input.busco} -e {input.functional_annotation} \
         -n {input.virulence} -m {input.megares} -pl {input.plasmid} "
        "-v {input.virulence} -p {input.prokka_results} -o {output}"
