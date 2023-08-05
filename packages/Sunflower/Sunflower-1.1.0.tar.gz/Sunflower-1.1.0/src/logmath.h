#include <math.h>
#include <stdio.h>

static inline double _logadd(const double p, const double q) {
  return p + log1p(exp(q - p));
}

static inline double logadd(const double p, const double q) {
  return (p > q) ? _logadd(p, q) : _logadd(q, p);
}
