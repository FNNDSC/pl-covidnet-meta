#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

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
parser.add_argument('-n', '--name', default='foo',
                    help='argument which sets example output file name')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='COVIDnet-meta',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE)

    output_file = outputdir / f'{options.name}.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()
