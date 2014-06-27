#!/usr/bin/env python

# re-ecriture et adaptation libre de http://xkcd.com/519/

import matplotlib
matplotlib.use('TkAgg')

from matplotlib import pyplot as plt
import numpy as np

plt.xkcd()

my_dpi=80
fig = plt.figure(dpi=my_dpi,figsize=(9,6))

fig.subplots_adjust(left=0.30,top=0.65,bottom=0.15)

fig.text(0.02,0.02,"adaptation libre de http://xkcd.com/519/",
         fontsize=12,ha='left')

fig.text(0.5,0.82,"Python:\ndes fondements\naux applications",
         fontsize=45, ha='center',va='center')

#plt.title("Python\ndes fondements\naux applications",fontsize=45)

ax = fig.add_subplot(1, 1, 1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.set_xlim([-0.5, 2.5])
ax.set_ylim([0, 110])
ax.bar([i-0.125 for i in range(3)], [5, 3, 100], 0.25)

ax.xaxis.set_ticks_position('bottom')
ax.tick_params(size=0)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["900 HEURES\nDE COURS", 
                    "400 HEURES\nDE DM", 
                    "UN MOOC\nA JOUER\nAVEC PYTHON"])
plt.yticks([])
ax.set_ylabel("apport pour\nune carriere\nreussie",
              rotation='horizontal',
              labelpad=100,
              fontsize=20)


fig.savefig('xkcd.png')

## the pictures I can see on FUN are 220 x 147
#(tx,ty)=(220,147)
#fig.set_size_inches (tx/my_dpi,ty/my_dpi)
#fig.savefig('xkcd-small.png')

plt.show()
