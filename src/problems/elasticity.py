import numpy as np
from mpi4py import MPI #parallelization
from dolfinx import mesh, fem, default_scalar_type
#dolfinx = FEniCS
from dolfinx.fem.petsc import LinearProblem
#petsc <- portable, extensible toolkit for scientific computation
import ufl #unified form language <- for mathmatical notation

# Simple Cantilever FEa problem <- rigid beam/truss
nelx, nely = 60,20
