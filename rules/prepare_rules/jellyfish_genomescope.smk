rule jellycount:
    input:
        rules.rmdup.output,
    conda:
        envs.jellyfish
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
    output:
        scope_file = config["scope_file"]
    params:
        scope_dir = directory(config["scope_dir"]),
        prefix = config["prefix"]
    shell:
        """
        genomescope2 -i {input} -o {params.scope_dir} -k 23 -n {params.prefix}
        """
