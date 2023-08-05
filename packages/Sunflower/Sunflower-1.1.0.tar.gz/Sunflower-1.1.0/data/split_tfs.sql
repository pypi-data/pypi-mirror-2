CREATE TABLE probs_TBP
       SELECT prob.seq_region_id, prob.seq_region_start, prob.seq_region_end,
              prob.probs
         FROM prob, tf
         WHERE prob.tf_id = tf.tf_id AND tf.name = "TBP";
# XXX: indexes need to be added
