from user_options import user

qsub_fname = "benchcable_spatial.sh"
ncpus = 16
mem = "15GB"
wall_time = "1:30:00"
email_address = f"{user}@nci.org.au"

#
## MPI stuff
#
mpi = True
num_cores = ncpus  # set to a number, if None it will use all cores...!
multiprocess = False
