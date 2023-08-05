/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */



#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

#include <Yayi/python/yayiIOPython/io_python.hpp>

void declare_jpg();
void declare_png();
void declare_raw();
#ifdef YAYI_IO_HDF5_ENABLED__
  void declare_hdf5();
#endif
#ifdef YAYI_IO_NUMPY_ENABLED__
  void declare_numpy();
#endif

void declare_numpy();

BOOST_PYTHON_MODULE( YayiIOPython )
{
  declare_jpg();
  declare_png();
  declare_raw();
  #ifdef YAYI_IO_HDF5_ENABLED__
    declare_hdf5();
  #endif
  #ifdef YAYI_IO_NUMPY_ENABLED__
    declare_numpy();
  #endif
}
