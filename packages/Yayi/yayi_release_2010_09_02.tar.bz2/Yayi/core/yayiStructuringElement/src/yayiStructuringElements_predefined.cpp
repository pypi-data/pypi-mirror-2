/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */


#include <Yayi/core/yayiStructuringElement/yayiRuntimeStructuringElements_predefined.hpp>

namespace yayi { namespace se {
#define SE_FROM_TABLE(c, x) c::from_table_multiple(x, x + sizeof(x)/sizeof(x[0]))

  s_coordinate<2>::scalar_coordinate_type const coords_hexa2D[] = 
  {
    0,0, 1,0, -1,0, 0,1, 0,-1, 1,-1, 1,1,
    0,0, 1,0, -1,0, 0,1, 0,-1, -1,-1, -1,1
  };

  const s_neighborlist_se_hexa_x< s_coordinate<2> > SEHex2D(SE_FROM_TABLE(s_coordinate<2>, coords_hexa2D));


  s_coordinate<2>::scalar_coordinate_type const coords_sq2D[] = 
  {
    0,0, 
    1,0, -1,0, 
    0,1, 0,-1, 
    1,-1, 1,1, -1,1, -1,-1
  };
    
  const s_neighborlist_se< s_coordinate<2> > SESquare2D(SE_FROM_TABLE(s_coordinate<2>, coords_sq2D));

  s_coordinate<2>::scalar_coordinate_type const coords_cross2D[] = 
  {
    0,0, 
    1,0, -1,0, 
    0,1, 0,-1 
  };
    
  const s_neighborlist_se< s_coordinate<2> > SECross2D(SE_FROM_TABLE(s_coordinate<2>, coords_cross2D));


  s_coordinate<3>::scalar_coordinate_type const coords_sq3D[] = 
  {
    0,0,0,
    1,0,0, -1,0,0, 
    0,1,0, 0,-1,0,
    1,-1,0, 1,1,0, -1,1,0, -1,-1,0, 
    
    0,0,-1,
    1,0,-1, -1,0,-1, 
    0,1,-1, 0,-1,-1,
    1,-1,-1, 1,1,-1, -1,1,-1, -1,-1,-1, 
    
    0,0,1,
    1,0,1, -1,0,1, 
    0,1,1, 0,-1,1,
    1,-1,1, 1,1,1, -1,1,1, -1,-1,1 
  };
    
  const s_neighborlist_se< s_coordinate<3> > SESquare3D(SE_FROM_TABLE(s_coordinate<3>, coords_sq3D));

  s_coordinate<1>::scalar_coordinate_type const coords_segmentX1D[] = {-1, 0, 1};
  const s_neighborlist_se< s_coordinate<1> > SESegmentX1D(SE_FROM_TABLE(s_coordinate<1>, coords_segmentX1D));




  s_coordinate<2>::scalar_coordinate_type const coords_segmentX2D[] = 
  {
    -1,0,
    0,0,
    1,0
  };
  const s_neighborlist_se< s_coordinate<2> > SESegmentX2D(SE_FROM_TABLE(s_coordinate<2>, coords_segmentX2D));


  s_coordinate<2>::scalar_coordinate_type const coords_segmentY2D[] = 
  {
    0,-1,
    0,0,
    0,1
  };
  const s_neighborlist_se< s_coordinate<2> > SESegmentY2D(SE_FROM_TABLE(s_coordinate<2>, coords_segmentY2D));


  s_coordinate<3>::scalar_coordinate_type const coords_segmentX3D[] = 
  {
    -1,0,0,
    0,0,0,
    1,0,0
  };
  const s_neighborlist_se< s_coordinate<3> > SESegmentX3D(SE_FROM_TABLE(s_coordinate<3>, coords_segmentX3D));

  s_coordinate<3>::scalar_coordinate_type const coords_segmentY3D[] = 
  {
    0,-1,0,
    0,0,0,
    0,1,0
  };
  const s_neighborlist_se< s_coordinate<3> > SESegmentY3D(SE_FROM_TABLE(s_coordinate<3>, coords_segmentY3D));


  s_coordinate<3>::scalar_coordinate_type const coords_segmentZ3D[] = 
  {
    0,0,0,
    0,0,-1,
    0,0,1,
  };

  const s_neighborlist_se< s_coordinate<3> > SESegmentZ3D(SE_FROM_TABLE(s_coordinate<3>, coords_segmentZ3D));

}}

