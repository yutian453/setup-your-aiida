"""I will remove the asterisk after testing """



"""Run a workflow from low kpoints to high kpoints"""
from time import sleep
import numpy as np
from aiida.manage.configuration import load_profile
from aiida.orm import (Bool, Int, Float, Str, Code, load_group, QueryBuilder, Group, WorkChainNode)
from aiida.plugins import DataFactory, WorkflowFactory
from aiida.engine import submit
from aiida_vasp.utils.aiida_utils import get_data_class, get_data_node
load_profile()


def get_structure():
    structure = load_node(2968)
    return structure

@calcfunction
def launch_aiida_low_kpoints(structure, code_string, resources, label):
    Dict = DataFactory('dict')
    KpointsData = DataFactory("array.kpoints")
    base_incar_dict = {
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
}

    base_config = {'code_string': code_string,
                   'potential_family': 'PBE',
                   'potential_mapping': {'Si': 'Si', },
                   'options': {'resources': resources,
                               'account': 'ucapyba',
                               'max_wallclock_seconds': 3600 * 10}}
    base_parser_settings = {'add_energies': True,
                            'add_forces': True,
                            'add_stress': True}
    code = Code.get_from_string(base_config['code_string'])
    Workflow = WorkflowFactory('vasp.relax')
    builder = Workflow.get_builder()
    builder.code = code
    builder.parameters = Dict(dict=base_incar_dict)
    builder.structure = structure
    builder.settings = Dict(dict={'parser_settings': base_parser_settings})
    builder.potential_family = Str(base_config['potential_family'])
    builder.potential_mapping = Dict(dict=base_config['potential_mapping'])
    kpoints = KpointsData()
    kpoints.set_kpoints_mesh([4, 4, 1])
    builder.kpoints = kpoints
    builder.options = Dict(dict=base_config['options'])
    builder.metadata.label = label
    builder.metadata.description = label
    builder.clean_workdir = Bool(False)
    builder.relax = Bool(True)
    builder.force_cutoff = Float(1e-5)
    builder.steps = Int(10)
    builder.positions = Bool(True)
    builder.shape = Bool(True)
    builder.volume = Bool(True)
    builder.convergence_on = Bool(True)
    builder.convergence_volume = Float(1e-5)
    builder.convergence_max_iterations = Int(2)
    builder.verbose = Bool(True)

    node = submit(builder)
    return node

@calcfunction
def launch_aiida_medium_kpoints(structure, code_string, resources, label):
    Dict = DataFactory('dict')
    KpointsData = DataFactory("array.kpoints")
    base_incar_dict = {
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
}

   base_config = {'code_string': code_string,
                   'potential_family': 'PBE',
                   'potential_mapping': {'Si': 'Si',},
                   'options': {'resources': resources,
                               'account': 'ucapyba',
                               'max_wallclock_seconds': 3600 * 10}}
    base_parser_settings = {'add_energies': True,
                            'add_forces': True,
                            'add_stress': True}
    code = Code.get_from_string(base_config['code_string'])
    Workflow = WorkflowFactory('vasp.relax')
    builder = Workflow.get_builder()
    builder.code = code
    builder.parameters = Dict(dict=base_incar_dict)
    builder.structure = structure
    builder.settings = Dict(dict={'parser_settings': base_parser_settings})
    builder.potential_family = Str(base_config['potential_family'])
    builder.potential_mapping = Dict(dict=base_config['potential_mapping'])
    kpoints = KpointsData()
    kpoints.set_kpoints_mesh([7, 7, 1])
    builder.kpoints = kpoints
    builder.options = Dict(dict=base_config['options'])
    builder.metadata.label = label
    builder.metadata.description = label
    builder.clean_workdir = Bool(False)
    builder.relax = Bool(True)
    builder.force_cutoff = Float(1e-5)
    builder.steps = Int(10)
    builder.positions = Bool(True)
    builder.shape = Bool(True)
    builder.volume = Bool(True)
    builder.convergence_on = Bool(True)
    builder.convergence_volume = Float(1e-5)
    builder.convergence_max_iterations = Int(2)
    builder.verbose = Bool(True)

    node = submit(builder)
    return node

@calcfunction
def launch_aiida_high_kpoints(structure, code_string, resources, label):
    Dict = DataFactory('dict')
    KpointsData = DataFactory("array.kpoints")
    base_incar_dict = {
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
}

   base_config = {'code_string': code_string,
                   'potential_family': 'PBE',
                   'potential_mapping': {'Si': 'Si',},
                   'options': {'resources': resources,
                               'account': 'ucapyba',
                               'max_wallclock_seconds': 3600 * 10}}
    base_parser_settings = {'add_energies': True,
                            'add_forces': True,
                            'add_stress': True}
    code = Code.get_from_string(base_config['code_string'])
    Workflow = WorkflowFactory('vasp.relax')
    builder = Workflow.get_builder()
    builder.code = code
    builder.parameters = Dict(dict=base_incar_dict)
    builder.structure = structure
    builder.settings = Dict(dict={'parser_settings': base_parser_settings})
    builder.potential_family = Str(base_config['potential_family'])
    builder.potential_mapping = Dict(dict=base_config['potential_mapping'])
    kpoints = KpointsData()
    kpoints.set_kpoints_mesh([13, 13, 1])
    builder.kpoints = kpoints
    builder.options = Dict(dict=base_config['options'])
    builder.metadata.label = label
    builder.metadata.description = label
    builder.clean_workdir = Bool(False)
    builder.relax = Bool(True)
    builder.force_cutoff = Float(1e-5)
    builder.steps = Int(10)
    builder.positions = Bool(True)
    builder.shape = Bool(True)
    builder.volume = Bool(True)
    builder.convergence_on = Bool(True)
    builder.convergence_volume = Float(1e-5)
    builder.convergence_max_iterations = Int(2)
    builder.verbose = Bool(True)

    node = submit(builder)
 
@workfunction
 def main(code_string, resources, group_name, sleep_seconds=60):
    group = load_group(group_name)
    structure = get_structure()
    node_low_kpoints = launch_aiida_low_kpoints(structure, code_string, resources,
                                         "Si VASP calc on kpoints(441)")
    group.add_nodes(node_low_kpoints)

    while True:
        if node_low_kpoints.is_terminated:
            break
        print("Waiting for relaxation calculation to be done.")
        sleep(sleep_seconds)

    if node_low_kpoints.is_finished_ok:
            structure = node_relax.outputs.structure_relaxed.clone()
            node = launch_aiida_medium_kpoints(
                structure, code_string, resources,
                "Si VASP calc on kpoints(771)")
            group.add_nodes(node)
            print(node)
    else:
        print("Relaxation calculation on kpoints(771) failed.")

    
    while True:
        if node_medium_kpoints.is_terminated:
            break
        print("Waiting for relaxation on kpoints(771) calculation to be done.")
        sleep(sleep_seconds)

    if node_medium_kpoints.is_finished_ok:
            structure = node_relax.outputs.structure_relaxed.clone()
            node = launch_aiida_high_kpoints(
                structure, code_string, resources,
                "Si VASP calc on kpoints(13131)")
            group.add_nodes(node)
            print(node)
    else:
        print("Relaxation calculation failed.")



if __name__ == '__main__':
    # code_string is chosen among the list given by 'verdi code list'
    code_string = 'vasp@Grace'

    resources = {'parallel_env':'mpi', 'tot_num_mpiprocs':64}

    # Here it assumes existance of the group "Bulk_modulus_SiC_test",
    # made by 'verdi group create "Bulk_modulus_SiC_test"'.
    group_name  = "Kpoints convergence"
    main(code_string, resources, group_name)
    # calc_bulk_modulus(group_name)
