"""Produces the projection onto the symmetric subspace."""
from itertools import permutations
import numpy as np
import scipy as sp
from toqito.perms.permutation_operator import permutation_operator


def symmetric_projection(dim: int,
                         p_val: int = 2,
                         partial: bool = False) -> np.ndarray:
    """
    Produce the projection onto the symmetric subspace.

    Produces the orthogonal projection onto the symmetric subspace of `p`
    copies of `dim`-dimensional space. If `partial = True`, then the symmetric
    projection (PS) isn't the orthogonal projection itself, but rather a matrix
    whose columns form an orthonormal basis for the symmetric subspace (and
    hence the PS * PS' is the orthogonal projection onto the symmetric
    subspace.)

    :param dim: The dimension of the local systems.
    :param p_val: Default value of 2.
    :param partial: Default value of 0.
    :return: Projection onto the symmetric subspace.
    """
    dimp = dim**p_val

    if p_val == 1:
        return sp.sparse.eye(dim)

    p_list = np.array(list(permutations(np.arange(1, p_val+1))))
    p_fac = np.math.factorial(p_val)
    sym_proj = sp.sparse.lil_matrix((dimp, dimp))

    for j in range(p_fac):
        sym_proj += permutation_operator(dim*np.ones(p_val), p_list[j, :], False, True)
    sym_proj = sym_proj/p_fac

    if partial:
        sym_proj = sym_proj.todense()
        sym_proj = sp.sparse.lil_matrix(sp.linalg.orth(sym_proj))
    return sym_proj