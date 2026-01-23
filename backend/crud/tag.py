from crud.base import CRUDBase
from models.tag import Tag
from schemas.tag import TagCreate, TagUpdate, TagRead

class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    pass


tag_crud = CRUDTag(Tag)
