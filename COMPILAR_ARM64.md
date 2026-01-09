# Como Compilar para ARM64

## 🎯 Configuração Rápida para ARM64

Este projeto suporta compilação otimizada para **ARM64 (arm64-v8a)**.

### Dispositivo Alvo
- **Modelo**: RMX3834 (Realme GT Neo 3T)
- **Kernel**: 5.15.178-android13-8-gabf75819a85e-ab569
- **Arquitetura**: ARM64 (aarch64)

## 🚀 Compilação Rápida

```bash
# 1. Clone o repositório com submódulos
git clone --recurse-submodules https://github.com/rafaelmeloreisnovo/Magisk_Rafaelia.git
cd Magisk_Rafaelia

# 2. Configure para ARM64 (opcional, mas recomendado para builds mais rápidas)
cp config.prop.sample config.prop
# Edite config.prop e descomente: abiList=arm64-v8a

# 3. Instale o Magisk NDK
python3 build.py ndk

# 4. Compile tudo
python3 build.py -v all
```

O APK gerado estará em `out/app-debug.apk` (ou `out/app-release.apk` se usar `-r`).

## 📋 Detalhes da Configuração

### Arquivo config.prop

Para compilar apenas ARM64 (recomendado para dispositivos modernos):

**Opção 1: Editar manualmente**
```bash
# Copie o arquivo de exemplo
cp config.prop.sample config.prop

# Edite config.prop com seu editor preferido e descomente a linha:
# abiList=arm64-v8a
# (remova o # do início da linha)
```

**Opção 2: Criar diretamente**
```bash
# Crie config.prop com a configuração ARM64
cat > config.prop << 'EOF'
# Magisk_Rafaelia Build Configuration
# Build only for ARM64 (recommended for modern devices)
abiList=arm64-v8a
EOF
```

**Vantagens de compilar apenas ARM64:**
- ✅ Compilação 4x mais rápida
- ✅ APK menor (~30% de redução)
- ✅ Otimizado para dispositivos modernos (RMX3834, etc.)

### Arquiteturas Suportadas

O Magisk_Rafaelia suporta as seguintes arquiteturas:

- ✅ **arm64-v8a** (ARM 64-bit) - **RECOMENDADO**
- armeabi-v7a (ARM 32-bit)
- x86 (Intel/AMD 32-bit)
- x86_64 (Intel/AMD 64-bit)
- riscv64 (RISC-V 64-bit, experimental)

**Padrão:** Se você não criar `config.prop`, o sistema compilará para todas as arquiteturas (exceto riscv64).

### Compilar para Múltiplas Arquiteturas

Se você deseja compilar para todas as arquiteturas, edite `config.prop`:

```properties
# Compilar para todas as arquiteturas
abiList=armeabi-v7a,x86,arm64-v8a,x86_64
```

Ou deixe o arquivo vazio para usar o padrão.

### Compilar para Apenas uma Arquitetura Específica

```properties
# Apenas ARM 32-bit
abiList=armeabi-v7a

# Apenas x86 64-bit
abiList=x86_64
```

## 🔧 Opções de Compilação

### Modo Release (otimizado)
```bash
python3 build.py -r all
```

### Modo Debug (com símbolos de depuração)
```bash
python3 build.py -v all
```

### Compilar apenas binários nativos
```bash
python3 build.py -v native
```

### Compilar apenas o APK
```bash
python3 build.py -v app
```

## 📱 Instalação no Dispositivo

```bash
# Instalar o APK
adb install out/app-debug.apk

# Ou via linha de comando
adb push out/app-debug.apk /sdcard/
adb shell pm install /sdcard/app-debug.apk
```

## 🔍 Verificar Arquitetura Compilada

```bash
# Verificar binários ARM64 gerados
ls -la native/out/arm64-v8a/

# Exemplo de saída esperada:
# magisk
# magiskboot
# magiskinit
# magiskpolicy
```

## ❓ Solução de Problemas

### Erro: NDK não encontrado
```bash
python3 build.py ndk
```

### Limpar build anterior
```bash
python3 build.py clean
```

### Verificar ABIs sendo compiladas
```bash
python3 build.py -v all 2>&1 | grep "APP_ABI"
```

Você deverá ver: `APP_ABI=arm64-v8a`

## 📚 Mais Informações

- [Como Obter o APK (Português)](COMO_OBTER_APK.md)
- [How to Get APK (English)](HOW_TO_GET_APK.md)
- [README Principal](README.MD)

## 🎯 Nota para RMX3834

Este dispositivo é ARM64 nativo. A configuração padrão está otimizada para:
- Compilação mais rápida (apenas 1 arquitetura)
- Melhor desempenho (código nativo ARM64)
- Menor tamanho do APK (sem bibliotecas desnecessárias)

---

**Magisk_Rafaelia** - Compilação otimizada para ARM64 🚀
