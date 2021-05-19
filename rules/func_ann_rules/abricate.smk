rule megares:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        megares_report = config["megares"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate --db megares {input} > {output}"

rule ncbi:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        ncbi_report = config["ncbi"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate {input} > {output}"

rule plasmid:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        plasmids_report = config["plasmids"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate --db plasmidfinder {input} > {output}"

rule virulence:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        plasmids_report = config["virulence"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate --db vfdb {input} > {output}"

rule serotype:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        plasmids_report = config["serotype"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate --db ecoh {input} > {output}"
        
rule abricate_summary:
    input:
        megares = rules.megares.output,
        ncbi = rules.ncbi.output,
        plasmids = rules.plasmid.output,
        virulence = rules.virulence.output,
        serotype = rules.serotype.output,
    output:
        whole_report = config["abricate_summary"]
    threads: 1
    conda:
        envs.abricate
    shell:
        "abricate --summary {input} > {output}"