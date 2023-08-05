/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiDistancesPython/distances_python.hpp>
#include <Yayi/core/yayiDistances/morphological_distance.hpp>
using namespace bpy;


void declare_binary_distance() {

  def("DistanceFromSetsBoundary",
    &yayi::distances::DistanceFromSetsBoundary, 
    "(im_source, SE, im_distance) : Performs the morphological distance transform from the sets boundary");
  
}
