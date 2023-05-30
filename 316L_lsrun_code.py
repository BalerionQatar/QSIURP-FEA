import subprocess
from lasso.dyna import D3plot, ArrayType

kfilepath = "lsrun -submit 'C:\\Users\\Mohammad Annan\\Desktop\\test3.k'"
#subprocess.call(f'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe {kfilepath}"', shell = True)
d3plot = D3plot("d3plot", state_array_filter=[ArrayType.node_displacement])
d3plot.plot()
print(d3plot.header.n_shells)


