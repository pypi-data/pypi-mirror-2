/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiIOPython/io_python.hpp>

using namespace yayi::IO;

yayi::IImage* read_jpeg(const std::string & filename) {

  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret = yayi::IO::readJPG (filename, image);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return image;

}

void declare_jpg() {
  
  bpy::def("readJPG", &read_jpeg, "(filename) : returns the specified Jpeg image", bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("writeJPG",&yayi::IO::writeJPG, "(filename, image) : writes the image into the specified file");


}

