import glob
import imageio
from PIL import Image
import numpy as np

import cPickle
import matplotlib.pyplot as plt
from python_visual_mpc.video_prediction.utils_vpred.animate_tkinter import color_code_distrib
from python_visual_mpc.video_prediction.misc.makegifs2 import assemble_gif

def save_video_mp4(filename, frames):
    writer = imageio.get_writer(filename + '.mp4', fps=10)
    for i, frame in enumerate(frames):
        print 'frame',i
        writer.append_data(frame)
    writer.close()

def main():

    # file = '/home/frederik/Documents/lsdc/experiments/cem_exp/benchmarks_sawyer/predprop_1stimg_bckgd/exp/unseen_clutter/verbose/gen_image_t3.pkl'

    app_gen_distrib = True
    individual_ex = False

    for cem_dir in range(5):
        filedir = '/home/frederik/Documents/catkin_ws/src/visual_mpc/experiments/cem_exp/benchmarks_sawyer/wristrot/videos/record_cem{}'.format(cem_dir)
        print 'processing dir ', filedir
        dict = cPickle.load(open(filedir+'/pred.pkl', "rb"))

        dest_dir = filedir

        t = 3

        # plt.imshow(np.squeeze(gen_distrib[0][0]))
        # plt.show()
        b = 0
        suf = ''

        for itr in range(3):
            vid_list = []
            gen_images = dict['gen_images_t{}_iter{}'.format(t, itr)]
            gen_distrib = dict['gen_distrib_t{}_iter{}'.format(t, itr)]
            gen_distrib = color_code_distrib(gen_distrib, 1, renormalize=True)

            if individual_ex:
                for b in range(1):
                    gen_images_b = [im[b] for im in gen_images]
                    gen_distrib_b = [im[b] for im in gen_distrib]
                    if app_gen_distrib:
                        suf = 'distrib'
                        out_im = [np.concatenate([im, distrib], axis=0) for im, distrib in zip(gen_images_b,
                                                                                               gen_distrib_b)]
                    else:
                        out_im = gen_images_b
                        suf = ''
            else:
                vid_list.append(gen_images)
                out_im = assemble_gif(vid_list, num_exp=8)
                suf = '_strip'

            save_video_mp4(dest_dir + '/gen_images_b{}_t{}_iter{}{}'.format(b, t,itr,suf), out_im)

if __name__ == '__main__':
    main()

