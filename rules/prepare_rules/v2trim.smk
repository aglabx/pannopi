rule v2trim:
    input:
        v2trim_in_forward = config["v2trim_in_file1"] ,
        v2trim_in_reverse = config["v2trim_in_file2"],
    conda:
        envs.v2trim
    threads: workflow.cores
    output:
        v2trim_out_forward = config["v2trim_out_file1"] ,
        v2trim_out_reverse = config["v2trim_out_file2"],
        v2trim_statistics = config["v2trim_out_statistics"],
    params:
        v2trim_dir =  config["v2trim_dir"],
        v2trim_prefix = config["prefix"],
    shell:
        """v2trim -1 {input.v2trim_in_forward} \
                 -2 {input.v2trim_in_reverse} \
                 -o {params.v2trim_dir} \
                 -p {params.v2trim_prefix} \
                 -t {threads}
                 """