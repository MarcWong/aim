#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    UIED segmentation


Description:
    A GUI element detection toolkit that leverages old-fashioned computer
    vision algorithms for non-text region extraction, and deep learning
    models to perform classifications and text detection.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Xie, M., Feng, S., Xing, Z., Chen, J., and Chen, C. (2020). UIED: A
        Hybrid Tool for GUI Element Detection. In Proceedings of the 28th ACM
        Joint Meeting on European Software Engineering Conference and
        Symposium on the Foundations of Software Engineering (ESEC/FSE '20),
        pp. 1655-1659. ACM. doi: https://doi.org/10.1145/3368089.3417940

    2.  Chen, J., Xie, M., Xing, Z., Chen, C., Xu, X., Zhu, L., and Li, G.
        (2020). Object Detection for Graphical User Interface: Old Fashioned
        or Deep Learning or a Combination? In Proceedings of the 28th ACM
        Joint Meeting on European Software Engineering Conference and
        Symposium on the Foundations of Software Engineering (ESEC/FSE '20),
        pp. 1202-1214. ACM. doi: https://doi.org/10.1145/3368089.3409691


Change log:
    v1.0 (2022-08-05)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Any, Dict, List, Optional, Union

# Third-party modules
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: UIED segmentation.

    Reference:
        Based on Xie et al.'s Python implementation available at https://github.com/MulongXie/UIED.
    """

    # Public methods
    @classmethod
    def execute_metric(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_segments: Optional[Dict[str, Any]] = None,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_segments: GUI segments (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - UIED segmented image (str, image (PNG) encoded in Base64)
        """
        # Get all elements
        if gui_segments is not None:
            segmented_im_b64: str = gui_segments["img_b64"]
        else:
            raise ValueError("The value of 'gui_segments' cannot be 'None'.")

        return [
            segmented_im_b64,
        ]
