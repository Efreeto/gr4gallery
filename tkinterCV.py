#!/usr/bin/python

# http://stackoverflow.com/questions/17073227/display-an-opencv-video-in-tkinter-using-multiprocessing
import array

import numpy as np
from multiprocessing import Process, Queue
import cv2
from PIL import Image, ImageTk
try:    # Python 2
    # from Queue import Empty
    import Tkinter as tk
    import Tkconstants, tkFileDialog
except: # Python 3
    # from queue import Empty
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog

import sys
import os
import glob

# tkinter GUI functions----------------------------------------------------------
global root
global vidIm

def quit_(root, process, *whatever):
    process.terminate()
    root.destroy()


# def quitCallback():

def update_image(image_label, frame):
    global vidIm
    if len(frame) == 0:
        return
    if len(frame.shape) == 2:
        im = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    else:
        im = frame
        vidIm = im

    a = Image.fromarray(im)
    b = ImageTk.PhotoImage(image=a)
    image_label.configure(image=b)
    image_label._image_cache = b  # avoid garbage collection
    root.update()

def update_all(root, params):
    imlLabel, queue = params

    update_image(imlLabel, queue.get())
    root.after(0, func=lambda: update_all(root, params))

def stepCV(cap):
    flag, frame = cap.read()
    if flag == 0:
        return None

    a = 0.5
    im = cv2.resize(frame, (0, 0), fx=a, fy=a)
    im = CONVERT_bgr_to_rgb(im)
    return im

# multiprocessing image processing functions-------------------------------------
def image_capture(queue):
    cap = cv2.VideoCapture(0)
    loopingCV = 1
    while loopingCV:
        im = stepCV(cap)
        queue.put(im)
    cap.release()

def SET_cwd():
    # os.getcwd()
    print(askdirectory())

def SET_cwd(path):
    os.chdir(path)
    RECREATE_im()

def ASK_cwd():
    SET_cwd(askdirectory())

def SET_cwdDefault():
    SET_cwd('D:\VIEW\wallpapers')

class gr4gallery():
    def __init__(self, frameGallery, frameSelectedPic):
        self.FrameGallery = frameGallery
        self.FrameSelectedPic = frameSelectedPic
        self.pics = []

    def REMOVE_oldPics(self):
        print('destroying pics '+ str(len(self.pics)))
        for pic in self.pics:
            pic.destroy()
        del self.pics[:]
            
    def DISPLAY_Gallery(self, pIms):
        gridW = 3
        picH = 150
        picInd = 0
        self.REMOVE_oldPics()
        print (pIms)
        for pIm in pIms:
        #     imLabel.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    
            #self.pics.append( tk.Label(self.FrameGallery) )
    
            # self.pics.append( tk.Button(self.FrameGallery, text='Q', command=lambda: quit_(root, p)) )
            print (pIm)
            self.pics.append( tk.Button(self.FrameGallery, command=lambda pIm=pIm: self.SELECT_pic(pIm)) )
            # self.pics[-1].get
            picCol = picInd % gridW
            picRow = int(picInd / gridW)
            # self.pics[-1].pack()
            self.pics[-1].grid(row=picRow, column=picCol, rowspan=1, columnspan=1, sticky=tk.NSEW)
            im = self.RESIZE_height(self.LOAD_im(pIm), picH)
            self.SHOW_imageIn(self.pics[-1], im)
            self.pics[-1].configure(height=picH)
            picInd += 1
        
    def LOAD_im(self, path):
        im = cv2.imread(path)
        im = self.CONVERT_bgr_to_rgb(im)
        return im
    
    def CONVERT_bgr_to_rgb(self, bgr_img):
        b, g, r = cv2.split(bgr_img)
        rgb_img = cv2.merge([r,g,b])
        return rgb_img
        # return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        
    def RESIZE(self, im, dim):
        # use inter cubic of inter whatsoever if its bigger or smaller than original
        return cv2.resize(im, dim, interpolation = cv2.INTER_CUBIC)

    def RESIZE_width(self, im, w):
        r = float(w) / im.shape[0]
        dim = (int(im.shape[1] * r), w)
        return self.RESIZE(im,dim)
    
    def RESIZE_height(self, im, h):
        r = float(h) / im.shape[1]
        dim = (h, int(im.shape[0] * r))
        return self.RESIZE(im,dim)
    
    def SELECT_pic(self, path):
        # heigh = self.FrameSelectedPic.get('height')
        height = 500
        print(path + " = image trying to select")
        self.SHOW_imageIn(self.FrameSelectedPic,
                    self.RESIZE_height(self.LOAD_im(path), height ) )

    def SHOW_imageIn(self, obj, im):
        a = Image.fromarray(im)
        b = ImageTk.PhotoImage(image=a)
        obj.configure(image=b)
        obj._image_cache = b
    
def CONVERT_bgr_to_rgb(bgr_img):
    b, g, r = cv2.split(bgr_img)
    rgb_img = cv2.merge([r,g,b])
    return rgb_img
    # return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        
def SAVE_snapshot():
    im = CONVERT_bgr_to_rgb(vidIm)  # This will actually convert rgb to bgr (same operation). This is necessary because imwrite saves images in the reverse order
    cv2.imwrite('snapshot.png', im)
    RECREATE_im()

def RECREATE_im():
    print (os.getcwd())

    types = ('*.png','*.jpg','*.bmp') # the tuple of file types
    pIms = []
    for t in types:
        pIms.extend(glob.glob(t))

    snapshotGallery.DISPLAY_Gallery(pIms)

def askdirectory():
    """Returns a selected directoryname."""

    # defining options for opening a directory
    dir_opt = options = {}
    options['initialdir'] = 'C:\\'
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'This is a title'
    return tkFileDialog.askdirectory(**dir_opt)

def GUI_setup(root):
    global snapshotGallery
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # GUI Items
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # frAddList
    # ____________________________________________________ frames
    frMain = tk.LabelFrame(root, padx=5)

    frLeft = tk.LabelFrame(frMain, padx=5, width= 320, text="Add by list" )
    frTags = tk.LabelFrame(frMain, padx=5,  text="Detected tags")
    frPics = tk.LabelFrame(frMain, padx=5,  text="Pictures in cwd")
    frPicShow = tk.LabelFrame(frMain, padx=5,  text="Selected picture")
    # ____________________________________________________ images
    imlLabel = tk.Label(frLeft)
    imlSelected = tk.Label(frPicShow)
    # ____________________________________________________ texts
    # ____________________________________________________ sliders
    global slTags
    slTags = tk.Scale(frTags, from_=0, to_=10, orient=tk.HORIZONTAL)
    # ____________________________________________________ entries
    enHell = tk.Entry(frLeft, text='tkInter back in town')
    global strNumTags
    strNumTags = tk.StringVar()
    lbNumTags = tk.Label(frTags, textvariable=strNumTags)
    strNumTags.set( "0  found" )

    # ____________________________________________________ buttons
    btnQuit = tk.Button(frLeft, text='Q', command=lambda: quit_(root, p))
    btnSnap = tk.Button(frLeft, text='SAVE snapshot', command=SAVE_snapshot)

    # button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
    button_opt = {'padx': 5, 'pady': 5}
    btnOpenFolder = tk.Button(frTags, text='ASK directory', command=ASK_cwd)
    btnSetDefaultFolder = tk.Button(frTags, text='SET default', command=SET_cwdDefault)



    # btnSetDefaultFolder = tk.Button(frTags, text='SET default', command=SET_cwdDefault)
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # grid definitions
    #____________________________________________________
    frMain.grid (sticky=tk.NSEW)
    #____________________________________________________
    frLeft.grid (row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

    imlLabel.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    btnSnap.grid(row=4, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    enHell.grid (row=1, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    btnQuit.grid(row=0, column=3, rowspan=4, columnspan=1, sticky=tk.NSEW )

    #____________________________________________________
    frTags.grid (row=2, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW )

    btnOpenFolder.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW, **button_opt)
    btnSetDefaultFolder.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW, **button_opt)

    lbNumTags.grid(row=1, column=2, rowspan=1, columnspan=1)#, sticky=tk.NSEW )
    slTags.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    # imlTags.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )

    #____________________________________________________
    frPics.grid (row=2, column=4, rowspan=1, columnspan=1, sticky=tk.NSEW )

    imlSelected.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    #____________________________________________________
    frPicShow.grid (row=2, column=5, rowspan=1, columnspan=1, sticky=tk.NSEW )
    
    snapshotGallery = gr4gallery(frPics, imlSelected)
    print ('GUI initialized...')

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Key binding

    # return
    return imlLabel


def HOTKEY_setup(root, p):
    # root.bind( '<Escape>', quit_(root, p) )
    pass

if __name__ == '__main__':
    queue = Queue()
    print ('queue initialized...')
    root = tk.Tk()
    # root.columnconfigure(0, weight=1)
    # root.configure(sticky=tk.NSEW )
    # root.pack( expand  =True)
    imlLabel = GUI_setup(root)

    p = Process(target=image_capture, args=(queue,))

    HOTKEY_setup(root, p)

    p.start()
    print ('image capture process has started...')

    root.minsize(width=640, height=100)

    # setup the update callback (recursive calling inside)
    params = imlLabel, queue
    root.after(0, func=lambda: update_all(root, params))


    print ('root.after was called...')
    root.mainloop()
    print ('mainloop exit')
    p.terminate()
    # p.join()
    print ('image capture process exit')
