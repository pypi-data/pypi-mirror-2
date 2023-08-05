/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#if YAYI_IO_HDF5_ENABLED__

#include <Yayi/python/yayiIOPython/io_python.hpp>

using namespace yayi::IO;

yayi::IImage* read_hdf5(const std::string & filename, const std::string & image_name = "")
{
  using namespace yayi;
  yayi::IImage* image = 0;
  yaRC ret;
  if(image_name == "")
    ret = yayi::IO::readHDF5 (filename, image);
  else
    ret = yayi::IO::readHDF5 (filename, image, image_name);
  if(ret != yaRC_ok)
    throw errors::yaException(ret);
  
  return image;

}

BOOST_PYTHON_FUNCTION_OVERLOADS(read_hdf5_overloads, read_hdf5, 1, 2);
BOOST_PYTHON_FUNCTION_OVERLOADS(write_hdf5_overloads, writeHDF5, 2, 3);

void declare_hdf5() {

  bpy::def("readHDF5", 
           read_hdf5, 
           read_hdf5_overloads(
             bpy::args("filename", "dataset_name"), 
             "returns the specified HDF5 image")[bpy::return_value_policy<bpy::manage_new_object>()]);
  
  bpy::def("writeHDF5",
           yayi::IO::writeHDF5, 
           write_hdf5_overloads(
             bpy::args("filename", "image", "dataset_name"), 
             "writes the image into the specified file"));

}


#endif
