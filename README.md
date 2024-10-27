```bash
docker exec -it mpi-master bash
```

```bash
mpirun -np 5 --allow-run-as-root --hostfile /root/hosts python3 /root/work/main.py
```