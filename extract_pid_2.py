def extract_nodes():
    element_section = False
    node_section = False
    nodes = {}
    node_ids = set()

    with open("cube_v2.k", 'r') as file:
        for line in file:
            line = line.strip()
            if '*ELEMENT_SHELL' in line:
                element_section = True
            elif '*NODE' in line:
                element_section = False
                node_section = True
            elif element_section == True:
                if line.split()[1].isdigit() == True:
                    split_line = line.split()
                    if int(line.split()[1]) == 2:
                        node_ids.add(split_line[2])
                        node_ids.add(split_line[3])
                        node_ids.add(split_line[4])
                        node_ids.add(split_line[5])
            elif '*SECTION_SHELL' in line:
                node_section = False
            elif node_section == True and element_section == False:
                split_line = line.split()
                if split_line[0].isdigit() == True:
                    if split_line[0] in node_ids:
                        nodes[split_line[0]] = split_line[1:4]

    return nodes


nodes = extract_nodes()
print(nodes)
