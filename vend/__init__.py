import os
import sys

v_path = os.path.sep.join([
    os.path.dirname(os.path.realpath(__file__)), 'vendor'])
if os.path.isdir(v_path):
    sys.path.append(v_path)
