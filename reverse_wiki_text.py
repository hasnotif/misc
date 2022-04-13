#!/usr/bin/env python3
# reverse_wiki_text.py reverses the order of clearly defined segments in a Wiki text.

# eg.

# ORIGINAL:                 REVERSED:
# == 1 Apr ==               == 4 Apr ==
#
# #Lorem ipsum              #Lorem ipsum
# #dolor amit               #dolor amit
#                 ===>
# == 4 Apr ==               == 1 Apr ==
#
# #Lorem ipsum              #Lorem ipsum
# #dolor amit               #dolor amit

import argparse

def main():
    parser = argparse.ArgumentParser(description="Reverses the order of clearly defined segments in a Wiki text.")
    parser.add_argument("-i", "--input", required=True, help="specify input Wiki text file")
    args = parser.parse_args()

    print("Reversing wiki text...", end=" ")

    with open(args.input, "r") as r:
        lines = r.readlines()

    # find index of starting segment
    for i in range(len(lines)):
        if "==" in lines[i]:
            start_idx = i
            break

    # separate Wiki text into (i) pre-segment, (ii) segments
    pre_segment = lines[:start_idx]
    segments = lines[start_idx:]

    # reverse
    new_segments = []
    start_flag = True
    new_seg = []
    for i in range(len(segments)):
        if "==" in segments[i]:
            if start_flag:
                new_seg.append(segments[i])
                start_flag = False
            else:
                new_segments.insert(0, new_seg)
                new_seg = [segments[i]]
        else:
            new_seg.append(segments[i])
    new_segments.insert(0, new_seg)
    new_segments.insert(0, pre_segment)
    flattened_new_segments = flatten_list(new_segments)

    with open("reversed_wiki_text.txt", "w") as w:
        w.writelines(flattened_new_segments)

    print("Done!")

def flatten_list(l):
    flat_list = []
    for ele in l:
        if type(ele) is list:
            for item in ele:
                flat_list.append(item)
        else:
            flat_list.append(ele)
    return flat_list

main()

    



    

