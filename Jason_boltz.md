(base) [cheny69@li04e02 ~]$ touch ~/.condarc
(base) [cheny69@li04e02 ~]$ nano .condarc

# paste the lines below
envs_dirs: 
- /sc/arion/work/cheny69/(test-env)/envs 
pkgs_dirs: 
- /sc/arion/work/cheny69/(test-env)/pkgs

(base) [cheny69@li04e02 ~]$ conda create -n (test-env) python=3.12

# to check your environment location
(base) [cheny69@li04e02 ~]$ conda env list
(base) [cheny69@li04e02 ~]$ cd ../../../sc/arion/work/cheny69/
(base) [cheny69@li04e02 cheny69]$ conda activate (test-env)
((test-env)) [cheny69@li04e02 cheny69]$ pip install "torch>=2.2" "numpy>=1.26,<2.0" "hydra-core==1.3.2" "pytorch-lightning==2.5.0" "rdkit>=2024.3.2" "dm-tree==0.1.8" "requests==2.32.3" "pandas>=2.2.2" "types-requests" "einops==0.8.0" "einx==0.3.0" "fairscale==0.4.13" "mashumaro==3.14" "modelcif==1.2" "wandb==0.18.7" "click==8.1.7" "pyyaml==6.0.2" "biopython==1.84" "scipy==1.13.1" "numba==0.61.0" "gemmi==0.6.5" "scikit-learn==1.6.1" "chembl_structure_pipeline==1.2.2"
((test-env)) [cheny69@li04e02 cheny69]$ pip install boltz[cuda] -U
((test-env)) [cheny69@li04e02 cheny69]$ conda deactivate


(base) [cheny69@li04e02 cheny69]$ conda deactivate
cd ../../../../hpc/users/cheny69

