rule rmdup:
    input:
        v2trim_out_forward = rules.v2trim.output.v2trim_out_forward,
        v2trim_out_reverse = rules.v2trim.output.v2trim_out_reverse,
    conda:
        envs.rmdup
    threads: workflow.cores - 1
    log: config["rmdup_log"]
    benchmark: config["rmdup_bench"]
    output:
        rmdup_out_forward = config["rmdup_out_file1"],
        rmdup_out_reverse = config["rmdup_out_file2"],
        rmdup_out_statistics = config["rmdup_out_statistics"] ,
    params:
        rmdup_dir = directory(config["rmdup_dir"]),
        rmdup_prefix = config["rmdup_prefix"]
    shell:
        """rmdup -1 {input.v2trim_out_forward} \
                 -2 {input.v2trim_out_reverse} \
                 -o {params.rmdup_dir} \
                 -p {params.rmdup_prefix} \
                 -t {threads} 2> {log} | tee -a {log}"""

