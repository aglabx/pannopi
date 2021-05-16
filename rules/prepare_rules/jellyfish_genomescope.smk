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
        envs.r
    output:
        scope_file = config["scope_file"]
    params:
        scope = tools.genomescope,
        scope_dir = directory(config["scope_dir"])
    shell:
        """
        Rscript {params.scope} {input} 23 100 {params.scope_dir} 1000
        """
