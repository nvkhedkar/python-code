import multiprocessing
import numpy as np
import trimesh
from pyglet import gl
import pyvista as pv
import argparse
import os, re, sys, logging, time
from datetime import datetime
from glob import glob

LOG_FORMAT = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s'

import logging
logFormatter = logging.Formatter(LOG_FORMAT)


def get_loggers(id, toconsole=True):
    _logger = logging.getLogger(f'lg{id}')
    _logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(f"{os.path.splitext(os.path.basename(__file__))[0]}_train_{id}.log")
    fileHandler.setFormatter(logFormatter)
    _logger.addHandler(fileHandler)

    if toconsole:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        _logger.addHandler(consoleHandler)
    return _logger


def get_console_loggers(id):
    _logger = logging.getLogger(f'lgc{id}')
    _logger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _logger.addHandler(consoleHandler)
    return _logger


def get_file_loggers(id):
    _logger = logging.getLogger(f'lg{id}')
    _logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(f"{os.path.splitext(os.path.basename(__file__))[0]}_train_{id}.log")
    fileHandler.setFormatter(logFormatter)
    _logger.addHandler(fileHandler)
    return _logger


logger = get_loggers(9)
chunksize, npools = 100, 3


class LogArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        logger.error(msg)
        sys.exit(1)
        # raise Exception(msg)


parser = LogArgumentParser()

BASE_PATH = './data_obj'
OBJ_PATH = f'{BASE_PATH}/raw'
OUT_PATH = f'{BASE_PATH}/img'
DATA_TYPE = ['train']
angles = [
    [1., 0., 0.5],
    [0.8660254, 0.5, 0.5],
    [0.5, 0.8660254, 0.5],
    [0., 1., 0.5],
    [-0.5, 0.8660254, 0.5],
    [-0.8660254,  0.5, 0.5],
    [-1., 0.,  0.5],
]


class MeshWorks:
    def __init__(self, id=1):
        self.mf = ''
        self.logger = get_file_loggers(id)
        self.clogger = get_console_loggers(id)
        self.id = id

    def load_mesh(self, root, filename, full):
        mesh = trimesh.load_mesh(full)
        return mesh

    def read_mesh(self, root, filename, full):
        mesh = trimesh.load_mesh(full)
        print(full, mesh.is_watertight)
        sm = trimesh.exchange.stl.export_stl_ascii(mesh)
        # sm.export(f'{root}/{filename}.stl')
        with open(f'{root}/{filename}.stl', 'w') as f:
            f.write(sm + "\n")

    def mesh_to_png(self, root, filename, full):
        mesh = trimesh.load_mesh(full)
        scene = mesh.scene()

        window_conf = gl.Config(double_buffer=True, depth_size=24)
        gl.glMatrixMode(gl.GL_PROJECTION)
        png = scene.save_image(resolution=[1080, 1080],
                               window_conf=window_conf)

        print('rendered bytes:', len(png))
        # write the render to a volume we should have docker mounted
        with open(f'{root}/{filename}.png', 'wb') as f:
            f.write(png)

    def get_plotter(self):
        plotter = pv.Plotter(off_screen=True, window_size=[512, 512],
                             # lighting='none'
                             )
        plotter.set_background('white')
        plotter.view_isometric()
        hdlight = pv.Light(light_type='headlight',
                           # intensity=0.5
                           )
        # plotter.add_light(hdlight)
        return plotter

    def pyvista_clip(self, name, root, filename, full, cs=4):
        mesh = trimesh.load_mesh(full)
        pvmesh = pv.wrap(mesh)
        bounds = pvmesh.bounds

        # p.add_mesh(mesh, style='wireframe', color='blue', label='Input')
        def clip_solid(_bounds, axis, n=8, _cs=cs):
            print(axis)
            normal, i, j = [1, 0, 0], 0, 1
            if axis == 'y':
                normal, i, j = [0, 1, 0], 2, 3
            if axis == 'z':
                normal, i, j = [0, 0, 1], 4, 5
            clipped = []
            for k in range(n):
                bnds = float(_bounds[j] - _bounds[i]) / float(n + 1)
                bnd_depth = bnds / 2.
                clip_bounds = list(_bounds)
                for m in range(6):
                    if m % 2 == 0:
                        clip_bounds[m] = clip_bounds[m] - 0.1
                    else:
                        clip_bounds[m] = clip_bounds[m] + 0.1
                _loc = bnds * (k + 1)
                # clip_bounds[i] = _loc
                clip_bounds[j] = _loc # + bnd_depth
                print(axis, k)
                # clipped.append()
                clipped = pvmesh.clip_box(clip_bounds, invert=False)
                plotter = self.get_plotter()
                plotter.add_mesh(clipped,
                                 color=[0.3, 0.5, 0.8],
                                 specular=1,
                                 )
                edges = clipped.extract_feature_edges(15)
                plotter.add_mesh(edges, color=[0.1, 0.1, 0.2],
                                 line_width=1.35,
                                 )

                plotter.view_vector(normal)

                plotter.screenshot(f'{root}/{name}_clip_{axis}{k + 1:03}_{_cs:02}.png', transparent_background=False)
                _cs += 1
            return _cs
            print(cs)
            cs = clip_solid(bounds, 'x', _cs=cs)
            print(cs)
            cs = clip_solid(bounds, 'y', _cs=cs)
            print(cs)
            cs = clip_solid(bounds, 'z', _cs=cs)

    def log_only_file(self, name, outpath, filename, full):
        prefix = os.path.splitext(filename)[0]
        self.logger.info(f'{outpath}/{prefix}_{name}_{self.id}_00.png')
        return

    def pyvista_mesh(self, name, root, filename, full):
        # print(full)
        self.clogger.info(f'|{filename}|{name}')
        splitfull = os.path.split(full)
        self.logger.info(f'|{full}|{name}|start')
        prefix = os.path.splitext(filename)[0]
        self.logger.info(f'|{filename}|load mesh')
        mesh = trimesh.load_mesh(full)
        watertight = mesh.is_watertight
        if watertight:
            watertight = 1
        else:
            watertight = 0
        self.logger.info(f'|{filename}|load mesh done|watertight: {watertight}')

        plotter = pv.Plotter(off_screen=True, window_size=[512, 512],
                             # lighting='none'
                             )
        plotter.set_background('white')# [0.9, 0.9, 0.9], top='white')
        plotter.view_isometric()
        hdlight = pv.Light(light_type='headlight',
                           intensity=0.75
                           )
        # plotter.enable_eye_dome_lighting()
        plotter.enable_3_lights()
        plotter.add_light(hdlight)

        try:
            self.logger.info(f'|{filename}|convert to pvmesh')
            pvmesh = pv.wrap(mesh)
            self.logger.info(f'|{filename}|extract edges')
            edges = pvmesh.extract_feature_edges(15, boundary_edges=True,
                                                 non_manifold_edges=False,
                                                 feature_edges=True,
                                                 manifold_edges=False)
            actor = plotter.add_mesh(pvmesh,
                                     color=[0.5, 0.5, 0.5],
                                     # specular=0.8,
                                     # smooth_shading=True,
                                     # pbr=True,
                                     # metallic=0.8,
                                     # roughness=0.1,
                                     # diffuse=1
                                     )
            try:
                self.logger.info(f'|{filename}|add edges')
                plotter.add_mesh(edges, color=[0.25, 0.25, 0.25],
                                 line_width=1.35,
                                 )
            except Exception as e:
                import traceback, sys
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.logger.error(f'Exception: File: {root}/{prefix}.obj | {watertight} | {exc_type} | value: {exc_value}\n')
                with open(f'exceptions{self.id}.txt', 'a') as f:
                    f.write(f"Exception: File: {root}/{prefix}.obj | {watertight} | {exc_type} | value: {exc_value}\n")

            base_name = f'{prefix}_{name}_{watertight}'
            self.logger.info(f'|{filename}|screenshot start')
            for va in [x for x in range(7)]:
                plotter.view_vector(angles[va])
                plotter.screenshot(f'{root}/{base_name}_t0{va}.png', transparent_background=False)
                self.logger.info(f'|{filename}|screenshot {va}')

            plotter.clear()
            with open(f'good_files_{self.id}.txt', 'a') as f:
                f.write(f"Good File: {root}/{prefix}.obj | watertight: {watertight}\n")
        except Exception as e:
            import traceback, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.error(f'Exception: File: {root}/{prefix}.obj | {watertight} | {exc_type} | value: {exc_value}\n')
            with open(f'exceptions{self.id}.txt', 'a') as f:
                f.write(f"Exception: File: {root}/{prefix}.obj | watertight: {watertight} | {exc_type} | value: {exc_value}")
            plotter.clear()
        self.logger.info(f'|{full}|finished -------------------------------')

    def pyvista_slices(self, root, filename, full):
        mesh = trimesh.load_mesh(full)
        pvmesh = pv.wrap(mesh)
        edges = pvmesh.extract_feature_edges(30)
        plotter = self.get_plotter()
        slices = pvmesh.slice_along_axis(n=10, axis='x', generate_triangles=True)
        # plotter.view_vector([1, 0, 0])
        # for i in range(3):
        plotter.add_mesh(slices, color=[0.1, 0.3, 0.5], line_width=1)
        plotter.screenshot(f'{root}/{filename}_slice_x.png', transparent_background=False)
        # plotter.view_isometric()

    def run_list(self, arrin, begin):
        cnt = begin
        for f in arrin:
            splitf = os.path.split(f)
            dirname, filename, cls = os.path.dirname(f), splitf[-1], splitf[-2]
            cnt += 1
            name = f'color_{cnt:04}'
            outpath = re.sub(OBJ_PATH, OUT_PATH, dirname)
            self.pyvista_mesh(name, outpath, filename[:-4], f)
            continue

    def start(self, indir, outdir):
        if os.path.exists('./good_files.txt'):
            os.unlink('./good_files.txt')
        if os.path.exists('./exceptions.txt'):
            os.unlink('./exceptions.txt')
        for root, dirnames, filenames in os.walk(indir):
            root = re.sub(r'\\', "/", root)
            cnt = 0
            for filename in filenames:
                full = f'{root}/{filename}'
                splitroot = os.path.split(root)
                if splitroot[-1] in ['bearing', 'bushing', 'castors_and_wheels', 'clamp',
                                     'disc', 'fitting',  'flange', 'fork_joint',
                                     'gear', 'handles', 'hinge', 'hook', 'motor', 'nut', 'pin']:
                    print(f'skip: {full}')
                    continue
                if splitroot[-1] not in ['screws_and_bolts']:
                    continue
                if (filename.endswith('obj')
                    and not re.search('^color', filename)):
                    cnt += 1
                    name = f'color_{cnt:04}'

                    outpath = re.sub(OBJ_PATH, OUT_PATH, root)
                    # print(outpath, name)
                    if not os.path.exists(outpath):
                        os.makedirs(outpath)
                    self.pyvista_mesh(name, outpath, filename[:-4], full)

                    # self.pyvista_clip(name, outpath, filename, full)


def task(files, i, id):
    print('Sleeping for 0.5 seconds')
    print(len(files), files[0], i*100, i*100+100, id)
    # print(os.path.dirname(files[0]), os.path.split(files[0])[-1])
    time.sleep(1)
    print('Finished sleeping')


def run_list_only_files(arrin, begin, poolid):
    cnt = begin * chunksize
    for f in arrin:
        splitf = os.path.split(f)
        dirname, filename, cls = os.path.dirname(f), splitf[-1], splitf[-2]
        cnt += 1
        name = f'color_{cnt:05}'
        outpath = re.sub(OBJ_PATH, '', dirname)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        mw = MeshWorks(id=poolid)
        mw.log_only_file(name, outpath, filename[:-4], f)
        prefix = os.path.splitext(filename[:-4])[0]
        logger.info(f'{outpath}/{prefix}_{name}_{poolid}_00.png')


def run_list(arrin, begin, poolid, _chunksize):
    cnt = begin * _chunksize
    for f in arrin:
        splitf = os.path.split(f)
        dirname, filename, cls = os.path.dirname(f), splitf[-1], splitf[-2]
        cnt += 1
        name = f'color_{cnt:05}'
        outpath = re.sub(OBJ_PATH, OUT_PATH, dirname)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        mw = MeshWorks(id=poolid)
        mw.pyvista_mesh(name, outpath, filename[:-4], f)


def create_chunks(arr, _chunksize):
    return [arr[i:i + _chunksize] for i in range(0, len(arr), _chunksize)]


# def filter_class(x, class_name):
#     if class_name in x:
#         return x

if __name__ == "__main__":
    start_time = time.perf_counter()
    # processes = []
    allfiles = [str(f) for f in glob(f'{OBJ_PATH}/{DATA_TYPE[0]}/**/*.obj')]
    print(allfiles)
    classes = list(set([os.path.basename(os.path.split(x)[-2]) for x in allfiles]))
    print(classes)

    for cls in classes:
        cls_list = list(filter(lambda x: cls in x, allfiles))
        npools = 4
        chunksize = len(cls_list) // npools
        if chunksize > 100:
            chunksize = 100
        if chunksize == 0:
            chunksize = len(cls_list)
        logger.info(f'{cls}, {len(cls_list)}, {chunksize}, {npools}')
        chunks = create_chunks(cls_list, chunksize)
        for i in range(0, len(chunks), npools):
            processes = []
            for j in range(npools):
                ii = i + j
                if ii >= len(chunks):
                    continue
                logger.info(f'class: {cls}, n: {len(cls_list)}, chunk: {i}, pool: {j}, begin: {ii}')
                x = chunks[ii]
                p = multiprocessing.Process(target=run_list, args=(x, ii, ii % npools, chunksize))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()

    sys.exit()

