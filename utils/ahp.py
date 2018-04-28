import numpy as np

import pyahp


def run_ahp(alternatives: list):
    side = len(alternatives)

    model_dict = {
        'name': 'Recommend AHP Model',
        'method': 'approximate',
        'criteria': ['cost', 'duration', 'mode'],
        'subCriteria': {},
        'alternatives': alternatives,
        'preferenceMatrices': {
            'criteria': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            'alternatives:cost': np.full((side, side), 1),
            'alternatives:duration': np.full((side, side), 1),
            'alternatives:mode': np.full((side, side), 1)
        }
    }

    return pyahp.parse(model_dict).get_priorities()
