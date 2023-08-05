/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_CHANNELS_PROCESS_HPP__
#define YAYI_CHANNELS_PROCESS_HPP__

/*!@file
 * This file contains the declaration for channel processing on "multispectral" images
 * @author Raffi Enficiaud
 */

#include <Yayi/core/yayiPixelProcessing/yayiPixelProcessing.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>



namespace yayi {

  /*!@brief Copy one channel of the input image into another channel of another image (potentially the same image)
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy_one_channel_to_another(const IImage* imin, const unsigned int channel_input, const unsigned int channel_output, IImage* imout);


  /*!@brief Copy one channel of the input image into another image which can accept a scalar representation of the pixel of the first image.
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy_one_channel(const IImage* imin, const unsigned int channel_input, IImage* imout);

  /*!@brief Copy the content of the input image into the specified channel of the output image
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy_to_channel(const IImage* imin, const unsigned int channel_output, IImage* imout);



  /*!@brief Split the color input image into the first three components (images should be of the same size).
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy_split_channels(const IImage* imin, IImage* imo1, IImage* imo2, IImage* imo3);
  
  
  /*!@brief Compose the first three channels of the output images from each source image (images should be of the same size and sources should be
   * of the same type).
   *
   * @author Raffi Enficiaud
   */
  YPix_ yaRC copy_compose_channels(const IImage* imin1, const IImage* imin2, const IImage* imin3, IImage* imout);

}


#endif

