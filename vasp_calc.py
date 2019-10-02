"""This is an example of calculation for VASP"""
from aiida_vasp.utils.aiida_utils import get_data_class, get_data_node
from aiida.engine import submit


code = Code.get_from_string("vasp@Grace")   # Code you set for this calculation
builder = code.get_builder()

#Give a description of your job
builder.metadata.label = "simple VASP run"             
builder.metadata.description = "Example - simple VASP run"
builder.metadata.options.withmpi = True              # Add gerun in your _aiidasubmit.sh

#Select structure or create structure
structure = load_node(2968)                         # The structure in the database you want to use
builder.structure = structure

#Define calculation
param_cls = get_data_class('dict')
builder.parameters = param_cls(dict={
# ! Startparemeter 
  'SYSTEM':'Si',
  'ISYM' :2,                      # 0-nonsym 1-usesym 2-fastsym
  'ISTART':0,                     # 0-nwe job, 1-restart
  'ICHARG':2,                     # charge: 1-file 2-atom 10-const
  'INIWAV':1,                     # electro: 0-lowe 1-rand 

# ! ELectronic Relaxation  
  'ISPIN':1,                      # spin polarisation 1-no 2-yes
  'PREC':'Accurate',              # Low/Medium/High/Normal/Single/Accurate
  'ENCUT':200,                    # Energy cutoff                              
  'GGA':'MK',                     # Functional
  'PARAM1':0.1234,
  'PARAM2':1.0000,
  'LUSE_VDW':'.TRUE.',
  'AGGAC':0.0000,
  'LASPH':'.TRUE.',
 #'VOSKOMN':1,                    # Vosko Wilk Nusair interpolation
  'ALGO':'FAST',                  # IALGO = 48 (Davidson: 38)+ RMM-DISS algorithm for electrons
  'NELM':300,                     # Max iteration in SC loop
  'NELMIN': 3,                    # Min iteration in SC loop
  'EDIFF':1.0E-6,                 # [Global break cond. for the electrons. SC-loop] Energy
  'LREAL': 'Auto',                # F-small molecule A-normal system

# ! Ioinic Relaxation
  'ISIF':2,                       # Stress tensor, 0-not, 2-ralax only positions, 3-relax cell shape+positions
  'EDIFFG':-0.02,                 # Convergence criterion for foreces (-0.03 for TS)
  'NSW': 600,                     # Max steps
  'IBRION':2,                     # 0-MD 1-Brodyn(opt,TS) 2-CG(opt) 3-damped MD(opt) 5-frequency calculation 44-dimer
  'POTIM':0.4,                    # Ion step size/time step(fs) for MD fc-0.01

# ! MD run
 #'TEIN':20.0,                    # Initial temperature
 #'TEBEG':20.0,                   # TEEND = 0.0 temperature during run
 #'SMASS':-3.00,                  # Nose mass parameter (am)
 #'RWIGS':-1.00,                  # Atomic Wigner radii

# ! DOS related values
  'ISMEAR': -5,                   # -5-accurate total energy and DOS 0-large cell 1-metal
  'SIGMA':0.10,                   
 #'EMIN':10,
 #'EMAX':-10,                     # Atomic Wigner-Seitz radii

# ! Dimer method
 #'MAXMIX':60,                    

# ! Frequency Calculation
 #'NFREE':2,

# ! Write
  'NWRITE':2,                     # How much will be written out
 #'LCHARG': '.True.',             # Write restart charge file
 #'LWAVE':'.True.',               # Write restart wf file
 #'LVHAR':'.False.',              # Write LOCPOT, Hartree potential only
 #'LVTOT':'.False.',              # Write LOCPOT, total locl potential
  'NPAR':4,                       # Adjust to number of processors best on berni up to 8 CPUs Close it when doing fc
 #'LPLANE':'.True.'
 #'LORBIT':11,                    # Write magnetic moment for each atom
})

#Select pseudopotentials
builder.potential = DataFactory('vasp.potcar').get_potcars_from_structure(
        structure=builder.structure, family_name='PBE', mapping={'Si': 'Si','Ag':'Ag'}) #It corrects its order automatically according to your POSCAR

# Add vde_kernel.bindat to input folder
builder.metadata.options.prepend_text = 'cp /home/ucapyba/vdw_kernel.bindat vdw_kernel.bindat'

#Define K-point mesh in reciprocal space
kpoints = get_data_class('array.kpoints')()
kpoints.set_cell_from_structure(structure)
kpoints.set_kpoints_mesh([4,4,4])     
builder.kpoints = kpoints

#Set resources
builder.metadata.options.resources = {'parallel_env':'mpi', 'tot_num_mpiprocs':64}   #tot_num_mpiprocs is the number of cores you set for this calculation

#Set time
builder.metadata.options.max_wallclock_seconds = 30*60  #here is 30 mins

#If you want to check your input files before submitting the job(Inputs can be found in submit_test in the current working directory, but you don't submit to your remote computer)
#builder.metadata.dry_run =True

#Submit the job
calcjob = submit(builder)
print('Submitted Caljob with PK='+str(calcjob.pk))
