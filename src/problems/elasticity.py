import numpy as np
from mpi4py import MPI #parallelization
from dolfinx import mesh, fem, default_scalar_type
#dolfinx = FEniCS
from dolfinx.fem.petsc import LinearProblem
#petsc <- portable, extensible toolkit for scientific computation
import ufl #unified form language <- for mathmatical notation

#Goal: solve linear elasticity on a cantilever beam, uniform material.
Lx, Ly = 2.0, 1.0
nelx, nely = 60,20

domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    points = ((0.0,0.0), (Lx, Ly)),
    n = (nelx, nely),
    cell_type = mesh.CellType.quadrilateral
)
#Basis functions
V = fem.functionspace(domain, ("Lagrange", 1, (domain.geometry.dim,)))
E,nu =1.0, 0.3
mu = E/(2*(1+nu)) 
lmbda = E*nu /((1+nu)*(1-2*nu))
def sigma(u) -> ufl.core.expr.Expr:
    """Apply Hooke's law for 3D isotropic Materials to calculate 
    Cauchy Stress Tensor Matrix for every material point"""
    strain = ufl.sym(ufl.grad(u)) #stress tensor (symmetric)
    volumetric_change = ufl.tr(strain)
    identity_matrix = ufl.Identity(len(u))
    shear_stress = 2*mu*strain
    volumetric_stress = lmbda*volumetric_change*identity_matrix
    return shear_stress + volumetric_stress

def left_boundary(x) -> np.bool:
    """Function to determine if we are at left edge of mesch."""
    return np.isclose(x[0], 0.0, atol=0.05)

def right_boundary(x):
     """Function to determine if we are at right edge of mesch."""
     return np.isclose(x[0], Lx, atol=0.05)

fdim = domain.topology.dim-1
right_facets = mesh.locate_entities_boundary(domain, fdim, right_boundary)

facet_tags = mesh.meshtags(
    domain, fdim, right_facets, np.full_like(right_facets, 1, dtype=np.int32)
) #Edges in 2D
ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)

traction = fem.Constant(domain, default_scalar_type((0.0, -0.01))) #(force per unit length/area along edge

fixed_dofs = fem.locate_dofs_geometrical(V, left_boundary)
u_zero = np.zeros(domain.geometry.dim, dtype=default_scalar_type)
bc = fem.dirichletbc(u_zero, fixed_dofs, V)

body_force = fem.Constant(domain, (0.0,0.0))

#Weak form
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

a = ufl.inner(sigma(u), ufl.sym(ufl.grad(v))) * ufl.dx 
L = ufl.dot(body_force, v) * ufl.dx + ufl.dot(traction, v) * ds(1)

#Solve

problem = LinearProblem(
    a, L, bcs=[bc],
    petsc_options={"ksp_type": "preonly", "pc_type": "lu"},
    petsc_options_prefix="beam_elasticity", 
)
uh = problem.solve()

print("Max displacement:", np.max(np.abs(uh.x.array)))

