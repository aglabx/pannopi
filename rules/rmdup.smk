rule rmdup:
    input:
        v2trim_out_forward = rules.trimming.output.v2trim_out_forward,
        v2trim_out_reverse = rules.trimming.output.v2trim_out_reverse,
    conda:
        envs.rmdup
    threads: 20
    output:
        rmdup_out_forward = config["rmdup_out_file1"],
        rmdup_out_reverse = config["rmdup_out_file2"],
        rmdup_out_statistics = config["rmdup_out_statistics"] ,
    params:
        rmdup_dir = directory(config["rmdup_dir"]) 
    shell:
        """rmdup -1 {input.v2trim_out_forward} \
                 -2 {input.v2trim_out_reverse} \
                 -o {params.rmdup_dir} \
                 -t {threads} """

