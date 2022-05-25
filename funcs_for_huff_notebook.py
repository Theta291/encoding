from graphviz import Graph
from IPython.display import display, clear_output
import time

def count_chars(string):
    count_dict = {}
    for char in string:
        if char in count_dict:
            count_dict[char] += 1
        else:
            count_dict[char] = 1
    return count_dict

def display_tree(tree, showchange=False, highlight=None, clear=True):
    sleep_time = 0
    if showchange:
        if not hasattr(display_tree, 'old_tree'):
            showchange = False

    if showchange:
        sleep_time = 2
        d1 = Graph('old Huffman tree')
        d1.node_attr.update(style='filled', fillcolor='white')
        for node in tree:
            if node not in display_tree.old_tree:
                left_child_pos = node[2]
                right_child_pos = node[2]+1
                break

        for pos, node in enumerate(display_tree.old_tree):
            strpos = str(pos)
            if showchange and pos == left_child_pos:
                d1.attr('node', fillcolor='lightgray')
            d1.node(strpos, f"'{node[0]}': {node[1]}")
            if showchange and pos == right_child_pos:
                d1.attr('node', fillcolor='white')
            child = node[2]
            if child is not None:
                d1.edge(strpos, str(child))
                d1.edge(strpos, str(child+1))

        if clear:
            clear_output(wait=True)
        display(d1)
        time.sleep(sleep_time)

    display_tree.old_tree = list(tree)

    d = Graph('Huffman tree')
    d.node_attr.update(style='filled', fillcolor='white')

    for pos, node in enumerate(tree):
        strpos = str(pos)
        if (showchange and pos == left_child_pos) \
                or (highlight is not None and node == highlight):
            d.attr('node', fillcolor='lightgray')
        d.node(strpos, "'" + node[0] + "': " + str(node[1]))
        if (showchange and pos == right_child_pos) \
                or (highlight is not None and node == highlight):
            d.attr('node', fillcolor='white')
        child = node[2]
        if child is not None:
            d.edge(strpos, str(child))
            d.edge(strpos, str(child+1))

    if clear:
        clear_output(wait=True)
    display(d)
    time.sleep(sleep_time)

def display_decode(tree, encoded_string):
    sleep_time = 1
    encode_size = len(encoded_string)
    decoded_string_list = []
    current_node = tree[-1]
    line2 = [' ' for i in range(encode_size)]

    for i, bit in enumerate(encoded_string):
        if bit == '0':
            left_child_position = current_node[2]
            current_node = tree[left_child_position]
        elif bit == '1':
            right_child_position = current_node[2]+1
            current_node = tree[right_child_position]
        key = current_node[0]
        if len(key) == 1:
            decoded_string_list.append(key)
        display_tree(tree, highlight=current_node)
        display(encoded_string)
        line2[i-1] = ' '
        line2[i] = '^'
        display(''.join(line2))
        display(''.join(decoded_string_list))
        time.sleep(sleep_time)
        if len(key) == 1:
            current_node = tree[-1]
            display_tree(tree, highlight=current_node)
            display(encoded_string)
            display(''.join(line2))
            display(''.join(decoded_string_list))
            time.sleep(sleep_time)
