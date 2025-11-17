/*
 * native/cpio/cpio_parser.h
 */
#ifndef CPIO_PARSER_H
#define CPIO_PARSER_H
#include <stdint.h>
#include <stddef.h>

/* Simple streaming feed callback */
typedef int (*cpio_feed_cb_t)(const unsigned char *buf, size_t len, void *userdata);

/* Parse a newc (070701) cpio stream from fd (starting at current pos).
   max_bytes: 0 = unlimited; otherwise cap total extracted payload processed.
   Returns 0 on success, negative on error.
*/
int cpio_parse_fd(int fd, uint64_t max_bytes, cpio_feed_cb_t feed, void *userdata);

#endif /* CPIO_PARSER_H */
