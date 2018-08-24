#BSUB -J conda_create_env
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -W 01:00
#BSUB -q general
#BSUB -n 1
#
conda env create -f py_intro_lb_env_file.yml
