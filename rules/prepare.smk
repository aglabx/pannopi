rule trim:
    message:
        "Trimming the raw reads"
    input:
        forward_read = config["raw_fastq_1"],
        rewerse_read = config["raw_fastq_2"]
    output:
        trim_out_file1 = config["trim_out_file_1"],
        trim_out_file2 = config["trim_out_file_2"]
    params:
        in_prefix = config["trim_in_prefix"],
        out_prefix = config["trim_out_prefix"],
        v2trim_path = tools.v2trim,
        ill_ext_path = tools.ill_ext,
    shell:
        """
        {params.v2trim_path} \
            {params.in_prefix} \
            {params.out_prefix} \
            20 0 fastq \
            {params.ill_ext_path}
        """

rule rmdub:
    message:
        "Optical duplacates deliting"
    input:
        rules.trim.output
    output:
        rmdub_out_file1 = config["rmdub_file_1"],
        rmdub_out_file2 = config["rmdub_file_2"]
    params:
        in_prefix = config["rmdub_in_prefix"],
        out_prefix = config["rmdub_out_prefix"],
        rmdub_path = tools.rmdub,
    shell:
        """
        {params.rmdub_path} \
            {params.in_prefix} \
            {params.out_prefix} \
            3000 3 0,30
        """
