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
#include <Yayi/core/yayiDistances/quasi_distance.hpp>
using namespace bpy;


void declare_quasi_distance() {
  def("QuasiDistance",
    &yayi::distances::quasi_distance, 
    "(im_source, SE, im_distance, im_residuals) : Performs the unregularized quasi-distance morphological transform");
  
  def("QuasiDistancesWeighted",
    &yayi::distances::quasi_distance_weighted, 
    "(im_source, SE, weights, im_distance, im_residuals) : Performs the unregularized weighted quasi-distance morphological transform");

  def("DistanceRegularization",
    &yayi::distances::DistancesRegularization, 
    "(im_distance, SE, im_regular_distance) : forces the 1-Lipschitz property on the distance map returned by the QuasiDistance algorithm");
}
