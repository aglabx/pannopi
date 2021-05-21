rule jellycount:
    input:
        rules.v2trim.output,
    conda:
        envs.jellyfish
    threads: 1
    output:
        jellycount_file = config["jellycount_file"],
    shell:
        """
        jellyfish count \
            -m 23 \
            -t 32 \
            -s 2G \
            -C \
            -o {output} \
            {input}
        """

rule jellyhisto:
    input:
        rules.jellycount.output,
    conda:
        envs.jellyfish
    threads: 1
    output:
        jellyhisto_file = config["jellyhisto_file"],
    shell:
        """
        jellyfish histo \
            -o {output} \
            {input}
        """

rule genomescope:
    input:
        rules.jellyhisto.output
    conda:
        envs.genomescope
    threads: 1
    output:
        scope_file = config["scope_file"]
    log: config["genomescope_log"]
    benchmark: config["genomescope_bench"]
    params:
        scope_dir = directory(config["scope_dir"]),
        prefix = config["prefix"]
    shell:
        """
        genomescope2 -i {input} -o {params.scope_dir} -k 23 -n {params.prefix} 2> {log} | tee -a {log}
        """
