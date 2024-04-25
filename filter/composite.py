from __future__ import annotations

import cv2
import numpy as np
import numpy.typing as npt

from filter.base import BaseFilter


class CompositeSegmentationFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'segmentation'

    def __repr__(self) -> str:
        return 'segmentation'

    def __str__(self) -> str:
        return 'segmentation'

    def apply(self, image: npt.NDArray) -> npt.NDArray:
        # Convert the image to 8-bit 3-channel format if it's not already
        if image.dtype != np.uint8 or len(image.shape) != 3 or image.shape[2] != 3:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        connectivity = int(self.parameter.get('connectivity', 1))
        distance_type = self.parameter.get('distance_type', cv2.DIST_L1)
        mask_size = int(self.parameter.get('mask_size', 0))
        threshold = int(self.parameter.get('threshold', 1))
        kernel_size = int(self.parameter.get('kernel_size', 1))
        distance_transform = int(self.parameter.get('distance_transform', 1))
        morphology_operation = self.parameter.get('morphology_operation', cv2.MORPH_DILATE)
        threshold_type = self.parameter.get('threshold_type', cv2.THRESH_BINARY)

        # Convert to grayscale
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply threshold
        _, binary_threshold = cv2.threshold(grayscale, threshold, 255, threshold_type)

        # Apply dilation
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilation = cv2.morphologyEx(binary_threshold, morphology_operation, kernel)

        # Apply distance transform
        dist_transform = cv2.distanceTransform(dilation, distance_type, mask_size)

        # Apply threshold to distance transform
        _, dist_threshold = cv2.threshold(dist_transform, distance_transform, 255, cv2.THRESH_BINARY)

        # Convert to 8-bit image
        dist_threshold = np.uint8(dist_threshold)

        # Apply connected components
        _, labels = cv2.connectedComponents(dist_threshold, connectivity)

        # Apply watershed
        labels = labels.astype(np.int32)
        cv2.watershed(image, labels)

        # Highlight boundaries
        image[labels == -1] = [255, 0, 0]

        return image
