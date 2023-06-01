import subprocess
from lasso.dyna import D3plot, ArrayType

def run():
    kfilepath = "lsrun -submit 'C:\\Users\\Mohammad Annan\\Desktop\\test_final.k'"
    #subprocess.call(f'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe {kfilepath}"', shell = True)

    d3plot = D3plot("d3plot")
    pstrain = d3plot.arrays[ArrayType.element_shell_bending_moment]
    pstrain = pstrain.mean(axis = 2)
    d3plot.plot(3, field = pstrain[3], fringe_limits= (0, 0.6))
    # plotting loads this link: file:///C:/Users/MOHAMM~1/AppData/Local/Temp/lasso/tmpze4reeb2.html. it's a gui of the element shell bending moment

