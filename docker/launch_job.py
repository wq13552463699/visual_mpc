import json
import argparse
import pdb
import os
import re
import pdb

def launch_job_func(run_script, hyper, nworkers=8, interactive=False, name='', ngpu=8, test=0, nsplit=None, isplit=None, fullcmd=None):

    data = {}

    if fullcmd is '':
        start_dir = "/workspace/visual_mpc/docker"
    else:
        start_dir = "/workspace/video_prediction"
    data["aceName"] = "nv-us-west-2"
    data["command"] = \
    "cd /result && tensorboard --logdir . & \
     export VMPC_DATA_DIR=/mnt/pushing_data;\
     export TEN_DATA=/mnt/tensorflow_data;\
     export ALEX_DATA=/mnt/pretrained_models;\
     export RESULT_DIR=/result;\
     export NO_ROS='';\
     export PATH=/opt/conda/bin:/usr/local/mpi/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; \
     cd /workspace/visual_mpc/docker; git pull; \
     cd /workspace/video_prediction; git pull; \
     cd {}; \
     ".format(start_dir)

    data['dockerImageName'] = "ucb_rail8888/tf_mj1.5:latest"

    data["datasetMounts"] = [{"containerMountPoint": "/mnt/tensorflow_data/sim/mj_pos_ctrl_appflow", "id": 8906},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/appflow_nogenpix", "id": 8933},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/updown_sact_onpolonly", "id": 9606},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/updown_sact_onpolonly_iter1,2", "id": 9607},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/updown_sact_comb", "id": 9224},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/onpol_finet1,2", "id": 9741},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/onpol_finet1", "id": 9740},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/appflow_nogenpix_mj1.5", "id": 9006},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/cartgripper_flowonly", "id": 9007},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/multi_view_models/autograsp", "id": 10169},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/mj_pos_ctrl", "id": 8930},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/pos_ctrl", "id": 8948},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/pos_ctrl_updown_rot_sact", "id": 8951},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/pos_ctrl_updown_sact", "id": 8950},
                             {"containerMountPoint": "/mnt/tensorflow_data/sim/onpolicy/updown_sact_onpolonly_iter2", "id": 9525},
                             {"containerMountPoint": "/mnt/tensorflow_data/gdn/startgoal_shad", "id": 9087},
                             {"containerMountPoint": "/mnt/tensorflow_data/gdn/96x128/cartgripper_tdac_flowpenal", "id": 9287},
                             {"containerMountPoint": "/mnt/pretrained_models/autograsp", "id": 10194},
                             {"containerMountPoint": "/mnt/pretrained_models/autograsp_reopen_ind", "id": 10466},
                             {"containerMountPoint": "/mnt/pretrained_models/autograsp_nostate_long", "id": 10237},
                             {"containerMountPoint": "/mnt/pretrained_models/autograsp_notouch_long", "id": 10238},
                             {"containerMountPoint": "/mnt/pretrained_models/bair_action_free/model.savp.transformation.flow.last_frames.2.generate_scratch_image.false.batch_size.16", "id": 9161},
                             {"containerMountPoint": "/mnt/pretrained_models/bair_action_free/model.multi_savp.ngf.64.shared_views.true.num_views.2.tv_weight.0.001.transformation.flow.last_frames.2.generate_scratch_image.false.batch_size.16", "id": 9223},
                             {"containerMountPoint": "/mnt/pretrained_models/bair_action_free/model.multi_savp.num_views.2.tv_weight.0.001.transformation.flow.last_frames.2.generate_scratch_image.false.batch_size.16", "id": 9387},
                             {"containerMountPoint": "/mnt/pretrained_models/lift_push_last_subsequence/vae/model.savp.tv_weight.0.001.transformation.flow.last_frames.2.generate_scratch_image.false.batch_size.16", "id":9534},
                             {"containerMountPoint": "/mnt/pretrained_models/bair_action_free/grasp_push_2views", "id": 9823},
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_startgoal_masks6e4", "id": 9138},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/mj_lift", "id": 10048},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/cartgripper_startgoal_2view_lift_above_obj", "id": 10061},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/cartgripper_startgoal_2view_lift", "id": 10188},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/ag_reopen_records", "id": 10401},
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_const_dist", "id": 9259},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_startgoal_short", "id": 8949},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_startgoal_2view", "id": 10476},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_startgoal_masks", "id": 8914},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_startgoal_3obj", "id": 9948},  # mj_pos_ctrl_appflow
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper", "id": 8350},  # cartgripper
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/cartgripper_lift_benchmark", "id": 9538},  # cartgripper
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_mj1.5", "id": 8974},
                             {"containerMountPoint": "/mnt/pushing_data/onpolicy/mj_pos_noreplan_fast_tfrec", "id": 8807},  #mj_pos_noreplan_fast_tfrec    | gtruth mujoco planning pushing
                             {"containerMountPoint": "/mnt/pushing_data/onpolicy/mj_pos_noreplan_fast_tfrec_fewdata", "id": 8972},
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/cartgripper_updown_sact", "id": 8931},
                             {"containerMountPoint": "/mnt/pushing_data/onpolicy/updown_sact_bounded_disc", "id": 9363},
                             {"containerMountPoint": "/mnt/pushing_data/cartgripper/grasping/ag_scripted_longtraj", "id": 10217},
                             {"containerMountPoint": "/mnt/pushing_data/sawyer_grasping/ag_long_records_15kfullres", "id": 11398}
                             ]

    data["aceInstance"] = "ngcv{}".format(ngpu)
    if interactive == 'True':
        command = "/bin/sleep 360000"
        data["name"] = 'int' + name

    elif fullcmd is not '':
        command = fullcmd
        data["name"] = name
    else:
        if 'trainvid' in run_script:
            command = "python " + run_script + " --hyper ../../" + hyper
            data["name"] = str.split(command, '/')[-2]
        else:
            if nsplit is not None:
                split = '--nsplit {} --isplit {}'.format(nsplit, isplit)
            else: split = ''
            command = "python " + run_script + " " + hyper + " --nworkers {} {}".format(nworkers, split)
            expname = hyper.partition('cem_exp')[-1]
            data["name"] = '-'.join(re.compile('\w+').findall(expname + split))

    data["command"] += command
    data["resultContainerMountPoint"] = "/result"
    data["publishedContainerPorts"] = [6006] #for tensorboard

    with open('autogen.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print('#######################')
    print('command', data["command"])

    if not bool(test):
        os.system("ngc batch run -f autogen.json")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='write json configuration for ngc')
    parser.add_argument('run_script', type=str, help='relative path to the script to launch', default="")
    parser.add_argument('hyper', type=str, help='relative path to hyperparams file', default="")
    parser.add_argument('--int', default='False', type=str, help='interactive')
    parser.add_argument('--nworkers', default=8, type=str, help='additional arguments')
    parser.add_argument('--name', default='', type=str, help='additional arguments')
    parser.add_argument('--ngpu', default=8, type=int, help='number of gpus')
    parser.add_argument('--test', default=0, type=int, help='testrun')
    parser.add_argument('--cmd', default='', type=str, help='full command')
    args = parser.parse_args()

    launch_job_func(args.run_script, args.hyper, args.nworkers, args.int, args.name, args.ngpu, args.test, fullcmd=args.cmd)

