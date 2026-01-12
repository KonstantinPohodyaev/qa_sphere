from enum import StrEnum

class TagType(StrEnum):
    '''Типы тегов'''

    DATA = 'data'
    METADATA = 'metadata'
    SYSTEM = 'system'
    PIPELINE = 'pipeline'
    PIPELINE_VERSION = 'pipeline_version'
    PIPELINE_RUN = 'pipeline_run'
    PIPELINE_RUN_ARTIFACT = 'pipeline_run_artifact'