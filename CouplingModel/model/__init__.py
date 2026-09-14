from .model import Oxalate, LRChain, LRSquare, J1J2Square, IsingSquare

__all__ = ['Oxalate', 'LRChain', 'LRSquare', 'J1J2Square', "IsingSquare"]

REGISTRED_MODELS = {
    'Oxalate': Oxalate,
    'LRChain': LRChain,
    'LRSquare': LRSquare,
    'J1J2Square': J1J2Square,
    'IsingSquare': IsingSquare
}