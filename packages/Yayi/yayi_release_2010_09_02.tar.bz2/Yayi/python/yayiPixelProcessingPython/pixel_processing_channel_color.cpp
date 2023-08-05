/*
 *  -:- LICENCE -:- 
 * Copyright Raffi Enficiaud 2007-2010
 * 
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file ../../LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 * 
 *  -:- LICENCE -:- 
 */

#include <Yayi/python/yayiPixelProcessingPython/pixelprocessing_python.hpp>


#include <Yayi/core/yayiPixelProcessing/image_channels_process.hpp>
#include <Yayi/core/yayiPixelProcessing/image_color_process.hpp>


using namespace bpy;

void declare_channel_color() {

  def("CopyOneChannelIntoAnother",
    &yayi::copy_one_channel_to_another,
    args("im_source", "channel_input", "channel_output", "im_destination"),
    "Copy the channel channel_input of the first image into the channel channel_output of the second image");

  def("CopyOneChannel",
    &yayi::copy_one_channel,
    args("im_source", "channel_input", "im_destination"),
    "Copy the channel channel_input of the first image into the second (scalar) image");
    
  def("CopyIntoChannel",
    &yayi::copy_to_channel,
    args("im_source", "channel_output", "im_destination"),
    "Copy the input image (im_source) into the specified channel (channel_output) of the output image (im_destination)");

  def("CopySplitChannels",
    &yayi::copy_split_channels,
    args("im_source", "channel1_out", "channel2_out", "channel3_out"),
    "Copy each channel of the input image into the output images");

  def("CopyComposeChannels",
    &yayi::copy_compose_channels,
    args("im_source1", "im_source2", "im_source3", "im_out"),
    "Copy each image pixel into a channel of the output image (in the same order as provided)");






  def("RGB_to_HLS_l1",
    &yayi::RGB_to_HLS_l1,
    args("im_source", "im_destination"),
    "Transforms the colour space of the the RGB input image to HLS l1");
  def("HLS_l1_to_RGB",
    &yayi::HLS_l1_to_RGB,
    args("im_source", "im_destination"),
    "Transforms the colour space of the the HLS l1 input image to RGB");


}

