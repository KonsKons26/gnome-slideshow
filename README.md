# gnome-slideshows
## script to automate the creation of .xml files for setting up slideshow background on GNOME.

### info

The directory structure must look like this, and each folder  
will become a background slideshow  
.  
├── Folder_1  
│   ├── 6mZeJ5F.png  
│   ├── 7C79quQ.png  
│   ├── mw6km0E.jpeg  
│   └── XmPUpF7.jpeg  
├── Folder_2  
│   ├── 1319312.jpeg  
│   ├── 1354554.png  
│   ├── 910286.jpg  
│   ├── 910289.jpg  
├── Folder_3  
│   ├── 1uAmcxV.jpeg  
│   ├── 5ycm1HO.png  
│   ├── exfQ9Pm.png  
│   └── fggJQ7f.jpeg  
└── update_slideshows.py  

Run the program like so:  
```bash
$ ./update_slideshows.py -i /path/to/parent/folder -s 300 -t 0.5
```
using `-i` for the path, `-s` for the static time, and `-t` for the transition time.  
Then you end up with a new .xml file for each Folder_*  
i.e.:  
`Folder_1_slideshow.xml`, `Folder_2_slideshow.xml` and, `Folder_3_slideshow.xml`  
and a new .xml inside ~/.local/share/gnome-background-properties/  
named custom_slide_shows.xml  

Then simply open Settings -> Appearance and select one of the new slideshow wallpapers
