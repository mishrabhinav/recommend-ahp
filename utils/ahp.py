import pickle

import numpy as np
import pyahp
from flask import _request_ctx_stack
from pymongo import DESCENDING

from matrix.core import Matrix, enumerize, DEFAULT_SETTINGS
from matrix.enums import Cost, Duration, Mode
from models import Rules


def _construct_preference_matrix(rule_matrix: Matrix, criterion, alternatives, forecasts, settings):
    side = len(alternatives)
    norm_alts = [enumerize(alt['legs'][0], forecasts, settings) for alt in alternatives]
    pm = np.full((side, side), 1, dtype='float')

    for i in range(side):
        for j in range(i + 1, side):
            preference = rule_matrix.compare(criterion, norm_alts[i], norm_alts[j])
            pm[i][j] = preference
            pm[j][i] = 1.0 / preference

    return pm


def _run_individual_ahp(username, alternatives: list, forecasts, settings=DEFAULT_SETTINGS):
    rules = Rules.objects.raw({'user': username}).order_by([('created_on', DESCENDING)]).limit(1)

    if rules.count():
        rule_matrix: Matrix = pickle.loads(rules.first().rules)
    else:
        rule_matrix = Matrix([], {})

    cost_pm = _construct_preference_matrix(rule_matrix, Cost, alternatives, forecasts, settings)
    duration_pm = _construct_preference_matrix(rule_matrix, Duration, alternatives, forecasts, settings)
    mode_pm = _construct_preference_matrix(rule_matrix, Mode, alternatives, forecasts, settings)

    model_dict = {
        'name': 'Recommend AHP Model',
        'method': 'approximate',
        'criteria': ['cost', 'duration', 'mode'],
        'subCriteria': {},
        'alternatives': [str(idx) for idx in range(len(alternatives))],
        'preferenceMatrices': {
            'criteria': np.full((3, 3), 1),
            'alternatives:cost': cost_pm,
            'alternatives:duration': duration_pm,
            'alternatives:mode': mode_pm
        }
    }

    return pyahp.parse(model_dict).get_priorities()


def run_ahp(alternatives: list, forecasts, group, settings=DEFAULT_SETTINGS):
    group_priorities = []

    for user in group:
        group_priorities.append(_run_individual_ahp(user, alternatives, forecasts, settings))

    num_users = len(group)
    num_alternatives = len(alternatives)

    results = []

    for i in range(num_alternatives):
        pref = 1
        for j in range(num_users):
            pref *= group_priorities[j][i]**(1/num_users)

        results.append(pref)

    return results
