#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin, PathMapper

import shutil
import copy
import json

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _                      _     _            _                         _
      | |                    (_)   | |          | |                       | |
 _ __ | |______ ___ _____   ___  __| |_ __   ___| |_ ______ _ __ ___   ___| |_ __ _
| '_ \| |______/ __/ _ \ \ / / |/ _` | '_ \ / _ \ __|______| '_ ` _ \ / _ \ __/ _` |
| |_) | |     | (_| (_) \ V /| | (_| | | | |  __/ |_       | | | | | |  __/ || (_| |
| .__/|_|      \___\___/ \_/ |_|\__,_|_| |_|\___|\__|      |_| |_| |_|\___|\__\__,_|
| |
|_|
"""


parser = ArgumentParser(description='A ChRIS plugin that analyzes an upstream COVID prediction.json file and, if COVID infection inferred, will exit with an exception. This has the effect of coloring the node red in the DAG representation.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-p', '--predictionGlob', default='**/prediction-default.json',
                    help='the upstream prediction file glob (for multiprediction)')
parser.add_argument('-P', '--prediction', default = '',
                    help='single prediction file')

parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')

@staticmethod
def run_one(options):
    # fetch input data and copy to output
    with open('{}/prediction-default.json'.format(options.inputdir)) as f:
      classification_data = json.load(f)
    shutil.copy('{}/prediction-default.json'.format(options.inputdir),
                '{}/prediction-default.json'.format(options.outputdir))

    print("COVID infection probability: %f" % round(float(classification_data['COVID-19'])*100, 2))

    if classification_data['prediction'] == "COVID-19":
        print("")
        print("This plugin will raise an exception which, if run in the ChRIS UI will")
        print("Have the effect of coloring this node in the compute graph RED.")
        print("")
        raise Exception("COVID infection inferred!")

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='COVIDnet-meta',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='4Gi',      # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)
    print('Version: %s' % f'{__version__}')

    if options.prediction:
        run_one(options)
    else:
        mapper = PathMapper.file_mapper(
            input_dir=Path(options.inputdir),
            output_dir=Path(options.outputdir),
            glob=options.predictionGlob
        )
        for sub_input, sub_output in mapper:
            sub_options = copy.copy(options)
            sub_options.prediction = str(sub_input.name)
            sub_options.inputdir = str(sub_input.parent)
            sub_options.outputdir = str(sub_output.parent)
            run_one(sub_options)

    output_file = outputdir / f'{__pkg}.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()
