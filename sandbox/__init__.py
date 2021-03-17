"""
Module initialisation for sandbox
Created on 15/04/2020

@authors: Daniel Escallon, Simon Virgo, Miguel de la Varga
@Project Lead: Florian Wellmann
"""
# Main information for all the modules to work (calibration data, projector and sensor)
__version__ = '1.0'

# Panel body setting colors and other parameters
_panel_extension = False
def panel_extension():
    import panel as pn
    css = '''
        body {
          margin:0px;
          background-color: #FFFFFF;
        }
        .panel {
          background-color: #000000;
          overflow: hidden;
        }
        .bk.frame {
          background-color: #FFFFFF;
          color: #FFFFFF;
        }
        .bk.legend {
          background-color: #16425B;
          color: #CCCCCC;
        }
        .bk.hot {
          background-color: #2896A5;
          color: #CCCCCC;
        }
        .bk.profile {
          background-color: #40C1C7;
          color: #CCCCCC;
        }
        .bk.colorbar {
          background-color: #2896A5;
          color: #CCCCCC;
        '''
    pn.extension('vtk', raw_css=[css])
    _panel_extension = True
panel_extension()
import os
_package_dir = os.path.dirname(__file__)
_calibration_dir = os.path.abspath(os.path.dirname(__file__) + '/../notebooks/calibration_files/')+os.sep
_test_data = {'topo': os.path.abspath(os.path.dirname(__file__) +
                                      '/../notebooks/tutorials/06_LoadSaveTopoModule/saved_DEMs/')+os.sep,
              'landslide_topo': os.path.abspath(os.path.dirname(__file__) +
                                                '/../notebooks/tutorials/07_LandslideSimulation/saved_DEMs/')+os.sep,
              'landslide_release': os.path.abspath(os.path.dirname(__file__) +
                                                   '/../notebooks/tutorials/07_LandslideSimulation/'
                                                   'saved_ReleaseAreas/')+os.sep,
              'landslide_simulation': os.path.abspath(os.path.dirname(__file__) +
                                                      '/../notebooks/tutorials/07_LandslideSimulation/'
                                                      'simulation_data/')+os.sep,
              'gempy_data': os.path.abspath(os.path.dirname(__file__) +
                                            '/../notebooks/tutorials/04_GempyModule/Model_Construction/'
                                            'Bennisson_model/data/')+os.sep,
              'test': os.path.abspath(os.path.dirname(__file__) + '/../tests/test_data/')+os.sep,
              'landscape_generation': os.path.abspath(os.path.dirname(__file__) +
                                                      '/../notebooks/tutorials/09_LandscapeGeneration/')+os.sep
              }

# Create folders if not existing
# Topo folder
if not os.path.isdir(_test_data.get("topo")):
    os.mkdir(_test_data.get("topo"))

# Landslides folders
if not os.path.isdir(_test_data.get("landslide_topo")):
    os.mkdir(_test_data.get("landslide_topo"))
if not os.path.isdir(_test_data.get("landslide_release")):
    os.mkdir(_test_data.get("landslide_release"))
if not os.path.isdir(_test_data.get("landslide_simulation")):
    os.mkdir(_test_data.get("landslide_simulation"))

# Test folders
if not os.path.isdir(_test_data.get("test")):
    os.mkdir(_test_data.get("test"))
    os.mkdir(_test_data.get("test")+"temp")

# Landscape folders
if not os.path.isdir(_test_data.get("landscape_generation")+"checkpoints"):
    os.mkdir(_test_data.get("landscape_generation")+"checkpoints")
if not os.path.isdir(_test_data.get("landscape_generation")+"results"):
    os.mkdir(_test_data.get("landscape_generation")+"results")
if not os.path.isdir(_test_data.get("landscape_generation")+"saved_DEMs"):
    os.mkdir(_test_data.get("landscape_generation")+"saved_DEMs")
    os.mkdir(_test_data.get("landscape_generation") + "saved_DEMs/test")

# Gempy folders
if not os.path.isdir(_test_data.get("gempy_data")):
    os.mkdir(_test_data.get("gempy_data"))

# download sample files. If already downloaded they are ignored
from sandbox.utils.download_sample_datasets import (download_test_data,
                                                    download_topography_data,
                                                    download_landscape_name,
                                                    download_landscape_all)


if __name__ == '__main__':
    pass

