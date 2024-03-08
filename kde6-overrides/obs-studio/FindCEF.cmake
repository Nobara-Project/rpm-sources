include(FindPackageHandleStandardArgs)

find_path(CEF_INCLUDE_DIR "obs-cef/cef_version.h" HINTS /usr/include)

find_library(
  CEF_LIBRARY
  NAMES libcef.so "Chromium Embedded Framework"
  NO_DEFAULT_PATH
  PATHS /usr/local/lib64/obs-cef /usr/lib64/obs-cef /usr/local/lib/obs-cef /usr/lib/obs-cef)

find_library(
  CEFWRAPPER_LIBRARY
  NAMES libcef_dll_wrapper.a
  NO_DEFAULT_PATH
  PATHS /usr/local/lib64/obs-cef /usr/lib64/obs-cef /usr/local/lib/obs-cef /usr/lib/obs-cef)

mark_as_advanced(CEFWRAPPER_LIBRARY CEFWRAPPER_LIBRARY_DEBUG)

if(NOT CEF_LIBRARY)
  message(WARNING "Could NOT find Chromium Embedded Framework library (missing: CEF_LIBRARY)")
  set(CEF_FOUND FALSE)
  return()
endif()

if(NOT CEFWRAPPER_LIBRARY)
  message(WARNING "Could NOT find Chromium Embedded Framework wrapper library (missing: CEFWRAPPER_LIBRARY)")
  set(CEF_FOUND FALSE)
  return()
endif()

message(STATUS "Found Chromium Embedded Framework: ${CEF_LIBRARY};${CEF_WRAPPER_LIBRARY}")

set(CEF_LIBRARIES ${CEF_LIBRARY} optimized ${CEFWRAPPER_LIBRARY})

if(CEFWRAPPER_LIBRARY_DEBUG)
  list(APPEND CEF_LIBRARIES debug ${CEFWRAPPER_LIBRARY_DEBUG})
endif()

find_package_handle_standard_args(CEF DEFAULT_MSG CEF_LIBRARY CEFWRAPPER_LIBRARY CEF_INCLUDE_DIR)

mark_as_advanced(CEF_LIBRARY CEF_WRAPPER_LIBRARY CEF_LIBRARIES CEF_INCLUDE_DIR)

if(NOT TARGET CEF::Wrapper)
  if(IS_ABSOLUTE "${CEF_LIBRARIES}")
    add_library(CEF::Wrapper UNKNOWN IMPORTED)
    add_library(CEF::Library UNKNOWN IMPORTED)

    set_target_properties(CEF::Wrapper PROPERTIES IMPORTED_LOCATION ${CEFWRAPPER_LIBRARY})

    set_target_properties(CEF::Library PROPERTIES IMPORTED_LOCATION ${CEF_LIBRARY})

    if(DEFINED CEFWRAPPER_LIBRARY_DEBUG)
      set_target_properties(CEF::Wrapper PROPERTIES IMPORTED_LOCATION_DEBUG ${CEFWRAPPER_LIBRARY_DEBUG})
    endif()
  else()
    add_library(CEF::Wrapper INTERFACE IMPORTED)
    add_library(CEF::Library INTERFACE IMPORTED)

    set_target_properties(CEF::Wrapper PROPERTIES IMPORTED_LIBNAME ${CEFWRAPPER_LIBRARY})

    set_target_properties(CEF::Library PROPERTIES IMPORTED_LIBNAME ${CEF_LIBRARY})

    if(DEFINED CEFWRAPPER_LIBRARY_DEBUG)
      set_target_properties(CEF::Wrapper PROPERTIES IMPORTED_LIBNAME_DEBUG ${CEFWRAPPER_LIBRARY_DEBUG})
    endif()
  endif()

  set_target_properties(CEF::Wrapper PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CEF_INCLUDE_DIR}")

  set_target_properties(CEF::Library PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CEF_INCLUDE_DIR}")
endif()
