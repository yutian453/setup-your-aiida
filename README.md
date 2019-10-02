# setup-your-aiida-

This is a guideline for setting up aiida on your supercomputer Grace/Thomas
-----------

1. Check prerequisites from the website below

   https://aiida-core.readthedocs.io/en/latest/install/prerequisites.html

2. Install aiida on your computer, I recommend you use python3 because it's possible many plugins in aiida need python3 environment.
 
   https://aiida-core.readthedocs.io/en/latest/install/installation.html

3. Activate aiida 
   $ source ~/.virtualenvs/aiida/bin/activate
4. Install Plugins

   Note: Chosing the right branch of plugin is crucial before installation. You can go to github to find which branch is the latest version.
   Instruction of installing aiida-vasp plugin
   
   $ pip install aiida-vasp
   $ reentry scan -r aiida
   
5. Setup a computer
   $ verdi computer setup
   ---
   This is my example on Grace (* parts are different on Thomas)
   Computer label: "Grace" (* Thomas)
   Hostname: "grace.rc.ucl.ac.uk"  ( * thomas.rc.ucl.ac.uk )
   Description: Grace computer for aiida tests (*)
   Transport plugin: ssh
   Scheduler plugin: sge   
   Shebang line: #!/bin/bash -l
   Work directory on the computer: /home/ucapyba/Scratch/scratch/{username}/aiida_run (* /scratch/scratch/{username}/aiida_run)
   Mpirun_command: gerun
   prepend_text: 
   #$ -S /bin/bash 
   (* #$ -S /bin/bash
      #$ -P Gold
      #$ -A ***)
   
   mpiprocs_per_machine: "2"
   prepend_text: |
   module load mymodule
   export NEWVAR=1
