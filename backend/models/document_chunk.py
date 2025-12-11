from sqlalchemy import Column, Integer, String, BigInteger, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy import text
from core.database import Base  # Assuming Base is defined in core.database, need to verify/create that too.

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(BigInteger, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb")) # metadata is reserved in SQLAlchemy
    embedding = Column(Vector(768))

    # HNSW Index definition matching SQL
    __table_args__ = (
        Index(
            "document_chunks_embedding_idx",
            embedding,
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
