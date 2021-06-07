rule annotation:
    input:
        rules.contera.output
    conda:
        envs.prokka
    threads: workflow.cores - 1
    output:
        annotation_faa = config["annotation_faa"],
        annotation_gbk = config["annotation_gbk"],
        report_txt = config["prokka_report"],
    log: config["prokka_log"]
    benchmark: config["prokka_bench"]
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
            --centre X --compliant {input} 2> {log} | tee -a {log}
        """
