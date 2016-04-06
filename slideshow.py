# 
# Avi Schwarzschild
# Photo organization program
# photo.py
# August 2014
#

import os
from shutil import move, copyfile
from PIL import Image, ImageOps
import datetime

def make_tnail(src, dst, size):
    copyfile(src, dst)
    img = Image.open(dst)
    thumb = ImageOps.fit(img, size, Image.ANTIALIAS)
    thumb.save(dst, 'JPEG')

def number_photos(rootdir, dst='target'):
    if not os.path.exists(dst):
        os.makedirs(dst)
    else:
        os.system('rm -rf target/*')
        print 'rm -rf target/*'

    print 'Working...'
    for subdir, dirs, files in os.walk(rootdir):
        i = 1
        for file in files:
            newname = os.path.join(dst, str(i)+'.jpg')
            thumbname = os.path.join(dst, 't'+str(i)+'.jpg')
            copyfile(os.path.join(rootdir,file), newname)
            size = (4272/2, 2848/2)
            img = Image.open(newname)
            (width, height) = img.size
            if width >  height:
                thumb = ImageOps.fit(img, size, Image.ANTIALIAS)
            else: 
                thumb = ImageOps.fit(img, (2848/3, 4272/3), Image.ANTIALIAS)
            thumb.save(newname, 'JPEG')
            make_tnail(newname, thumbname, (width/8, height/8))
            i += 1

def count_photos(rootdir):
    return len([name for name in os.listdir(rootdir)])

def make_html(num_photos, title, header):
    num_photos += 1
    header = '<html>\n\
    <head>\n\
        <meta charset="utf-8">\n\
        <meta http-equiv="X-UA-Compatible" content="IE=edge">\n\
        <title>%s</title>\n\
        <meta name="description" content="">\n\
        <meta name="viewport" content="width=device-width, initial-scale=1">\n\
        <link href="http://fonts.googleapis.com/css?family=Open+Sans|Open+Sans+Condensed:700" rel="stylesheet" type="text/css">\n\
        <link rel="stylesheet" href="../statics/demostyles.css">\n\
        <link rel="stylesheet" href="../statics/simple-slideshow-styles.css">\n\
        <style>\n\
          img#home{\n\
            height: 20px;\n\
            float: right;\n\
            margin-right: 50px;\n\
            margin-top: 25px;\n\
          }\n\
          </style>\n\
    </head>\n\
    <body>\n\
        <div id="container">\n\
        <header>\n\
            <h1>%s</h1>\n\
            <p><span class="desc">%s</span></p><a href="../index"><img id="home" height="20px" src="../statics/house.jpg"></a>\n\
        </header>\n ' %(title, title, header)

    grid = '<br><br><br><div id="grid"><br><center>'
    for i in xrange(1,num_photos):
        link = '\n <img src=t%d.jpg>' %(i)
        grid = grid + link
    grid = grid + '</center></div>'

    body = '<div class="bss-slides num2" tabindex="1" autofocus="autofocus">'
    for i in xrange(1, num_photos):
        body = body + '<figure>\n\
              <center><img src="'+ str(i) + '.jpg" /><figcaption></figcaption></center>\n\
            </figure>\n'
    body = body + '</div> <!-- // bss-slides --> \n\
            </div> \n'

    footer = '<br><br><br> <center><A href="index.html">SLIDES</A>&nbsp&nbsp \
            <A href="grid.html">GRID</A></center>\
            <footer><emph>Avi Schwarzschild</emph> <br> %s</footer>  \n\
            \n\
            <script src="../statics/better-simple-slideshow.min.js"></script>\n\
            <script>\n\
            var opts = {\n\
                auto : {\n\
                    speed : 3500, \n\
                    pauseOnHover : true\n\
                },\n\
                fullScreen : false, \n\
                swipe : true\n\
            };\n\
            makeBSS(".num1", opts);\n\
            \n\
            var opts2 = {\n\
                auto : false,\n\
                fullScreen : true,\n\
                swipe : true\n\
            };\n\
            makeBSS(".num2", opts2);\n\
            </script>\n\
            </body>\n\
            </html>' % (datetime.datetime.now().strftime("%B %d, %Y"))  
    fn = open('target/index.html', 'w')
    fn.truncate()
    fn.write(header + body + footer)
    fn.close()

    fn = open('target/grid.html', 'w')
    fn.truncate()
    fn.write(header + grid + footer)
    fn.close()

    # copyfile('statics/simple-slideshow-styles.css', 'target/simple-slideshow-styles.css')
    # copyfile('statics/demostyles.css', 'target/demostyles.css')
    # copyfile('statics/better-simple-slideshow.min.js', 'target/better-simple-slideshow.min.js')
    print 'html pages created'

def sync(dest):
    cmd = 'rsync -avz --delete -e "ssh -p 2222" target/ avi@koplon.com:public_html/%s' %(dest)
    print cmd
    done = raw_input('Continue? (return for yes) ')
    if not done:
        os.system(cmd)

def main():
        rootdir = raw_input('rootdir: ')
        title = raw_input('Title: ')
        header = raw_input('Header: ')
        number_photos(rootdir)
        num_photos = count_photos(rootdir)
        make_html(num_photos, title, header)
        dest = raw_input('Album Name: ')
        sync(dest)



main()

