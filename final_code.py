import subprocess
import os
import numpy as np
from stl import mesh
import numpy as np
from stl import mesh
import subprocess


def read_stl(stl_file):
    stl_mesh = mesh.Mesh.from_file(stl_file)

    nodes = []
    elements = []
    node_id = 1
    element_id = 1
    node_dict = {}

    for i, facet in enumerate(stl_mesh.vectors):
        node_ids = []
        for vertex in facet:
            node_key = tuple(vertex)
            if node_key not in node_dict:
                node_dict[node_key] = node_id
                nodes.append(vertex)
                node_ids.append(node_id)
                node_id += 1
            else:
                node_ids.append(node_dict[node_key])

        elements.append(node_ids)
        element_id += 1

    return np.array(nodes), np.array(elements)


# template = {"*KEYWORD":[], "*TITLE":[],"*CONTROL_ACCURACY":[], "*CONTROL_HOURGLASS":[]}
template = []


def write_k(stl_file):
    # Open the input file and output file
    with open(stl_file, 'r') as stl_file:
        # Read each line from the input file
        for line in stl_file:
            # Write the line to the output file
            if line == "*ELEMENT_SHELL":
                break
            template.append(line)


k_file = 'bumper.k'
text_file = 'cube_v2.k'
# subprocess.run(['code', text_file])
stl_file = 'cube.stl'
stl_mesh = mesh.Mesh.from_file(stl_file)

# Load the STL files mesh
storage_nodes = []
for triangle in stl_mesh.points:
    for vertex in [triangle[:3], triangle[3:6], triangle[6:9]]:
        vertex_tuple = tuple(vertex)
        if vertex_tuple not in storage_nodes:
            storage_nodes.append(vertex_tuple)


# Cleans up the vertices first
def clean_up(input):
    possibility_one = str(input).split()

    if ']' in possibility_one:
        possibility_one.remove(']')
    if '[' in possibility_one:
        possibility_one.remove('[')
    if '[' in possibility_one[0]:
        possibility_one[0] = possibility_one[0].split('[')[1]

    return possibility_one


storage_elements = []
for i in stl_mesh.vectors:
    storage_elements.append(clean_up(i[0]))
    storage_elements.append(clean_up(i[1]))
    storage_elements.append(clean_up(i[2]))


content = """$# LS-DYNA Keyword file created by LS-PrePost(R) V4.5.0 (Beta) - 01Sep2017
$# Created on May-27-2023 (01:16:36)
*KEYWORD
*TITLE
$  Author Mohammad Annan
$  Units  mm, ms, kg => GPa
$
$  Description
$  Novel converter from .stl to .k
$#                                                                         title
Explicit bumper test
*CONTROL_ACCURACY
$#     osu       inn    pidosu      iacc    
         0         2         0         0
*CONTROL_HOURGLASS
$#     ihq        qh  
         5      0.03
*CONTROL_SHELL
$#  wrpang     esort     irnxx    istupd    theory       bwc     miter      proj
      20.0         2        -1         0         2         2         2         0
$# rotascl    intgrd    lamsht    cstyp6    tshell      
       1.0         0         0         1         0
$# psstupd   sidt4tu     cntco    itsflg    irquad    w-mode   stretch      icrq
         0         0         0         0         2       0.0       0.0         0
$#  nfail1    nfail4   psnfail    keepcs     delfr   drcpsid    drcprm   intperr
         0         0         0         0         0         0       1.0         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
      20.0         0       0.0       0.0       0.0         0
*DATABASE_BNDOUT
$#      dt    binary      lcur     ioopt     
      0.01         0         0         1
*DATABASE_RBDOUT
$#      dt    binary      lcur     ioopt     
      0.01         0         0         1
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       1.0         0         0         0         0
$#   ioopt     
         0
*MAT_PIECEWISE_LINEAR_PLASTICITY
$#     mid        ro         e        pr      sigy      etan      fail      tdel
         17.80000E-6     210.0       0.3      0.28      0.031.00000E21       0.0
$#       c         p      lcss      lcsr        vp  
       0.0       0.0         0         0       0.0
$#    eps1      eps2      eps3      eps4      eps5      eps6      eps7      eps8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$#     es1       es2       es3       es4       es5       es6       es7       es8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
*MAT_PIECEWISE_LINEAR_PLASTICITY
$#     mid        ro         e        pr      sigy      etan      fail      tdel
         27.80000E-6     210.0       0.3      0.28      0.031.00000E21       0.0
$#       c         p      lcss      lcsr        vp  
       0.0       0.0         0         0       0.0
$#    eps1      eps2      eps3      eps4      eps5      eps6      eps7      eps8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$#     es1       es2       es3       es4       es5       es6       es7       es8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
*MAT_RIGID
$#     mid        ro         e        pr         n    couple         m     alias
         37.80000E-6     210.0       0.3       0.0       0.0       0.0          
$#     cmo      con1      con2    
       1.0         4         7
$#lco or a1        a2        a3        v1        v2        v3  
       0.0       0.0       0.0       0.0       0.0       0.0
*DEFINE_CURVE
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         1         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                10.0
              100.01                10.0\n"""

bottom_content = """*SECTION_SHELL
$#   secid    elform      shrf       nip     propt   qr/irid     icomp     setyp
         1         2  0.833333         5       1.0         0         0         1
$#      t1        t2        t3        t4      nloc     marea      idof    edgset
       1.0       1.0       1.0       1.0       0.0       0.0       0.0         0
*PART
$#                                                                         title
Bumper
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         3         0         0         0         0         0
*BOUNDARY_PRESCRIBED_MOTION_RIGID
$#     pid       dof       vad      lcid        sf       vid     death     birth
         1         3         0         1      -1.0         01.00000E28       0.0
*BOUNDARY_SPC_NODE
$#     nid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         1         1         1         1         1         1
*CONTACT_AUTOMATIC_NODES_TO_SURFACE
$#     cid                                                                 title
$#    ssid      msid     sstyp     mstyp    sboxid    mboxid       spr       mpr
         1         1         3         3         0         0         0         0
$#      fs        fd        dc        vc       vdc    penchk        bt        dt
       0.1       0.1       0.0       0.0       0.0         0       0.01.00000E20
$#     sfs       sfm       sst       mst      sfst      sfmt       fsf       vsf
       1.0       1.0       0.0       0.0       1.0       1.0       1.0       1.0
$#    soft    sofscl    lcidab    maxpar     sbopt     depth     bsort    frcfrq
         0       0.1         0     1.025       0.0         2         0         1
$#  penmax    thkopt    shlthk     snlog      isym     i2d3d    sldthk    sldstf
       0.0         0         0         1         0         0       0.0       0.0
*END"""


def remove_duplicates(nodes):
    unique_nodes = {}  # Create an empty dictionary

    for node in nodes:
        # The coordinates of the node are converted to a tuple and used as the key
        # The value is the node itself
        unique_nodes[tuple(node)] = node

    return list(unique_nodes.values())


unique_nodes = remove_duplicates(storage_elements)


def form_shells(unique_nodes):
    shells = []

    for i in range(0, len(unique_nodes), 8):
        if (i+8) <= len(unique_nodes):
            shell_1 = [i+1, i+2, i+3, i+4]
            shell_2 = [i+5, i+6, i+7, i+8]
            shell_3 = [i+1, i+2, i+5, i+6]
            shell_4 = [i+3, i+4, i+7, i+8]
            shell_5 = [i+1, i+4, i+5, i+8]
            shell_6 = [i+2, i+3, i+6, i+7]
            shells.append(shell_1)
            shells.append(shell_2)
            shells.append(shell_3)
            shells.append(shell_4)
            shells.append(shell_5)
            shells.append(shell_6)

    return shells


shells = form_shells(unique_nodes)


shell_elements = form_shells(unique_nodes)
# write_shells_to_file(shell_elements)
with open('test3.k', 'w') as f:
    f.write(content)
    f.write('*ELEMENT_SHELL\n')
    f.write('$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8\n')
    for i, shell in enumerate(shells, 1):
        n1, n2, n3, n4 = shell
        n5 = n6 = n7 = n8 = 0
        f.write(f'{i:8}{1:8}{n1:8}{n2:8}{n3:8}{n4:8}{n5:8}{n6:8}{n7:8}{n8:8}\n')

    f.write("""*NODE\n$#   nid               x               y               z      tc      rc  \n""")
    for i in range(len(unique_nodes)):
        if i+1 < 10:
            f.write("       {:<1}  {:>14.6f}  {:>14.6f}  {:>14.6f}       0       0\n".format(
                i+1,
                float(unique_nodes[i][0].replace(']', '')),
                float(unique_nodes[i][1].replace(']', '')),
                float(unique_nodes[i][2].replace(']', ''))))
        elif i+1 >= 10 and i+1 < 100:
            f.write("      {:<2}  {:>14.6f}  {:>14.6f}  {:>14.6f}       0       0\n".format(
                i+1,
                float(unique_nodes[i][0].replace(']', '')),
                float(unique_nodes[i][1].replace(']', '')),
                float(unique_nodes[i][2].replace(']', ''))))
        elif i+1 >= 100 and i + 1 < 1000:
            f.write("     {:<3}  {:>14.6f}  {:>14.6f}  {:>14.6f}       0       0\n".format(
                i+1,
                float(unique_nodes[i][0].replace(']', '')),
                float(unique_nodes[i][1].replace(']', '')),
                float(unique_nodes[i][2].replace(']', ''))))
        else:
            f.write("    {:<4}  {:>14.6f}  {:>14.6f}  {:>14.6f}       0       0\n".format(
                i+1,
                float(unique_nodes[i][0].replace(']', '')),
                float(unique_nodes[i][1].replace(']', '')),
                float(unique_nodes[i][2].replace(']', ''))))
        # if i+1 < 10:
        #     f.write("       {:<1}  {:>14.6f}  {:>14.6f}  {:>14.6f}       0       0\n".format(
        #         i+1, float(unique_nodes[i][0].replace(']', '')), float(unique_nodes[i][1].replace(']', '')), float(unique_nodes[i][2].replace(']', ''))))
        # if i+1 >= 10 and i+1 < 100:
        #     f.write("      {:<4}  {:>14.6f}  {:>14.6f}{:>14.6f}       0       0\n".format(i+1, float(unique_nodes[i][0].replace(']', '')), float(unique_nodes[i][1].replace(']', '')), float(unique_nodes[i][2].replace(']', ''))))
        # if i+1 >= 100 and i + 1 < 1000:
        #     f.write("     {:<4}  {:>14.6f}  {:>14.6f}{:>14.6f}       0       0\n".format(i+1, float(unique_nodes[i][0].replace(']', '')), float(unique_nodes[i][1].replace(']', '')), float(unique_nodes[i][2].replace(']', ''))))
        # if i+1 >= 1000:
        #     f.write("    {:<4}  {:>14.6f}  {:>14.6f}{:>14.6f}       0       0\n".format(i+1, float(unique_nodes[i][0].replace(']', '')), float(unique_nodes[i][1].replace(']', '')), float(unique_nodes[i][2].replace(']', ''))))
    f.write(bottom_content)


# subprocess.run(['code', 'test3.k'])


def run_simulation(input_file):
    # Run the LS-DYNA simulation
    # Note: replace 'C:\Program Files\LS-DYNA\ls-dyna.exe' with the actual path to your LS-DYNA executable
    subprocess.run(
        ['C:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA\lsdyna.exe', 'i=' + input_file])


input_file = 'test3.k'

# Make sure the input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} not found.")


# Run the simulation
run_simulation(input_file)

# Postprocess the results
# For this example, we simply print a message
print("Simulation completed.")


# Write to a .cfile
with open("your_script.cfile", "w") as file:
    file.write("open d3plot\n")

subprocess.run(["lspp4", "-nographics", "-c", "your_script.cfile"])
