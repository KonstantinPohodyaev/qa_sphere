from crud.base import BaseCRUD
from models.pipeline import Pipeline
from schemas.pipeline import PipelineCreate, PipelineUpdate


class PipelineCRUD(BaseCRUD[Pipeline, PipelineCreate, PipelineUpdate]):
    '''CRUD для Pipeline'''
    model = Pipeline
    create_schema = PipelineCreate
    update_schema = PipelineUpdate


pipeline_crud = PipelineCRUD(Pipeline)
