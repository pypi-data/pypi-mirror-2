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

yayi::IImage* read_raw(const std::string & filename, yayi::s_coordinate<0> s, yayi::type t) {

  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret = yayi::IO::readRAW (filename, s, t, image);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return image;

}

void declare_raw() {
  
  bpy::def("readRAW", &read_raw, "(filename, size, type) : returns the specified RAW image", bpy::return_value_policy<bpy::manage_new_object>());
  bpy::def("writeRAW",&yayi::IO::writeRAW, "(filename, image) : writes the image into the specified file");


}

