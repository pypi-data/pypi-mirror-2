/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/python/yayiReconstructionPython/reconstruction_python.hpp>


#include <boost/python/ssize_t.hpp>
#include <boost/python/module.hpp>
#include <boost/python/detail/none.hpp>

namespace bpy = boost::python;

void declare_morphological_reconstructions();
void declare_morphological_fill_holes();
BOOST_PYTHON_MODULE( YayiReconstructionPython )
{
  declare_morphological_reconstructions();
  declare_morphological_fill_holes();
}
