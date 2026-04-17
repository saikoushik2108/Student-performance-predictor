from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def create_model():
    model = DiscreteBayesianNetwork([
        ('StudyHours', 'Performance'),
        ('Attendance', 'Performance'),
        ('Sleep', 'Performance'),
        ('Motivation', 'Performance'),
        ('PreviousGrades', 'Performance')
    ])

    # Priors
    cpd_study = TabularCPD('StudyHours', 3, [[0.3], [0.4], [0.3]])
    cpd_attendance = TabularCPD('Attendance', 3, [[0.2], [0.5], [0.3]])
    cpd_sleep = TabularCPD('Sleep', 3, [[0.3], [0.5], [0.2]])
    cpd_motivation = TabularCPD('Motivation', 3, [[0.3], [0.4], [0.3]])
    cpd_grades = TabularCPD('PreviousGrades', 3, [[0.3], [0.4], [0.3]])

    # Performance CPD (simplified but realistic pattern)
    # Total combinations = 3^5 = 243
    # We'll generate values programmatically instead of typing manually

    import numpy as np

    pass_probs = []

    for study in range(3):
        for attendance in range(3):
            for sleep in range(3):
                for motivation in range(3):
                    for grades in range(3):

                        score = (
                            study * 0.25 +
                            attendance * 0.2 +
                            sleep * 0.15 +
                            motivation * 0.2 +
                            grades * 0.2
                        )

                        prob = min(0.1 + (score / 2.5), 0.99)
                        pass_probs.append(prob)

    pass_probs = np.array(pass_probs)
    fail_probs = 1 - pass_probs

    cpd_performance = TabularCPD(
        variable='Performance',
        variable_card=2,
        values=[pass_probs, fail_probs],
        evidence=['StudyHours', 'Attendance', 'Sleep', 'Motivation', 'PreviousGrades'],
        evidence_card=[3, 3, 3, 3, 3]
    )

    model.add_cpds(
        cpd_study, cpd_attendance, cpd_sleep,
        cpd_motivation, cpd_grades,
        cpd_performance
    )

    model.check_model()

    return VariableElimination(model)