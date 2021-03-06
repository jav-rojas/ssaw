from os.path import join
from tempfile import gettempdir

from pytest import raises

from ssaw import ExportApi
from ssaw.exceptions import NotFoundError
from ssaw.models import ExportJob

from . import my_vcr


@my_vcr.use_cassette()
def test_export_notfound(session):
    with raises(NotFoundError):
        assert ExportApi(session).get_info(123)


@my_vcr.use_cassette()
def test_export_info(session, params):

    r = ExportApi(session).get_info(params['JobId'])
    assert isinstance(r, ExportJob), 'Should get back an ExportJob object'
    assert r.job_id == params['JobId'], "Should get back the same job id"


@my_vcr.use_cassette()
def test_export_cancel(session, params):
    r = ExportApi(session).cancel(params['JobId'])
    assert r is None, 'Does not return anything'


@my_vcr.use_cassette()
def test_export_start(session, params):
    job = ExportJob(params['QuestionnaireId'])
    r = ExportApi(session).start(job)
    assert isinstance(r, ExportJob), "Should get back the created job"


@my_vcr.use_cassette()
def test_export_get(session, params):
    tempdir = gettempdir()
    r = ExportApi(session).get(questionnaire_identity=params['QuestionnaireId'],
                               export_path=tempdir, export_type='Tabular')
    assert r == join(tempdir, 'health_survey_1_Tabular_All.zip')
