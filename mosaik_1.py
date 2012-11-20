#! /usr/bin/env python
# -*- coding:utf8 -*-


import sqlite3
import Image
import glob
import random
import os
C = 128


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


def get_proportion(w, h, base_size=256):
    """
    Get new proportion to resize image.
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
image_colection = '/home/byka/images/vacation/'
im_out_mozaik = 'vacation.png'
resize_dir_name = "resize_vacation_pic"
resize_dir = os.path.join(work_dir, resize_dir_name)
#print resize_dir
#base_size = 256
db_name = "vacation.db"


print work_dir

# size to image in pixel, image to db
output_pixel_size = 512
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

#print os.path.join(image_colection, "*.jpg")


files = glob.glob(os.path.join(image_colection, "*.JPG"))
files += glob.glob(os.path.join(image_colection, "*.jpg"))

#print "Files -", files
# Input data to db
conn = sqlite3.connect(os.path.join(work_dir, db_name))
c = conn.cursor()
for f in files:
    print f
    # path to save resize file
    file_name = os.path.basename(f) + '.png'
    print file_name
    save_path = os.path.join(resize_dir, file_name)

    if not os.path.exists(save_path):
        im = Image.open(f)
        if im.mode == 'RGB':
            w, h = im.size
            # proportional resize image for pixel
            im_resize = im.resize(get_proportion(w, h,
                                    base_size=output_pixel_size),
                                    1)  # what is 0!!!
            #print "file %s was resized..." % f

            # get r, g, b color
            r, g, b = get_color(im_resize)
#            print r, g, b
            # create new image for paste im_resize, and set base color.
            im_for_pixel = Image.new("RGBA",
                                    size=(output_pixel_size,
                                            output_pixel_size),
                                    color = (r, g, b, 0))

            w_resize, h_resize = im_resize.size
            if w_resize >= h_resize:
                x = 0
                y = output_pixel_size / 2 - h_resize / 2
            else:
                y = 0
                x = output_pixel_size / 2 - w_resize / 2

            im_for_pixel.paste(im_resize, (x, y))
            im_for_pixel.save(save_path)
            #print "file %s was detected color..." % f
            data = (save_path, r, g, b)
            #  todo, correct work with non ascii symbols
            try:
                c.execute(
                    "INSERT INTO colors (path, r, g, b) values (?, ?, ?, ?)",
                    data)
            except:
                print "File name contains non ASCII symbols..."
            #print "file %s was insert to db..." % f

        else:
            print "file %s is wrong mode..." % f
conn.commit()
conn.close()

#im = Image.open('a78848323a179be7c68dfb740b0f760f-p9omob.jpg', 'r')
im = Image.open('/home/byka/images/vacation/IMG_6961.JPG', 'r')
print im.size
resize_image_for_mozaik = 1
if resize_image_for_mozaik:
    w, h = im.size
    im = im.resize((get_proportion(w, h, 1024)), 0)
#im = Image.open('99px_ru_avatar_vkontakte_11995.jpg', 'r')
w, h = im.size
print "w, h - %s, %s" % (w, h)
#mozaika_res_w, mozaika_res_h = w, h #get_proportion(w, h)

im_out = Image.new("RGBA", size=(w, h), color=(255, 255, 255, 255))
#im_out.paste(im, (0, 0))
print im_out.size
#im_out = Image.new("RGB", size = (mozaika_res_w*output_pixel_size,
#                                 mozaika_res_h*output_pixel_size))
print "Create output image..."

#im_resize = im.resize((mozaika_res_w, mozaika_res_h), 0) # what is 0!!!
#im_resize.save(os.path.join(work_dir, 'im_resize.jpg'))
#print "Resize input image..."

# Color generating


def color_sheme_generate():
    colors = {}
    for a in range(0, 265, 256 / 8):
        for b in range(0, 265, 256 / 8):
            for c in range(0, 265, 256 / 8):
#                for c in range(0, 265, 256 / 8):

                colors[(a, b, c)] = 0

    return colors


f_test_name = 1
#############################################################


def image_manipulation_test(i, j, C, d, lin, c, im_out):
    """
    ir, jr - x, y coordinate
    C - value of base image
    d - div
    lin - some symbol
    c - db cursor
    """
#        global f_test_name
#        for i in xrange(ir, ir + C, C / d):
#            for j in xrange(jr, jr + C, C / d):
    r = g = b = []
#    color_sheme = color_sheme_generate()

# Find the main color of pise of image

    for i_px in range(i, i + C / d):
        for j_px in range(j, j + C / d):
            try:
                r.append(im.getpixel((i_px, j_px))[0])
                g.append(im.getpixel((i_px, j_px))[1])
                b.appent(im.getpixel((i_px, j_px))[2])
            except:
                pass
            #print r, g, b

    r_total = sum(r) / len(r)
    g_total = sum(g) / len(g)
    b_total = sum(b) / len(b)

    #print (r_total, g_total, b_total)

# Find the main color in persent
    total = 0
    for i_px in range(i, i + C / d):
        for j_px in range(j, j + C / d):
            try:
                r, g, b = im.getpixel((i_px, j_px))
                if r_total <= r < r_total + 32:
                    if g_total <= g < g_total + 32:
                        if b_total <= b < b_total + 32:
                            total += 1
                            #print total
            except:
                pass

    in_persent = total * 100 / ((C / d) * (C / d))
#    print in_persent, '%'
###############################################################################

###############################################################################
            #
            #for key in color_sheme.keys():
                #r_cs, g_cs, b_cs = key
                #if r_cs <= r < r_cs + 32:
                    #if g_cs <= g < g_cs + 32:
                        #if b_cs <= b < b_cs + 32:
                            ##print key
                            #color_sheme[key] += 1
    #list_of_colors = []
    #for key in color_sheme.keys():
        #list_of_colors.append([color_sheme[key], key])
    #list_of_colors.sort()

    #color = list_of_colors[-1][1]
    #total = list_of_colors[-1][0]
    #in_persent = total * 100 / ((C / d) * (C / d))
    ##print "in_persent - %s" % in_persent, (C / d)*(C / d)

###############################################################################

    x, y = i, j

    if in_persent < 40 and d <= 4:
        d = d * 2
        #print "C, d = ", C, d
        add_value = (C / d) * 2
        for i_new in xrange(i, i + add_value, C / d):
            for j_new in xrange(j, j + add_value, C / d):
                #print i_new, j_new
                image_manipulation_test(i_new, j_new, C, d, lin, c, im_out)
    else:
        #print d
        db_result = c.execute("""SELECT path, r, g, b, ((r-%s)*(r-%s) +
                                (g-%s)*(g-%s) +
                                (b-%s)*(b-%s)) AS dcolor FROM colors
                                ORDER BY dcolor ASC LIMIT 10""" %
                        (str(r_total), str(r_total),
                        str(g_total), str(g_total),
                        str(b_total), str(b_total))
                        )
        paths = []
        for f in db_result:
            paths.append(f)
        index = random.randint(1, len(paths))
        #print index, len(paths)
        im_pixel = paths[index - 1]
        #print im_pixel
        im_insert_pixel = Image.open(im_pixel[0], 'r')
        im_res = im_insert_pixel.resize((C / d, C / d), 1)
#        print d,
#        print im_res.split()
#        r, g, b, a = im_res.split()
        #print a

        #print im_out
        try:
            im_out.paste(im_res, (x, y), im_res.split()[3])
            #im_out.save("./test/%s.png" % f_test_name)
            f_test_name += 1
        except:
            pass
        #print "Paste"

    return True

#############################################################


conn = sqlite3.connect(os.path.join(work_dir, db_name))
c = conn.cursor()
print "Please wait, creating foto mozaiki was begin..."
#im_out.paste(im, (0, 0))
#im_out.save('./test/0.png')
for i in xrange(0, w, C):
    for j in xrange(0, h, C):
        image_manipulation_test(i, j, C, 1, '+', c, im_out)

    to_end = i * 100 / w
    print to_end, '%'


print "Thanks for waiting!"
conn.close()
im_out.save(im_out_mozaik)
print "Output image was creating sucsesfull!!!"