import pandas as pd
from causal_testing.specification.causal_dag import CausalDAG
from causal_testing.specification.variable import Input, Output
from causal_testing.specification.scenario import Scenario
from causal_testing.specification.causal_specification import CausalSpecification
from causal_testing.testing.causal_test_outcome import Positive
from causal_testing.testing.base_test_case import BaseTestCase
from causal_testing.testing.causal_test_case import CausalTestCase
from causal_testing.testing.causal_test_engine import CausalTestEngine
from causal_testing.data_collection.data_collector import ObservationalDataCollector
from causal_testing.testing.estimators import LinearRegressionEstimator

OBSERVATIONAL_DATA_PATH = "observational_data.csv"


def whatever(observational_data_path: str):
    past_execution_df = pd.read_csv(observational_data_path)
    _, causal_test_engine, causal_test_case = engine_setup(observational_data_path)

    linear_regression_estimator = LinearRegressionEstimator(
        ('edit_object',), 2, 3,
        {'create_object', 'delete_object'},
        ('grade',),
        df=past_execution_df
    )

    causal_test_result = causal_test_engine.execute_test(linear_regression_estimator, causal_test_case, 'ate')


def engine_setup(observational_data_path: str):
    causal_dag = CausalDAG('dag.dot')

    # variables
    create_object = Input('create_object', int)
    edit_object = Input('edit_object', int)
    delete_object = Input('delete_object', int)
    grade = Output('grade', int)

    # scenario
    scenario = Scenario(
        variables={
            create_object,
            edit_object,
            delete_object,
            grade
        },
        constraints={
            create_object.z3 == 3,
            edit_object.z3 == 3,
            delete_object.z3 == 3
        }
    )

    # causal specification
    causal_specification = CausalSpecification(scenario, causal_dag)

    base_test_case = BaseTestCase(
        treatment_variable=edit_object,
        outcome_variable=grade
    )

    causal_test_case = CausalTestCase(
        base_test_case=base_test_case,
        expected_causal_effect=Positive,
        control_value=3,
        treatment_value=2
    )

    data_collector = ObservationalDataCollector(scenario, observational_data_path)

    causal_test_engine = CausalTestEngine(causal_specification, data_collector)

    minimal_adjustment_set = causal_dag.identification(base_test_case)

    return minimal_adjustment_set, causal_test_engine, causal_test_case
