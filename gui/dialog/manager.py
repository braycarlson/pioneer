from __future__ import annotations

from gui.dialog.composite.segmentation import CompositeSegmentation
from gui.dialog.opencv.bilateral import OpenCVBilateral
from gui.dialog.opencv.black_hat import OpenCVBlackHat
from gui.dialog.opencv.brightness import OpenCVBrightness
from gui.dialog.opencv.canny import OpenCVCanny
from gui.dialog.opencv.clahe import OpenCVCLAHE
from gui.dialog.opencv.closing import OpenCVClosing
from gui.dialog.opencv.contour import OpenCVContour
from gui.dialog.opencv.contrast import OpenCVContrast
from gui.dialog.opencv.dilation import OpenCVDilation
from gui.dialog.opencv.difference_of_gaussians import OpenCVDifferenceOfGaussians
from gui.dialog.opencv.erosion import OpenCVErosion
from gui.dialog.opencv.gaussian import OpenCVGaussian
from gui.dialog.opencv.histogram_equalization import OpenCVHistogramEqualization
from gui.dialog.opencv.hough import OpenCVHough
from gui.dialog.opencv.laplacian import OpenCVLaplacian
from gui.dialog.opencv.median import OpenCVMedian
from gui.dialog.opencv.morphological_gradient import OpenCVMorphologicalGradient
from gui.dialog.opencv.opening import OpenCVOpening
from gui.dialog.opencv.orb import OpenCVORB
from gui.dialog.opencv.scharr import OpenCVScharrOperator
from gui.dialog.opencv.sift import OpenCVSIFT
from gui.dialog.opencv.sharpen import OpenCVSharpen
from gui.dialog.opencv.skeletonize import OpenCVSkeletonize
from gui.dialog.opencv.sobel import OpenCVSobel
from gui.dialog.opencv.superpixel_segmentation import OpenCVSuperpixelSegmentation
from gui.dialog.opencv.threshold import OpenCVThreshold
from gui.dialog.opencv.top_hat import OpenCVTopHat

from gui.dialog.scikit.bilateral import ScikitBilateral
from gui.dialog.scikit.black_hat import ScikitBlackHat
from gui.dialog.scikit.brightness import ScikitBrightness
from gui.dialog.scikit.canny import ScikitCanny
from gui.dialog.scikit.clahe import ScikitCLAHE
from gui.dialog.scikit.closing import ScikitClosing
from gui.dialog.scikit.contour import ScikitContour
from gui.dialog.scikit.contrast import ScikitContrast
from gui.dialog.scikit.dilation import ScikitDilation
from gui.dialog.scikit.difference_of_gaussians import ScikitDifferenceOfGaussians
from gui.dialog.scikit.erosion import ScikitErosion
from gui.dialog.scikit.gaussian import ScikitGaussian
from gui.dialog.scikit.histogram_equalization import ScikitHistogramEqualization
from gui.dialog.scikit.hough import ScikitHough
from gui.dialog.scikit.laplacian import ScikitLaplacian
from gui.dialog.scikit.median import ScikitMedian
from gui.dialog.scikit.morphological_gradient import ScikitMorphologicalGradient
from gui.dialog.scikit.opening import ScikitOpening
from gui.dialog.scikit.orb import ScikitORB
from gui.dialog.scikit.scharr import ScikitScharrOperator
from gui.dialog.scikit.sift import ScikitSIFT
from gui.dialog.scikit.sharpen import ScikitSharpen
from gui.dialog.scikit.skeletonize import ScikitSkeletonize
from gui.dialog.scikit.sobel import ScikitSobel
from gui.dialog.scikit.superpixel_segmentation import ScikitSuperpixelSegmentation
from gui.dialog.scikit.threshold import ScikitThreshold
from gui.dialog.scikit.top_hat import ScikitTopHat

from gui.dialog.scikit.dbscan import ScikitDBSCAN
from gui.dialog.scikit.hog import ScikitHOG
from gui.dialog.scikit.watershed import ScikitWatershed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.dialog.floating import Dialog
    from typing_extensions import ClassVar, Self


class DialogManager:
    _instance: DialogManager = None

    _mapping: ClassVar[dict[str, Dialog]] = {
        # Composite
        'composite_segmentation': CompositeSegmentation,

        # OpenCV
        'opencv_bilateral': OpenCVBilateral,
        'opencv_black_hat': OpenCVBlackHat,
        'opencv_brightness': OpenCVBrightness,
        'opencv_canny': OpenCVCanny,
        'opencv_clahe': OpenCVCLAHE,
        'opencv_closing': OpenCVClosing,
        'opencv_contour': OpenCVContour,
        'opencv_contrast': OpenCVContrast,
        'opencv_difference_of_gaussians': OpenCVDifferenceOfGaussians,
        'opencv_dilation': OpenCVDilation,
        'opencv_erosion': OpenCVErosion,
        'opencv_gaussian': OpenCVGaussian,
        'opencv_histogram_equalization': OpenCVHistogramEqualization,
        'opencv_hough': OpenCVHough,
        'opencv_laplacian': OpenCVLaplacian,
        'opencv_median': OpenCVMedian,
        'opencv_morphological_gradient': OpenCVMorphologicalGradient,
        'opencv_opening': OpenCVOpening,
        'opencv_orb': OpenCVORB,
        'opencv_scharr': OpenCVScharrOperator,
        'opencv_sift': OpenCVSIFT,
        'opencv_sharpen': OpenCVSharpen,
        'opencv_skeletonize': OpenCVSkeletonize,
        'opencv_sobel': OpenCVSobel,
        'opencv_superpixel_segmentation': OpenCVSuperpixelSegmentation,
        'opencv_threshold': OpenCVThreshold,
        'opencv_top_hat': OpenCVTopHat,

        # Scikit
        'scikit_bilateral': ScikitBilateral,
        'scikit_black_hat': ScikitBlackHat,
        'scikit_brightness': ScikitBrightness,
        'scikit_canny': ScikitCanny,
        'scikit_clahe': ScikitCLAHE,
        'scikit_closing': ScikitClosing,
        'scikit_contour': ScikitContour,
        'scikit_contrast': ScikitContrast,
        'scikit_dbscan': ScikitDBSCAN,
        'scikit_difference_of_gaussians': ScikitDifferenceOfGaussians,
        'scikit_dilation': ScikitDilation,
        'scikit_erosion': ScikitErosion,
        'scikit_gaussian': ScikitGaussian,
        'scikit_histogram_equalization': ScikitHistogramEqualization,
        'scikit_hog': ScikitHOG,
        'scikit_hough': ScikitHough,
        'scikit_laplacian': ScikitLaplacian,
        'scikit_median': ScikitMedian,
        'scikit_morphological_gradient': ScikitMorphologicalGradient,
        'scikit_opening': ScikitOpening,
        'scikit_orb': ScikitORB,
        'scikit_scharr': ScikitScharrOperator,
        'scikit_sift': ScikitSIFT,
        'scikit_sharpen': ScikitSharpen,
        'scikit_skeletonize': ScikitSkeletonize,
        'scikit_sobel': ScikitSobel,
        'scikit_superpixel_segmentation': ScikitSuperpixelSegmentation,
        'scikit_threshold': ScikitThreshold,
        'scikit_top_hat': ScikitTopHat,
        'scikit_watershed': ScikitWatershed
    }

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reference = {}

        return cls._instance

    def create(self, tid: str, signal: str, fid: str) -> Dialog:
        if tid not in self.reference:
            self.reference[tid] = {}

        dialog = self._mapping.get(signal)
        instance = dialog(fid)

        pair = (signal + fid)
        self.reference[tid][pair] = instance

        return instance

    def get(self, tid: str, signal: str, fid: str) -> Dialog:
        pair = (signal + fid)

        if tid not in self.reference or pair not in self.reference[tid]:
            return self.create(tid, signal, fid)

        return self.reference[tid][pair]

    def remove(self, tid: str, signal: str, fid: str) -> None:
        pair = (signal, fid)

        if tid in self.reference and pair in self.reference[tid]:
            del self.reference[tid][pair]

    def reset(self, tab: str) -> None:
        if tab in self.reference:
            del self.reference[tab]

    def view(self) -> None:
        for tid, dialog in self.reference.items():
            print(tid, dialog)
