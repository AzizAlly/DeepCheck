# Project information module
__author__ = "Aziz Ali"
__email__ = "alyyaziz45@gmail.com"
__supervisor__ = "Mr. Hassan"
__project__ = "DeepCheck"
__version__ = "1.0.0"
__description__ = "Deepfake Detection System - University Project"

def get_project_info():
    return {
        "project": __project__,
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "supervisor": __supervisor__,
        "description": __description__
    }
