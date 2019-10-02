# Setup-your-aiida

This is a guideline for setting up aiida on your supercomputer Grace/Thomas
-----------

----
**1. Check prerequisites from the website below**

   https://aiida-core.readthedocs.io/en/latest/install/prerequisites.html


----
**2. Install aiida on your computer, I recommend you use python3 because it's possible many plugins in aiida need python3 environment.**
 
   https://aiida-core.readthedocs.io/en/latest/install/installation.html


----
**3. Activate aiida** 
        
       $ source ~/.virtualenvs/aiida/bin/activate


----
**4. Install Plugins**

   Note: Chosing the right branch of plugin is crucial before installation. You can go to github to find which branch is the latest version.
   Instruction of installing aiida-vasp plugin
   
       $ (aiida) install aiida-vasp
   
       $ (aiida) reentry scan -r aiida
   

----
**5. Setup a computer**
   
   Be sure that you are able to connect to your cluster without typing your password.
   
   
       $(aiida) verdi computer setup
   
   
   This is my example on Grace (* parts are different on Thomas)
   
   > Computer label: "Grace" (* Thomas)
   
   > Hostname: "grace.rc.ucl.ac.uk"  ( * thomas.rc.ucl.ac.uk )
   
   Description: Grace computer for aiida tests (*)
   
   Transport plugin: ssh
   
   Scheduler plugin: sge   
   
   Shebang line: #!/bin/bash -l
   
   Work directory on the computer: /home/*****/Scratch/scratch/{username}/aiida_run (* /scratch/scratch/{username}/aiida_run)
   
   Mpirun_command: gerun
   
   prepend_text: 
   #$ -S /bin/bash 
   (* #$ -S /bin/bash
      
      #$ -P ***
      
      #$ -A ***)
   
    $(aiida) verdi computer configure ssh Grace (Thomas)
   
   User name: ucapy** (*)
   
   port Nr: 22
   
   Look_for_keys: True
   
   SSH key file: you can leave it empty to use the default SSH key
   
   Connection timeout: 30
   
   Allow_ssh agent: False
   
   SSH proxy_command: empty
   
   Compress file transfer: True
   
   GSS auth: False
    
   GSS kex: False
   
   GSS deleg_creds: False
   
   GSS host: grace.rc.ucl.ac.uk
   
   Load system host keys: True
   
   key policy: AutoAddPolicy
   
   Connection cooldown time(s): 5.0
 

----
**6.Test connection to your supercomputer**
    
    $ (aiida) verdi computer test Grace (* Thomas) 
 

----
**7. Set up code**
     
   Label: vasp  (quantumespresso)
    
   Description: vasp code for the aiida tests
    
   Default calculation input plugin: vasp.vasp (quantumespresso.pw)
    
   Installed on target computer: True
    
   Computer: Grace (Other computer you have set in aiida)
    
   Remote absolute path: /shared/ucl/apps/vasp/5.4.4-18apr2017/intel-2017/bin/vasp_std 
    (/shared/ucl/apps/quantum-expresso/6.1/intel-2017/bin/pw.x)
    
   Prepend text:
    
   module load vasp/5.4.4-18apr2017/intel-2017-update
   
   (module load xorg-utils/X11R7.7
     
   module load quantum-espresso/6.1-impi/intel2017)
   
    
    
    
    
   
   
 
