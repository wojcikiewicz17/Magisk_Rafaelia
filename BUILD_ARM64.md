# How to Compile for ARM64

## 🎯 Quick ARM64 Setup

This project is now pre-configured to compile for **ARM64 (arm64-v8a)** by default through the `config.prop` file.

### Target Device
- **Model**: RMX3834 (Realme GT Neo 3T)
- **Kernel**: 5.15.178-android13-8-gabf75819a85e-ab569
- **Architecture**: ARM64 (aarch64)

## 🚀 Quick Build

```bash
# 1. Clone the repository with submodules
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# 2. Install Magisk NDK
python3 build.py ndk

# 3. Build everything (ARM64 only by default)
python3 build.py -v all
```

The generated APK will be in `out/app-debug.apk` (or `out/app-release.apk` if using `-r`).

## 📋 Configuration Details

### config.prop File

The `config.prop` file in the project root defines:

```properties
# Compile only for ARM64
abiList=arm64-v8a
```

### Supported Architectures

Magisk_Rafaelia supports the following architectures:

- ✅ **arm64-v8a** (ARM 64-bit) - **DEFAULT**
- armeabi-v7a (ARM 32-bit)
- x86 (Intel/AMD 32-bit)
- x86_64 (Intel/AMD 64-bit)
- riscv64 (RISC-V 64-bit, experimental)

### Build for Multiple Architectures

If you want to build for all architectures, edit `config.prop`:

```properties
# Build for all architectures
abiList=armeabi-v7a,x86,arm64-v8a,x86_64
```

Or comment out the line:

```properties
# abiList=arm64-v8a
```

### Build for a Specific Architecture

```properties
# ARM 32-bit only
abiList=armeabi-v7a

# x86 64-bit only
abiList=x86_64
```

## 🔧 Build Options

### Release Mode (optimized)
```bash
python3 build.py -r all
```

### Debug Mode (with debug symbols)
```bash
python3 build.py -v all
```

### Build only native binaries
```bash
python3 build.py -v native
```

### Build only the APK
```bash
python3 build.py -v app
```

## 📱 Installing on Device

```bash
# Install the APK
adb install out/app-debug.apk

# Or via command line
adb push out/app-debug.apk /sdcard/
adb shell pm install /sdcard/app-debug.apk
```

## 🔍 Verify Compiled Architecture

```bash
# Check generated ARM64 binaries
ls -la native/out/arm64-v8a/

# Expected output:
# magisk
# magiskboot
# magiskinit
# magiskpolicy
```

## ❓ Troubleshooting

### Error: NDK not found
```bash
python3 build.py ndk
```

### Clean previous build
```bash
python3 build.py clean
```

### Check which ABIs are being built
```bash
python3 build.py -v all 2>&1 | grep "APP_ABI"
```

You should see: `APP_ABI=arm64-v8a`

## 📚 More Information

- [Como Obter o APK (Português)](COMO_OBTER_APK.md)
- [How to Get APK (English)](HOW_TO_GET_APK.md)
- [Main README](README.MD)

## 🎯 Note for RMX3834

This device is native ARM64. The default configuration is optimized for:
- Faster compilation (only 1 architecture)
- Better performance (native ARM64 code)
- Smaller APK size (no unnecessary libraries)

---

**Magisk_Rafaelia** - ARM64 optimized build 🚀
