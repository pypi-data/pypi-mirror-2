/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_COMMON_LABELS_HPP__
#define YAYI_COMMON_LABELS_HPP__

/*!@file
 * This file defines the labels used usually for determining the state of pixels, inside working images
 * @author Raffi Enficiaud
 */

namespace yayi
{

  //! Labels values for working images
  typedef enum e_labels 
  {
    e_lab_candidate,                      //!< The point is a candidate
    e_lab_processed,                      //!< The point has been processed
    e_lab_queued,                         //!< The point is inside a queue
    e_lab_queued2,                        //!< The point is inside a queue and potentially conflicting
    e_lab_watershed                       //!< The point is part of the watershed line
  } labels;
  
  
  
  //! Type to be used in order to define a label image (enums in C++ are coded as int, which is too expensive in terms of memory footprint).
  typedef yaUINT8 label_image_pixel_t;

}

#endif /* YAYI_COMMON_LABELS_HPP__ */
