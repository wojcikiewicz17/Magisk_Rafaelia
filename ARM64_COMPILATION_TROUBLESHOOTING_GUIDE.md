# Complete Guide: ARM64 Compilation with Error Resolution

## 🎯 Objective

This guide shows **step by step** how to compile Magisk_Rafaelia for ARM64 and how to **track and fix** each error that appears in GitHub Actions checks.

---

## 📋 Prerequisites

### System Requirements

```bash
# Check if you have the requirements
python3 --version  # Need 3.8 or higher
java -version      # Need Java 17 or 21
git --version      # Need 2.x or higher
```

### Required Tools

- **Linux**: Ubuntu 20.04+ or similar
- **macOS**: macOS 11+ (Big Sur or higher)
- **Windows**: WSL2 with Ubuntu or use native environment

---

## 🚀 Part 1: Initial Setup

### Step 1: Clone the Repository

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# Check you're on the correct branch
git branch
```

### Step 2: Configure for ARM64

```bash
# Create configuration file
cat > config.prop << 'EOF'
# Configuration for ARM64 only
abiList=arm64-v8a
EOF

# Verify it was created correctly
cat config.prop
```

### Step 3: Install Magisk NDK

```bash
# Download and install ONDK (Organized NDK)
python3 build.py ndk

# This will:
# - Download ONDK r29.2
# - Extract to ./ndk-arm64
# - Configure Rust environment
# - Verify tools
```

**If you get an error here:**
- Network error: Check your connection and try again
- Permission error: Run `chmod +x build.py`
- Python not found: Install Python 3.8+

---

## 🔨 Part 2: Local Compilation

### Step 4: First Compilation Attempt

```bash
# Compile in debug mode with verbose output
python3 build.py -v all

# This will:
# 1. Compile native code (C++/Rust) for arm64-v8a
# 2. Compile Android app (APK)
# 3. Package everything in out/app-debug.apk
```

### Step 5: Track the Compilation

The compilation has several stages. Watch the output:

```
✅ STEP 1: Building Rust modules
   - Compiling base...
   - Compiling core...
   - Compiling boot...
   
✅ STEP 2: Building C++ components
   - Building magisk
   - Building magiskboot
   - Building magiskinit
   - Building magiskpolicy
   
✅ STEP 3: Building Android app
   - Gradle sync
   - Building APK
   
✅ STEP 4: Packaging
   - Copying binaries
   - Creating APK
```

---

## 🐛 Part 3: Resolving Common Errors

### Error 1: NDK not found

**Symptom:**
```
Error: Android NDK not found
```

**Solution:**
```bash
# Reinstall NDK
python3 build.py ndk

# If it persists, configure manually
export ANDROID_NDK_HOME="$PWD/ndk-arm64"
```

---

### Error 2: Rust compilation error

**Symptom:**
```
error[E0425]: cannot find function `something` in this scope
```

**Solution:**
```bash
# Clean previous build
python3 build.py clean

# Update Rust in NDK
python3 build.py ndk

# Try again
python3 build.py -v native
```

---

### Error 3: Gradle fails to download dependencies

**Symptom:**
```
Could not resolve all dependencies
Connection timeout
```

**Solution:**
```bash
# Configure proxy (if needed)
export GRADLE_OPTS="-Dhttp.proxyHost=... -Dhttp.proxyPort=..."

# OR use local Gradle cache
./app/gradlew --refresh-dependencies

# Try build again
python3 build.py -v app
```

---

### Error 4: Out of memory during compilation

**Symptom:**
```
error: LLVM ERROR: out of memory
The system cannot find the file specified
```

**Solution:**
```bash
# Limit parallel jobs
export MAKEFLAGS="-j4"  # Adjust according to your RAM

# Configure Gradle to use less memory
export GRADLE_OPTS="-Xmx2g -XX:MaxMetaspaceSize=512m"

# Compile
python3 build.py -v all
```

---

### Error 5: Incorrect permissions

**Symptom:**
```
Permission denied: './build.py'
```

**Solution:**
```bash
# Fix permissions
chmod +x build.py
find . -name "*.sh" -exec chmod +x {} \;
find . -name "*.py" -exec chmod +x {} \;
```

---

## 📊 Part 4: Track GitHub Actions Checks

### Step 1: View Workflow Status

```bash
# View your recent commits
git log --oneline -5

# Push your branch
git push origin your-branch

# In browser, go to:
# https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

### Step 2: Identify Which Check Failed

The main workflows are:

1. **build.yml** - Complete build
2. **ci.yml** - Full RAFAELIA pipeline
3. **quality-gates.yml** - Quality checks
4. **codeql.yml** - Security analysis

**Where to look:**
- ✅ Green = Passed
- ❌ Red = Failed
- 🟡 Yellow = In progress
- ⚪ Gray = Not executed

### Step 3: View Error Logs

**On GitHub:**
1. Click on the failed check (red X)
2. Click on the failed job
3. Expand the step that has the error
4. Read the complete error

**Example error log:**
```
Run python3 build.py -v all
Building Rust modules...
error: could not compile `core`
  |
45 | let result = something()?;
  |              ^^^^^^^^^ not found in this scope
```

### Step 4: Download Complete Logs

```bash
# Use GitHub CLI (optional)
gh run list --limit 5
gh run view <run-id>
gh run download <run-id>
```

---

## 🔄 Part 5: Correction Cycle

### Iterative Flow

```
1. COMPILE locally
   ↓
2. FAILED?
   ├─ YES → See the error, fix it, go back to step 1
   └─ NO → Continue
   ↓
3. COMMIT your changes
   ↓
4. PUSH to GitHub
   ↓
5. TRACK the checks
   ↓
6. CHECKS PASSED?
   ├─ YES → Success! 🎉
   └─ NO → See logs, fix, go back to step 3
```

### Practical Example

```bash
# 1. Local test
python3 build.py -v native
# ❌ Error found in rafaelia_audit.rs

# 2. Fix the file
nano native/src/core/rafaelia_audit.rs
# Make the necessary correction

# 3. Test again
python3 build.py -v native
# ✅ Passed!

# 4. Test complete build
python3 build.py -v all
# ✅ Passed!

# 5. Commit
git add native/src/core/rafaelia_audit.rs
git commit -m "fix: correct compilation error in rafaelia_audit"

# 6. Push
git push origin your-branch

# 7. Track on GitHub Actions
# https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia/actions
```

---

## 🔍 Part 6: Advanced Debugging

### See Exactly What Is Being Compiled

```bash
# Ultra-verbose mode
python3 build.py -v all 2>&1 | tee build.log

# Then analyze the log
grep -i "error" build.log
grep -i "warning" build.log
grep "APP_ABI" build.log  # Confirm ARM64
```

### Verify Generated Binaries

```bash
# List ARM64 binaries
ls -lh native/out/arm64-v8a/

# Check architecture
file native/out/arm64-v8a/magisk
# Should show: ELF 64-bit LSB executable, ARM aarch64

# Check symbols
nm native/out/arm64-v8a/magisk | grep rafaelia
```

### Test on Real Device

```bash
# Connect your ARM64 Android device
adb devices

# Push binary
adb push native/out/arm64-v8a/magisk /data/local/tmp/
adb shell chmod +x /data/local/tmp/magisk

# Test
adb shell /data/local/tmp/magisk --version
```

---

## 📱 Part 7: APK Installation

### After Successful Compilation

```bash
# APK will be in:
ls -lh out/app-debug.apk

# Install on device
adb install out/app-debug.apk

# OR to reinstall
adb install -r out/app-debug.apk

# OR copy to phone
adb push out/app-debug.apk /sdcard/Download/
# Then install manually through file manager
```

---

## 🎯 Part 8: Verification Checklist

Before committing/pushing, verify:

- [ ] `python3 build.py -v native` passed without errors
- [ ] `python3 build.py -v all` passed without errors
- [ ] APK was generated in `out/app-debug.apk`
- [ ] Verified it's ARM64: `file native/out/arm64-v8a/magisk`
- [ ] Tested installation on device (optional)
- [ ] Commit message is descriptive
- [ ] Push was done to correct branch

---

## 💡 Pro Tips

### 1. Incremental Compilation

```bash
# Compile only what changed
python3 build.py -v native  # Only native code
python3 build.py -v app     # Only APK
```

### 2. Release Build (Optimized)

```bash
# For production
python3 build.py -r all

# Generates out/app-release.apk (smaller and faster)
```

### 3. Clean When Necessary

```bash
# Clean build artifacts
python3 build.py clean

# Clean everything including NDK (last resort)
rm -rf ndk-arm64 out native/out
python3 build.py ndk
```

### 4. Configuration for CI

```bash
# Use .github/ci.prop for CI
# Already configured for ARM64:
cat .github/ci.prop
# abiList=arm64-v8a
```

---

## 🆘 Support

### Useful Resources

- **Main README**: [README.MD](README.MD)
- **Compilation Guide**: [BUILD_ARM64.md](BUILD_ARM64.md)
- **How to Get APK**: [HOW_TO_GET_APK.md](HOW_TO_GET_APK.md)
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)

### Where to Ask for Help

1. **GitHub Issues**: Describe your error with complete logs
2. **Pull Requests**: Show what you tried to do
3. **Discussions**: For general questions

### Issue Template for Compilation Error

```markdown
**Error Description:**
[Describe what happened]

**Environment:**
- OS: [Linux/macOS/Windows]
- Python: [version]
- Java: [version]

**Command Executed:**
```bash
python3 build.py -v all
```

**Error Log:**
```
[Paste complete log here]
```

**What I Already Tried:**
- [ ] Cleaned build with `build.py clean`
- [ ] Reinstalled NDK with `build.py ndk`
- [ ] Checked config.prop
- [ ] Other: [describe]
```

---

## ✅ Conclusion

Now you have a complete guide to:
1. ✅ Configure environment for ARM64
2. ✅ Compile locally
3. ✅ Identify and fix errors
4. ✅ Track GitHub Actions checks
5. ✅ Iterate until success

**Next step:** Start with [Step 1](#step-1-clone-the-repository)!

---

**Magisk_Rafaelia** - ARM64 Compilation Simplified 🚀
