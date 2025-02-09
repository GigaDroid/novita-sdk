#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union, Any
import os
from PIL import Image
from .serializer import JSONe
from enum import Enum
from .utils import batch_download_images
import base64


# --------------- ControlNet ---------------

class ControlNetMode(Enum):
    BALANCED = 0
    PROMPT_IMPORTANCE = 1
    CONTROLNET_IMPORTANCE = 2

    def __str__(self):
        return self.name


class ControlNetResizeMode(Enum):
    JUST_RESIZE = 0
    RESIZE_OR_CORP = 1
    RESIZE_AND_FILL = 2

    def __str__(self):
        return self.name


class ControlNetPreprocessor(Enum):
    NULL = 'none'
    CANNY = 'canny'
    DEPTH = 'depth'
    DEPTH_LERES = 'depth_leres'
    DEPTH_LERES_PLUS_PLUS = 'depth_leres++'
    HED = 'hed'
    HED_SAFE = 'hed_safe'
    MEDIAPIPE_FACE = 'mediapipe_face'
    MLSD = 'mlsd'
    NORMAL_MAP = 'normal_map'
    OPENPOSE = 'openpose'
    OPENPOSE_HAND = 'openpose_hand'
    OPENPOSE_FACE = 'openpose_face'
    OPENPOSE_FACEONLY = 'openpose_faceonly'
    OPENPOSE_FULL = 'openpose_full'
    CLIP_VISION = 'clip_vision'
    COLOR = 'color'
    PIDINET = 'pidinet'
    PIDINET_SAFE = 'pidinet_safe'
    PIDINET_SKETCH = 'pidinet_sketch'
    PIDINET_SCRIBBLE = 'pidinet_scribble'
    SCRIBBLE_XDOG = 'scribble_xdog'
    SCRIBBLE_HED = 'scribble_hed'
    SEGMENTATION = 'segmentation'
    THRESHOLD = 'threshold'
    DEPTH_ZOE = 'depth_zoe'
    NORMAL_BAE = 'normal_bae'
    ONEFORMER_COCO = 'oneformer_coco'
    ONEFORMER_ADE20K = 'oneformer_ade20k'
    LINEART = 'lineart'
    LINEART_COARSE = 'lineart_coarse'
    LINEART_ANIME = 'lineart_anime'
    LINEART_STANDARD = 'lineart_standard'
    SHUFFLE = 'shuffle'
    TILE_RESAMPLE = 'tile_resample'
    INVERT = 'invert'
    LINEART_ANIME_DENOISE = 'lineart_anime_denoise'
    REFERENCE_ONLY = 'reference_only'
    REFERENCE_ADAIN = 'reference_adain'
    REFERENCE_ADAIN_PLUS_ATTN = 'reference_adain+attn'
    INPAINT = 'inpaint'
    INPAINT_ONLY = 'inpaint_only'
    INPAINT_ONLY_PLUS_LAMA = 'inpaint_only+lama'
    TILE_COLORFIX = 'tile_colorfix'
    TILE_COLORFIX_PLUS_SHARP = 'tile_colorfix+sharp'

    def __str__(self):
        return self.name


@dataclass
class ControlnetUnit(JSONe):
    model: str
    weight: Optional[float] = 1
    module: Optional[ControlNetPreprocessor] = ControlNetPreprocessor.NULL
    input_image: Optional[str] = None
    control_mode: Optional[ControlNetMode] = ControlNetMode.BALANCED
    resize_mode: Optional[ControlNetResizeMode] = ControlNetResizeMode.RESIZE_OR_CORP
    mask: Optional[str] = None
    processor_res: Optional[int] = 512
    threshold_a: Optional[int] = 64
    threshold_b: Optional[int] = 64
    guidance_start: Optional[float] = 0.0
    guidance_end: Optional[float] = 1.0
    pixel_perfect: Optional[bool] = False


# --------------- Samplers ---------------
@dataclass
class Samplers:
    EULER_A = 'Euler a'
    EULER = 'Euler'
    LMS = 'LMS'
    HEUN = 'Heun'
    DPM2 = 'DPM2'
    DPM2_A = 'DPM2 a'
    DPM2_KARRAS = 'DPM2 Karras'
    DPM2_A_KARRAS = 'DPM2 a Karras'
    DPMPP_S_A = 'DPM++ 2S a'
    DPMPP_M = 'DPM++ 2M'
    DPMPP_SDE = 'DPM++ SDE'
    DPMPP_KARRAS = 'DPM++ Karras'
    DPMPP_S_A_KARRAS = 'DPM++ 2S a Karras'
    DPMPP_M_KARRAS = 'DPM++ 2M Karras'
    DPMPP_SDE_KARRAS = 'DPM++ SDE Karras'
    DDIM = 'DDIM'
    PLMS = 'PLMS'
    UNIPC = 'UniPC'


# --------------- Refiner ---------------
@dataclass
class Refiner:
    checkpoint: str
    switch_at: float

# --------------- ADEtailer ---------------


@dataclass
class ADEtailer:
    prompt: str
    negative_prompt: Optional[str] = None
    steps: Optional[int] = 20
    strength: Optional[float] = 0.5
    seed: Optional[int] = None


# --------------- Text2Image ---------------


@dataclass
class Txt2ImgRequestExtra(JSONe):
    enable_nsfw_detection: bool


@dataclass
class Txt2ImgRequest(JSONe):
    prompt: str
    negative_prompt: Optional[str] = None
    model_name: str = 'dreamshaper_5BakedVae.safetensors'
    sampler_name: str = None
    batch_size: int = 1
    n_iter: int = 1
    steps: int = 20
    cfg_scale: float = 7
    height: int = 512
    width: int = 512

    seed: Optional[int] = -1
    restore_faces: Optional[bool] = False
    sd_vae: Optional[str] = None
    clip_skip: Optional[int] = None

    controlnet_units: Optional[List[ControlnetUnit]] = None
    controlnet_no_detectmap: Optional[bool] = False

    enable_hr: Optional[bool] = False
    hr_upscaler: Optional[str] = 'R-ESRGAN 4x+'
    hr_scale: Optional[float] = 2.0
    hr_resize_x: Optional[int] = None
    hr_resize_y: Optional[int] = None

    sd_refiner: Optional[Refiner] = None

    adetailer: Optional[ADEtailer] = None

    extra: Optional[Txt2ImgRequestExtra] = None


class Txt2ImgResponseCode(Enum):
    NORMAL = 0
    INTERNAL_ERROR = -1
    INVALID_JSON = 1
    MODEL_NOT_EXISTS = 2
    TASK_ID_NOT_EXISTS = 3
    INVALID_AUTH = 4
    HOST_UNAVAILABLE = 5
    PARAM_RANGE_ERROR = 6
    COST_BALANCE_ERROR = 7
    SAMPLER_NOT_EXISTS = 8
    TIMEOUT = 9

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class Txt2ImgResponseData(JSONe):
    task_id: str
    warn: Optional[str] = None


@dataclass
class Txt2ImgResponse(JSONe):
    code: Txt2ImgResponseCode
    msg: str
    data: Optional[Txt2ImgResponseData] = None


#  --------------- Image2Image ---------------


@dataclass
class Img2ImgRequest(JSONe):
    model_name: str = 'dreamshaper_5BakedVae.safetensors'
    sampler_name: str = None
    init_images: List[str] = None
    mask: Optional[str] = None
    resize_mode: Optional[int] = 0
    denoising_strength: Optional[float] = 0.75
    cfg_scale: Optional[float] = None
    mask_blur: Optional[int] = 4
    inpainting_fill: Optional[int] = 1
    inpaint_full_res: Optional[int] = 0
    inpaint_full_res_padding: Optional[int] = 32
    inpainting_mask_invert: Optional[int] = 0
    initial_noise_multiplier: Optional[float] = 1.0
    prompt: Optional[str] = None
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    batch_size: Optional[int] = 1
    n_iter: Optional[int] = 1
    steps: Optional[int] = 20
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    restore_faces: Optional[bool] = False
    sd_vae: Optional[str] = None
    clip_skip: Optional[int] = None

    controlnet_units: Optional[List[ControlnetUnit]] = None
    controlnet_no_detectmap: Optional[bool] = False

    sd_refiner: Optional[Refiner] = None


class Img2ImgResponseCode(Enum):
    NORMAL = 0
    INTERNAL_ERROR = -1
    INVALID_JSON = 1
    MODEL_NOT_EXISTS = 2
    TASK_ID_NOT_EXISTS = 3
    INVALID_AUTH = 4
    HOST_UNAVAILABLE = 5
    PARAM_RANGE_ERROR = 6
    COST_BALANCE_ERROR = 7
    SAMPLER_NOT_EXISTS = 8
    TIMEOUT = 9

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class Img2ImgResponseData(JSONe):
    task_id: str
    warn: Optional[str] = None


@dataclass
class Img2ImgResponse(JSONe):
    code: Img2ImgResponseCode
    msg: str
    data: Optional[Img2ImgResponseData] = None


# --------------- NSFWDetectionResult ---------------

@dataclass
class NSFWDetectionResult(JSONe):
    valid: bool
    confidence: float


# --------------- Progress ---------------


class ProgressResponseStatusCode(Enum):
    INITIALIZING = 0
    RUNNING = 1
    SUCCESSFUL = 2
    FAILED = 3
    TIMEOUT = 4

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)

    def finished(self):
        return self in (ProgressResponseStatusCode.SUCCESSFUL, ProgressResponseStatusCode.FAILED, ProgressResponseStatusCode.TIMEOUT)


# --------------- NSFWDetectionResult ---------------

@dataclass
class NSFWDetectionResult(JSONe):
    valid: bool
    confidence: float


@dataclass
class ProgressData(JSONe):
    status: ProgressResponseStatusCode
    progress: int
    eta_relative: int
    enable_nsfw_detection: bool
    imgs: Optional[List[str]] = None
    imgs_bytes: Optional[List[str]] = None
    info: Optional[str] = ""
    failed_reason: Optional[str] = ""
    current_images: Optional[List[str]] = None
    submit_time: Optional[str] = ""
    execution_time: Optional[str] = ""
    txt2img_time: Optional[str] = ""
    finish_time: Optional[str] = ""
    nsfw_detection_result: Optional[List[NSFWDetectionResult]] = None




class ProgressResponseCode(Enum):
    NORMAL = 0
    INTERNAL_ERROR = -1
    INVALID_JSON = 1
    MODEL_NOT_EXISTS = 2
    TASK_ID_NOT_EXISTS = 3
    INVALID_AUTH = 4
    HOST_UNAVAILABLE = 5
    PARAM_RANGE_ERROR = 6
    COST_BALANCE_ERROR = 7
    SAMPLER_NOT_EXISTS = 8
    TIMEOUT = 9

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class ProgressResponse(JSONe):
    code: ProgressResponseCode
    data: Optional[ProgressData] = None
    msg: Optional[str] = ""

    def download_images(self):
        if self.data.imgs is not None and len(self.data.imgs) > 0:
            self.data.imgs_bytes = batch_download_images(self.data.imgs)

# --------------- Upscale ---------------


class UpscaleResizeMode(Enum):
    SCALE = 0
    SIZE = 1


@dataclass
class UpscaleRequest(JSONe):
    image: str
    upscaler_1: Optional[str] = 'R-ESRGAN 4x+'
    resize_mode: Optional[UpscaleResizeMode] = UpscaleResizeMode.SCALE
    upscaling_resize: Optional[float] = 2.0
    upscaling_resize_w: Optional[int] = None
    upscaling_resize_h: Optional[int] = None
    upscaling_crop: Optional[bool] = False

    upscaler_2: Optional[str] = None
    extras_upscaler_2_visibility: Optional[float] = None
    gfpgan_visibility: Optional[float] = None
    codeformer_visibility: Optional[float] = None
    codeformer_weight: Optional[float] = None


class UpscaleResponseCode(Enum):
    NORMAL = 0
    INTERNAL_ERROR = -1
    INVALID_JSON = 1
    MODEL_NOT_EXISTS = 2
    TASK_ID_NOT_EXISTS = 3
    INVALID_AUTH = 4
    HOST_UNAVAILABLE = 5
    PARAM_RANGE_ERROR = 6
    COST_BALANCE_ERROR = 7
    SAMPLER_NOT_EXISTS = 8
    TIMEOUT = 9

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class UpscaleResponseData(JSONe):
    task_id: str
    warn: Optional[str] = None


@dataclass
class UpscaleResponse(JSONe):
    code: UpscaleResponseCode
    msg: str
    data: Optional[UpscaleResponseData] = None

# --------------- Cleanup ---------------


@dataclass
class CleanupRequest(JSONe):
    image_file: str
    mask_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class CleanupResponse(JSONe):
    image_file: str
    image_type: str


InputImage = Union[str, os.PathLike, Image.Image]

# --------------- Outpainting ---------------


@dataclass
class OutpaintingRequest(JSONe):
    image_file: str
    width: Optional[int] = 512
    height: Optional[int] = 512
    center_x: Optional[int] = 0
    center_y: Optional[int] = 0
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class OutpaintingResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Remove Background ---------------


@dataclass
class RemoveBackgroundRequest(JSONe):
    image_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class RemoveBackgroundResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Remove Text ---------------


@dataclass
class RemoveTextRequest(JSONe):
    image_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class RemoveTextResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Reimage ---------------


@dataclass
class ReimagineRequest(JSONe):
    image_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class ReimagineResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Doodle ---------------


@dataclass
class DoodleRequest(JSONe):
    image_file: str
    prompt: str
    similarity: float = None
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class DoodleResponse(JSONe):
    image_file: str
    image_type: str


# --------------- Mix Pose ---------------

@dataclass
class MixPoseRequest(JSONe):
    image_file: str
    pose_image_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class MixPoseResponse(JSONe):
    image_file: str
    image_type: str


# --------------- Replace Background ---------------

@dataclass
class ReplaceBackgroundRequest(JSONe):
    image_file: str
    prompt: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class ReplaceBackgroundResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Replace Sky ---------------


@dataclass
class ReplaceSkyRequest(JSONe):
    image_file: str
    sky: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class ReplaceSkyResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Replace Object ---------------


@dataclass
class ReplaceObjectRequest(JSONe):
    image_file: str
    object_prompt: str
    prompt: str
    negative_prompt: Optional[str] = None
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class ReplaceObjectResponse(JSONe):
    image_file: str
    image_type: str


# --------------- V3 Task Result ---------------
# {
#   "task": {
#     "task_id": "a910c8f7-76ce-40bd-b805-f00f3ddd7dc1",
#     "status": "TASK_STATUS_SUCCEED"
#   },
#   "images": [
#     {
#       "image_url": "https://faas-output-image.s3.ap-southeast-1.amazonaws.com/dev/replace_object_a910c8f7-76ce-40bd-b805-f00f3ddd7dc1_0.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASVPYCN6LRCW3SOUV%2F20231019%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Date=20231019T084537Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=b9ad40a5cb3aecf89602c15fe72d28be5d8a33e0bfe3656ce968295fde1aab31",
#       "image_type": "png",
#       "image_url_ttl": 3600
#     }
#   ]
# }

@dataclass
class V3TaskImage(JSONe):
    image_url: str
    image_type: str
    image_url_ttl: int
    nsfw_detection_result: Optional[NSFWDetectionResult] = None


@dataclass
class V3TaskVideo(JSONe):
    video_url: str
    video_type: str
    video_url_ttl: int
    nsfw_detection_result: Optional[NSFWDetectionResult] = None


class V3TaskResponseStatus(Enum):
    TASK_STATUS_SUCCEED = "TASK_STATUS_SUCCEED"
    TASK_STATUS_QUEUED = "TASK_STATUS_QUEUED"
    TASK_STATUS_FAILED = "TASK_STATUS_FAILED"


@dataclass
class V3AsyncSubmitResponse(JSONe):
    task_id: str


@dataclass
class V3TaskResponseTask(JSONe):
    task_id: str
    status: V3TaskResponseStatus


@dataclass
class V3TaskResponseExtra(JSONe):
    seed: str
    enable_nsfw_detection: bool


@dataclass
class V3TaskResponse(JSONe):
    extra: V3TaskResponseExtra
    task: V3TaskResponseTask
    images: List[V3TaskImage] = None
    videos: List[V3TaskVideo] = None

    def finished(self):
        return self.task.status == V3TaskResponseStatus.TASK_STATUS_SUCCEED or self.task.status == V3TaskResponseStatus.TASK_STATUS_FAILED

    def get_image_urls(self):
        return [image.image_url for image in self.images]

    def get_video_urls(self):
        return [video.video_url for video in self.videos]

    def download_images(self):
        if self.images is not None and len(self.images) > 0:
            self.images_encoded = [base64.b64encode(_).decode('ascii') for _ in batch_download_images(self.get_image_urls())]

    def download_videos(self):
        if self.videos is not None and len(self.videos) > 0:
            self.video_bytes = batch_download_images(self.get_video_urls())

# --------------- Restore Faces ---------------


@dataclass
class RestoreFaceRequest(JSONe):
    image_file: str
    fidelity: Optional[float] = 0.7
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class RestoreFaceResponse(JSONe):
    image_file: str
    image_type: str


# --------------- Tile ---------------
@dataclass
class CreateTileRequest(JSONe):
    prompt: str
    negative_prompt: Optional[str] = None
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class CreateTileResponse(JSONe):
    image_file: str
    image_type: str

# --------------- Merge Face ---------------


@dataclass
class MergeFaceRequest(JSONe):
    image_file: str
    face_image_file: str
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class MergeFaceResponse(JSONe):
    image_file: str
    image_type: str

# --------------- LCM Txt2Img ---------------


@dataclass
class LCMTxt2ImgRequest(JSONe):
    prompt: str
    height: Optional[int] = 512
    width: Optional[int] = 512
    image_num: Optional[int] = 4
    steps: Optional[int] = 4
    guidance_scale: Optional[float] = 7.5


@dataclass
class LCMTxt2ImgResponseImage(JSONe):
    image_file: str
    image_type: str


@dataclass
class LCMTxt2ImgResponse(JSONe):
    images: List[LCMTxt2ImgResponseImage]

# --------------- ADEtailer ---------------


class ADETailerResponseCode(Enum):
    NORMAL = 0
    INTERNAL_ERROR = -1
    INVALID_JSON = 1
    MODEL_NOT_EXISTS = 2
    TASK_ID_NOT_EXISTS = 3
    INVALID_AUTH = 4
    HOST_UNAVAILABLE = 5
    PARAM_RANGE_ERROR = 6
    COST_BALANCE_ERROR = 7
    SAMPLER_NOT_EXISTS = 8
    TIMEOUT = 9

    UNKNOWN = 100

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class ADETailerRequest(JSONe):
    model_name: str
    input_image: str
    prompt: str
    steps: Optional[int] = 20
    strength: Optional[float] = 0.3
    negative_prompt: Optional[str] = None
    vae: Optional[str] = None
    seed: Optional[int] = None
    clip_skip: Optional[int] = None


@dataclass
class ADETailerResponseData(JSONe):
    task_id: str
    warn: Optional[str] = None


@dataclass
class ADETailerResponse(JSONe):
    code: ADETailerResponseCode
    msg: str
    data: Optional[ADETailerResponseData] = None


# --------------- Training ---------------


@dataclass
class UploadAssetRequest(JSONe):
    file_extension: str = "png"


@dataclass
class UploadAssetResponse(JSONe):
    upload_url: str
    method: str
    assets_id: str


@dataclass
class TrainingImageDatasetItem(JSONe):
    assets_id: str


@dataclass
class TrainingExpertSetting(JSONe):
    instance_prompt: str = None
    class_prompt: str = None
    max_train_steps: int = None
    learning_rate: str = None
    seed: int = None
    lr_scheduler: str = None
    with_prior_preservation: bool = None
    prior_loss_weight: float = None
    lora_r: int = None
    lora_alpha: int = None
    lora_text_encoder_r: int = None
    lora_text_encoder_alpha: int = None


@dataclass
class TrainingComponent(JSONe):
    name: str
    args: List[Dict[str, Any]]


FACE_TRAINING_DEFAULT_COMPONENTS = [
    TrainingComponent(
        name="face_crop_region",
        args=[{
            "name": "ratio",
            "value": "1.4"
        }]
    ),
    TrainingComponent(
        name="resize",
        args=[
            {
                "name": "height",
                "value": "512",
            },
            {
                "name": "width",
                "value": "512",
            }
        ]
    ),
    TrainingComponent(
        name="face_restore",
        args=[
            {
                "name": "method",
                "value": "gfpgan_1.4"
            },
            {
                "name": "upscale",
                "value": "1.0"
            }
        ]
    ),
]


@dataclass
class CreateTrainingSubjectRequest(JSONe):
    name: str
    base_model: str
    image_dataset_items: List[TrainingImageDatasetItem]
    width: int = 512
    height: int = 512
    expert_setting: TrainingExpertSetting = None
    components: List[TrainingComponent] = None


@dataclass
class CreateTrainingSubjectResponse(JSONe):
    task_id: str


@dataclass
class QueryTrainingSubjectModel(JSONe):
    model_name: str
    model_status: str


@dataclass
class QueryTrainingSubjectStatusResponse(JSONe):
    task_id: str
    task_status: str
    model_type: str
    models: List[QueryTrainingSubjectModel]

# --------------- Training Style ---------------


@dataclass
class TrainingStyleImageDatasetItem(JSONe):
    assets_id: str
    caption: str


@dataclass
class CreateTrainingStyleRequest(JSONe):
    name: str
    base_model: str
    image_dataset_items: List[TrainingStyleImageDatasetItem]
    width: int = 512
    height: int = 512
    expert_setting: TrainingExpertSetting = None
    components: List[TrainingComponent] = None


@dataclass
class CreateTrainingStyleResponse(JSONe):
    task_id: str


@dataclass
class TrainingTaskInfoModel(JSONe):
    model_name: str
    model_status: str


@dataclass
class TrainingTaskInfo(JSONe):
    task_name: str
    task_id: str
    task_type: str
    task_status: str
    created_at: int
    models: List[TrainingTaskInfoModel]


@dataclass
class TrainingTaskPagination(JSONe):
    next_cursor: Optional[str] = None


@dataclass
class TrainingTaskListResponse(JSONe):
    tasks: List[TrainingTaskInfo] = field(default_factory=lambda: [])
    pagination: TrainingTaskPagination = None


class TrainingTaskList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_by_task_name(self, task_name: str):
        for task in self:
            if task.task_name == task_name:
                return task
        return None

    def filter_by_task_type(self, task_type: str):
        return TrainingTaskList([task for task in self if task.task_type == task_type])

    def filter_by_task_status(self, task_status: str):
        return TrainingTaskList([task for task in self if task.task_status == task_status])

    def filter_by_model_status(self, model_status: str):
        return TrainingTaskList([task for task in self if any(model.model_status == model_status for model in task.models)])

    def sort_by_created_at(self):
        return TrainingTaskList(sorted(self, key=lambda x: x.created_at, reverse=True))


# --------------- Image to Video ---------------

class Img2VideoResizeMode(Enum):
    ORIGINAL_DIMENSION = "ORIGINAL_DIMENSION"
    CROP_TO_ASPECT_RATIO = "CROP_TO_ASPECT_RATIO"


@dataclass
class Img2VideoRequest(JSONe):
    model_name: str
    image_file: str
    steps: int
    frames_num: int = 14
    frames_per_second: int = 6
    seed: Optional[int] = None
    image_file_resize_mode: Optional[str] = Img2VideoResizeMode.CROP_TO_ASPECT_RATIO
    motion_bucket_id: Optional[int] = 127
    cond_aug: Optional[float] = 0.02


@dataclass
class Img2VideoResponse(JSONe):
    task_id: str

# --------------- LCM Image to Image ---------------


@dataclass
class LCMLoRA(JSONe):
    model_name: str
    strenth: Optional[float] = 1.0


@dataclass
class LCMEmbedding(JSONe):
    model_name: str


@dataclass
class LCMImg2ImgRequest(JSONe):
    model_name: str
    input_image: str
    prompt: str
    negative_prompt: Optional[str] = None
    sd_vae: Optional[str] = None
    loras: Optional[List[LCMLoRA]] = None
    embeddings: Optional[List[LCMEmbedding]] = None
    seed: Optional[int] = None
    image_num: Optional[int] = 1
    steps: Optional[int] = 8
    clip_skip: Optional[int] = None
    guidance_scale: Optional[float] = 0


@dataclass
class LCMImg2ImgResponseImage(JSONe):
    image_url: str
    image_type: str
    image_url_ttl: int


@dataclass
class LCMImg2ImgResponse(JSONe):
    images: List[LCMImg2ImgResponseImage]


# --------------- Make Photo ---------------

@dataclass
class MakePhotoLoRA(JSONe):
    model_name: str
    strength: Optional[float] = 1.0


@dataclass
class MakePhotoRequest(JSONe):
    image_assets_ids: List[str]
    model_name: str
    prompt: str
    negative_prompt: Optional[str] = None
    loras: List[MakePhotoLoRA] = None
    height: Optional[int] = 1024
    width: Optional[int] = 1024
    image_num: Optional[int] = 1
    steps: Optional[int] = 50
    seed: Optional[int] = None
    guidance_scale: Optional[float] = 7.5
    sampler_name: Optional[str] = Samplers.EULER_A
    strength: Optional[float] = 0.25
    crop_face: Optional[bool] = True
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class MakePhotoResponse(JSONe):
    task_id: str


@dataclass
class InstantIDControlnetUnit(JSONe):
    model_name: str
    strength: Optional[float]
    preprocessor: Optional[ControlNetPreprocessor]


InstantIDLora = MakePhotoLoRA


@dataclass
class InstantIDRequestControlNet(JSONe):
    units: List[InstantIDControlnetUnit]


@dataclass
class InstantIDRequest(JSONe):
    face_image_assets_ids: List[str]
    ref_image_assets_ids: List[str]
    model_name: str = None
    prompt: str = None
    negative_prompt: str = None
    width: int = None
    height: int = None
    id_strength: float = 1.
    adapter_strength: float = 1.
    steps: int = 20
    seed: int = -1
    image_num: int = 1
    guidance_scale: float = 5.
    sampler_name: str = 'Euler'
    controlnet: InstantIDRequestControlNet = None
    loras: List[InstantIDLora] = None
    extra: Dict = field(default_factory=lambda: dict())

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


# --------------- Common V3 ---------------

@dataclass
class CommonV3Request(JSONe):
    extra: Dict[str, Any] = field(default_factory=lambda: dict())
    request: Any = field(default_factory=lambda: dict())


@dataclass
class CommonV3Extra(JSONe):
    response_image_type: str = "jpeg"
    enable_nsfw_detection: bool = False
    nsfw_detection_level: int = 0
    custom_storage: Dict[str, Any] = field(default_factory=lambda: dict())
    enterprise_plan: Dict[str, Any] = field(default_factory=lambda: dict())

# --------------- Img2ImgV3 ---------------


@dataclass
class Img2V3ImgLoRA(JSONe):
    model_name: str
    strength: Optional[float] = 1.0


@dataclass
class Img2ImgV3Embedding(JSONe):
    model_name: str


@dataclass
class Img2ImgV3ControlNetUnit(JSONe):
    model_name: str
    image_base64: str
    strength: Optional[float] = 1.0
    preprocessor: Optional[ControlNetPreprocessor] = "canny"
    guidance_start: Optional[float] = 0
    guidance_end: Optional[float] = 1


@dataclass
class Img2ImgV3ControlNet(JSONe):
    units: List[Img2ImgV3ControlNetUnit]


@dataclass
class Img2ImgV3Request(JSONe):
    model_name: str
    image_base64: str
    prompt: str
    width: Optional[int] = 512
    height: Optional[int] = 512
    negative_prompt: Optional[str] = None
    sd_vae: Optional[str] = None
    loras: Optional[List[Img2V3ImgLoRA]] = None
    embeddings: Optional[List[Img2ImgV3Embedding]] = None
    seed: Optional[int] = -1
    image_num: Optional[int] = 1
    steps: Optional[int] = 20
    clip_skip: Optional[int] = None
    guidance_scale: Optional[float] = 7.5
    strength: Optional[float] = 0.5
    sampler_name: Optional[str] = Samplers.EULER_A
    extra: Dict = field(default_factory=lambda: dict())
    controlnet: Optional[Img2ImgV3ControlNet] = None

    def set_image_type(self, image_type: str):
        self.extra['response_image_type'] = image_type


@dataclass
class Img2ImgV3Response(JSONe):
    task_id: str

# --------------- Txt2ImgV3 ---------------


@dataclass
class Txt2ImgV3Embedding(JSONe):
    model_name: str


@dataclass
class Txt2ImgV3LoRA(JSONe):
    model_name: str
    strength: Optional[float] = 1.0


@dataclass
class Txt2ImgV3HiresFix(JSONe):
    target_width: int
    target_height: int
    strength: float = 0.5
    upscaler: str = "Latent"


@dataclass
class Txt2ImgV3Refiner(JSONe):
    switch_at: float = 0.5


@dataclass
class Txt2ImgV3Request(JSONe):
    model_name: str
    prompt: str
    height: Optional[int] = 512
    width: Optional[int] = 512
    image_num: Optional[int] = 1
    sd_vae: Optional[str] = None
    steps: Optional[int] = 20
    guidance_scale: Optional[float] = 7.5
    sampler_name: Optional[str] = Samplers.EULER_A
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    loras: Optional[List[Txt2ImgV3LoRA]] = None
    embeddings: Optional[List[Txt2ImgV3Embedding]] = None
    refiner: Optional[Txt2ImgV3Refiner] = None
    hires_fix: Optional[Txt2ImgV3HiresFix] = None
    clip_skip: Optional[int] = None


@dataclass
class Txt2ImgV3Response(JSONe):
    task_id: str

# --------------- Model ---------------


class ModelType(Enum):
    CHECKPOINT = "checkpoint"
    LORA = "lora"
    VAE = "vae"
    CONTROLNET = "controlnet"
    TEXT_INVERSION = "textualinversion"
    UPSCALER = "upscaler"

    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)


@dataclass
class CivitaiImageMeta(JSONe):
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    sampler_name: Optional[str] = None
    steps: Optional[int] = None
    cfg_scale: Optional[int] = None
    seed: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None
    model_name: Optional[str] = None


@dataclass
class CivitaiImage(JSONe):
    url: str
    nsfw: str
    meta: Optional[CivitaiImageMeta] = None


@dataclass
class ModelInfo(JSONe):
    name: str
    hash: str
    civitai_version_id: int
    sd_name: str
    third_source: str
    download_status: int
    download_name: str
    dependency_status: int
    type: ModelType
    civitai_nsfw: Optional[bool] = False
    civitai_model_id: Optional[int] = 0
    civitai_link: Optional[str] = None
    civitai_images: Optional[List[CivitaiImage]] = field(default_factory=lambda: [])
    civitai_download_url: Optional[str] = None
    civitai_allow_commercial_use: Optional[bool] = True
    civitai_allow_different_license: Optional[bool] = True
    civitai_create_at: Optional[str] = None
    civitai_update_at: Optional[str] = None
    civitai_tags: Optional[str] = None
    civitai_download_count: Optional[int] = 0
    civitai_favorite_count: Optional[int] = 0
    civitai_comment_count: Optional[int] = 0
    civitai_rating_count: Optional[int] = 0
    civitai_rating: Optional[float] = 0.0
    novita_used_count: Optional[int] = None
    civitai_image_url:  Optional[str] = None
    civitai_image_nsfw:  Optional[bool] = False
    civitai_origin_image_url:  Optional[str] = None
    civitai_image_prompt:  Optional[str] = None
    civitai_image_negative_prompt:  Optional[str] = None
    civitai_image_sampler_name:  Optional[str] = None
    civitai_image_height: Optional[int] = None
    civitai_image_width:  Optional[int] = None
    civitai_image_steps:  Optional[int] = None
    civitai_image_cfg_scale:  Optional[int] = None
    civitai_image_seed:  Optional[int] = None


@dataclass
class ModelData(JSONe):
    models: List[ModelInfo] = None


@dataclass
class MoodelsResponse(JSONe):
    code: int
    msg: str
    data: Optional[ModelData] = field(default_factory=lambda: [])


class ModelList(list):
    """A list of ModelInfo"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_by_civitai_version_id(self, civitai_version_id: int):
        for model in self:
            if model.civitai_version_id == civitai_version_id:
                return model
        return None

    def get_by_name(self, name):
        for model in self:
            if model.name == name:
                return model
        return None

    def get_by_sd_name(self, sd_name):
        for model in self:
            if model.sd_name == sd_name:
                return model
        return None

    def list_civitai_tags(self) -> List[str]:
        s = set()
        for model in self:
            if model.civitai_tags:
                s.update(s.strip()
                         for s in model.civitai_tags.split(",") if s.strip())
        return list(s)

    def filter_by_civitai_tags(self, *tags):
        ret = []
        for model in self:
            if model.civitai_tags:
                if set(tags).issubset(set(s.strip() for s in model.civitai_tags.split(","))):
                    ret.append(model)
        return ModelList(ret)

    def filter_by_nsfw(self, nsfw: bool):
        return ModelList([model for model in self if model.civitai_nsfw == nsfw])

    def filter_by_type(self, type):
        return ModelList([model for model in self if model.type == type])

    def filter_by_civitai_model_id(self, civitai_model_id: int):
        return ModelList([model for model in self if model.civitai_model_id == civitai_model_id])

    def filter_by_civitai_model_name(self, name: str):
        return ModelList([model for model in self if model.name == name])

    def sort_by_civitai_download(self):
        return ModelList(sorted(self, key=lambda x: x.civitai_download_count, reverse=True))

    def sort_by_civitai_rating(self):
        return ModelList(sorted(self, key=lambda x: x.civitai_rating, reverse=True))

    def sort_by_civitai_favorite(self):
        return ModelList(sorted(self, key=lambda x: x.civitai_favorite, reverse=True))

    def sort_by_civitai_comment(self):
        return ModelList(sorted(self, key=lambda x: x.civitai_comment, reverse=True))


# --------------- Model V3 ---------------

@dataclass
class ModelInfoTypeV3(JSONe):
    name: str
    display_name: str


class ModelInfoStatus(Enum):
    UNAVAILABLE = 0
    AVAILABLE = 1


@dataclass
class ModelInfoV3(JSONe):
    id: int
    name: str
    sd_name: str
    type: ModelInfoTypeV3
    status: ModelInfoStatus
    hash_sha256: Optional[str] = None
    categories: Optional[List[str]] = None
    download_url: Optional[str] = None
    base_model: Optional[str] = None
    source: Optional[str] = None
    download_url_ttl: Optional[int] = None
    sd_name_in_api: Optional[str] = None
    is_nsfw: Optional[bool] = None
    visibility: Optional[str] = None
    cover_url: Optional[str] = None


class ModelListV3(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_by_name(self, name):
        for model in self:
            if model.name == name:
                return model
        return None

    def get_by_sd_name(self, sd_name):
        for model in self:
            if model.sd_name == sd_name:
                return model
        return None

    def filter_by_type(self, type):
        return ModelListV3([model for model in self if model.type.name == type])

    def filter_by_nsfw(self, nsfw: bool):
        return ModelListV3([model for model in self if model.is_nsfw == nsfw])

    def filter_by_status(self, status: ModelInfoStatus):
        return ModelListV3([model for model in self if model.status == status])

    def filter_by_source(self, source: str):
        return ModelListV3([model for model in self if model.source == source])

    def filter_by_visibility(self, visibility: str):
        return ModelListV3([model for model in self if model.visibility == visibility])

    def filter_by_available(self, available: bool):
        return ModelListV3([model for model in self if model.status == ModelInfoStatus.AVAILABLE])

    def sort_by_name(self):
        return ModelListV3(sorted(self, key=lambda x: x.name))


@dataclass
class ModelsPaginationV3(JSONe):
    next_cursor: Optional[str] = None


@dataclass
class MoodelsResponseV3(JSONe):
    models: List[ModelInfoV3] = None
    pagination: ModelsPaginationV3 = None


# --------------- User Info ---------------
@dataclass
class UserInfoResponse(JSONe):
    allow_features: List[str] = None
    credit_balance: int = 0
    free_trial: Dict[str, int] = field(default_factory=lambda: {})
