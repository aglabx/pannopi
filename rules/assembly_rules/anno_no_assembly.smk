rule assembly:
    input:
        assembly = config["assembly_provided"]
    output:
        assembly = config["assembly"]
    params:
        assembly_dir = config["assembly_dir"]
    shell:
        """
        echo 'Assembly found in {input}... start filtering and annotation'
        
        cp {input} {output}
        """
