#!/usr/bin/python
"""Usage: statcvs_wrapper.py DIRECTORY"""

import sys
import os
import os.path
import subprocess
import shutil
from format import FormatadorCVSReport
from prdg.util import proc

OUT_DIRNAME = 'cvs_report'
LOG_FILENAME = 'cvs_log.txt'

def main():
    if len(sys.argv) != 2:
        raise RuntimeError(__doc__)
    
    path = sys.argv[1]    
    if not os.path.isdir(path):
        raise RuntimeError('Argument should be a directory.')
        
    jar_path = os.environ.get('STATCVS_JAR_PATH')
    if not jar_path:
        raise RuntimeError('STATCVS_JAR_PATH environment variable not set.')
    
    
    os.chdir(path)
    
    temp_filename = LOG_FILENAME + '.tmp'
    proc.call_subprocess_to_file(['cvs', 'log'], temp_filename)
    proc.call_subprocess_to_file(['iconv', '-f latin1', '-t utf8', temp_filename], LOG_FILENAME)     
        
    if os.access(OUT_DIRNAME, os.F_OK):
        shutil.rmtree(OUT_DIRNAME)
    os.mkdir(OUT_DIRNAME)    
    
    subprocess.call([
        'java',
        '-jar',
        os.environ['STATCVS_JAR_PATH'], 
        '-output-dir', 
        OUT_DIRNAME,
        LOG_FILENAME, 
        '.'
    ])
    
    print >> sys.stderr, 'Formatando %s ...' % OUT_DIRNAME 
           
    formatador = FormatadorCVSReport()
    formatador.formatar(OUT_DIRNAME)    
    
    subprocess.call(['firefox', os.path.join(OUT_DIRNAME, 'index.html')])
    
    
    
    
