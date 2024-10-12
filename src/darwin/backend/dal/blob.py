from typing import Optional
from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Blob as M_Blob, BlobId
from darwin.backend.schemas import Blob as S_Blob


class BlobDal(Dal_I):
    def create(self, blob: M_Blob):
        with self.db_session() as db:
            db_blob = S_Blob(
                id=blob.id,
                location_type=blob.location_type,
                reference=blob.reference,
            )
            db.add(db_blob)
    
    def get(self, blob_id: BlobId) -> Optional[M_Blob]:
        with self.db_session() as db:
            maybe_blob = db.get(S_Blob, blob_id)
            if maybe_blob is None:
                return None
            return M_Blob.model_validate(maybe_blob)
    