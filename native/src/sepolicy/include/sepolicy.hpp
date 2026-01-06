/*
 * Original Magisk Copyright:
 * Copyright 2017 - 2025, John Wu (@topjohnwu)
 *
 * RAFAELIA Framework Additions:
 * Copyright 2025, Rafael Melo Reis (rafaelmeloreisnovo)
 * Instituto Rafael - CientiEspiritual Philosophy
 *
 * This file is part of Magisk_Rafaelia, a derivative work of Magisk.
 * 
 * Magisk_Rafaelia is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * ---
 * RAFAELIA PHILOSOPHY (Aspirational Commentary - Not Part of License):
 * 
 * Sacred Cycle: VAZIO → VERBO → CHEIO → RETRO (EMPTY → ACTION → FULL → FEEDBACK)
 * Motto: "Amor, Luz e Coerência" (Love, Light and Coherence)
 * Ethica[8]: Transparency, Accountability, Fairness, Privacy, Security,
 *            Reliability, Safety, Sustainability
 * ---
 */

#pragma once

#include <sepol/policydb/policydb.h>
#include <sepol/policydb/services.h>
#include <sepol/policydb/expand.h>
#include <sepol/policydb/conditional.h>
#include <sepol/policydb/avtab.h>
#include <sepol/policydb/hashtab.h>

#define SELINUX_MNT          "/sys/fs/selinux"
#define SELINUX_VERSION      SELINUX_MNT "/policyvers"
#define PLAT_POLICY_DIR      "/system/etc/selinux/"
#define VEND_POLICY_DIR      "/vendor/etc/selinux/"
#define PROD_POLICY_DIR      "/product/etc/selinux/"
#define ODM_POLICY_DIR       "/odm/etc/selinux/"
#define SYSEXT_POLICY_DIR    "/system_ext/etc/selinux/"
#define SPLIT_PLAT_CIL       "/system/etc/selinux/plat_sepolicy.cil"
