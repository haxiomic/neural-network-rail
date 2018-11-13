# -*- coding: utf-8 -*-
import sys
import glob
import os.path 
import xml.etree.ElementTree as ElementTree

def process_file(filepath):
    with open(filepath) as open_file:
        xml = ElementTree.fromstring(open_file.read())

    tags = []
    for item in xml.findall('object'):
        tag = {}
        for child in item:
            if (child.tag == 'name'):
                tag['name'] = child.text
            elif (child.tag == 'bndbox'):
                tag['bbox'] = [ float(c.text) for c in child ]
        tags.append(tag)

    return '\n'.join([
        "{} 0.00 0 0.0 {}.00 {}.00 {}.00 {}.00 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0".format(tag['name'], *tag['bbox'])
        for tag in tags
    ])

def save_file(filename, content):
    with open(filename, 'w') as open_file:
        open_file.write(content)

def main():
    # '../training/labels/*.xml'
    filepaths = glob.glob('/Users/hpgmiskin/code/Hackathons/HackTrain/London Victoria Stuff/5/London Victoria/DCIM/108_VIRB/LABELS/*.xml')
    print(filepaths)
    basepath = os.path.commonpath(filepaths)
    print(basepath)
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        [name, extension] = filename.split('.')
        kitti_data = process_file(filepath)
        filename = os.path.join(basepath, '{}.txt'.format(name))
        print(filename)
        save_file(filename, kitti_data)

if __name__ == "__main__":
    main()