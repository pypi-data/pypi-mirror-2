/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#ifndef YAYI_IO_HPP__
#define YAYI_IO_HPP__

/*! @file
 *  @brief Global definition for the I/O library
 *
 */


#include <Yayi/core/yayiCommon/common_config.hpp>
#include <Yayi/core/yayiImageCore/include/yayiImageCore.hpp>



#ifdef YAYI_EXPORT_IO_
#define YIO_ MODULE_EXPORT
#else
#define YIO_ MODULE_IMPORT
#endif


namespace yayi
{
  namespace IO
  {

    //! Reads a PNG file
    YIO_ yaRC readPNG (const string_type &filename, IImage*& image);
    //! Writes the image into the provided PNG file
    YIO_ yaRC writePNG(const string_type &filename, const IImage* const & image);

    //! Reads a JPG file
    YIO_ yaRC readJPG (const string_type &filename, IImage*& image);
    //! Writes the image into the provided JPG file
    YIO_ yaRC writeJPG(const string_type &filename, const IImage* const & image);

    //! Reads a RAW file
    //! For this type of file, the dimensions and the type of the image should be provided
    YIO_ yaRC readRAW (const string_type &filename, const s_coordinate<0> &sizes, const type &image_type_, IImage* &out_image);
    //! Writes the image into the provided RAW file
    YIO_ yaRC writeRAW(const string_type &filename, const IImage* const & image);

    // HDF5 Support
    #ifdef YAYI_IO_HDF5_ENABLED__
    //! Reads a HDF5 file
    //! The image name can be added to the command, in order to read parts of the HDF5 file
    YIO_ yaRC readHDF5 (const string_type &filename, IImage* &out_image, const std::string &image_name = "yayi_image_1");
    YIO_ yaRC writeHDF5(const string_type &filename, const IImage* const & image, const std::string &image_name = "yayi_image_1");    
    #endif
    
    

  }
}

#endif

