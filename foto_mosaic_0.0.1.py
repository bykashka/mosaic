#! /usr/bin/env python
# -*- coding:utf8 -*-


import sqlite3
import Image
import os, sys
import glob
import numpy



def get_color(im_obj):
    """
    Return basic color of image like tupl - (r, g, b)
    """
    #im = Image.open(path, 'r')
    x, y = im_obj.size

    r, g, b = 0, 0, 0
    for i in xrange(x):
        for j in xrange(y):
            color_px = im_obj.getpixel((i, j))
            #print color_px
            r += color_px[0]
            g += color_px[1]
            b += color_px[2]

    r = r / (x * y)
    g = g / (x * y)
    b = b / (x * y)
    return (r, g, b)

def get_proportion(w, h, base_size = 256):
    """
    Return new proportion (w, h). 
    """
    large_side = base_size
    k = float(w) / float(h)
    
    if w > h:
        w_prop = large_side
        h_prop = int(w_prop / k)
    elif w < h:
        h_prop = large_side
        w_prop = int(h_prop * k)
    else:
        h_prop = w_prop = large_side

    return (w_prop, h_prop)

# initialisation
work_dir = os.getcwd()
print work_dir
image_colection = './OgromKolCveti2012'
image_for_mozaik = './sonja.jpg'
im_out_mozaik = './s.jpg'
resize_dir_name = "resize_flover"
resize_dir = os.path.join(work_dir, resize_dir_name)
#print resize_dir
#base_size = 256
db_name = "flovers_new.db"


print work_dir

# size to image in pixel, image to db
output_pixel_size = 64
r, g, b = 0, 0, 0

# Creating database if not exists
conn = sqlite3.connect(os.path.join(work_dir, db_name))
conn.execute("create table if not exists colors(path, r, g, b)")
conn.commit()
conn.close()
print "db created sucsesful..."

# Create dir for resize images
if not os.path.exists(resize_dir):
    os.mkdir(resize_dir)

print 'create dir - %s' % resize_dir_name

files = glob.glob(os.path.join(image_colection, "*.jpg"))
# Input data to db
conn = sqlite3.connect(os.path.join(work_dir, db_name))
c = conn.cursor()
for f in files:
    print f
    # path to save resize file
    sawe_path = os.path.join(resize_dir, os.path.basename(f))
    
    if not os.path.exists(sawe_path):
        im = Image.open(f)
        if im.mode == 'RGB':
            w, h = im.size
            # proportional resize image for pixel
            im_resize = im.resize(get_proportion(w, h, base_size = output_pixel_size), 0) # what is 0!!!
            #print "file %s was resized..." % f

            # get r, g, b color
            r, g, b = get_color(im_resize)
            print r, g, b
            # create new image for paste im_resize, and set base color.
            im_for_pixel = Image.new("RGB", size = (output_pixel_size, output_pixel_size), color = (r, g, b))

            w_resize, h_resize = im_resize.size
            if w_resize >= h_resize:
                x = 0
                y = output_pixel_size/2 - h_resize/2
            else:
                y = 0
                x = output_pixel_size/2 - w_resize/2

            im_for_pixel.paste(im_resize, (x, y))
            im_for_pixel.save(sawe_path)
            #print "file %s was detected color..." % f
            data = (sawe_path, r, g, b)

            c.execute("INSERT INTO colors (path, r, g, b) values (?, ?, ?, ?)", data)
            #print "file %s was insert to db..." % f
            
        else:
            print "file %s is wrong mode..." % f
conn.commit()
conn.close()

im = Image.open(image_for_mozaik, 'r')
w, h = im.size
#mozaika_res_w, mozaika_res_h = w, h
mozaika_res_w, mozaika_res_h = get_proportion(w, h)

im_out = Image.new("RGB", size = (mozaika_res_w*output_pixel_size, mozaika_res_h*output_pixel_size))
#print "Create output image..."

im_resize = im.resize((mozaika_res_w, mozaika_res_h), 0) # what is 0!!!
im_resize.save(os.path.join(work_dir, 'im_resize.jpg'))
#print "Resize input image..."


conn = sqlite3.connect(os.path.join(work_dir, db_name))
c = conn.cursor()
print "Please wait, creating foto mozaiki was begin..."
for i in xrange(mozaika_res_h):
    for j in xrange(mozaika_res_w):
#        r, g, b = im.getpixel((j, i))
        r, g, b = im_resize.getpixel((j, i))
        
        d = c.execute("""SELECT path, r, g, b, ((r-%s)*(r-%s) + 
                                        (g-%s)*(g-%s) + 
                                        (b-%s)*(b-%s)) AS dcolor FROM colors
                        ORDER BY dcolor ASC LIMIT 5""" %
                      (str(r), str(r), str(g), str(g), str(b), str(b))
                      )
        paths = []
        for f in d:
            paths.append(f)
        index = numpy.random.randint(len(paths))
        im_pixel = paths[index]
        #print im_pixel
        im_insert_pixel = Image.open(im_pixel[0], 'r')
        im_out.paste(im_insert_pixel,(j*output_pixel_size, i*output_pixel_size))
    #percent = i * 100 / mozaika_res_h
    #print percent
print "Thenks for waiting!"
conn.close()
im_out.save(im_out_mozaik)
print "Output image was creating sucsesfull!!!"

