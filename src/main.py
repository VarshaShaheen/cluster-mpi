from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define matrix size
N = 4

# Master process initializes matrices
if rank == 0:
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)
else:
    A = None
    B = None

# Broadcast matrices to all processes
A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

# Determine rows for each process
rows_per_process = N // size
start_row = rank * rows_per_process
end_row = start_row + rows_per_process if rank != size - 1 else N

# Each process computes its part of the result
partial_C = np.dot(A[start_row:end_row, :], B)

# Gather partial results
gathered_C = comm.gather(partial_C, root=0)

# Master process assembles the final result
if rank == 0:
    C = np.vstack(gathered_C)
    print("Resultant Matrix C:")
    print(C)
