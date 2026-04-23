from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np

def create_model():
    model = DiscreteBayesianNetwork([
        ('IQ', 'LearningAbility'),
        ('LearningAbility', 'Performance'),

        ('StudyHours', 'Performance'),
        ('Attendance', 'Performance'),
        ('Sleep', 'Performance'),
        ('Motivation', 'Performance'),
        ('PreviousGrades', 'Performance')
    ])

    # Priors
    cpd_iq = TabularCPD('IQ', 3, [[0.3], [0.4], [0.3]])

    cpd_study = TabularCPD('StudyHours', 3, [[0.3], [0.4], [0.3]])
    cpd_attendance = TabularCPD('Attendance', 3, [[0.2], [0.5], [0.3]])
    cpd_sleep = TabularCPD('Sleep', 3, [[0.3], [0.5], [0.2]])
    cpd_motivation = TabularCPD('Motivation', 3, [[0.3], [0.4], [0.3]])
    cpd_grades = TabularCPD('PreviousGrades', 3, [[0.3], [0.4], [0.3]])

    # IQ → Learning Ability
    cpd_learning = TabularCPD(
        variable='LearningAbility',
        variable_card=3,
        values=[
            [0.7, 0.3, 0.1],
            [0.2, 0.5, 0.3],
            [0.1, 0.2, 0.6]
        ],
        evidence=['IQ'],
        evidence_card=[3]
    )

    # Generate Performance Probabilities
    pass_probs = []

    for la in range(3):
        for study in range(3):
            for attendance in range(3):
                for sleep in range(3):
                    for motivation in range(3):
                        for grades in range(3):

                            score = (
                                la * 0.25 +
                                study * 0.2 +
                                attendance * 0.15 +
                                sleep * 0.1 +
                                motivation * 0.15 +
                                grades * 0.15
                            )

                            prob = min(0.1 + (score / 3.0), 0.99)
                            pass_probs.append(prob)

    pass_probs = np.array(pass_probs)
    fail_probs = 1 - pass_probs

    cpd_performance = TabularCPD(
        variable='Performance',
        variable_card=2,
        values=[pass_probs, fail_probs],
        evidence=[
            'LearningAbility',
            'StudyHours',
            'Attendance',
            'Sleep',
            'Motivation',
            'PreviousGrades'
        ],
        evidence_card=[3,3,3,3,3,3]
    )

    model.add_cpds(
        cpd_iq, cpd_learning,
        cpd_study, cpd_attendance, cpd_sleep,
        cpd_motivation, cpd_grades,
        cpd_performance
    )

    model.check_model()

    return VariableElimination(model)