# test:

set(optim_part_begin "//cmake generated part for optimizations - do not edit")
set(optim_part_end "//end cmake generated part for optimizations - do not edit")

set(optimization_library_relative_path "Fulguro")

function(add_optimization_info file_name)
  message("Current source : " ${file_name})
  file(RELATIVE_PATH relative_p ${YAYI_CORE_DIR} ${file_name})
  message("Current source relative path : " ${relative_p})
  get_source_file_property(is_header ${file_name} LANGUAGE) #HEADER_FILE_ONLY)
  message("Is this a header ? : " ${is_header})
  
  if(NOT ${is_header} STREQUAL "")
    message("Unsupported type, file skipped")
    return()
  endif()


  #set(path_to_check ${YAYI_CORE_DIR}/${optimization_library_relative_path}/${relative_p})
  set(path_to_check ${YAYI_CORE_DIR}/${relative_p})
  file(TO_NATIVE_PATH ${path_to_check} result_path_to_check)

  if(NOT EXISTS ${result_path_to_check})
    return()
  endif()
  
  message("The optimized file exists for header ${relative_p} -> adding specializations")
  
  file(READ ${file_name} file_content)

  string(REGEX MATCH "${optim_part_begin}.*${optim_part_end}" var_out ${file_content})
  message("Regex = " ${var_out})


  set(part_to_add "${optim_part_begin}\n")
  set(part_to_add "${part_to_add}// #include \"Yayi/${optimization_library_relative_path}/${relative_p}\"\n")
  set(part_to_add "${part_to_add}${optim_part_end}")

  if(var_out STREQUAL "")
    # no additional include exists, we can safely add one if needed
    set(var_out2 ${file_content}${part_to_add}\n)

  else()
    # Something already exists: we should check and replace the content
    # or remove it completely

    if(NOT ${var_out} STREQUAL ${part_to_add})
      string(REGEX REPLACE "${optim_part_begin}.*${optim_part_end}" ${part_to_add} var_out2 ${file_content})
    endif()
  endif()

  message("Replaced string is " ${var_out2})

endfunction(add_optimization_info)


# to test the function
# get_target_property(CURRENT_SOURCES YayiCommon SOURCES)
# message("Sources are : " ${CURRENT_SOURCES})
# foreach(loop_var ${CURRENT_SOURCES})
#  add_optimization_info(${loop_var})
# endforeach()
