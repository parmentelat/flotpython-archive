#!/usr/bin/env python

from glob import glob

user="pthierry"

skel_pre = "<html><body><ul>\n"
skel_post = "</ul></body></html>\n"
url_format = "<li><a href='https://connect.inria.fr/ipythonExercice/W{week}/{name}.ipynb/{user}'>W{week} - {name}</a></li>\n"


def main ():
    with open ("connect.html", "w") as f:
        f.write(skel_pre)
        for ipynb in glob ("W[0-9]*/*.ipynb"):
            dir,file = ipynb.split('/')
            week=dir.replace('W','')
            name=file.replace('.ipynb','')
            f.write (url_format.format(week=week,name=name,user=user))
        f.write(skel_post)

if __name__ == '__main__':
    main()
