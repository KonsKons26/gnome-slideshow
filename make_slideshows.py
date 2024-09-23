#!/usr/bin/env python3

import os
import argparse


def get_absolute_paths(folder_path):
    abs_paths = []
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            abs_path = os.path.abspath(os.path.join(dirpath, filename))
            abs_paths.append(abs_path)
    return abs_paths


def gen_xmls(base_directory, static_t, transition_t):
    folders = []
    with os.scandir(base_directory) as entries:
        for entry in entries:
            if entry.is_dir():
                folders.append(entry.name)

    for folder in folders:
        folder_path = os.path.join(base_directory, folder)
        f_paths = get_absolute_paths(folder_path)

        # Modify the duration here
        # Both for how long the image stays (static)
        # and how fast the transition happens (transition)
        static = f"""  
    <static>
        <duration>{static_t}</duration>
        <file>{{img}}</file>
    </static>"""

        transition = f"""    
    <transition>
        <duration>{transition_t}</duration>
        <from>{{img1}}</from>
        <to>{{img2}}</to>
    </transition>"""

        start = """<?xml version="1.0" ?>
    <background>"""

        end = "\n</background>"

        xml = start

        for i in range(len(f_paths)):
            if i < len(f_paths) - 1:
                xml += static.format(img=f_paths[i])
                xml += transition.format(img1=f_paths[i], img2=f_paths[i + 1])
            else:
                xml += static.format(img=f_paths[i])

        xml += end
        output = f"{folder}_slideshow.xml"
        output_path = os.path.join(base_directory, output)
        with open(output_path, "w") as xml_write:
            xml_write.write(xml)


def update_gnome_properties(base_directory):
    properties_xml = os.path.expanduser("~/.local/share/gnome-background-properties/custom_slide_shows.xml")

    abs_paths = get_absolute_paths(base_directory)

    wallpaper_block = """
    <wallpaper>
        <name>{n}</name>
        <filename>{f}</filename>
        <options>zoom</options>
        <shade_type>solid</shade_type>
    </wallpaper>"""

    start = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
<wallpapers>"""

    end = "\n</wallpapers>"

    xml = start
    for f in abs_paths:
        if f.endswith(".xml"):
            print(f)
            n = f.split("/")[-1].split("_slideshow")[0]
            xml += wallpaper_block.format(n=n, f=f)
    xml += end

    with open(properties_xml, "w") as write_xml:
        write_xml.write(xml)

def main():
    parser = argparse.ArgumentParser(description="Generate slideshows from folders and update GNOME properties.")
    parser.add_argument(
        "-i", "--input", 
        default=os.getcwd(), 
        help="The base directory containing folders. Defaults to the current working directory."
    )
    parser.add_argument(
        "-s", "--static-duration", 
        type=int, 
        default=300, 
        help="Duration (in seconds) for each image to remain static. Defaults to 300 seconds."
    )
    parser.add_argument(
        "-t", "--transition-duration", 
        type=float, 
        default=0.5, 
        help="Duration (in seconds) for the transition between images. Defaults to 0.5 seconds."
    )
    
    args = parser.parse_args()
    base_directory = args.input
    static_t = args.static_duration
    transition_t = args.transition_duration

    gen_xmls(base_directory, static_t, transition_t)
    update_gnome_properties(base_directory)


if __name__ == "__main__":
    main()

