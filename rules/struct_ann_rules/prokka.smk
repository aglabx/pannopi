rule annotation:
    input:
        rules.assembly.output.assembly
    conda:
        envs.prokka
    threads: workflow.cores
    output:
        annotation_faa = config["annotation_faa"],
        annotation_gbk = config["annotation_gbk"],
    params:
        dir = directory(config["annotation_dir"]),
        prokka_prefix = config["prefix"]
    shell:
        """
        prokka \
            --force \
            --cpus {threads} \
            --outdir {params.dir} \
            --prefix {params.prokka_prefix} \
            --centre X --compliant {input}
        """