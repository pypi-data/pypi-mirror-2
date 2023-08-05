/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__
#define YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__

/*!@file
 * This file defines some usual structuring elements
 *
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiCommon/common_coordinates.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_t.hpp>
#include <Yayi/core/yayiStructuringElement/include/yayiRuntimeStructuringElement_hexagon_t.hpp>



namespace yayi { namespace se {

  
  /*!@brief Hexagonal alternating structuring element
   * This SE changes its shape according to the line on which it is centered. The two shapes are ("x" represents a neighbor and "." an adjacent point not in the
   * neighborhood):
   * 
   * . x x      x x .
   * x x x      x x x
   * . x x      x x .
   *
   * @remark: This se "approximates" the unit euclidian ball
   * @todo Raffi: voir les listes doxygen
   */
  YSE_ extern const s_neighborlist_se_hexa_x< s_coordinate<2> > SEHex2D;
  
  //! @todo : Raffi: ??
  YSE_ extern const s_neighborlist_se_hexa_x< s_coordinate<3> > SEHex3D;


  /*!@brief Square structuring element (2D)
   * Square rigid structuring element (2D)
   * 
   * x x x
   * x x x
   * x x x
   *
   * @remark: This se is the unit ball for L\infty distance on 2D
   * @todo Raffi: voir les listes doxygen et les commandes latex
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESquare2D;

  /*!@brief Cross structuring element (2D)
   * Cross rigid structuring element (2D)
   * 
   *   x 
   * x x x
   *   x 
   *
   * @remark: This se is the unit ball for L1 distance on 2D
   * @todo Raffi: voir les listes doxygen et les commandes latex
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SECross2D;



  /*! Line structuring element / segment of unit size along X (1D)
   * 
   * x x x
   * 
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<1> > SESegmentX1D;

  /*! Line structuring element / segment of unit size along X (2D)
   * 
   * x x x
   * 
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESegmentX2D;

  /*! Line structuring element / segment of unit size along Y (2D)
   *   x
   *   x
   *   x
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<2> > SESegmentY2D;



  /*! Line structuring element / segment of unit size along X (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentX3D;

  /*! Line structuring element / segment of unit size along Y (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentY3D;

  /*! Line structuring element / segment of unit size along Z (3D)
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESegmentZ3D;

  /*!@brief Square structuring element (3D)
   * Square rigid structuring element (3D), having a thickness of 3 and is a SESquare2D along z axis
   * 
   * @remark: This se is the unit ball for L\infty distance on 3D
   * @todo Raffi: voir les listes doxygen et les commandes latex
   */
  YSE_ extern const s_neighborlist_se< s_coordinate<3> > SESquare3D;


}}

#endif /* YAYI_STRUCTURING_ELEMENT_PREDEFINED_HPP__ */
