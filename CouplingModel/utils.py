import jax
import jax.numpy as jnp
import numpy as np

import time

def initial_state(Q):
    key=jax.random.PRNGKey(int(str(time.time()).split('.')[1]))
    return jax.random.uniform(key, shape=(1,6*Q+Q*(Q-1)//2),dtype='float64', minval=0.0, maxval=2*jnp.pi)[0]


def preprocess_energy_inputs(operators, onsites, couplings, S_operators):
    '''
    This function performs either preprocessing data and serves as a interface to switch between 
    models in order to calculate the Energy(). 
    
    It returns two index vectors indicating the implicated terms in Energy() calculation, following 
    the convention (X, Y, Z) = (0, 1, 2) and (XX, YY, ZZ) = (0, 1, 2). It also asserts that input 
    data type fits Energy() requirements and it's coherent with the chosen model (via terms).

    Inputs:

        - operators: (ArrayLike of str) Hamiltonian operators implicated in the model. 
                Example: terms = ['Z','ZZ','X'].

        - onsites: (ArrayLike) Strenght of the field in each considered component. Must have the same 
                length as the number of field terms in "terms" and must be put in order 
                (onsites_x, onsites_y, onsites_z). Example: onsites=(onsites_x, onsites_z).

        - couplings: (ArrayLike) Set of matrices describing the coupling strenght in each component
                    considered in the model. Must have the same length as the number of field terms 
                    in "terms" and must be put in order (J_xx, J_yy, J_zz).

    Outputs:

        - onsite_terms_idx: (jnp.array(int)) Index vector of field terms acording to convention.

        - coupling_terms_idx: (jnp.array(int)) Index vector of cross terms acording to convention.

            Example: 
                                                  onsite_terms_idx = Array([0, 2], dtype=int64)
                  terms = ['Z','ZZ','X']  ---->
                                                  coupling_terms_idx = Array([2], dtype=int64)

        - onsites: (jnp.array(float64)) Preprocessed onsites array.

        - couplings: (jnp.array(float64)) Preprocessed couplings.
    '''
    convention = {'X': 0, 'Y':1, 'Z':2}
   
    if len(jnp.shape(couplings)) == 2:    couplings= jnp.array([couplings])

    control = [char in list(convention.keys()) 
               for op_group in operators 
               for op in op_group 
               for char in op]
    
    assert all(control), f"All operands must be {list(convention.keys())} or pairs of them"
    
    onsites = jnp.array(onsites) 
    couplings = jnp.array(couplings)

    onsite_terms_idx = jnp.array([convention[op] for op in operators[0]], dtype='int32')
    coupling_terms_idx = jnp.array([[convention[letter] for letter in op] for op in operators[1]], dtype='int32')
 
    if len(onsite_terms_idx) != jnp.shape(onsites)[0]:
        raise ValueError(f"There must be the same number of field terms and onsites, "
                         f"but there {len(onsite_terms_idx)} field terms and {jnp.shape(onsites)[0]} onsites")

    if len(coupling_terms_idx) != jnp.shape(couplings)[0]:
        raise ValueError(f"There must be the same number of cross terms and couplings components, "
                         f"but there are {len(coupling_terms_idx)} field terms and {jnp.shape(couplings)[0]} couplings")

    if S_operators:
        onsites /= 2
        couplings /= 4

    else:
        pass
    
    return  onsites, couplings, onsite_terms_idx, coupling_terms_idx

