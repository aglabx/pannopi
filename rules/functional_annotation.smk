include: "func_ann_rules/eggnog.smk"

include: "func_ann_rules/abricate.smk"

include: "func_ann_rules/mlst.smk"


#rule goann:
#    input:
#        egg = rules.eggnog.output,
#    output:
#        config["goann_out"]
#    params:
#        obo_annotation = tools.obo_annotation,
#        goobo = tools.goobo,
#        outdir = config["goann_outdir"]
#    shell:
#        """
#        python {params.goobo} -g {params.obo_annotation} -e {input.egg} -o {params.outdir}
#        """