Original article:
http://www.gr4viton.cz/2015/10/gr4gallery-gallery-in-python-2-7-10-opencv-3-0-0-tkinter-gui/

=
> # gr4gallery = Gallery in Python 2.7.10 + OpenCV 3.0.0 + Tkinter GUI

> Publikováno 9-10-2015

> Hi there fellows, a project emerged from the need of using OpenCV with GUI possibilities larger than trackbar. I am currently keen on Python, but I didn’t want to spend any time finding out how to make OpenCV + Python + Qt work, because the commercial licensing of Qt borthered me too much. Therefore I turned to the only other python GUI library I know so far the good ol‘ Tkinter.

> ![screenshot](http://www.gr4viton.cz/wp-content/uploads/2015/10/screenshot-1024x244.png)

> Although I had a rough time finding how to make it work together, in the end I find some discussion where they had a simple example. The code took webcam video stream captured by OpenCV and transformed its image data to tkinter label background periodically by a little help of multiprocessing.

> I think its not a clearest solution, but it works so I am trying to build my project on it. The code does not include the upper class, it was just a snippet and with my not so great knowledge of Python I was not able (after a boring half hour trying) to rewrite it to work. It was complaining about some Pickling problem when I tried to write it class style, so I stopped trying for now.

> Instead I created a little demonstration program. It is essencially „a gallery“ that is disk image browser with extra webcam snapshot capabilities. You can use all the mighty OpenCV functions to play with pictures and webcam stream and use the easy tkinter gui to make interactions with the user.

> Webcam on the left, browsed folder in the middle and selected image on the right. Many of the label texts are confusing and the saving or loading may switch RGB and BGR channels.

> Whole project created in Python with PyCharm as a devenv is accessible through git repository here:

> https://github.com/gr4viton/gr4gallery

> The code is a mess as I wrote it in about 2 hours, but you’ll get the idea how to fuse these tools together 😉

> PS: If you happen to succeed in rewriting it into class please send it to me 😉

> Příspěvek byl publikován v rubrice app, educ, OpenCV, pcvision, project, Python, tkinter se štítky OpenCV, pcVision, project, python, tkinter a jeho autorem je admin. Můžete si jeho odkaz uložit mezi své oblíbené záložky nebo ho sdílet s přáteli.

=
