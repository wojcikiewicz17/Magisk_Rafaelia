/*
 * native/bootimg/bootimg_parser.h
 * API para detecção e análise de boot images (RAFAELIA CAMADA 1)
 *
 * Principais funções:
 *   - parse_boot_image(): detecta versão/estrutura e preenche boot_image_info
 *
 * Estrutura retornada contém offsets e tamanhos para kernel, ramdisk, second,
 * dtbo/dtb, vendor_boot se detectado, além da page_size e header_bytes.
 *
 * O parser tenta:
 *   1) interpretar como v1 clássico (preferência)
 *   2) heurística para vendor_boot / v3/v4 (fallback)
 *
 * Retorna 0 em sucesso, negativo em erro.
 */
#ifndef RAFAELIA_BOOTIMG_PARSER_H
#define RAFAELIA_BOOTIMG_PARSER_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    RAF_BOOT_UNKNOWN = 0,
    RAF_BOOT_V1,
    RAF_BOOT_VENDOR, /* vendor_boot present */
    RAF_BOOT_V3,     /* heurística: newer header layout */
    RAF_BOOT_V4
} raf_boot_version_t;

struct boot_image_info {
    raf_boot_version_t version;
    uint32_t page_size;        /* page size used for alignment */
    size_t header_size;        /* bytes consumed by header region (page aligned) */

    /* kernel */
    size_t kernel_offset;
    size_t kernel_size;

    /* ramdisk */
    size_t ramdisk_offset;
    size_t ramdisk_size;

    /* second (optional) */
    size_t second_offset;
    size_t second_size;

    /* device tree / dtbo */
    size_t dtb_offset;
    size_t dtb_size;

    /* vendor_boot (if present) */
    int has_vendor_boot;
    size_t vendor_boot_offset;
    size_t vendor_boot_size;

    /* raw pointers into original buffer (optional convenience) */
    const uint8_t *raw_buf;
    size_t raw_buf_size;
};

/*
 * Parse the provided buffer (in_buf/in_sz) and fill boot_image_info.
 * This function does NOT allocate for payloads; it only computes offsets/sizes.
 *
 * Returns:
 *   0 on success (boot_image_info filled)
 *  -1 invalid args
 *  -2 not a recognizable boot image
 *  -3 buffer too small/incomplete
 */
int parse_boot_image(const uint8_t *in_buf, size_t in_sz, struct boot_image_info *out);

#ifdef __cplusplus
}
#endif

#endif /* RAFAELIA_BOOTIMG_PARSER_H */
