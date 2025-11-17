/*
 * native/bootimg/bootimg.h
 * RAFAELIA — Boot image header definitions + utilities (MVP universal)
 *
 * Este header define:
 *  - boot image v1 minimal header (AOSP)
 *  - utility align_to()
 *  - constantes e macros úteis para parser/repack
 *
 * Nota: Esta implementação é intencionalmente defensiva e compatível com o
 * MVP do RAFAELIA_MAGISKBOOT_Ω. Para produção, substitua por headers AOSP
 * oficiais / up-to-date quando necessário.
 */
#ifndef RAFAELIA_BOOTIMG_H
#define RAFAELIA_BOOTIMG_H

#include <stdint.h>
#include <stddef.h>

#define BOOT_MAGIC "ANDROID!"
#define BOOT_MAGIC_SIZE 8

/* Minimal AOSP boot_img v1 header (simplified, matches most devices) */
struct boot_img_hdr_v1 {
    char magic[BOOT_MAGIC_SIZE];   /* "ANDROID!" */
    uint32_t kernel_size;          /* size in bytes */
    uint32_t kernel_addr;          /* physical load addr */
    uint32_t ramdisk_size;         /* size in bytes */
    uint32_t ramdisk_addr;
    uint32_t second_size;
    uint32_t second_addr;
    uint32_t tags_addr;
    uint32_t page_size;
    uint32_t dt_size;
    uint32_t unused;               /* reserved / future */
    char name[16];
    char cmdline[512];
} __attribute__((packed));

/* Generic constants */
#define DEFAULT_PAGE_SIZE 2048U
#define BOOT_HEADER_MAX_SIZE (64 * 1024) /* cap for safety */

/* Align helper */
static inline size_t align_to(size_t off, size_t page) {
    if (page == 0) return off;
    return ((off + page - 1) / page) * page;
}

#endif /* RAFAELIA_BOOTIMG_H */
