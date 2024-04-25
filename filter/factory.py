from __future__ import annotations

from filter.composite import (
    CompositeSegmentationFilter,
)
from filter.opencv import (
    OpenCVBilateralFilter,
    OpenCVBlackHatFilter,
    OpenCVBrightnessFilter,
    OpenCVCannyFilter,
    OpenCVCLAHEFilter,
    OpenCVClosingFilter,
    OpenCVContourFilter,
    OpenCVContrastFilter,
    OpenCVDifferenceOfGaussiansFilter,
    OpenCVDilationFilter,
    OpenCVErosionFilter,
    OpenCVGaussianBlurFilter,
    OpenCVHistogramEqualizationFilter,
    OpenCVHoughTransformFilter,
    OpenCVLaplacianFilter,
    OpenCVMedianBlurFilter,
    OpenCVMorphologicalGradientFilter,
    OpenCVOpeningFilter,
    OpenCVORBFilter,
    OpenCVScharrFilter,
    OpenCVSobelFilter,
    OpenCVSIFTFilter,
    OpenCVSharpenFilter,
    OpenCVSkeletonizeFilter,
    OpenCVSuperpixelSegmentationFilter,
    OpenCVThresholdFilter,
    OpenCVTopHatFilter
)
from filter.scikit import (
    ScikitBilateralFilter,
    ScikitBlackHatFilter,
    ScikitBrightnessFilter,
    ScikitCannyFilter,
    ScikitCLAHEFilter,
    ScikitClosingFilter,
    ScikitContourFilter,
    ScikitContrastFilter,
    ScikitDBSCANFilter,
    ScikitDifferenceOfGaussiansFilter,
    ScikitDilationFilter,
    ScikitErosionFilter,
    ScikitGaussianBlurFilter,
    ScikitHistogramEqualizationFilter,
    ScikitHOGFilter,
    ScikitHoughTransformFilter,
    ScikitLaplacianFilter,
    ScikitMedianBlurFilter,
    ScikitMorphologicalGradientFilter,
    ScikitOpeningFilter,
    ScikitORBFilter,
    ScikitScharrFilter,
    ScikitSobelFilter,
    ScikitSIFTFilter,
    ScikitSharpenFilter,
    ScikitSkeletonizeFilter,
    ScikitSuperpixelSegmentationFilter,
    ScikitThresholdFilter,
    ScikitTopHatFilter,
    ScikitWatershedFilter
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from filter.base import BaseFilter


class FilterFactory:
    @staticmethod
    def create_filter(data: dict[str: float | str]) -> BaseFilter:
        library = data.get('library')

        match library:
            case 'composite':
                mapping = {
                    'segmentation': CompositeSegmentationFilter
                }

            case 'opencv':
                mapping = {
                    'bilateral': OpenCVBilateralFilter,
                    'black_hat': OpenCVBlackHatFilter,
                    'brightness': OpenCVBrightnessFilter,
                    'canny': OpenCVCannyFilter,
                    'clahe': OpenCVCLAHEFilter,
                    'closing': OpenCVClosingFilter,
                    'contour': OpenCVContourFilter,
                    'contrast': OpenCVContrastFilter,
                    'dilation': OpenCVDilationFilter,
                    'difference_of_gaussians': OpenCVDifferenceOfGaussiansFilter,
                    'erosion': OpenCVErosionFilter,
                    'gaussian': OpenCVGaussianBlurFilter,
                    'histogram_equalization': OpenCVHistogramEqualizationFilter,
                    'hough': OpenCVHoughTransformFilter,
                    'laplacian': OpenCVLaplacianFilter,
                    'median': OpenCVMedianBlurFilter,
                    'morphological_gradient': OpenCVMorphologicalGradientFilter,
                    'opening': OpenCVOpeningFilter,
                    'orb': OpenCVORBFilter,
                    'scharr': OpenCVScharrFilter,
                    'sift': OpenCVSIFTFilter,
                    'sharpen': OpenCVSharpenFilter,
                    'skeletonize': OpenCVSkeletonizeFilter,
                    'sobel': OpenCVSobelFilter,
                    'superpixel_segmentation': OpenCVSuperpixelSegmentationFilter,
                    'threshold': OpenCVThresholdFilter,
                    'top_hat': OpenCVTopHatFilter
                }

            case 'scikit':
                mapping = {
                    'bilateral': ScikitBilateralFilter,
                    'black_hat': ScikitBlackHatFilter,
                    'brightness': ScikitBrightnessFilter,
                    'canny': ScikitCannyFilter,
                    'clahe': ScikitCLAHEFilter,
                    'closing': ScikitClosingFilter,
                    'contour': ScikitContourFilter,
                    'contrast': ScikitContrastFilter,
                    'dbscan': ScikitDBSCANFilter,
                    'dilation': ScikitDilationFilter,
                    'difference_of_gaussians': ScikitDifferenceOfGaussiansFilter,
                    'erosion': ScikitErosionFilter,
                    'gaussian': ScikitGaussianBlurFilter,
                    'histogram_equalization': ScikitHistogramEqualizationFilter,
                    'hog': ScikitHOGFilter,
                    'hough': ScikitHoughTransformFilter,
                    'laplacian': ScikitLaplacianFilter,
                    'median': ScikitMedianBlurFilter,
                    'morphological_gradient': ScikitMorphologicalGradientFilter,
                    'opening': ScikitOpeningFilter,
                    'orb': ScikitORBFilter,
                    'scharr': ScikitScharrFilter,
                    'sift': ScikitSIFTFilter,
                    'sharpen': ScikitSharpenFilter,
                    'skeletonize': OpenCVSkeletonizeFilter,
                    'sobel': ScikitSobelFilter,
                    'superpixel_segmentation': ScikitSuperpixelSegmentationFilter,
                    'threshold': ScikitThresholdFilter,
                    'top_hat': ScikitTopHatFilter,
                    'watershed': ScikitWatershedFilter,
                }

            case 'pil':
                mapping = {

                }

            case _:
                mapping = {}

        name = data.get('name')
        parameter = data.get('parameter')

        instance = mapping.get(name)

        if instance:
            return instance(parameter)

        message = f"Unknown filter type: {name}"
        raise ValueError(message)
