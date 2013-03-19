Getting started
===============
.. Note:: Make sure that you have successfully installed the blacktie module before trying the activities below.

To test whether your installation was successful, open a new terminal session and type the following command. ::

  $ blacktie

You should see the help text for blacktie and it should look something like this:

.. code-block:: none
  
  usage: blacktie [-h] [--prog {tophat,cufflinks,cuffmerge,cuffdiff,all}]
		  [--hide-logs] [--mode {analyze,dry_run,qsub_script}]
		  config_file

  This script reads options from a yaml formatted file and organizes the
  execution of tophat/cufflinks runs for multiple condition sets.

  positional arguments:
    config_file           Path to a yaml formatted config file containing setup
			  options for the runs.

  optional arguments:
    -h, --help            show this help message and exit
    --prog {tophat,cufflinks,cuffmerge,cuffdiff,all}
			  Which program do you want to run? (default: tophat)
    --hide-logs           Make your log directories hidden to keep a tidy
			  'looking' base directory. (default: False)
    --mode {analyze,dry_run,qsub_script}
			  1) 'analyze': run the analysis pipeline. 2) 'dry_run':
			  walk through all steps that would be run and print out
			  the command lines; however, do not send the commands
			  to the system to be run. 3) 'qsub_script': generate
			  bash scripts suitable to be sent to a compute
			  cluster's SGE through the qsub command. (default:
			  analyze)

If this worked, great! Let's move on to what all that means.

The configuration file
----------------------
The configuration file is a `YAML-based <http://en.wikipedia.org/wiki/YAML>`_ document that is where we will store all of the complexity of the options, input and output files of the typical tophat/cufflinks workflow.  This way we have though about what we want to do with our RNA-seq data from start to finish before we actually start the analysis.  Also, this config file acts as a check on our poor memory.  If you get strange results you don't have to worry about whether you entered the samples backwards since you can go back to this config file and see exactly what files and settings were used.

.. Note:: If you are running blacktie in ``analyze`` mode, you will have many more files created that document every step of the process where the output files are actually placed as well as central log files.

Here is a dummy example of a config file:

.. code-block:: yaml
  :linenos:

  # The document starts after the '---'

  # By the way: everything after a '#' on a line
  # will be ignored by the program and acts as a
  # comment or note to explain things.

  ---
  # run_options is a dictionary that contains variables that will be needed for
  # many or all stages of the run
  run_options:
    base_dir: /path/to/project/base_dir
    run_id: False         #  name your run: if false; uses current date/time for uniqe run_id everytime
    bowtie_indexes_dir: /path/to/bowtie2_indexes 
    email_info:
      sender: from_me@gmail.com           # for now only sending from gmail accounts is supported (will change soon)
      to: to_you@email.com
      li: /path/to/file/containing/base64_encoded/login_info      # base64_encoded pswrd for from_me@email.com



  # `tophat_options`:
  # -----------------
  # This is a dictionary that contains variables needed for all the tophat runs.
  # The names of the key:value combinations are taken directly from the tophat
  # option names but have the leading '-' removed.

  # -o becomes o; --library-type becomes library-type

  # **This is true for the cufflinks, cuffmerge, cuffdiff option dictionaries.** 

  # `from_conditions`:
  # ------------------
  # This is a special value that tells blacktie that you don't want to name a single
  # value for this option but would rather set the value individually for each of
  # your samples/conditions.  If you set the `o` value here: 

  #    **all of your different sample results would
  #      be written to the same output directory and
  #      each would overwrite the next!**
  # Hence: from_conditions

  # However if you made all of your libraries the same way, things like `r` and
  # `mate-std-dev` can be set here to avoid writing the same values over and over
  # and perhaps making a mistake or two.

  # `positional_args`:
  # ------------------
  # This is a dictionary inside of the `tophat_options` dictionary.
  # It is where you put the arguments to tophat that do not have 'flags' to make
  # their identity explicit like `-o path/to/output_dir` or `--library-type fr-unstranded`

  # For tophat, these values are 
  #     [1] the bowtie index name
  #     [2] the fastq files containing the left_reads
  #     [3] the fastq files containing the right_reads

  # They will be different for cufflinks, cuffmerge, cuffdiff so consult the
  # respective help text or manuals, but you should be fine if you just use what
  # I have set up in this file already.
  
  tophat_options:
    o: from_conditions
    library-type: fr-unstranded
    p: 6
    r: 125
    mate-std-dev: 25
    G: from_conditions
    no-coverage-search: True
    positional_args:
      bowtie2_index: from_conditions
      left_reads: from_conditions
      right_reads: from_conditions
	
  cufflinks_options:
    o: from_conditions
    p: 7
    GTF-guide: from_conditions
    3-overhang-tolerance: 5000
    frag-bias-correct: from_conditions # if not False; path to genome fasta
    multi-read-correct: True
    upper-quartile-norm: True
    positional_args:
      accepted_hits: from_conditions

  cuffmerge_options:
    o: from_conditions # output directory
    ref-gtf: from_conditions
    p: 6
    ref-sequence: from_conditions
    positional_args:
      assembly_list: from_conditions # file with path to cufflinks gtf files to be merged

  cuffdiff_options:
    o: from_conditions
    labels: from_conditions
    p: 6
    time-series: True
    upper-quartile-norm: True
    frag-bias-correct: from_conditions
    multi-read-correct: True
    positional_args:
      transcripts_gtf: from_conditions
      sample_bams: from_conditions


  # `condition_queue`:
  # ------------------
  # This is a list of info related to each sample/condition contained in your RNA-sequence
  # experiment(s)

  # `name`: the name of this condition and suffix of the `output_dir` for each 
  #         program.  Usually something like a time-point ID or treatment type.
  #         Should be as short as possible while still being a useful label. 

  # `group_id`: this is how you group different experiments to be included in a
  #             single cuffmerge/cuffdiff program call.  All conditions in a time
  #             series should share the same `group_id` and be placed in
  #             `condition_queue` in the order that you want them to be sent to
  #             cuffdiff.

  # `left_reads`: a list of the paths to fastq files containing left reads for
  #               each condition. 

  # `right_reads`: list of fastqs containing the right mates for the fastqs in
  #                `left_reads`.
  #                 **NOTE** right mate file must be in same order as provided to `left_reads`

  condition_queue:
    -
      name: exp1_control
      group_id: 0
      left_reads:
	- /path/to/exp1_control/techRep1.left_reads.fastq
	- /path/to/exp1_control/techRep2.left_reads.fastq
      right_reads:
	- /path/to/exp1_control/techRep1.right_reads.fastq
	- /path/to/exp1_control/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: exp1_treatment
      group_id: 0
      left_reads:
	- /path/to/exp1_treatment/techRep1.left_reads.fastq
	- /path/to/exp1_treatment/techRep2.left_reads.fastq
      right_reads:
	- /path/to/exp1_treatment/techRep1.right_reads.fastq
	- /path/to/exp1_treatment/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: exp2_control
      group_id: 1
      left_reads:
	- /path/to/exp2_control/techRep1.left_reads.fastq
	- /path/to/exp2_control/techRep2.left_reads.fastq
      right_reads:
	- /path/to/exp2_control/techRep1.right_reads.fastq
	- /path/to/exp2_control/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: exp2_treatment
      group_id: 1
      left_reads:
	- /path/to/exp2_treatment/techRep1.left_reads.fastq
	- /path/to/exp2_treatment/techRep2.left_reads.fastq
      right_reads:
	- /path/to/exp2_treatment/techRep1.right_reads.fastq
	- /path/to/exp2_treatment/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename
    

  ...


Using e-mail notifications
--------------------------
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.

Using different modes
---------------------
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.

Tutorial
===============

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.