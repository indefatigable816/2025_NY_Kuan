# Boltz x Minerva user guide
> Please replace **(your_username)** **(test-env)** with yours

## Before running
>- get added into a Project to line up for gpu (BSUB -P <project_name>)

### useful switch between home and work

    cd ../../../../hpc/users/(your_username)
    cd ../../../sc/arion/work/(your_username)/

### Under hpc/users/(your_username)

#### set up configuration for venv

    touch ~/.condarc
    nano .condarc

#### paste the lines below so that venv is build in sc/arion/work

    envs_dirs: 
    - /sc/arion/work/(your_username)/(test-env)/envs 
    pkgs_dirs: 
    - /sc/arion/work/(your_username)/(test-env)/pkgs

### Under sc/arion/work/(your_username)

#### set up venv 

    conda create -n (test-env) python=3.12
    conda activate (test-env)

#### to check your environment location

    conda env list

#### prepare dependencies

    conda activate (test-env)
    pip install "torch>=2.2" "numpy>=1.26,<2.0" "hydra-core==1.3.2" "pytorch-lightning==2.5.0" "rdkit>=2024.3.2" "dm-tree==0.1.8" "requests==2.32.3" "pandas>=2.2.2" "types-requests" "einops==0.8.0" "einx==0.3.0" "fairscale==0.4.13" "mashumaro==3.14" "modelcif==1.2" "wandb==0.18.7" "click==8.1.7" "pyyaml==6.0.2" "biopython==1.84" "scipy==1.13.1" "numba==0.61.0" "gemmi==0.6.5" "scikit-learn==1.6.1" "chembl_structure_pipeline==1.2.2" "boltz[cuda]" -U "lightning[extra]==2.5.0.post0"

## While running

> Prepare a .yaml file with sequences and a .lsf file with configuration and commands. Examples are provided below.

### Example .lsf file

    #!/bin/bash
    #BSUB -P acc_DiseaseGeneCell
    #BSUB -J HER2
    #BSUB -q gpu
    #BSUB -R rusage[mem=30000]
    #BSUB -R span[hosts=1]
    #BSUB -gpu num=1
    #BSUB -n 1
    #BSUB -W 24:00
    #BSUB -L /bin/bash
    #BSUB -o out.%J.%I
    #BSUB -e err.%J.%I
    WKDIR="/sc/arion/work/cheny69"
    SEED=1
    module purge
    module load anaconda3/2024.06
    source ~/.bashrc
    conda activate boltz0929
    ml proxies/1
    boltz predict $WKDIR/prot.yaml --out_dir $WKDIR/result/$SEED/ --use_msa_server --cache $WKDIR/mol/ --seed $SEED 

### Example .yaml file

    version: 1  # Optional, defaults to 1
    sequences:
    - protein:
        id: WT
        sequence: TQVCTGTDMKLRLPASPETHLDMLRHLYQGCQVVQGNLELTYLPTNASLSFLQDIQEVQGYVLIAHNQVRQVPLQRLRIVRGTQLFEDNYALAVLDNGDPLNNTTPVTGASPGGLRELQLRSLTEILKGGVLIQRNPQLCYQDTILWKDIFHKNNQLALTLIDTNRSRACHPCSPMCKGSRCWGESSEDCQSLTRTVCAGGCARCKGPLPTDCCHEQCAAGCTGPKHSDCLACLHFNHSGICELHCPALVTYNTDTFESMPNPEGRYTFGASCVTACPYNYLSTDVGSCTLVCPLHNQEVTAEDGTQRCEKCSKPCARVCYGLGMEHLREVRAVTSANIQEFAGCKKIFGSLAFLPESFDGDPASNTAPLQPEQLQVFETLEEITGYLYISAWPDSLPDLSVFQNLQVIRGRILHNGAYSLTLQGLGISWLGLRSLRELGSGLALIHHNTHLCFVHTVPWDQLFRNPHQALLHTANRPEDECVGEGLACHQLCARGHCWGPGPTQCVNCSQFLRGQECVEECRVLQGLPREYVNARHCLPCHPECQPQNGSVTCFGPEADQCVACAHYKDPPFCVARCPSGVKPDLSYMPIWKFPDEEGACQPCPINCTHSCVDLDDKGCPAEQRASPLTS


> refer to [Boltz github](https://github.com/jwohlwend/boltz) (especially the [prediction.md](https://github.com/jwohlwend/boltz/blob/cb04aeccdd480fd4db707f0bbafde538397fa2ac/docs/prediction.md#L4)) and [LSF_HowToWrite](https://labs.icahn.mssm.edu/minervalab/documentation/lsf-job-scheduler/). Also refer to [GPU_instruction](https://labs.icahn.mssm.edu/minervalab/documentation/gpgpu/) and [Conda_instruction](https://labs.icahn.mssm.edu/minervalab/documentation/conda/) for minerva.

## More

### Example file for batch mode

    #!/bin/bash
    #BSUB -P acc_DiseaseGeneCell
    #BSUB -J HER2[1-10]          # run 10 array jobs, index = 1..10
    #BSUB -q gpu
    #BSUB -R rusage[mem=20000]
    #BSUB -R span[hosts=1]
    #BSUB -gpu num=1
    #BSUB -n 1
    #BSUB -W 24:00
    #BSUB -L /bin/bash
    #BSUB -o out.%J.%I
    #BSUB -e err.%J.%I

    # Use LSB_JOBINDEX as seed (1–10)
    SEED=$LSB_JOBINDEX
    WKDIR="/sc/arion/work/cheny69"

    module purge
    module load anaconda3/2024.06
    source ~/.bashrc
    conda activate boltz0929
    ml proxies/1

    boltz predict $WKDIR/prot.yaml \
        --out_dir $WKDIR/results/$SEED/ \
        --use_msa_server \
        --cache $WKDIR/mol/ \
        --seed $SEED 
