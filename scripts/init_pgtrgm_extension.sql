-- #!/bin/sh
-- psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOF
-- CREATE EXTENSION pg_trgm;
-- SELECT * FROM pg_extension;
-- SET pg_trgm.similarity_threshold = 0.7;
-- EOF

CREATE EXTENSION pg_trgm;
SELECT * FROM pg_extension;
SET pg_trgm.similarity_threshold = 0.7;