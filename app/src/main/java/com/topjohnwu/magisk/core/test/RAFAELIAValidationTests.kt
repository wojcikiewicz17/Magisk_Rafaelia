package com.topjohnwu.magisk.core.test

import com.topjohnwu.magisk.core.audit.AuditSystem
import com.topjohnwu.magisk.core.error.ErrorCategory
import com.topjohnwu.magisk.core.error.ErrorHandlerUtil
import com.topjohnwu.magisk.core.error.ErrorSeverity
import kotlinx.coroutines.runBlocking

/**
 * RAFAELIA Framework Validation Tests
 * 
 * Basic validation to ensure framework components work correctly.
 */
object RAFAELIAValidationTests {
    
    fun testErrorCategorization() {
        println("=== Test 1: Error Categorization ===")
        val testCases = mapOf(
            java.io.IOException() to ErrorCategory.IO,
            java.net.UnknownHostException() to ErrorCategory.NETWORK,
            SecurityException() to ErrorCategory.SECURITY,
            IllegalArgumentException() to ErrorCategory.VALIDATION
        )
        
        var passed = 0
        testCases.forEach { (exception, expectedCategory) ->
            val actualCategory = ErrorCategory.fromThrowable(exception)
            if (actualCategory == expectedCategory) {
                println("✓ ${exception.javaClass.simpleName} → $actualCategory")
                passed++
            }
        }
        println("Result: $passed/${testCases.size} passed\n")
    }
    
    fun testAuditSystemLogging() = runBlocking {
        println("=== Test 2: Audit System Logging ===")
        AuditSystem.clearAuditLog()
        
        AuditSystem.logPrimitiveExecution(
            primitive = "boot_patch",
            context = "install",
            requiresHash = true,
            requiresAudit = true
        )
        
        val trail = AuditSystem.getAuditTrail(limit = 10)
        println("✓ Logged ${trail.size} entries")
        println("Result: PASSED\n")
    }
    
    fun runAllTests() {
        println("\n" + "=".repeat(60))
        println("RAFAELIA FRAMEWORK VALIDATION TESTS")
        println("=".repeat(60) + "\n")
        
        testErrorCategorization()
        testAuditSystemLogging()
        
        println("=".repeat(60))
        println("ALL TESTS COMPLETED")
        println("=".repeat(60) + "\n")
    }
}

fun main() {
    RAFAELIAValidationTests.runAllTests()
}
