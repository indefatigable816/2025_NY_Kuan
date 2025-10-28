# Boltz x Minerva user guide
> Please replace **cheny69** **boltz0929** with yours

## Before running
>- get added into a Project to line up for gpu (BSUB -P <project_name>)

### useful switch between home and work

    cd ../../../../hpc/users/cheny69
    cd ../../../sc/arion/work/cheny69/

### Under hpc/users/cheny69

#### set up configuration for venv

    touch ~/.condarc
    nano .condarc

#### paste the lines below so that venv is build in sc/arion/work

    envs_dirs: 
    - /sc/arion/work/cheny69/boltz0929/envs 
    pkgs_dirs: 
    - /sc/arion/work/cheny69/boltz0929/pkgs

### Under sc/arion/work/cheny69

#### set up venv 

    conda create -n boltz0929 python=3.12
    conda activate boltz0929

#### to check your environment location

    conda env list

#### prepare dependencies

    conda activate boltz0929
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

### GIT

    ssh cheny69@minerva.hpc.mssm.edu
    scp -r project/boltz/ cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/boltz/
    conda env list
    scp -r cheny69@minerva.hpc.mssm.edu:/sc/arion/work/cheny69/results/ .
    out.200463721.0
    err.200463728.1
    # build venv for running boltz
    conda create -n boltz929 python=3.12
    conda activate boltz929
    pip install "torch>=2.2" "numpy>=1.26,<2.0" "hydra-core==1.3.2" "pytorch-lightning==2.5.0" "rdkit>=2024.3.2" "dm-tree==0.1.8" "requests==2.32.3" "pandas>=2.2.2" "types-requests" "einops==0.8.0" "einx==0.3.0" "fairscale==0.4.13" "mashumaro==3.14" "modelcif==1.2" "wandb==0.18.7" "click==8.1.7" "pyyaml==6.0.2" "biopython==1.84" "scipy==1.13.1" "numba==0.61.0" "gemmi==0.6.5" "scikit-learn==1.6.1" "chembl_structure_pipeline==1.2.2"
    pip install boltz[cuda] -U
    # go to work
    cd ../../../sc/arion/work/cheny69/
    # git commands
    git init
    git add .
    git config --global user.email "ind.."
    git config --global user.name "inde..."
    git commit -m "first commit"
    git branch -M main
    git push -u origin main
    git pull origin main
    # resolve any conflicts
    git push origin main

