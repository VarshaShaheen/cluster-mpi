from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define matrix size
N = 1000

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
remainder = N % size

# Calculate start and end indices for each process
if rank < remainder:
    start_row = rank * (rows_per_process + 1)
    end_row = start_row + rows_per_process + 1
else:
    start_row = rank * rows_per_process + remainder
    end_row = start_row + rows_per_process

# Each process computes its part of the result
partial_C = np.dot(A[start_row:end_row, :], B)

# Print load balancing information
print(f"Process {rank}: Computing rows {start_row} to {end_row - 1} (Total rows: {end_row - start_row})")

# Gather partial results
gathered_C = comm.gather(partial_C, root=0)

# Master process assembles the final result
if rank == 0:
    # Sort the gathered results based on the ranks (optional, but good practice)
    gathered_C = [gathered_C[i] for i in range(size)]
    C = np.vstack(gathered_C)
    print("\nResultant Matrix C:")
    print(C)
