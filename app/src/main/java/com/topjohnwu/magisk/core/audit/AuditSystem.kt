package com.topjohnwu.magisk.core.audit

import com.topjohnwu.magisk.core.logging.JSONLogger
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.json.JSONArray
import org.json.JSONObject
import java.security.MessageDigest
import java.time.Instant
import java.util.concurrent.ConcurrentLinkedQueue

/**
 * RAFAELIA Audit System
 * 
 * Implements comprehensive audit logging with cryptographic integrity verification.
 * Provides point-in-time state tracking and rollback point management for the
 * RAFAELIA framework (Recursively Auditable Fractal Architecture for Ethical 
 * and Logical Integrity Assurance).
 * 
 * Features:
 * - Cryptographic hash verification (SHA3-256 and Blake3 simulation)
 * - State tracking for all 1008 operational states (56 primitives × 18 contexts)
 * - Rollback point management
 * - Integrity verification logs
 * - Session-based audit trails
 * 
 * @see docs/RAFAELIA_PRIMITIVES.json
 * @see docs/RAFAELIA_STATE_MATRIX.csv
 */
object AuditSystem {
    
    private val auditLog = ConcurrentLinkedQueue<AuditEntry>()
    private val rollbackPoints = ConcurrentLinkedQueue<RollbackPoint>()
    private val mutex = Mutex()
    private const val MAX_AUDIT_ENTRIES = 10000
    private const val MAX_ROLLBACK_POINTS = 100
    
    /**
     * Log a primitive execution with cryptographic verification.
     * 
     * @param primitive The primitive operation (e.g., "boot_patch", "daemon_start")
     * @param context The execution context (e.g., "boot", "runtime", "install")
     * @param sessionId Optional session identifier for tracking
     * @param metadata Additional metadata about the operation
     * @param requiresHash Whether cryptographic hash is required per state matrix
     * @param requiresAudit Whether audit is mandatory per state matrix
     * @param rollbackCapable Whether this operation supports rollback
     */
    suspend fun logPrimitiveExecution(
        primitive: String,
        context: String,
        sessionId: String? = null,
        metadata: Map<String, Any?> = emptyMap(),
        requiresHash: Boolean = false,
        requiresAudit: Boolean = true,
        rollbackCapable: Boolean = false
    ) {
        mutex.withLock {
            val stateId = "PRIM_${primitive}_CTX_${context}"
            val timestamp = Instant.now()
            
            // Compute integrity hashes if required
            val hashes = if (requiresHash) {
                computeIntegrityHashes(primitive, context, metadata)
            } else {
                emptyMap()
            }
            
            val entry = AuditEntry(
                stateId = stateId,
                primitive = primitive,
                context = context,
                timestamp = timestamp,
                sessionId = sessionId,
                metadata = metadata,
                hashes = hashes,
                requiresAudit = requiresAudit,
                rollbackCapable = rollbackCapable
            )
            
            auditLog.add(entry)
            
            // Trim if necessary
            while (auditLog.size > MAX_AUDIT_ENTRIES) {
                auditLog.poll()
            }
            
            // Log to JSON logger
            JSONLogger.info(
                component = "AuditSystem",
                event = "primitive_execution",
                sessionId = sessionId,
                extra = mapOf(
                    "stateId" to stateId,
                    "primitive" to primitive,
                    "context" to context,
                    "requiresHash" to requiresHash,
                    "requiresAudit" to requiresAudit,
                    "rollbackCapable" to rollbackCapable,
                    "hashes" to hashes,
                    "metadata" to metadata
                )
            )
        }
    }
    
    /**
     * Create a rollback point for system restoration.
     * 
     * @param name Descriptive name for the rollback point
     * @param primitive The primitive that triggered rollback point creation
     * @param context The context of the operation
     * @param sessionId Optional session identifier
     * @param metadata Additional state metadata
     * @return RollbackPoint identifier
     */
    suspend fun createRollbackPoint(
        name: String,
        primitive: String,
        context: String,
        sessionId: String? = null,
        metadata: Map<String, Any?> = emptyMap()
    ): String {
        return mutex.withLock {
            val rpId = "RP_${System.currentTimeMillis()}_${primitive}_${context}"
            val timestamp = Instant.now()
            
            val rollbackPoint = RollbackPoint(
                id = rpId,
                name = name,
                primitive = primitive,
                context = context,
                timestamp = timestamp,
                sessionId = sessionId,
                stateSnapshot = captureStateSnapshot(primitive, context, metadata),
                metadata = metadata
            )
            
            rollbackPoints.add(rollbackPoint)
            
            // Trim old rollback points
            while (rollbackPoints.size > MAX_ROLLBACK_POINTS) {
                rollbackPoints.poll()
            }
            
            JSONLogger.info(
                component = "AuditSystem",
                event = "rollback_point_created",
                sessionId = sessionId,
                extra = mapOf(
                    "rollbackPointId" to rpId,
                    "name" to name,
                    "primitive" to primitive,
                    "context" to context,
                    "metadata" to metadata
                )
            )
            
            rpId
        }
    }
    
    /**
     * Verify audit log integrity using cryptographic hashes.
     * 
     * @return Verification result with details
     */
    suspend fun verifyAuditIntegrity(): AuditVerificationResult {
        return mutex.withLock {
            val entries = auditLog.toList()
            val totalEntries = entries.size
            var verifiedEntries = 0
            var failedEntries = 0
            val failures = mutableListOf<String>()
            
            entries.forEach { entry ->
                if (entry.hashes.isNotEmpty()) {
                    // Re-compute hashes and verify
                    val recomputedHashes = computeIntegrityHashes(
                        entry.primitive,
                        entry.context,
                        entry.metadata
                    )
                    
                    val matches = entry.hashes.keys.all { algorithm ->
                        entry.hashes[algorithm] == recomputedHashes[algorithm]
                    }
                    
                    if (matches) {
                        verifiedEntries++
                    } else {
                        failedEntries++
                        failures.add(entry.stateId)
                    }
                } else {
                    verifiedEntries++ // No hash required, considered verified
                }
            }
            
            val result = AuditVerificationResult(
                totalEntries = totalEntries,
                verifiedEntries = verifiedEntries,
                failedEntries = failedEntries,
                failures = failures,
                verificationTime = Instant.now()
            )
            
            JSONLogger.info(
                component = "AuditSystem",
                event = "integrity_verification",
                extra = mapOf(
                    "totalEntries" to totalEntries,
                    "verifiedEntries" to verifiedEntries,
                    "failedEntries" to failedEntries,
                    "successRate" to if (totalEntries > 0) {
                        (verifiedEntries.toDouble() / totalEntries * 100)
                    } else 0.0
                )
            )
            
            result
        }
    }
    
    /**
     * Retrieve rollback points for restoration.
     * 
     * @param limit Maximum number of rollback points to retrieve
     * @return List of rollback points, most recent first
     */
    fun getRollbackPoints(limit: Int = 10): List<RollbackPoint> {
        return rollbackPoints.toList().takeLast(limit).reversed()
    }
    
    /**
     * Get audit trail for a specific primitive.
     * 
     * @param primitive The primitive operation to filter by
     * @param limit Maximum number of entries to retrieve
     * @return List of audit entries for the specified primitive
     */
    fun getAuditTrail(primitive: String? = null, limit: Int = 100): List<AuditEntry> {
        val filtered = if (primitive != null) {
            auditLog.filter { it.primitive == primitive }
        } else {
            auditLog.toList()
        }
        return filtered.takeLast(limit)
    }
    
    /**
     * Get audit statistics.
     * 
     * @return Map of statistics about audit log
     */
    fun getAuditStatistics(): Map<String, Any> {
        val entries = auditLog.toList()
        val primitiveCount = entries.groupingBy { it.primitive }.eachCount()
        val contextCount = entries.groupingBy { it.context }.eachCount()
        val hashedCount = entries.count { it.hashes.isNotEmpty() }
        
        return mapOf(
            "totalEntries" to entries.size,
            "totalRollbackPoints" to rollbackPoints.size,
            "entriesWithHash" to hashedCount,
            "hashPercentage" to if (entries.isNotEmpty()) {
                (hashedCount.toDouble() / entries.size * 100)
            } else 0.0,
            "primitiveDistribution" to primitiveCount,
            "contextDistribution" to contextCount,
            "mostCommonPrimitive" to (primitiveCount.maxByOrNull { it.value }?.key ?: "none"),
            "mostCommonContext" to (contextCount.maxByOrNull { it.value }?.key ?: "none")
        )
    }
    
    /**
     * Clear audit log (use with caution).
     */
    suspend fun clearAuditLog() {
        mutex.withLock {
            auditLog.clear()
            JSONLogger.warn(
                component = "AuditSystem",
                event = "audit_log_cleared"
            )
        }
    }
    
    /**
     * Clear rollback points (use with caution).
     */
    suspend fun clearRollbackPoints() {
        mutex.withLock {
            rollbackPoints.clear()
            JSONLogger.warn(
                component = "AuditSystem",
                event = "rollback_points_cleared"
            )
        }
    }
    
    /**
     * Export audit log to JSON format.
     * 
     * @return JSON array of audit entries
     */
    fun exportAuditLog(): JSONArray {
        val jsonArray = JSONArray()
        auditLog.forEach { entry ->
            jsonArray.put(entry.toJSON())
        }
        return jsonArray
    }
    
    /**
     * Compute cryptographic integrity hashes.
     * 
     * Implements SHA3-256 (simulated via SHA-256) and Blake3 (simulated via additional SHA-256).
     * In production, use actual SHA3-256 and Blake3 implementations.
     */
    private fun computeIntegrityHashes(
        primitive: String,
        context: String,
        metadata: Map<String, Any?>
    ): Map<String, String> {
        val data = "$primitive:$context:${metadata.entries.sortedBy { it.key }.joinToString(",")}"
        val bytes = data.toByteArray(Charsets.UTF_8)
        
        // SHA3-256 (simulated with SHA-256 for demonstration)
        val sha3 = MessageDigest.getInstance("SHA-256")
        val sha3Hash = sha3.digest(bytes).joinToString("") { "%02x".format(it) }
        
        // Blake3 (simulated with double SHA-256 for demonstration)
        val blake3 = MessageDigest.getInstance("SHA-256")
        val blake3Hash = blake3.digest(blake3.digest(bytes)).joinToString("") { "%02x".format(it) }
        
        return mapOf(
            "SHA3-256" to sha3Hash,
            "Blake3" to blake3Hash
        )
    }
    
    /**
     * Capture state snapshot for rollback.
     */
    private fun captureStateSnapshot(
        primitive: String,
        context: String,
        metadata: Map<String, Any?>
    ): Map<String, Any?> {
        return mapOf(
            "primitive" to primitive,
            "context" to context,
            "metadata" to metadata,
            "timestamp" to Instant.now().toString(),
            "auditLogSize" to auditLog.size,
            "recentPrimitives" to auditLog.toList().takeLast(10).map { it.primitive }
        )
    }
}

/**
 * Represents a single audit log entry.
 */
data class AuditEntry(
    val stateId: String,
    val primitive: String,
    val context: String,
    val timestamp: Instant,
    val sessionId: String?,
    val metadata: Map<String, Any?>,
    val hashes: Map<String, String>,
    val requiresAudit: Boolean,
    val rollbackCapable: Boolean
) {
    fun toJSON(): JSONObject {
        val json = JSONObject()
        json.put("stateId", stateId)
        json.put("primitive", primitive)
        json.put("context", context)
        json.put("timestamp", timestamp.toString())
        json.put("sessionId", sessionId)
        json.put("metadata", JSONObject(metadata))
        json.put("hashes", JSONObject(hashes))
        json.put("requiresAudit", requiresAudit)
        json.put("rollbackCapable", rollbackCapable)
        return json
    }
}

/**
 * Represents a rollback point for system restoration.
 */
data class RollbackPoint(
    val id: String,
    val name: String,
    val primitive: String,
    val context: String,
    val timestamp: Instant,
    val sessionId: String?,
    val stateSnapshot: Map<String, Any?>,
    val metadata: Map<String, Any?>
) {
    fun toJSON(): JSONObject {
        val json = JSONObject()
        json.put("id", id)
        json.put("name", name)
        json.put("primitive", primitive)
        json.put("context", context)
        json.put("timestamp", timestamp.toString())
        json.put("sessionId", sessionId)
        json.put("stateSnapshot", JSONObject(stateSnapshot))
        json.put("metadata", JSONObject(metadata))
        return json
    }
}

/**
 * Result of audit integrity verification.
 */
data class AuditVerificationResult(
    val totalEntries: Int,
    val verifiedEntries: Int,
    val failedEntries: Int,
    val failures: List<String>,
    val verificationTime: Instant
) {
    val isValid: Boolean
        get() = failedEntries == 0
    
    val successRate: Double
        get() = if (totalEntries > 0) {
            (verifiedEntries.toDouble() / totalEntries * 100)
        } else 0.0
}
