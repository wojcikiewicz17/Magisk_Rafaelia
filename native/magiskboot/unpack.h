/*
 * native/magiskboot/unpack.h
 *
 * Unpack API (MVP)
 *
 * Inputs:
 *   in_buf / in_sz - buffer containing full boot image
 *
 * Outputs (allocated, caller must free):
 *   *kernel_buf / *kernel_sz
 *   *ramdisk_buf / *ramdisk_sz
 *   *page_size - detected page size
 *   *has_vendor_boot - heuristic flag (0/1)
 *
 * Returns 0 on success, negative on error.
 */
int unpack_boot_image(const uint8_t *in_buf, size_t in_sz,
                      uint8_t **kernel_buf, size_t *kernel_sz,
                      uint8_t **ramdisk_buf, size_t *ramdisk_sz,
                      uint32_t *page_size, int *has_vendor_boot);

#endif /* RAFAELIA_UNPACK_H */
