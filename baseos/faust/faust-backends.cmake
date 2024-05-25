# faust-backends.cmake : this file selects all possible backends.
#
# Possible configuration values are among: 
#    OFF       don't include the backend
#    COMPILER  embed the backend in the faust compiler
#    STATIC    embed the backend in the faust static library
#    DYNAMIC   embed the backend in the faust dynamic library
#    WASM      embed the backend in the faust wasm library


set ( C_BACKEND      COMPILER STATIC DYNAMIC        CACHE STRING  "Include C backend"         FORCE )
set ( CPP_BACKEND    COMPILER STATIC DYNAMIC        CACHE STRING  "Include CPP backend"       FORCE )
set ( JAVA_BACKEND   COMPILER STATIC DYNAMIC        CACHE STRING  "Include JAVA backend"      FORCE )
set ( LLVM_BACKEND   COMPILER STATIC DYNAMIC        CACHE STRING  "Include LLVM backend"      FORCE )
set ( RUST_BACKEND   COMPILER STATIC DYNAMIC        CACHE STRING  "Include Rust backend"      FORCE )
set ( WASM_BACKEND   COMPILER STATIC DYNAMIC WASM   CACHE STRING  "Include WASM backend"      FORCE )
