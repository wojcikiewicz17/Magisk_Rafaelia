/*
 * native/repack/repack.h
 *
 * Repack API (MVP)
 * - in_buf/in_sz: original boot image buffer
 * - out_buf/out_sz: pointer to malloc'd buffer (free by caller)
 * - devpatch: if nonzero, apply developer-light patching (minimal, non-destructive)
 * - force: override policies
 * Returns 0 on success, negative on error.
 */
int repack_boot_image(const uint8_t *in_buf, size_t in_sz, uint8_t **out_buf, size_t *out_sz, int devpatch, int force);

#endif /* REPACK_H */
