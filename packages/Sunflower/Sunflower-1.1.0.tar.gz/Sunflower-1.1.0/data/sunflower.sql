/* max probs size: <64KiB */
/* 12 bytes for a BLOB with 1 byte in it */
CREATE TABLE prob (
  tf_id TINYINT(3) UNSIGNED NOT NULL
      REFERENCES tf (tf_id),
  seq_region_id TINYINT(3) UNSIGNED NOT NULL
      REFERENCES seq_region (seq_region_id),
  seq_region_start INT(10) UNSIGNED NOT NULL,
  seq_region_end INT(10) UNSIGNED NOT NULL,
  probs BLOB NOT NULL,

  # PRIMARY KEY (tf_id, seq_region_id, seq_region_start),
  # UNIQUE KEY (tf_id, seq_region_id, seq_region_end),
  KEY (seq_region_id, seq_region_start, seq_region_end)
) MAX_ROWS=40000000000 AVG_ROW_SIZE=30;

CREATE TABLE tf (
  tf_id TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,

  PRIMARY KEY (tf_id),
  UNIQUE KEY (name)
);

CREATE TABLE seq_region (
  seq_region_id TINYINT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(40) NOT NULL,

  PRIMARY KEY (seq_region_id),
  UNIQUE KEY (name)
);
